from datetime import datetime, timedelta

# from predictions.spreads import spread_results
# from Predictor_db.NBA_Predictor.db_management import get_predictions, get_results, insert_record
from utils.utils import get_winner

class RecordService:
    def __init__ (self, dynamoDbService):
        self.dynamoDbService = dynamoDbService
        
    def update_records(self): 
        today = datetime.today()
        yesterday = today - timedelta(1)
        #todo: don't hardcode dates
        yesterday = '2024-01-19'

        correct = 0
        games = 0
        games_2 = 0
        results = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(yesterday, 'results')
        predictions = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(yesterday, 'predictions')
        yesterdayRecord = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(yesterday, 'record')[0]
    
        correct, games = self.records(predictions, results)
        if games == 0:
            return
        score = {
            #todo: don't hardcode dates
            "date": '2024-01-20',
            "type-gameId": "record",
            "today": {
                "correct": correct,
                "total": games,
                "percentage": str(round(correct/games, 4))
            },
            "allTime": {
                "correct": yesterdayRecord['allTime']["correct"]+ correct,
                "total": yesterdayRecord['allTime']['total']+ games,
                "percentage": str(round((yesterdayRecord['allTime']["correct"]+ correct)/(yesterdayRecord['allTime']['total']+ games), 4))
            } 
        }
        print(score)
        self.dynamoDbService.create_item(score)
        return
        # todo: support multiple models
        # scores = get_predictions('scores', 'all')
        # correct, games = self.records(scores, results)

        # score = {
        #     "correct": correct,
        #     "total": games,
        #     "percentage": round(correct/games, 4)
        # }
        # insert_record(today, score, 'record_2')

        # scores = get_predictions('factors', 'all')
        # correct, games = self.records(scores, results)

        # score = {
        #     "correct": correct,
        #     "total": games,
        #     "percentage": round(correct/games, 4)
        # }
        # insert_record(today, score, 'record_3')

        # scores = get_predictions('montecarlohomefactors', 'all')
        # correct, games = self.records(scores, results)

        # score = {
        #     "correct": correct,
        #     "total": games,
        #     "percentage": round(correct/games, 4)
        # }
        # insert_record(today, score, 'record_4')

        # scores = get_predictions('streak_multiplier', 'all')
        # correct, games = self.records(scores, results)

        # score = {
        #     "correct": correct,
        #     "total": games,
        #     "percentage": round(correct/games, 4)
        # }
        # insert_record(today, score, 'streak_multiplier_record')

        # scores = get_predictions('streak_factor', 'all')
        # correct, games = self.records(scores, results)

        # score = {
        #     "correct": correct,
        #     "total": games,
        #     "percentage": round(correct/games, 4)
        # }
        # insert_record(today, score, 'streak_factor_record')

        # score = spread_results('spread_picks')
        # insert_record(today, score, 'spread_picks_record')

        # score = spread_results('home_spread_picks')
        # insert_record(today, score, 'home_spread_picks_record')
        
        # scores = get_predictions('home_streak_multiplier', 'all')
        # correct, games = self.records(scores, results)

        # score = {
        #     "correct": correct,
        #     "total": games,
        #     "percentage": round(correct/games, 4)
        # }
        # insert_record(today, score, 'home_streak_multiplier_record')
        # return score

    def records(self, predictions, results):
        games = 0
        correct = 0

        # game_ids = [x[0] for x in predictions]
        game_ids = [prediction['type-gameId'].split('::')[1] for prediction in predictions]
        for i in game_ids:
            prediction = [x for x in predictions if x['type-gameId'].split('::')[1] == i]
            result = [x for x in results if x['type-gameId'].split('::')[1] == i]
            if (prediction and result):
                prediction = prediction[0]
                result = result[0]
                predicted_winner = get_winner(prediction)
                actual_winner = get_winner(result)
                games += 1
                if (predicted_winner == actual_winner):
                    correct += 1
        return correct, games
    
    
    
# [
#     {'date': '2024-01-19', 'type-gameId': 'predictions::607', 'hometeam': 'Charlotte Hornets', 'awayteam': 'San Antonio Spurs', 'homescore': Decimal('120'), 'awayscore': Decimal('115')},
#     {'date': '2024-01-19', 'type-gameId': 'predictions::608', 'hometeam': 'Orlando Magic', 'awayteam': 'Philadelphia 76ers', 'homescore': Decimal('110'), 'awayscore': Decimal('120')},
#     {'date': '2024-01-19', 'type-gameId': 'predictions::609', 'hometeam': 'Boston Celtics', 'awayteam': 'Denver Nuggets', 'homescore': Decimal('105'), 'awayscore': Decimal('100')},
#     {'date': '2024-01-19', 'type-gameId': 'predictions::610', 'hometeam': 'Miami Heat', 'awayteam': 'Atlanta Hawks', 'homescore': Decimal('110'), 'awayscore': Decimal('105')},
#     {'date': '2024-01-19', 'type-gameId': 'predictions::611', 'hometeam': 'New Orleans Pelicans', 'awayteam': 'Phoenix Suns', 'homescore': Decimal('115'), 'awayscore': Decimal('120')},
#     {'date': '2024-01-19', 'type-gameId': 'predictions::613', 'hometeam': 'Portland Trail Blazers', 'awayteam': 'Indiana Pacers', 'homescore': Decimal('120'), 'awayscore': Decimal('110')},
#     {'date': '2024-01-19', 'type-gameId': 'predictions::614', 'hometeam': 'Los Angeles Lakers', 'awayteam': 'Brooklyn Nets', 'homescore': Decimal('115'), 'awayscore': Decimal('125')}
# ]
