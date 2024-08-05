def teamName(teamname, teams):

    teams = teams.get_teams()
    ID = [x for x in teams if x['full_name'] == teamname][0]
    ID = ID['abbreviation']
    return ID


def get_winner(game_data):
    if game_data['homescore'] >= game_data['awayscore']:
        return 'home'
    else:
        return 'away'
