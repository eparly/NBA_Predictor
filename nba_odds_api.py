import requests
import numpy as np
import json
import unittest.mock

from Predictor_db.NBA_Predictor.db_management import insert_odds, get_predictions

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get('API_KEY')

def match_order(A, B):
    A = np.array(A)
    B = np.array(B)

    game_order = []
    for j in range(len(A)):
        game_id = [i for i in range(len(
            B)) if A[:, 1:3][j][0] == B[:, 1:3][i][0] and A[:, 1:3][j][1] == B[:, 1:3][i][1]]
        if len(game_id) == 0:
            break
        game_id = B[game_id[-1]][0]

        game_order.append(game_id)

    return game_order


def set_odds():
    predictions = get_predictions('games', 'all')

    url = "https://sportspage-feeds.p.rapidapi.com/games"
    querystring = {"league": "NBA"}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "sportspage-feeds.p.rapidapi.com"
    }

    if predictions == ([0, 0, 0, 0, 0, 0]):
        response = unittest.mock.MagicMock()
        response.json.return_value = {
            "status": 200,
            "time": "2022-09-20T13:19:57.022Z",
            "games": 1,
            "skip": 0,
            "results": [
                {
                    "schedule": {
                        "date": "2022-02-13T23:30:00.000Z",
                        "tbaTime": False
                    },
                    "summary": "Los Angeles Rams @ Cincinnati Bengals",
                    "details": {
                        "league": "NFL",
                        "seasonType": "postseason",
                        "season": 2021,
                        "conferenceGame": False,
                        "divisionGame": False
                    },
                    "status": "final",
                    "teams": {
                        "away": {
                            "team": "Los Angeles Rams",
                            "location": "Los Angeles",
                            "mascot": "Rams",
                            "abbreviation": "LAR",
                            "conference": "NFC",
                            "division": "West"
                        },
                        "home": {
                            "team": "Cincinnati Bengals",
                            "location": "Cincinnati",
                            "mascot": "Bengals",
                            "abbreviation": "CIN",
                            "conference": "AFC",
                            "division": "North"
                        }
                    },
                    "lastUpdated": "2022-02-14T03:02:18.640Z",
                    "gameId": 278943,
                    "odds": [
                        {
                            "spread": {
                                "open": {
                                    "away": -4,
                                    "home": 4,
                                    "awayOdds": -110,
                                    "homeOdds": -115
                                },
                                "current": {
                                    "away": -4,
                                    "home": 4,
                                    "awayOdds": -110,
                                    "homeOdds": -110
                                }
                            },
                            "moneyline": {
                                "open": {
                                    "awayOdds": -193,
                                    "homeOdds": 166
                                },
                                "current": {
                                    "awayOdds": -196,
                                    "homeOdds": 168
                                }
                            },
                            "total": {
                                "open": {
                                    "total": 49.5,
                                    "overOdds": -110,
                                    "underOdds": -110
                                },
                                "current": {
                                    "total": 48.5,
                                    "overOdds": -110,
                                    "underOdds": -110
                                }
                            },
                            "openDate": "2022-01-31T13:46:07.823Z",
                            "lastUpdated": "2022-02-13T23:23:16.272Z"
                        }
                    ],
                    "venue": {
                        "name": "SoFi Stadium",
                        "city": "Inglewood",
                        "state": "CA",
                        "neutralSite": True
                    },
                    "scoreboard": {
                        "score": {
                            "away": 23,
                            "home": 20,
                            "awayPeriods": [
                                7,
                                6,
                                3,
                                7
                            ],
                            "homePeriods": [
                                3,
                                7,
                                10,
                                0
                            ]
                        },
                        "currentPeriod": 4,
                        "periodTimeRemaining": "0:00"
                    }
                },
                {
                    "schedule": {
                        "date": "2022-02-13T19:00:00.000Z",
                        "tbaTime": False
                    },
                    "summary": "Atlanta Hawks @ Boston Celtics",
                    "details": {
                        "league": "NBA",
                        "seasonType": "regular",
                        "season": 2021,
                        "conferenceGame": True,
                        "divisionGame": False
                    },
                    "status": "final",
                    "teams": {
                        "away": {
                            "team": "Atlanta Hawks",
                            "location": "Atlanta",
                            "mascot": "Hawks",
                            "abbreviation": "ATL",
                            "conference": "Eastern",
                            "division": "Southeast"
                        },
                        "home": {
                            "team": "Boston Celtics",
                            "location": "Boston",
                            "mascot": "Celtics",
                            "abbreviation": "BOS",
                            "conference": "Eastern",
                            "division": "Atlantic"
                        }
                    },
                    "lastUpdated": "2022-02-13T21:29:03.153Z",
                    "gameId": 268320,
                    "venue": {
                        "name": "TD Garden",
                        "city": "Boston",
                        "state": "MA",
                        "neutralSite": False
                    },
                    "odds": [
                        {
                            "spread": {
                                "open": {
                                    "away": 7,
                                    "home": -7,
                                    "awayOdds": -110,
                                    "homeOdds": -110
                                },
                                "current": {
                                    "away": 7.5,
                                    "home": -7.5,
                                    "awayOdds": -110,
                                    "homeOdds": -110
                                }
                            },
                            "moneyline": {
                                "open": {
                                    "awayOdds": 225,
                                    "homeOdds": -275
                                },
                                "current": {
                                    "awayOdds": 247,
                                    "homeOdds": -299
                                }
                            },
                            "total": {
                                "open": {
                                    "total": 220.5,
                                    "overOdds": -110,
                                    "underOdds": -110
                                },
                                "current": {
                                    "total": 223.5,
                                    "overOdds": -110,
                                    "underOdds": -110
                                }
                            },
                            "openDate": "2022-02-13T12:45:59.014Z",
                            "lastUpdated": "2022-02-13T19:23:41.660Z"
                        }
                    ],
                    "scoreboard": {
                        "score": {
                            "away": 95,
                            "home": 105,
                            "awayPeriods": [
                                28,
                                27,
                                23,
                                17
                            ],
                            "homePeriods": [
                                17,
                                28,
                                42,
                                18
                            ]
                        },
                        "currentPeriod": 4,
                        "periodTimeRemaining": "0:00"
                    }
                }
            ]
        }
    else:
        response = requests.get(url, headers=headers, params=querystring)
        a=0

    games = len(response.json()['results'])

    # games from this api arent in the same order as the other one, need to enter these ones in the same order as we do for all predictions
    spread_data = []
    i = 0
    for i in range(games):
        if "odds" not in response.json()['results'][i]:
            return 'no odds yet, check back later'
        spreads = response.json(
        )['results'][i]['odds'][0]['spread']['current']['home']
        hometeam = response.json()['results'][i]['teams']['home']['team']
        awayteam = response.json()['results'][i]['teams']['away']['team']

        spread_data.append((spreads, hometeam, awayteam))
    matched_order = match_order(spread_data, predictions)

    ordered_spreads = []
    for i in range(len(matched_order)):
        ordered_spreads.append((
            matched_order[i], spread_data[i][0], spread_data[i][1], spread_data[i][2]))
        insert_odds(values=ordered_spreads[i])

    return spread_data


game_ids = [
    427,
    428,
    429,
    430,
    431,
    432,
    433,
    434,
    435,
    436
]
# predictions = get_predictions('games', 'all')
# odds = get_predictions('odds', 'all')
# match_order(odds, predictions)

# set_odds()
