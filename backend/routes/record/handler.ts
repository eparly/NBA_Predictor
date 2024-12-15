import { APIGatewayProxyHandler } from 'aws-lambda';

import { DynamoDBService } from "../../dynamodb/DynamoDBService";
import { RecordController } from "./controller";
import { RecordType } from './types';

export const handler: APIGatewayProxyHandler = async (event, context) => {
    const tableName = process.env.TABLE_NAME;

    if (!tableName) {
        return {
            statusCode: 500,
            body: JSON.stringify({
                message: 'Missing environment variables',
            }),
        };
    }

    const dynamoDbService = new DynamoDBService(tableName);

    const controller = new RecordController(dynamoDbService);

    try {
        const queryType = event.queryStringParameters?.type as RecordType;
        const records = await controller.getRecords(queryType);
        console.log('Records:', records);
        if (!records) {
            return {
                statusCode: 404,
                body: JSON.stringify({
                    message: 'No records found',
                }),
            };
        }
        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            },
            body: JSON.stringify(records),
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({
                message: 'Error fetching records',
            }),
        };
    }
};