import { Duration, Stack, StackProps } from "aws-cdk-lib";
import { Table } from "aws-cdk-lib/aws-dynamodb";
import { Code, Function, LayerVersion, Runtime } from "aws-cdk-lib/aws-lambda";
import { Bucket } from "aws-cdk-lib/aws-s3";
import { Secret } from "aws-cdk-lib/aws-secretsmanager";
import { StateMachine } from "aws-cdk-lib/aws-stepfunctions";
import { LambdaInvoke } from "aws-cdk-lib/aws-stepfunctions-tasks";
import { Construct } from "constructs";

export type LambdaStackDeps = {
    bucket: Bucket
    table: Table
}

export class LambdaStack extends Stack {
    private readonly resultsLambda: Function
    private readonly recordLambda: Function
    constructor(scope: Construct, id: string, deps: LambdaStackDeps, props?: StackProps) {
        super(scope, id, props)

        const layerArn = 'arn:aws:lambda:ca-central-1:498430199007:layer:nba-api-layer:3'
        const lambdaLayer = LayerVersion.fromLayerVersionArn(this, 'NbaAPILayer', layerArn)

        const proxyArn = 'arn:aws:secretsmanager:ca-central-1:498430199007:secret:proxy-credentials-VPN1Ya'
        const secret = Secret.fromSecretCompleteArn(this, 'ProxyInfo', proxyArn)
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
        secret.grantRead(this.resultsLambda)

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

        const invokeResultsLambda = new LambdaInvoke(this, 'InvokeResultsLambda', {
            lambdaFunction: this.resultsLambda,
        })
        const invokeRecordLambda = new LambdaInvoke(this, 'InvokeRecordLambda', {
            lambdaFunction: this.recordLambda
        })

        const definition = invokeResultsLambda.next(invokeRecordLambda)
        const stateMachine = new StateMachine(this, 'StateMachine', {
            definition,
            // Set timeout once we know how long it should take
            // timeout: Duration.minutes(5)
        })

        this.resultsLambda.grantInvoke(stateMachine)
        this.recordLambda.grantInvoke(stateMachine)
    }
}