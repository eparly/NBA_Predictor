import { DynamoDBService } from "../../../../dynamodb/DynamoDBService";
import { DynamoDBPicks, PicksResponse } from "./types";

export class PicksController {
    private readonly dynamoDbService: DynamoDBService

    constructor(dynamoDbService: DynamoDBService) {
        this.dynamoDbService = dynamoDbService
    }
    
    public async getPicks(date: string, type: string): Promise<PicksResponse[]> {
        try {
            const picks = await this.dynamoDbService.getPicks(date, type)
            console.log('Picks:', picks)
            const response: PicksResponse[] = (picks.Items as DynamoDBPicks[] || []).map((item) => {
                console.log(item['type-gameId'].split('::')[2])
                return {
                    date: item.date,
                    gameId: Number(item['type-gameId'].split('::')[2]),
                    hometeam: item.hometeam,
                    awayTeam: item.awayteam,
                    actualOdds: Number(item.actual),
                    impliedOdds: Number(item.implied),
                    edge: Number(item.edge),
                    pick: item.pick,
                }
            })
            return response
        }
        catch (error) {
            console.error('Error fetching picks:', error)
            throw new Error('Error fetching picks')
        }
    }
}