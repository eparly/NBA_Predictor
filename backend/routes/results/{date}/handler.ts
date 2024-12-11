import { APIGatewayProxyHandler } from 'aws-lambda';
import { ResultsController } from './controller';
import { DynamoDBService } from '../../../dynamodb/DynamoDBService';

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

    const controller = new ResultsController(dynamoDbService);
    const date = event.pathParameters?.date;

    if (!date) {
        return {
            statusCode: 400,
            body: JSON.stringify({
                message: 'Missing date query parameter',
            }),
        };
    }

    // Validate date format
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(date)) {
        return {
            statusCode: 400,
            body: JSON.stringify({
                message: 'Invalid date format. Expected format: YYYY-MM-DD',
            }),
        };
    }

    try {
        const combinedData = await controller.getCombinedData(date);

        if (!combinedData.length) {
            return {
                statusCode: 404,
                body: JSON.stringify({
                    message: 'No results found for the given date',
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
            body: JSON.stringify(combinedData),
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({
                message: 'Error fetching data',
            }),
        };
    }
};