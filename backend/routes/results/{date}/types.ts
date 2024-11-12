export type DynamoDBResults = {
    date: string;
    'type-gameId': string;
    homescore: number;
    awayscore: number;
    hometeam: string;
    awayteam: string;
}

export type ResultsMap = {
    homeScore: number,
    awayScore: number,
    homeTeam: string,
    awayTeam: string,
}

export type ResultsResponse = {
    date: string,
    gameId: number,
    homeTeam: string,
    awayTeam: string,
    results: {
        homeScore: number,
        awayScore: number,
    },
    predictions: {
        homeScore: number,
        awayScore: number,
        confidence: number,
        correct: boolean,
    },
    odds: {
        homeML: number,
        awayML: number,
        spread: number,
    }
}