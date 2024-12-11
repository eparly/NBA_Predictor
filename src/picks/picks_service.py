from datetime import datetime
import dateutil
from dynamodb.dynamoDbService import DynamoDBService


class PicksService:
    def __init__(self, dynamoDbService: DynamoDBService, edge: float = 0.0, inverse_edge: float = 0.0):
        self.dynamoDbService = dynamoDbService
        
        self.edge = edge
        self.inverse_edge = inverse_edge
        eastern = dateutil.tz.gettz('US/Eastern')
        self.date = datetime.now(tz = eastern).strftime('%Y-%m-%d')
        
    def value_picks(self):
        odds = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.date, 'odds')
        predictions = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.date, 'predictions')
        
        for pred in predictions:
            game_id = pred['type-gameId'].split('::')[1]
            homescore = int(pred['homescore'])
            awayscore = int(pred['awayscore'])
            confidence = float(pred['confidence'])
            game_odds = [item for item in odds if item['type-gameId'].split('::')[1] == game_id][0]
            print('picking game', game_id)
            if (homescore >= awayscore):
                home_confidence = confidence
                away_confidence = 1 - confidence
                
                implied_home = 1 / home_confidence
                implied_away = 1 / away_confidence
                
                actual_home = float(game_odds['home_ml'])
                actual_away = float(game_odds['away_ml'])
                
                diff_home = actual_home - implied_home
                diff_away = actual_away - implied_away
                
                if (diff_home >= self.edge):
                    print('Value on home team', game_id)
                    record = {
                        'date': self.date,
                        'type-gameId': 'picks::value::'+game_id,
                        'hometeam': pred['hometeam'],
                        'awayteam': pred['awayteam'],
                        'pick': pred['hometeam'],
                        'actual': str(actual_home),
                        'implied': str(implied_home),
                        'edge': str(diff_home)
                    }
                    print('record', record)
                    self.dynamoDbService.create_item(record)
                elif (diff_away >= self.inverse_edge):
                    print('Value on away team', game_id)
                    record = {
                        'date': self.date,
                        'type-gameId': 'picks::value::'+game_id,
                        'hometeam': pred['hometeam'],
                        'awayteam': pred['awayteam'],
                        'pick': pred['awayteam'],
                        'actual': str(actual_away),
                        'implied': str(implied_away),
                        'edge': str(diff_away)
                    }
                else:
                    print('No value on home team', game_id)
            if (homescore < awayscore):
                home_confidence = 1 - confidence
                away_confidence = confidence
                
                implied_home = 1 / home_confidence
                implied_away = 1 / away_confidence
                print(game_odds)
                
                actual_home = float(game_odds['home_ml'])
                actual_away = float(game_odds['away_ml'])
                
                diff_home = actual_home - implied_home
                diff_away = actual_away - implied_away
                
                if (diff_away > self.edge):
                    print('Value on away team', game_id)
                    record = {
                        'date': self.date,
                        'type-gameId': 'picks::value::'+game_id,
                        'hometeam': pred['hometeam'],
                        'awayteam': pred['awayteam'],
                        'pick': pred['awayteam'],
                        'actual': str(actual_away),
                        'implied': str(implied_away),
                        'edge': str(diff_away)
                    }
                    print('record', record)
                    self.dynamoDbService.create_item(record)
                elif (diff_home > self.inverse_edge):
                    print('Value on home team', game_id)
                    record = {
                        'date': self.date,
                        'type-gameId': 'picks::value::'+game_id,
                        'hometeam': pred['hometeam'],
                        'awayteam': pred['awayteam'],
                        'pick': pred['hometeam'],
                        'actual': str(actual_home),
                        'implied': str(implied_home),
                        'edge': str(diff_home)
                    }
                    print('record', record)
                    self.dynamoDbService.create_item(record)
                else:
                    print('No value on away team', game_id)
        return
                
                
                
                
            
            
    
        
        
        
        
        