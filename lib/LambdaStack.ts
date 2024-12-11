import { Duration, Stack, StackProps } from "aws-cdk-lib";
import { Table } from "aws-cdk-lib/aws-dynamodb";
import { Code, Function, LayerVersion, Runtime } from "aws-cdk-lib/aws-lambda";
import { SqsEventSource } from "aws-cdk-lib/aws-lambda-event-sources";
import { Bucket } from "aws-cdk-lib/aws-s3";
import { Secret } from "aws-cdk-lib/aws-secretsmanager";
import { Queue } from "aws-cdk-lib/aws-sqs";
import { Choice, Condition, StateMachine, Wait, WaitTime } from "aws-cdk-lib/aws-stepfunctions";
import { LambdaInvoke, CallAwsService } from "aws-cdk-lib/aws-stepfunctions-tasks";
import { Construct } from "constructs";
import { SfnStateMachine } from "aws-cdk-lib/aws-events-targets";
import { Rule, Schedule } from "aws-cdk-lib/aws-events";


export type LambdaStackDeps = {
    bucket: Bucket
    table: Table
    predictionsQueue: Queue
    oddsQueue: Queue
}

export class LambdaStack extends Stack {
    private readonly resultsLambda: Function
    private readonly recordLambda: Function
    private readonly predictionLambdaStarter: Function
    private readonly predictionLambda: Function
    private readonly oddsLambda: Function
    private readonly picksLambda: Function
    constructor(scope: Construct, id: string, deps: LambdaStackDeps, props?: StackProps) {
        super(scope, id, props)

        const layerArn = 'arn:aws:lambda:ca-central-1:498430199007:layer:nba-api-layer:3'
        const lambdaLayer = LayerVersion.fromLayerVersionArn(this, 'NbaAPILayer', layerArn)

        const proxyArn = 'arn:aws:secretsmanager:ca-central-1:498430199007:secret:proxy-credentials-VPN1Ya'
        const proxySecret = Secret.fromSecretCompleteArn(this, 'ProxyInfo', proxyArn)
        const oddsArn = 'arn:aws:secretsmanager:ca-central-1:498430199007:secret:odds_api_key-hqCtvd'
        const oddsSecret = Secret.fromSecretCompleteArn(this, 'OddsInfo', oddsArn)
        this.resultsLambda = new Function(this, 'ResultsLambda', {
            runtime: Runtime.PYTHON_3_10,
            code: Code.fromAsset(__dirname+ '../../src'),
            handler: 'results/handler.lambda_handler',
            layers: [lambdaLayer],
            environment: {
                tableName: deps.table.tableName,
                bucketName: deps.bucket.bucketName,
            },
            timeout: Duration.minutes(1),
            memorySize: 256
        })
        proxySecret.grantRead(this.resultsLambda)

        deps.bucket.grantRead(this.resultsLambda)
        deps.table.grantReadWriteData(this.resultsLambda)

        this.recordLambda = new Function(this, 'RecordLambda', {
            runtime: Runtime.PYTHON_3_10,
            code: Code.fromAsset(__dirname + '../../src'),
            handler: 'record_units/handler.lambda_handler',
            layers: [lambdaLayer],
            environment: {
                tableName: deps.table.tableName,
                bucketName: deps.bucket.bucketName
            },
            timeout: Duration.minutes(1),
            memorySize: 256
        })
        deps.table.grantReadWriteData(this.recordLambda)

        this.predictionLambdaStarter = new Function(this, 'PredictionLambdaStarter', {
            runtime: Runtime.PYTHON_3_10,
            code: Code.fromAsset(__dirname + '../../src'),
            handler: 'predictions/predictions_starter/handler.lambda_handler',
            layers: [lambdaLayer], //might not be needed?
            environment: {
                tableName: deps.table.tableName,
                bucketName: deps.bucket.bucketName,
                predictionQueueUrl: deps.predictionsQueue.queueUrl
            },
            timeout: Duration.minutes(1),
            memorySize: 256
        })
        deps.table.grantReadWriteData(this.predictionLambdaStarter)
        deps.bucket.grantRead(this.predictionLambdaStarter)
        deps.predictionsQueue.grantSendMessages(this.predictionLambdaStarter)
        proxySecret.grantRead(this.predictionLambdaStarter)

        this.predictionLambda = new Function(this, 'PredictionLambda', {
            runtime: Runtime.PYTHON_3_10,
            code: Code.fromAsset(__dirname + '../../src'),
            handler: 'predictions/predictions/handler.lambda_handler',
            layers: [lambdaLayer],
            environment: {
                tableName: deps.table.tableName,
                bucketName: deps.bucket.bucketName,
                predictionQueueUrl: deps.predictionsQueue.queueUrl
            },
            timeout: Duration.minutes(5),
            memorySize: 256,
            reservedConcurrentExecutions: 1
        })
        deps.table.grantReadWriteData(this.predictionLambda)
        deps.bucket.grantRead(this.predictionLambda)
        deps.predictionsQueue.grantConsumeMessages(this.predictionLambda)
        this.predictionLambda.addEventSource(new SqsEventSource(deps.predictionsQueue, {
            batchSize: 1
        }))
        proxySecret.grantRead(this.predictionLambda)

        this.oddsLambda = new Function(this, 'OddsLambda', {
            runtime: Runtime.PYTHON_3_10,
            code: Code.fromAsset(__dirname + '../../src'),
            handler: 'odds/handler.lambda_handler',
            layers: [lambdaLayer],
            environment: {
                tableName: deps.table.tableName,
                bucketName: deps.bucket.bucketName,
                predictionQueueUrl: deps.predictionsQueue.queueUrl
            },
            timeout: Duration.minutes(5),
            memorySize: 256,
            reservedConcurrentExecutions: 1
        })

        oddsSecret.grantRead(this.oddsLambda)
        deps.table.grantReadWriteData(this.oddsLambda)
        deps.bucket.grantRead(this.oddsLambda)
        deps.oddsQueue.grantSendMessages(this.oddsLambda)

        this.picksLambda = new Function(this, 'PicksLambda', {
            runtime: Runtime.PYTHON_3_10,
            code: Code.fromAsset(__dirname + '../../src'),
            handler: 'picks/handler.lambda_handler',
            layers: [lambdaLayer],
            environment: {
                tableName: deps.table.tableName,
                bucketName: deps.bucket.bucketName,
                oddsQueueUrl: deps.oddsQueue.queueUrl
            },
            timeout: Duration.minutes(5),
            memorySize: 256,
            reservedConcurrentExecutions: 1
        })
        deps.table.grantReadWriteData(this.picksLambda)
        deps.oddsQueue.grantConsumeMessages(this.picksLambda)

        // Define the Step Function tasks
        const resultsTask = new LambdaInvoke(this, 'Invoke Results Lambda', {
            lambdaFunction: this.resultsLambda,
        })
    
        const recordTask = new LambdaInvoke(this, 'Invoke Record Lambda', {
            lambdaFunction: this.recordLambda,
        })
    
        const predictionStarterTask = new LambdaInvoke(this, 'Invoke Prediction Starter Lambda', {
            lambdaFunction: this.predictionLambdaStarter,
        })
    
        const waitTask = new Wait(this, 'Wait for Predictions', {
            time: WaitTime.duration(Duration.minutes(5)),
        })
    
        const checkQueueTask = new CallAwsService(this, 'Check SQS Queue', {
            service: 'sqs',
            action: 'getQueueAttributes',
            parameters: {
                QueueUrl: deps.predictionsQueue.queueUrl,
                AttributeNames: ['ApproximateNumberOfMessages'],
            },
            iamResources: ['*'],
            resultPath: '$.queueAttributes',
        })
    
        const choiceState = new Choice(this, 'Is Queue Empty?')
        const queueEmptyCondition = Condition.stringEquals('$.queueAttributes.Attributes.ApproximateNumberOfMessages', "0")
    
        const oddsTask = new LambdaInvoke(this, 'Invoke Odds Lambda', {
            lambdaFunction: this.oddsLambda,
        })

        const waitBeforeOddsTask = new Wait(this, 'Wait Before Odds', {
            time: WaitTime.duration(Duration.minutes(30)),
        })
    
        // Define the state machine
        const definition = resultsTask
            .next(recordTask)
            .next(predictionStarterTask)
            .next(waitTask)
            .next(checkQueueTask)
            .next(choiceState
                .when(queueEmptyCondition, waitBeforeOddsTask.next(oddsTask))
                .otherwise(waitTask))

    
        const stateMachine = new StateMachine(this, 'StateMachine', {
            definition,
            timeout: Duration.hours(1),
        })
    
        // Create a CloudWatch Event Rule to trigger the Step Function at 8 AM every day
        new Rule(this, 'ScheduleRule', {
            schedule: Schedule.cron({ minute: '0', hour: '8' }),
            targets: [new SfnStateMachine(stateMachine)],
        })
    }
}