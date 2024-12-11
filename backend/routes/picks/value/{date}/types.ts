export type PicksResponse = {
    date: string,
    gameId: number,
    hometeam: string,
    awayTeam: string,
    actualOdds: number,
    impliedOdds: number,
    edge: number,
    pick: string,
}

export type DynamoDBPicks = {
    date: string;
    'type-gameId': string;
    hometeam: string;
    awayteam: string;
    actual: string;
    implied: string;
    edge: string;
    pick: string;
}