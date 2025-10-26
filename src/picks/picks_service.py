from datetime import datetime, timedelta
import dateutil
from dynamodb.dynamoDbService import DynamoDBService


class PicksService:
    def __init__(self, dynamoDbService: DynamoDBService, edge: float = 0.0, inverse_edge: float = 0.0):
        self.dynamoDbService = dynamoDbService
        
        self.edge = edge
        self.inverse_edge = inverse_edge
        eastern = dateutil.tz.gettz('US/Eastern')
        self.date = datetime.now(tz = eastern).strftime('%Y-%m-%d')
        self.yesterday = (datetime.now(tz = eastern) - timedelta(1)).strftime('%Y-%m-%d')
        print('yesterday', self.yesterday)
    def all_picks(self):
        odds = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.date, 'odds')
        predictions = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.date, 'predictions')
        self.value_picks(odds, predictions)
        self.spread_picks(odds, predictions)
        self.total_picks(odds, predictions)
        self.ev_picks(odds, predictions)
        
    def value_picks(self, odds, predictions):
        
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
                    self.dynamoDbService.create_item(record)
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
    
    def spread_picks(self, odds, predictions):
       
        for pred in predictions:
            game_id = pred['type-gameId'].split('::')[1]
            homescore = int(pred['homescore'])
            awayscore = int(pred['awayscore'])
            game_odds = [item for item in odds if item['type-gameId'].split('::')[1] == game_id][0]
            spread_home = float(game_odds['spreadHome'])
            spread_away = float(game_odds['spreadAway'])
            spread_home_odds = float(game_odds['spreadHomeOdds'])
            spread_away_odds = float(game_odds['spreadAwayOdds'])
            
            predicted_home_score = homescore + spread_home
            
            if (predicted_home_score >= awayscore):
                record = {
                    'date': self.date,
                    'type-gameId': 'picks::spread::'+game_id,
                    'hometeam': pred['hometeam'],
                    'awayteam': pred['awayteam'],
                    'spreadOdds': str(spread_home_odds),
                    'pickTeam': pred['hometeam'],
                    'pickSpread': str(spread_home),
                }
                self.dynamoDbService.create_item(record)
            else:
                record = {
                    'date': self.date,
                    'type-gameId': 'picks::spread::'+game_id,
                    'hometeam': pred['hometeam'],
                    'awayteam': pred['awayteam'],
                    'spreadOdds': str(spread_away_odds),
                    'pickTeam': pred['awayteam'],
                    'pickSpread': str(spread_away),
                }
                self.dynamoDbService.create_item(record)
                
    def total_picks(self, odds, predictions):
        for pred in predictions:
            game_id = pred['type-gameId'].split('::')[1]
            homescore = int(pred['homescore'])
            awayscore = int(pred['awayscore'])
            game_odds = [item for item in odds if item['type-gameId'].split('::')[1] == game_id][0]
            
            predicted_total = homescore + awayscore
            total = float(game_odds['total'])
            if((predicted_total + 3) < total):
                    record = {
                        'date': self.date,
                        'type-gameId': 'picks::total::v2::'+game_id,
                        'hometeam': pred['hometeam'],
                        'awayteam': pred['awayteam'],
                        'total': str(total),
                        'pick': 'under',
                        'pickOdds': str(game_odds['totalUnder'])
                    }
                    self.dynamoDbService.create_item(record)
            else:
                record = {
                    'date': self.date,
                    'type-gameId': 'picks::total::v2::'+game_id,
                    'hometeam': pred['hometeam'],
                    'awayteam': pred['awayteam'],
                    'total': str(total),
                    'pick': 'over',
                    'pickOdds': str(game_odds['totalOver'])
                }
                self.dynamoDbService.create_item(record)
                
    def ev_picks(self, odds, predictions):
        ev_threshold = 0.5
        picks = []
        for pred in predictions:
            game_id = pred['type-gameId'].split('::')[1]
            homescore = int(pred['homescore'])
            awayscore = int(pred['awayscore'])
            confidence = float(pred['confidence'])
            try:
                game_odds = [item for item in odds if item['type-gameId'].split('::')[1] == game_id][0]
            except IndexError:
                continue

            # Calculate probabilities
            home_confidence = confidence if homescore >= awayscore else 1 - confidence
            away_confidence = 1 - home_confidence

            # Calculate payouts
            actual_home = float(game_odds['home_ml'])
            actual_away = float(game_odds['away_ml'])
            payout_home = actual_home - 1  # Subtracting 1 to account for the bet amount
            payout_away = actual_away - 1

            # Calculate EV for home and away
            ev_home = (home_confidence * payout_home) - (away_confidence * 1)
            ev_away = (away_confidence * payout_away) - (home_confidence * 1)

            # Make picks based on EV threshold
            if ev_home > ev_threshold:
                picks.append({
                    'type-gameId': f'picks::ev::{game_id}',
                    'pick': pred['hometeam'],
                    'actual': actual_home,
                    'hometeam': pred['hometeam'],
                    'awayteam': pred['awayteam'],
                })
            elif ev_away > ev_threshold:
                picks.append({
                    'type-gameId': f'picks::ev::{game_id}',
                    'pick': pred['awayteam'],
                    'actual': actual_away,
                    'hometeam': pred['hometeam'],
                    'awayteam': pred['awayteam'],
                })

        # Initialize all_time if not already set
        yesterday_record = self.dynamoDbService.get_items_by_date_and_exact_sort_key(self.yesterday, 'record::ev')
        yesterday_record = yesterday_record[0] if yesterday_record else {}

        all_time = yesterday_record.get('allTime', {
            "correct": 0,
            "total": 0,
            "percentage": "0.0",
            "units": "0.0",
            "bankroll": "100.0"
        })

        # Initialize bankroll as a string and convert when needed
        bankroll = float(all_time.get("bankroll", "100.0"))

        # Calculate Kelly Fraction and Bet Size
        for pick in picks:
            b = float(pick['actual']) - 1  # Net payout
            p = confidence  # Probability of winning
            q = 1 - p  # Probability of losing
            kelly_fraction = (b * p - q) / b

            # Apply 50% Kelly Criterion
            if kelly_fraction > 0:
                bet_size = bankroll * kelly_fraction * 0.50
                pick['kelly_fraction'] = kelly_fraction
                pick['bet_size'] = round(bet_size, 2)

        # Calculate total Kelly bets for the day
        total_kelly_bets = sum(pick['bet_size'] for pick in picks if 'bet_size' in pick)
        daily_cap = bankroll * 0.05  # 5% of the bankroll

        # Scale down bets if total exceeds daily cap
        if total_kelly_bets > daily_cap:
            scaling_factor = daily_cap / total_kelly_bets
            for pick in picks:
                if 'bet_size' in pick:
                    pick['bet_size'] = round(pick['bet_size'] * scaling_factor, 2)

        # Store picks in DynamoDB
        for pick in picks:
            record = {
                'date': self.date,
                'type-gameId': pick['type-gameId'],
                'pick': pick['pick'],
                'actual': str(pick['actual']),
                'bet_size': str(pick['bet_size']) if 'bet_size' in pick else '0.0',
                'hometeam': pick['hometeam'],
                'awayteam': pick['awayteam'],
            }
            self.dynamoDbService.create_item(record)
            
            

    # functions used to generate picks from previous days
    def generate_date_range(self, start_date: str, end_date: str):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        delta = timedelta(days=1)
        current = start
        dates = []
        while current <= end:
            dates.append(current.strftime('%Y-%m-%d'))
            current += delta
        return dates
    
    def run_for_date(self, date: str):
        eastern = dateutil.tz.gettz('US/Eastern')
        self.date = datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=eastern).strftime('%Y-%m-%d')
        # self.value_picks()
        # self.spread_picks()
        # self.total_picks()
        self.all_picks()
    
    def run_picks_service_for_date_range(self, start_date: str, end_date: str):
        dates = self.generate_date_range(start_date, end_date)
        for date in dates:
            print('running for date', date)
            self.run_for_date(date)