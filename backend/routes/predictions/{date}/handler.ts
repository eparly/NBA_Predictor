import { APIGatewayProxyHandler } from 'aws-lambda';
import { PredictionsController } from './controller';

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

    const controller = new PredictionsController(tableName);
    const date = event.pathParameters?.date;

    if (!date) {
        return {
            statusCode: 400,
            body: JSON.stringify({
                message: 'Missing date parameter',
            }),
        };
    }

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
        const predictions = await controller.getCombinedData(date);
        return {
            statusCode: 200,
            body: JSON.stringify(predictions),
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({
                message: 'Error fetching predictions',
            }),
        };
    }
};