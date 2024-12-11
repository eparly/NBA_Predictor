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

    public async getRecord(date: string): Promise<QueryOutput> {
        const params = {
            TableName: this.tableName,
            KeyConditionExpression: '#date = :date AND begins_with(#typeGameId, :record)',
            ExpressionAttributeNames: {
                '#date': 'date',
                '#typeGameId': 'type-gameId',
            },
            ExpressionAttributeValues: {
                ':date': date,
                ':record': 'record',
            },
        };

        return this.dynamoDb.query(params).promise();
    }

    public async getAllRecords(): Promise<QueryOutput> {
        const params = {
            TableName: this.tableName,
            FilterExpression: 'begins_with(#typeGameId, :record)',
            ExpressionAttributeNames: {
                '#typeGameId': 'type-gameId',
            },
            ExpressionAttributeValues: {
                ':record': 'record',
            },
        };
        const result = await this.dynamoDb.scan(params).promise();
        result.Items = result.Items?.sort((a, b) => (a.date < b.date ? 1 : -1));

        return result;
    }

    public async getPicks(date: string, type: string): Promise<QueryOutput> {
        const params = {
            TableName: this.tableName,
            KeyConditionExpression: '#date = :date AND begins_with(#typeGameId, :typeGameId)',
            ExpressionAttributeNames: {
                '#date': 'date',
                '#typeGameId': 'type-gameId',
            },
            ExpressionAttributeValues: {
                ':date': date,
                ':typeGameId': `picks::${type}`,
            },
        }
        console.log(params)

        const result = await this.dynamoDb.query(params).promise()
        return result

    }
}