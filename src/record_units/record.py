from datetime import datetime, timedelta

import dateutil.tz
from utils.utils import get_winner
from dynamodb.dynamoDbService import DynamoDBService

class RecordService:
    def __init__ (self, dynamoDbService: DynamoDBService):
        self.dynamoDbService = dynamoDbService
        eastern = dateutil.tz.gettz('US/Eastern')
        date = datetime.now(tz = eastern)
        self.str_date = date.strftime('%Y-%m-%d')
        self.yesterday = (date - timedelta(1)).strftime('%Y-%m-%d')
    
        
    def update_records(self): 
        results, most_recent_date = self.dynamoDbService.get_all_recent_records('results')
        predictions = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.yesterday, 'predictions')
        yesterdayRecord = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.yesterday, 'record')
        odds = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.yesterday, 'odds')
        
        yesterdayRecord = yesterdayRecord[0] if yesterdayRecord else {}
        correct, games = self.records(predictions, results)
        print('correct', correct)
        print('games', games)
        all_time = yesterdayRecord.get('allTime', {
                "correct": 0,
                "total": 0,
                "percentage": "0.0",
                "units": "0.0"
        })
        if games == 0:
            score = {
                "date": self.str_date,
                "type-gameId": "record",
                "today": {
                    "correct": 0,
                    "total": 0,
                    "percentage": '0.0',
                    "units": '0.0'
                },
                "allTime": {
                    "correct": all_time["correct"]+ correct,
                    "total": all_time['total']+ games,
                    "percentage": str(round((all_time["correct"]+ correct)/(all_time['total']+ games), 4)),
                    "units": str(float(all_time['units']))
                } 
            }
            print('no games yesterday')
        else:
            units = self.calculate_units(predictions, results, odds)

            score = {
                #todo: don't hardcode dates
                "date": self.str_date,
                "type-gameId": "record",
                "today": {
                    "correct": correct,
                    "total": games,
                    "percentage": str(round(correct/games, 4)),
                    "units": str(units)
                },
                "allTime": {
                    "correct": all_time["correct"]+ correct,
                    "total": all_time['total']+ games,
                    "percentage": str(round((all_time["correct"]+ correct)/(all_time['total']+ games), 4)),
                    "units": str(float(all_time['units']) + units)
                } 
            }
        print(score)
        self.dynamoDbService.create_item(score)
        return

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
                    units_won += float(single_game_odds['home_ml'])
                else:
                    units_won += float(single_game_odds['away_ml'])
        units_won -= len(game_ids_with_odds)
        return round(units_won, 3)
    
    def update_picks(self):
        # picks = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.yesterday, 'picks::value')
        # results = self.dynamoDbService.get_all_recent_records('results')
        
        
        #todo: Update dates
        # support record and record::value updates in the update records function
        #add this function to the step functions
        # run this function and picks lambda for all dates that have been missed. Try generating some script or lambda to do it all at once
        picks = self.dynamoDbService.get_items_by_date_and_sort_key_prefix('2024-12-08', 'picks::value')
        results = self.dynamoDbService.get_items_by_date_and_sort_key_prefix('2024-12-08', 'results')
        yesterdayRecord = self.dynamoDbService.get_items_by_date_and_sort_key_prefix('2024-12-08', 'record::value')

        print('yesterdayRecord', yesterdayRecord)
        all_time = yesterdayRecord.get('allTime', {
                "correct": 0,
                "total": 0,
                "percentage": "0.0",
                "units": "0.0"
        })
        if (len(picks) == 0):
            score = {
                "date": '2024-12-09',
                "type-gameId": "record::value",
                "today": {
                    "correct": 0,
                    "total": 0,
                    "percentage": '0.0',
                    "units": '0.0'
                },
                "allTime": all_time
            }
            print('no games yesterday')
        else:
            units, correct = self.calculate_picks_units(picks, results)
            print('units', units)
            print('correct', correct)
            score = {
                #todo: don't hardcode dates
                "date": '2024-12-09',
                "type-gameId": "record::value",
                "today": {
                    "correct": correct,
                    "total": len(picks),
                    "percentage": str(round(correct/len(picks), 4)),
                    "units": str(units)
                },
                "allTime": {
                    "correct": all_time["correct"] + correct,
                    "total": all_time['total']+ len(picks),
                    "percentage": str(round((all_time["correct"]+ correct)/(all_time['total']+ len(picks)), 4)),
                    "units": str(float(all_time['units']) + units)
                } 
            }
        print(score)
        self.dynamoDbService.create_item(score)
        return
    
    def calculate_picks_units(self, picks, results):
        results_game_ids = [x['type-gameId'].split('::')[-1] for x in results]
        picks_game_ids = [x['type-gameId'].split('::')[-1] for x in picks]
        units = 0
        correct = 0
        
        results_with_picks = [x for x in results_game_ids if x in picks_game_ids]
        
        for i in results_with_picks:
            pick = [x for x in picks if x['type-gameId'].split('::')[-1] == i][0]
            result =  [x for x in results if x['type-gameId'].split('::')[-1] == i][0]
            actual_winner = get_winner(result)
            predicted_winner = pick['pick']
            predicted_winner = 'home' if predicted_winner == result['hometeam'] else 'away'
            
            if predicted_winner == actual_winner:
                correct += 1
                units += float(pick['actual'])
        units -= len(results_with_picks)
        print('units', units)
        return round(units, 3) , correct

    #todo: add support for multiple models
   