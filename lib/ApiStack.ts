import { Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import { Runtime, Code } from "aws-cdk-lib/aws-lambda";
import { NodejsFunction } from "aws-cdk-lib/aws-lambda-nodejs";

import { RestApi, LambdaIntegration } from "aws-cdk-lib/aws-apigateway";
import { Table } from "aws-cdk-lib/aws-dynamodb";

export type ApiStackDeps = {
    table: Table
}

export class ApiStack extends Stack {

    constructor(scope: Construct, id: string, deps: ApiStackDeps, props?: StackProps) {
        super(scope, id, props)

        const predictorLambda = new NodejsFunction(this, 'GetPredictionsRoute', {
            runtime: Runtime.NODEJS_20_X,
            handler: 'handler',
            entry: 'backend/routes/predictions/{date}/handler.ts',
            environment: {
                TABLE_NAME: deps.table.tableName
            }
        })

        const resultsLambda = new NodejsFunction(this, 'GetResultsRoute', {
            runtime: Runtime.NODEJS_20_X,
            handler: 'handler',
            entry: 'backend/routes/results/{date}/handler.ts',
            environment: {
                TABLE_NAME: deps.table.tableName
            }
        })

        const recordLambda = new NodejsFunction(this, 'GetRecordRoute', {
            runtime: Runtime.NODEJS_20_X,
            handler: 'handler',
            entry: 'backend/routes/record/handler.ts',
            environment: {
                TABLE_NAME: deps.table.tableName
            }
        })

        const picksLambda = new NodejsFunction(this, 'GetValuePicksRoute', {
            runtime: Runtime.NODEJS_20_X,
            handler: 'handler',
            entry: 'backend/routes/picks/value/{date}/handler.ts',
            environment: {
                TABLE_NAME: deps.table.tableName
            }
        })

        const api = new RestApi(this, 'nbaApi', {
            restApiName: 'NBA API',
            description: 'This service serves NBA predictions'
        })

        api.root.addResource('predictions').addResource('{date}').addMethod('GET', new LambdaIntegration(predictorLambda))
        api.root.addResource('results').addResource('{date}').addMethod('GET', new LambdaIntegration(resultsLambda))
        api.root.addResource('record').addMethod('GET', new LambdaIntegration(recordLambda))
        api.root.addResource('picks').addResource('value').addResource('{date}').addMethod('GET', new LambdaIntegration(picksLambda))
        deps.table.grantReadData(predictorLambda)
        deps.table.grantReadData(resultsLambda)
        deps.table.grantReadData(recordLambda)
        deps.table.grantReadData(picksLambda)
    }

}