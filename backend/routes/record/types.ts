export type DynamoDBRecords = {
    date: string;
    'type-gameId': string;
    allTime: {
        correct: number;
        percentage: string;
        total: number;
        units: string;
    };
    today: {
        correct: number;
        percentage: string;
        total: number;
        units: string;
    }
}

export type RecordsResponse = {
    date: string;
    allTime: {
        correct: number;
        percentage: number;
        total: number;
        units: number;
    };
    today: {
        correct: number;
        percentage: number;
        total: number;
        units: number;
    }
}