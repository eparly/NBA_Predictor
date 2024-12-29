import { DynamoDBPredictions, DynamoDBOdds, PredictionsResponse } from './types';
import { DynamoDBService } from '../../../dynamodb/DynamoDBService';

export class PredictionsController {
    private dynamoDbService: DynamoDBService;

    constructor(dynamoDbService: DynamoDBService) {
        this.dynamoDbService = dynamoDbService
    }

    public async getCombinedData(date: string): Promise<PredictionsResponse[]> {
        
        try {
            const [predictionsData, oddsData] = await Promise.all([
                this.dynamoDbService.getPredictions(date),
                this.dynamoDbService.getOdds(date)
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
                        spread: Number(item.spreadHome),
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