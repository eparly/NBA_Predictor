import { DynamoDBService } from "../../../dynamodb/DynamoDBService"
import { DynamoDBOdds, DynamoDBPredictions } from "../../predictions/{date}/types";
import { DynamoDBResults, ResultsMap, ResultsResponse } from "./types";

export class ResultsController {
    private readonly dynamoDbService: DynamoDBService

    constructor(dynamoDbService: DynamoDBService) {
        this.dynamoDbService = dynamoDbService
    }

    public async getCombinedData(date: string): Promise<ResultsResponse[]> {
        try {
            const [resultsData, oddsData, predictionsData] = await Promise.all([
                this.dynamoDbService.getResults(date),
                this.dynamoDbService.getOdds(date),
                this.dynamoDbService.getPredictions(date)
            ]);

            if (!resultsData.Items?.length) {
                return [];
            }

            const resultsMap = new Map();
            (resultsData.Items as DynamoDBResults[] || []).forEach((item) => {
                const gameId = item['type-gameId'].split('::')[1];
                resultsMap.set(gameId, {
                    homeScore: item.homescore,
                    awayScore: item.awayscore,
                    homeTeam: item.hometeam,
                    awayTeam: item.awayteam,
                });
            });

            const predictionsMap = new Map();
            (predictionsData.Items as DynamoDBPredictions[] || []).forEach((item) => {
                const gameId = item['type-gameId'].split('::')[1];
                const correct = this.isPredictionCorrect(item, resultsMap.get(gameId));
                predictionsMap.set(gameId, {
                    correct: correct,
                    homeScore: item.homescore,
                    awayScore: item.awayscore,
                    confidence: item.confidence,
                });
            });

            const combinedData: ResultsResponse[] = (oddsData.Items as DynamoDBOdds[] || []).map((item) => {
                const gameId = item['type-gameId'].split('::')[1];
                return {
                    date: item.date,
                    gameId: Number(gameId),
                    homeTeam: item.hometeam,
                    awayTeam: item.awayteam,
                    predictions: predictionsMap.get(gameId),
                    odds: {
                        homeML: Number(item.home_ml),
                        awayML: Number(item.away_ml),
                        spread: Number(item.spread),
                    },
                    results: resultsMap.get(gameId),
                };
            });

            return combinedData;
        }
        catch (error) {
            console.error('Error fetching results:', error);
            throw new Error('Error fetching results');
        }
    }

    private isPredictionCorrect(prediction: DynamoDBPredictions, result: ResultsMap): boolean {
        console.log('prediction\n', prediction);
        console.log('result\n', result);

        
        const actualWinner = result.homeScore > result.awayScore ? 'home' : 'away';
        const predictedWinner = prediction.homescore >= prediction.awayscore ? 'home' : 'away';
        console.log('actualWinner\n', actualWinner);
        console.log('predictedWinner\n', predictedWinner);
        return actualWinner === predictedWinner;
    }
}