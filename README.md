# NBA_Predictor
A python script that attempts to predict the scores of the NBA games for that day.

From the games this ran on in the 2021-22 season, this model predicted the overall winner 70% of the time, 
beat the spread 56% of the time, and beat the totals 55% of the time

This model uses teams shooting percentages, frequencies, as well as the percentages and frequencies they allow on defence to predict the outcome of games.
This model takes the expected pace of the game to determine the number of possesions, and will then simulate each possesion of the game, for 1000 games to get the expected outcome of the match.

The NBA_GameFinder.py file will output all games that are scheduled to be played on the current day
