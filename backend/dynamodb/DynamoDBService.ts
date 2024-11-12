import { DocumentClient, QueryOutput } from "aws-sdk/clients/dynamodb";

export class DynamoDBService {
    private readonly dynamoDb: DocumentClient;
    private readonly tableName: string;

    constructor(tableName: string) {
        this.dynamoDb = new DocumentClient();
        this.tableName = tableName;
    }

    public async getPredictions(date: string): Promise<QueryOutput> {
        const params = {
            TableName: this.tableName,
            KeyConditionExpression: '#date = :date AND begins_with(#typeGameId, :predictions)',
            ExpressionAttributeNames: {
                '#date': 'date',
                '#typeGameId': 'type-gameId',
            },
            ExpressionAttributeValues: {
                ':date': date,
                ':predictions': 'predictions',
            },
        };

        return this.dynamoDb.query(params).promise();
    }

    public async getOdds(date: string): Promise<QueryOutput> { 
        const params = {
            TableName: this.tableName,
            KeyConditionExpression: '#date = :date AND begins_with(#typeGameId, :odds)',
            ExpressionAttributeNames: {
                '#date': 'date',
                '#typeGameId': 'type-gameId',
            },
            ExpressionAttributeValues: {
                ':date': date,
                ':odds': 'odds',
            },
        };

        return this.dynamoDb.query(params).promise();
    }

    public async getResults(date: string): Promise<QueryOutput> {
        const params = {
            TableName: this.tableName,
            KeyConditionExpression: '#date = :date AND begins_with(#typeGameId, :results)',
            ExpressionAttributeNames: {
                '#date': 'date',
                '#typeGameId': 'type-gameId',
            },
            ExpressionAttributeValues: {
                ':date': date,
                ':results': 'results',
            },
        };

        return this.dynamoDb.query(params).promise();
    }
}