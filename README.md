# NBA_Predictor
A python script that attempts to predict the scores of the NBA games for that day.

From the games this ran on in the 2021-22 season, this model predicted the overall winner 70% of the time, 
beat the spread 56% of the time, and beat the totals 55% of the time

This model(basketball5.0) uses teams shooting percentages, frequencies, as well as the percentages and frequencies they allow on defence to predict the outcome of games.
This model takes the expected pace of the game to determine the number of possesions, and will then simulate each possesion of the game, for 1000 games to get the expected outcome of the match.

The Basketball4.0 file is an older version of the model used at the end of the 2020-21 season and the start of the 2021-22 season. It uses a similar, but less in depth method as the basketball5.0 model. This has an overall record of 64% and beat the spread 60% of the time

The NBA_GameFinder file will output all games that are scheduled to be played on the current day
