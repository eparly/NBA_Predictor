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

export type SingleRecordResponse = {
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

export type RecordsResponse = {
    preds?: SingleRecordResponse[];
    picks?: SingleRecordResponse[];
}

export enum RecordType {
    preds = 'preds',
    value = 'value',
    all = 'all'
}