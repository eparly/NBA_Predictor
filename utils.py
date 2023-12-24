def teamName(teamname, teams):

    teams = teams.get_teams()
    ID = [x for x in teams if x['full_name'] == teamname][0]
    ID = ID['abbreviation']
    return ID


def get_winner(game_data):
    if game_data[3] >= game_data[4]:
        return 'home'
    else:
        return 'away'
