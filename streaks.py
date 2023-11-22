import pandas as pd
import matplotlib.pyplot as plt
from sportsipy.nba.schedule import Game, Schedule
from sportsipy.nba.teams import Teams
import pickle
import seaborn as sns

import time as t

def get_streak(team_name):
    # find the streak from the last game played
    # the last game played will be the last row in the table with a value for streak
    if team_name == 'BKN':
        team_name = 'BRK'
    if team_name == 'PHX':
        team_name = 'PHO'
    if team_name == 'CHA':
        team_name = 'CHO'
    try:
        schedule = Schedule(team_name)
    
        t.sleep(60)
        schedule = schedule.dataframe
        schedule = schedule[schedule['streak'] != '']
        streak = schedule['streak'].iloc[-1]
        return streak
    except:
        return ''



def update_streaks(teams, schedule):
    ROLLING_WINDOW = 10

    team_results = {}

    def average_points_streak(group):
        return group['points_scored'].mean(), len(group)

    for team in teams:
        games = []
        schedule = Schedule(team, '2022').dataframe
        game_info = schedule[['streak', 'date']]
        schedule['streak_length'] = schedule['streak'].str.extract('(\d+)').astype(int)
        schedule['streak_type'] = schedule['streak'].str.extract('([WL])')
        schedule['rolling_avg_points_scored'] = schedule['points_scored'].rolling(window = ROLLING_WINDOW).mean()

        schedule['games_played'] = schedule.groupby(['streak_length', 'streak_type'])[
            'points_scored'].transform('count')

        streak_avg_points = schedule.groupby(['streak_type', 'streak_length']).apply(average_points_streak)
        streak_avg_points = streak_avg_points.reset_index()
        streak_avg_points.columns = ['streak_type', 'streak_length', 'avg_points_scored']

        streak_avg_points['games_played'] = schedule.groupby(
            ['streak_type', 'streak_length'])['games_played'].first().reset_index(drop=True)
        streak_avg_points['teamname'] = team

        team_results[team] = streak_avg_points
        t.sleep(3)
        a=0
        #add results to mysql
        # insert_streaks(streak_avg_points, 'streaks')


    with open('streak_data', 'wb') as file:
        pickle.dump(team_results, file)


def visualize_streak_data(teams_data):
    # """
    # Visualize streak data for all teams with separate plots for winning and losing streaks.
    
    # Args:
    # teams_data (dict): A dictionary containing streak data for all teams. Each team's data is a DataFrame.
    # """

    # # Determine the maximum streak length across all teams and streak types
    # max_streak_length = max(
    #     max(max(team_data['streak_length'])
    #         for team_data in teams_data.values()),
    #     max(max(team_data['streak_length'])
    #         for team_data in teams_data.values()),
    # )

    # # Create subplots for winning and losing streaks
    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # # Set common labels for both subplots
    # fig.text(0.5, 0.02, 'Streak Length', ha='center', fontsize=12)
    # fig.text(0.04, 0.5, 'Average Points Scored',
    #          va='center', rotation='vertical', fontsize=12)

    # # Plot winning streaks
    # for team, team_data in teams_data.items():
    #     winning_data = team_data[team_data['streak_type'] == 'W']
    #     ax1.plot(winning_data['streak_length'], [
    #              x[0] for x in winning_data['avg_points_scored']], label=team, marker='o')

    # ax1.set_title('Winning Streaks')
    # ax1.set_xlim(1, max_streak_length)
    # ax1.legend(loc='upper right', bbox_to_anchor=(1.2, 1))

    # # Plot losing streaks
    # for team, team_data in teams_data.items():
    #     losing_data = team_data[team_data['streak_type'] == 'L']
    #     ax2.plot(losing_data['streak_length'], [
    #              x[0] for x in losing_data['avg_points_scored']], label=team, marker='o')

    # ax2.set_title('Losing Streaks')
    # ax2.set_xlim(1, max_streak_length)
    # ax2.legend(loc='upper right', bbox_to_anchor=(1.2, 1))


    # plt.tight_layout()
    # plt.show()
    all_teams_data = pd.concat(
        teams_data.values(), keys=teams_data.keys(), names=['Team'])

    # Define bin boundaries for average points scored
    bin_edges = [80, 90, 100, 110, 120, all_teams_data['avg_points_scored'].max()]

    # Binning the average points scored into categories
    bin_labels = ['<90', '90-100', '100-110', '110-120', '>=120']
    # Define a function to extract the points scored from the tuples


    def extract_points_scored(avg_points):
        return avg_points[0]

    # Apply the function to create a new column with the extracted points scored
    points_scored = [item[0]
                                       for item in all_teams_data['avg_points_scored'].values]
    bin_edges = [80, 90, 100, 110, 120,
                 max(points_scored)]
    all_teams_data['avg_points_category'] = pd.cut(
        points_scored, bins=bin_edges, labels=bin_labels)

    

    # Create a violin plot with binned average points scored
    sns.violinplot(x='avg_points_category', y='streak_length',
                hue='streak_type', data=all_teams_data)

    plt.xlabel('Average Points Scored Category')
    plt.ylabel('Streak Length')
    plt.title(
        'Violin Plot of Binned Streak Data by Average Points Scored for Multiple Teams')

    plt.show()


def create_point_change_violin_plots(data):
    # Create a DataFrame to hold the point change data
    point_change_data = pd.DataFrame(
        columns=['teamname', 'streak_type', 'point_change', 'game_number', 'streak_length'])

    for teamname, team_data in data.items():
        #find teams total weighted average points scored
        total_points = team_data['avg_points_scored'].apply(lambda x: x[0]*x[1]).sum()
        average_points = total_points/ team_data['games_played'].sum()
        # Iterate through each streak type and streak length
        for streak_type in ['W', 'L']:
            for streak_length in range(2, team_data["streak_length"].max() + 1):
                streak_data_filtered = team_data[(team_data['streak_length'] == streak_length) & (
                    team_data['streak_type'] == streak_type)]

                if len(streak_data_filtered) <= 0:
                    continue  # Skip streaks with only one game


                point_changes = streak_data_filtered['avg_points_scored'].apply(lambda x: x[0])
                relative_point_changes = pd.DataFrame()
                relative_point_changes['point_change'] = point_changes / average_points

                # Add the data to the point_change_data DataFrame
                # Start from the 2nd game (game number 2)
                game_number = streak_data_filtered['games_played']
                relative_point_changes['teamname'] = teamname
                relative_point_changes['streak_type'] = streak_type
                relative_point_changes['game_number'] = game_number
                relative_point_changes['streak_length'] = streak_length
                point_change_data = pd.concat(
                    [point_change_data, relative_point_changes])
                
                


    # Reset the index
    point_change_data = point_change_data.reset_index(drop=True)
    point_changes = point_change_data.groupby(['streak_type', 'streak_length'])[
        'point_change'].mean()
    # Create violin plots for point changes
    # plt.figure(figsize=(12, 6))
    # sns.violinplot(x='streak_length', y='point_change',
    #                hue='streak_type', data=point_change_data)
    # Calculate and annotate the average point change for each streak length and streak type
    # averages = point_change_data.groupby(['streak_length', 'streak_type'])[
    #     'point_change'].mean()
    # for i, label in enumerate(averages.index):
    #     x_position = i % (point_change_data['streak_length'].max() - 1)
    #     y_position = averages[label]
    #     ax.annotate(f'Avg: {y_position:.2f}', (x_position, y_position),
                    # fontsize=10, ha='center', va='bottom', color='black')


    # plt.xlabel('Streak Length')
    # plt.ylabel('Point Change')
    # plt.title(
    #     'Violin Plot of Point Changes in Average Points Scored by Game Number and Streak Length')

    # plt.show()
    with open('streak_point_changes', 'wb') as file:
        pickle.dump(point_changes, file)
    return point_changes

# schedule = Schedule('BOS', '2022')
# teams = Teams('2022')
# teams = teams.dataframes.index
# with open('streak_data', 'rb') as file:
#     team_results = pickle.load(file)
# # Call the function to visualize the data for all teams
# # visualize_streak_data(team_results)
# get_streak('BOS')
# point_changes = create_point_change_violin_plots(team_results)
# print(team_results)