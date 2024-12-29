export type DynamoDBPredictions = {
    date: string;
    'type-gameId': string;
    homescore: number;
    awayscore: number;
    confidence: string;
}

export type DynamoDBOdds = {
    date: string;
    'type-gameId': string;
    hometeam: string;
    awayteam: string;
    home_ml: string;
    away_ml: string;
    spreadAway: string;
    spreadHome: string;
    spreadAwayOdds: string;
    spreadHomeOdds: string;
    total: string;
    totalOver: string;
    totalUnder: string;
}

export type PredictionsResponse = {
    date: string,
    gameId: number,
    homeTeam: string,
    awayTeam: string,
    predictions: {
        homeScore: number,
        awayScore: number,
        confidence: number,
    },
    odds: {
        homeML: number,
        awayML: number,
        spread: number,
    }
};