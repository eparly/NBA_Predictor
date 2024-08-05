import { Duration, Stack, StackProps } from "aws-cdk-lib";
import { Table } from "aws-cdk-lib/aws-dynamodb";
import { Code, Function, LayerVersion, Runtime } from "aws-cdk-lib/aws-lambda";
import { Bucket } from "aws-cdk-lib/aws-s3";
import { Construct } from "constructs";

export type LambdaStackDeps = {
    bucket: Bucket
    table: Table
}

export class LambdaStack extends Stack {
    private readonly resultsLambda: Function
    constructor(scope: Construct, id: string, deps: LambdaStackDeps, props?: StackProps) {
        super(scope, id, props)

        const layerArn = 'arn:aws:lambda:ca-central-1:498430199007:layer:nba-api-layer:3'
        const lambdaLayer = LayerVersion.fromLayerVersionArn(this, 'NbaAPILayer', layerArn)

        const proxy_username = 'bihbbirx'
        const proxy_password = '19u2egbwdct9'
        const proxy_host = '64.64.118.149'
        const proxy_port = '6732'
        const PROXY = `http://${proxy_username}:${proxy_password}@${proxy_host}:${proxy_port}`
        this.resultsLambda = new Function(this, 'ResultsLambda', {
            runtime: Runtime.PYTHON_3_10,
            code: Code.fromAsset(__dirname+ '../../src'),
            handler: 'results/handler.lambda_handler',
            layers: [lambdaLayer],
            environment: {
                tableName: deps.table.tableName,
                bucketName: deps.bucket.bucketName,
                proxy: PROXY
            },
            timeout: Duration.minutes(1),
            memorySize: 256
        })
        deps.bucket.grantRead(this.resultsLambda)
        deps.table.grantReadWriteData(this.resultsLambda)
    }
}