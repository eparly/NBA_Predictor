from Predictor_db.NBA_Predictor.db_management import get_predictions, insert_spread_picks


def spread_picks(table):
    spreads = get_predictions(table, 'all')

    odds = get_predictions('odds', 'all')

    odds_dict = {odd[0]: odd for odd in odds}
    combined = []
    picks = []
    for spread in spreads:
        if spread[0] in odds_dict:
            combined_tuple = spread[:3] + \
                spread[4:5] + (odds_dict[spread[0]][1:2])

            combined.append(combined_tuple)

            if abs(combined_tuple[3]) >= abs(combined_tuple[4]):
                if combined_tuple[3] > 0 and combined_tuple[4] > 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[2], -1*combined_tuple[4]))
                if combined_tuple[3] < 0 and combined_tuple[4] < 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[1], combined_tuple[4]))

                if combined_tuple[3] > 0 and combined_tuple[4] < 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[2], -1*combined_tuple[4]))
                if combined_tuple[3] < 0 and combined_tuple[4] > 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[1], combined_tuple[4]))
            else:
                if combined_tuple[3] > 0 and combined_tuple[4] > 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[1], combined_tuple[4]))
                if combined_tuple[3] < 0 and combined_tuple[4] < 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[2], -1*combined_tuple[4]))

                if combined_tuple[3] > 0 and combined_tuple[4] < 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[2], -1*combined_tuple[4]))
                if combined_tuple[3] < 0 and combined_tuple[4] > 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[1], combined_tuple[4]))

    if table == 'spreads':
        insert_table = 'spread_picks'
    if table == 'homefactor_spreads':
        insert_table = 'home_spread_picks'
    for i in range(len(picks)):
        insert_spread_picks(picks[i], insert_table)
    a = 0
