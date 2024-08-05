from datetime import datetime, timedelta
from utils.utils import get_winner
from dynamodb.dynamoDbService import DynamoDBService

class RecordService:
    def __init__ (self, dynamoDbService: DynamoDBService):
        self.dynamoDbService = dynamoDbService
        
    def update_records(self): 
        today = datetime.today()
        yesterday = today - timedelta(1)
        #todo: don't hardcode dates
        #todo: add support for when no games were played? Maybe don't always pick yesterday
        #but the most recent day on record
        yesterday = '2024-01-19'

        correct = 0
        games = 0
        games_2 = 0
        results = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(yesterday, 'results')
        predictions = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(yesterday, 'predictions')
        yesterdayRecord = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(yesterday, 'record')[0]
        odds = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(yesterday, 'odds')
    
        correct, games = self.records(predictions, results)
        units = self.calculate_units(predictions, results, odds)
        if games == 0:
            return
        #todo: add support for multiple models
        score = {
            #todo: don't hardcode dates
            "date": '2024-01-20',
            "type-gameId": "record",
            "today": {
                "correct": correct,
                "total": games,
                "percentage": str(round(correct/games, 4)),
                "units": str(units)
            },
            "allTime": {
                "correct": yesterdayRecord['allTime']["correct"]+ correct,
                "total": yesterdayRecord['allTime']['total']+ games,
                "percentage": str(round((yesterdayRecord['allTime']["correct"]+ correct)/(yesterdayRecord['allTime']['total']+ games), 4)),
                "units": str(float(yesterdayRecord['allTime']['units']) + units)
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
    
    def calculate_units(self, predictions, results, odds):
        result_game_ids = [x['type-gameId'].split('::')[1] for x in results]
        odds_game_ids = [x['type-gameId'].split('::')[1] for x in odds]
        prediction_game_ids = [prediction['type-gameId'].split('::')[1] for prediction in predictions]
        game_ids_with_odds = [x for x in prediction_game_ids if x in odds_game_ids and x in result_game_ids]
        units_won = 0
        for i in game_ids_with_odds:
            prediction = [x for x in predictions if x['type-gameId'].split('::')[1] == i][0]
            result =  [x for x in results if x['type-gameId'].split('::')[1] == i][0]
            single_game_odds = [x for x in odds if x['type-gameId'].split('::')[1] == i][0]
            predicted_winner = get_winner(prediction)
            actual_winner = get_winner(result)
            if predicted_winner == actual_winner:
                if predicted_winner == 'home':
                    units_won += float(single_game_odds['homeML'])
                else:
                    units_won += float(single_game_odds['awayML'])
        units_won -= len(game_ids_with_odds)
        return round(units_won, 3)

    #todo: remove this function when support is added for multiple models
    def update_units(self):
        today = datetime.today()

        games_units = self.calculate_units('games')
        #todo: support multiple models
        # scores_units = self.calculate_units('scores')
        # factors_units = self.calculate_units('factors')
        # montecarlohomefactors_units = self.calculate_units('montecarlohomefactors')
        # streak_multiplier_units = self.calculate_units('streak_multiplier')
        # streak_factor_units = self.calculate_units('streak_factor')
        # home_streak_multiplier_units = self.calculate_units('home_streak_multiplier')

        # units = {
        #     "games": games_units,
        #     "scores": scores_units,
        #     "factors": factors_units,
        #     "montecarlohomefactors": montecarlohomefactors_units,
        #     "streak_multiplier": streak_multiplier_units,
        #     "streak_factor": streak_factor_units,
        #     "home_streak_multiplier": home_streak_multiplier_units
        # }
        # insert_units(today, units)
