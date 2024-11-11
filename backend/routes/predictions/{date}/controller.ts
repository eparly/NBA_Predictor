import { DynamoDB } from 'aws-sdk';
import { DynamoDBPredictions, DynamoDBOdds, PredictionsResponse } from './types';

export class PredictionsController {
    private dynamoDb: DynamoDB.DocumentClient;
    private tableName: string;

    constructor(tableName: string) {
        this.dynamoDb = new DynamoDB.DocumentClient();
        this.tableName = tableName;
    }

    public async getCombinedData(date: string): Promise<PredictionsResponse[]> {
        const predictionsParams = {
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

        const oddsParams = {
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
        }

        try {
            const [predictionsData, oddsData] = await Promise.all([
                this.dynamoDb.query(predictionsParams).promise(),
                this.dynamoDb.query(oddsParams).promise(),
            ]);

            const predictionsMap = new Map();
            (predictionsData.Items as DynamoDBPredictions[] || []).forEach((item) => {
                const gameId = item['type-gameId'].split('::')[1];
                predictionsMap.set(gameId, {
                    homeScore: item.homescore,
                    awayScore: item.awayscore,
                    confidence: item.confidence,
                });
            });

            const combinedData = (oddsData.Items as DynamoDBOdds[] || []).map((item) => {
                const gameId = item['type-gameId'].split('::')[1];
                return {
                    date: item.date,
                    gameId: Number(gameId),
                    homeTeam: item.hometeam,
                    awayTeam: item.awayteam,
                    predictions: predictionsMap.get(gameId) || {},
                    odds: {
                        homeML: Number(item.home_ml),
                        awayML: Number(item.away_ml),
                        spread: Number(item.spread),
                    }
                };
            })

            return combinedData;
        } catch (error) {
            console.error('Error fetching predictions:', error);
            throw new Error('Error fetching predictions');
        }
    }
}