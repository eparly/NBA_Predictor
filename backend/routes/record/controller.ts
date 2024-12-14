import { DynamoDBService } from "../../dynamodb/DynamoDBService";
import { DynamoDBRecords, RecordsResponse, RecordType, SingleRecordResponse } from "./types";

export class RecordController {
    private readonly dynamoDbService: DynamoDBService

    constructor(dynamoDbService: DynamoDBService) {
        this.dynamoDbService = dynamoDbService
    }

    public async getRecords(queryType?: RecordType): Promise<RecordsResponse | undefined> {
        try {
            let predRecords: SingleRecordResponse[] = []
            let picksRecords: SingleRecordResponse[] = []
            if (queryType && !Object.values(RecordType).includes(queryType)) {
                throw new Error('Invalid query type')
            }

            if (!queryType || queryType === RecordType.preds || queryType === RecordType.all) {
                const records = await this.dynamoDbService.getAllRecords()

                predRecords = (records.Items as DynamoDBRecords[] || []).map((item) => {
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
            }

            if (queryType === RecordType.value || queryType === RecordType.all) {
                const dbPicksRecords = await this.dynamoDbService.getAllPicksRecord(RecordType.value)
                picksRecords = (dbPicksRecords.Items as DynamoDBRecords[] || []).map((item) => {
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
            }

        
            if (!queryType || queryType === RecordType.preds) {
                return { preds: predRecords }
            }
            else if (queryType === RecordType.all) {
                return {
                    preds: predRecords,
                    picks: picksRecords
                } 
            }
            else if (queryType === RecordType.value) {
                return { picks: picksRecords }
            }
        }

        catch (error) {
            console.log('Error fetching records:', error)
            throw new Error('Error fetching records')
        }
    }
}