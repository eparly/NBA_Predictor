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
    
    def update_all_records(self):
        results = self.dynamoDbService.get_all_recent_records('results', self.yesterday)
        # results = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.yesterday, 'results')
        self.update_records(results)
        self.update_picks(results)
        self.update_totals(results)
        self.update_spreads(results)
        self.evaluate_and_update_ev_record(results)
        return

        
        
    def update_records(self, results): 
        predictions = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.yesterday, 'predictions')
        yesterdayRecord = self.dynamoDbService.get_items_by_date_and_exact_sort_key(self.yesterday, 'record')
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
    
    def update_picks(self, results):
        picks = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.yesterday, 'picks::value')
        yesterdayRecord = self.dynamoDbService.get_items_by_date_and_exact_sort_key(self.yesterday, 'record::value')

        yesterdayRecord = yesterdayRecord[0] if yesterdayRecord else {}
        all_time = yesterdayRecord.get('allTime', {
                "correct": 0,
                "total": 0,
                "percentage": "0.0",
                "units": "0.0"
        })
        if (len(picks) == 0):
            score = {
                "date": self.str_date,
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
                "date": self.str_date,
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
            if(predicted_winner == 'Los Angeles Clippers'):
                predicted_winner = 'LA Clippers'
            predicted_winner = 'home' if predicted_winner == result['hometeam'] else 'away'
            
            if predicted_winner == actual_winner:
                correct += 1
                units += float(pick['actual'])
        units -= len(results_with_picks)
        print('units', units)
        return round(units, 3) , correct
    
    def update_spreads(self, results):
        picks = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.yesterday, 'picks::spread')
        yesterdayRecord = self.dynamoDbService.get_items_by_date_and_exact_sort_key(self.yesterday, 'record::spread')

        yesterdayRecord = yesterdayRecord[0] if yesterdayRecord else {}
        all_time = yesterdayRecord.get('allTime', {
                "correct": 0,
                "total": 0,
                "percentage": "0.0",
                "units": "0.0"
        })
        if (len(picks) == 0):
            score = {
                "date": self.str_date,
                "type-gameId": "record::spread",
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
            units, correct = self.calculate_spread_units(picks, results)
            print('units', units)
            print('correct', correct)
            score = {
                #todo: don't hardcode dates
                "date": self.str_date,
                "type-gameId": "record::spread",
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
    
    def calculate_spread_units(self, picks, results):
        results_game_ids = [x['type-gameId'].split('::')[-1] for x in results]
        picks_game_ids = [x['type-gameId'].split('::')[-1] for x in picks]
        units = 0
        correct = 0
        
        results_with_picks = [x for x in results_game_ids if x in picks_game_ids]
        
        for i in results_with_picks:
            pick = [x for x in picks if x['type-gameId'].split('::')[-1] == i][0]
            result =  [x for x in results if x['type-gameId'].split('::')[-1] == i][0]
                        
            pick_spread = float(pick['pickSpread'])
            predicted_team = "home" if pick['pickTeam'] == result['hometeam'] else "away"
            
            
            if predicted_team == "home":
                actual_with_spread = int(result['homescore']) + pick_spread - int(result['awayscore'])
            else:
                actual_with_spread = int(result['awayscore']) + pick_spread - int(result['homescore'])           


            if actual_with_spread > 0:
                correct += 1
                units += float(pick['spreadOdds'])
                
        units -= len(results_with_picks)
        print('units', units)
        return round(units, 3) , correct
    
    def update_totals(self, results):
        picks = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.yesterday, 'picks::total::v2')
        yesterdayRecord = self.dynamoDbService.get_items_by_date_and_exact_sort_key(self.yesterday, 'record::total::v2')

        yesterdayRecord = yesterdayRecord[0] if yesterdayRecord else {}
        all_time = yesterdayRecord.get('allTime', {
                "correct": 0,
                "total": 0,
                "percentage": "0.0",
                "units": "0.0"
        })
        if (len(picks) == 0):
            score = {
                "date": self.str_date,
                "type-gameId": "record::total::v2",
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
            units, correct = self.calculate_total_units(picks, results)
            print('units', units)
            print('correct', correct)
            score = {
                "date": self.str_date,
                "type-gameId": "record::total::v2",
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

    def calculate_total_units(self, picks, results):
        results_game_ids = [x['type-gameId'].split('::')[-1] for x in results]
        picks_game_ids = [x['type-gameId'].split('::')[-1] for x in picks]
        units = 0
        correct = 0
        
        results_with_picks = [x for x in results_game_ids if x in picks_game_ids]
        
        for i in results_with_picks:
            pick = [x for x in picks if x['type-gameId'].split('::')[-1] == i][0]
            result =  [x for x in results if x['type-gameId'].split('::')[-1] == i][0]
                        
            pick_total = float(pick['total'])
            over_under = pick['pick']
            actual_total = int(result['homescore']) + int(result['awayscore'])
            
            if (actual_total >= pick_total and over_under == 'over'):
                correct += 1
                units += float(pick['pickOdds'])
            elif (actual_total <= pick_total and over_under == 'under'):
                correct += 1
                units += float(pick['pickOdds'])
        units -= len(results_with_picks)
        print('units', units)
        return round(units, 3) , correct

    # functions used to get pick records from previous days
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
        self.str_date = datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=eastern).strftime('%Y-%m-%d')
        self.yesterday = (datetime.strptime(date, '%Y-%m-%d') - timedelta(1)).strftime('%Y-%m-%d')
        print('running for date', self.str_date)
        print('yesterday', self.yesterday)
        self.update_all_records()
    
    def run_picks_service_for_date_range(self, start_date: str, end_date: str):
        dates = self.generate_date_range(start_date, end_date)
        for date in dates:
            print('running for date', date)
            self.run_for_date(date)

    def test_ev_picks(self, start_date: str, end_date: str, ev_threshold: float = 0.05):
        """
        Simulates running the ev_picks function for a given date range, evaluates the results, and stores the picks and records in DynamoDB.
        Filters picks based on the provided EV threshold.
        """
        dates = self.generate_date_range(start_date, end_date)
        total_units = 0
        total_correct = 0
        total_picks = 0
        bankrolls = []
        
        created_records = []
        

        for date in dates:
            # Set the date for the simulation
            eastern = dateutil.tz.gettz('US/Eastern')
            self.str_date = datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=eastern).strftime('%Y-%m-%d')
            self.yesterday = (datetime.strptime(date, '%Y-%m-%d') - timedelta(1)).strftime('%Y-%m-%d')

            # Fetch data for the date
            odds = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.str_date, 'odds')
            predictions = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.str_date, 'predictions')
            results = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.str_date, 'results')

            # Generate picks using ev_picks
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
                        'actual': actual_home
                    })
                elif ev_away > ev_threshold:
                    picks.append({
                        'type-gameId': f'picks::ev::{game_id}',
                        'pick': pred['awayteam'],
                        'actual': actual_away
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
            bankrolls.append(bankroll)

            # Calculate Kelly Fraction and Bet Size
            for pick in picks:
                b = float(pick['actual']) - 1  # Net payout
                p = confidence  # Probability of winning
                q = 1 - p  # Probability of losing
                kelly_fraction = (b * p - q) / b

                # Apply 50% Kelly Criterion
                if kelly_fraction > 0:
                    bet_size = bankroll * kelly_fraction * 0.50  # Increased from 25% to 50%
                    pick['kelly_fraction'] = kelly_fraction
                    pick['bet_size'] = round(bet_size, 2)

            # Calculate total Kelly bets for the day
            total_kelly_bets = sum(pick['bet_size'] for pick in picks if 'bet_size' in pick)
            daily_cap = bankroll * 0.10  # 5% of the bankroll

            # Scale down bets if total exceeds daily cap
            if total_kelly_bets > daily_cap:
                scaling_factor = daily_cap / total_kelly_bets
                for pick in picks:
                    if 'bet_size' in pick:
                        pick['bet_size'] = round(pick['bet_size'] * scaling_factor, 2)

            # Check for negative bankroll
            if bankroll <= 0:
                print(f"Bankroll depleted on {self.str_date}. Ending simulation.")
                break

            # Update bankroll based on results
            for pick in picks:
                if 'bet_size' in pick:
                    result = [x for x in results if x['type-gameId'].split('::')[-1] == pick['type-gameId'].split('::')[-1]]
                    if result:
                        result = result[0]
                        actual_winner = get_winner(result)
                        predicted_winner = pick['pick']
                        if predicted_winner == result['hometeam']:
                            predicted_winner = 'home'
                        else:
                            predicted_winner = 'away'

                        if predicted_winner == actual_winner:
                            bankroll += pick['bet_size'] * (float(pick['actual']) - 1)
                        else:
                            bankroll -= pick['bet_size']

            # Evaluate picks
            units, correct = self.evaluate_picks(picks, results)
            total_units += units
            total_correct += correct
            total_picks += len(picks)

            # Store picks in DynamoDB
            for pick in picks:
                record = {
                    'date': self.str_date,
                    'type-gameId': pick['type-gameId'],
                    'pick': pick['pick'],
                    'actual': str(pick['actual']),
                    'bet_size': str(pick['bet_size']) if 'bet_size' in pick else '0.0'
                }
                self.dynamoDbService.create_item(record)
                created_records.append([record['type-gameId'], record['date']])

            # Store daily record in DynamoDB
            yesterday_record = self.dynamoDbService.get_items_by_date_and_exact_sort_key(self.yesterday, 'record::ev')
            yesterday_record = yesterday_record[0] if yesterday_record else {}

            all_time = yesterday_record.get('allTime', {
                "correct": 0,
                "total": 0,
                "percentage": "0.0",
                "units": "0.0"
            })

            # Update all-time record with bankroll as a string
            updated_all_time = {
                "correct": all_time["correct"] + correct,
                "total": all_time["total"] + len(picks),
                "percentage": str(round((all_time["correct"] + correct) / (all_time["total"] + len(picks)), 4) if (all_time["total"] + len(picks)) > 0 else 0.0),
                "units": str(float(all_time["units"]) + units),
                "bankroll": str(round(bankroll, 2))
            }

            daily_record = {
                'date': self.str_date,
                'type-gameId': 'record::ev',
                'today': {
                    'correct': correct,
                    'total': len(picks),
                    'percentage': str(round(correct / len(picks), 4) if len(picks) > 0 else 0.0),
                    'units': str(units)
                },
                'allTime': updated_all_time
            }
            self.dynamoDbService.create_item(daily_record)
            created_records.append([daily_record['type-gameId'], daily_record['date']])

        # Print summary
        print(f"Total Units: {total_units}")
        print(f"Total Correct: {total_correct}")
        print(f"Total Picks: {total_picks}")
        print(f"Accuracy: {round(total_correct / total_picks, 4) if total_picks > 0 else 0.0}")
        print(f"Final Bankroll: {round(bankroll, 2)}")
        print(f"Bankrolls over time: {bankrolls}")
        print(f"Max Bankroll: {round(max(bankrolls), 2)}")
        print(f"Min Bankroll: {round(min(bankrolls), 2)}")
        
        # Cleanup: Delete all created records
        print("Cleaning up created records...")
        for record in created_records:
            self.dynamoDbService.delete_item(record[1], record[0])
        print("Cleanup complete.")
        return

    def evaluate_picks(self, picks, results):
        """
        Evaluates the picks against the results and calculates units won/lost and correct picks.
        """
        results_game_ids = [x['type-gameId'].split('::')[-1] for x in results]
        picks_game_ids = [x['type-gameId'].split('::')[-1] for x in picks]
        units = 0
        correct = 0

        results_with_picks = [x for x in results_game_ids if x in picks_game_ids]

        for i in results_with_picks:
            pick = [x for x in picks if x['type-gameId'].split('::')[-1] == i][0]
            result = [x for x in results if x['type-gameId'].split('::')[-1] == i][0]
            actual_winner = get_winner(result)
            predicted_winner = pick['pick']

            if predicted_winner == 'Los Angeles Clippers':
                predicted_winner = 'LA Clippers'
            predicted_winner = 'home' if predicted_winner == result['hometeam'] else 'away'

            if predicted_winner == actual_winner:
                correct += 1
                units += float(pick['actual'])
        units -= len(results_with_picks)
        return round(units, 3), correct

    def evaluate_and_update_ev_record(self, results):
        """
        Evaluates EV picks for a given date, updates the record in DynamoDB, and maintains a running total of the bankroll.
        """
        # Fetch picks for the date
        picks = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.yesterday, 'picks::ev')

        # Initialize all_time if not already set
        yesterday_record = self.dynamoDbService.get_items_by_date_and_exact_sort_key(self.yesterday, 'record::ev')
        yesterday_record = yesterday_record[0] if yesterday_record else {}

        all_time = yesterday_record.get('allTime', {
            "correct": 0,
            "total": 0,
            "percentage": "0.0",
            "units": "0.0",
            "bankroll": "100.0"  # Default starting bankroll
        })

        # Evaluate picks
        units, correct = self.evaluate_picks(picks, results)

        # Calculate bankroll
        bankroll = float(all_time.get("bankroll", "100.0"))
        for pick in picks:
            result = [x for x in results if x['type-gameId'].split('::')[-1] == pick['type-gameId'].split('::')[-1]]
            if result:
                result = result[0]
                actual_winner = get_winner(result)
                predicted_winner = pick['pick']

                if predicted_winner == result['hometeam']:
                    predicted_winner = 'home'
                else:
                    predicted_winner = 'away'

                if predicted_winner == actual_winner:
                    bankroll += float(pick['bet_size']) * (float(pick['actual']) - 1)
                else:
                    bankroll -= float(pick['bet_size'])

        # Calculate bankroll change from the previous day
        previous_bankroll = float(all_time.get("bankroll", "100.0"))
        bankroll_change = bankroll - previous_bankroll

        # Update all-time record
        updated_all_time = {
            "correct": all_time["correct"] + correct,
            "total": all_time["total"] + len(picks),
            "percentage": str(round((all_time["correct"] + correct) / (all_time["total"] + len(picks)), 4) if (all_time["total"] + len(picks)) > 0 else 0.0),
            "units": str(float(all_time["units"]) + units),
            "bankroll": str(round(bankroll, 2))
        }

        # Create daily record
        daily_record = {
            'date': self.str_date,
            'type-gameId': 'record::ev',
            'today': {
                'correct': correct,
                'total': len(picks),
                'percentage': str(round(correct / len(picks), 4) if len(picks) > 0 else 0.0),
                'units': str(units),
                'bankroll_change': str(round(bankroll_change, 2))
            },
            'allTime': updated_all_time
        }

        # Store the record in DynamoDB
        self.dynamoDbService.create_item(daily_record)
        print(f"EV Record updated for {self.str_date}: {daily_record}")
        return
