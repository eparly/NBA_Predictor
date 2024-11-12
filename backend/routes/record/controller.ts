import { DynamoDBService } from "../../dynamodb/DynamoDBService";
import { DynamoDBRecords, RecordsResponse } from "./types";

export class RecordController {
    private readonly dynamoDbService: DynamoDBService

    constructor(dynamoDbService: DynamoDBService) {
        this.dynamoDbService = dynamoDbService
    }

    public async getRecords(): Promise<RecordsResponse[]> {
        try {
            const records = await this.dynamoDbService.getAllRecords()
            
            const response: RecordsResponse[] = (records.Items as DynamoDBRecords[] || []).map((item) => {
                return {
                    date: item.date,
                    allTime: {
                        correct: item.allTime.correct,
                        percentage: Number(item.allTime.percentage),
                        total: item.allTime.total,
                        units: Number(item.allTime.units),
                    },
                    today: {
                        correct: item.today.correct,
                        percentage: Number(item.today.percentage),
                        total: item.today.total,
                        units: Number(item.today.units),
                    }

                }
            })

            return response
        }

        catch (error) {
            console.error('Error fetching records:', error)
            throw new Error('Error fetching records')
        }
    }
}