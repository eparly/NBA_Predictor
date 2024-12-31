# NBA_Predictor

This is my newest version of the NBA Predictor, now equipped with a robust prediction model and many new features!

## Features

- Single, sophisticated prediction model
- Tracking model performance
- Daily predictions for winners and spreads
- AWS infrastructure for automated execution and scalability
- Website to display picks [www.ethanparliament.com/nba](https://www.ethanparliament.com/nba)

## Project Overview

1. **Data Collection**: 
   - Data is collected from various sports APIs to gather historical data on NBA games, teams, and odds.

2. **Prediction Model**: 
   - A prediction model uses historical data to predict the outcomes of NBA games, including winners, spreads and totals.
   - The model is continuously updated with the newest data to improve its accuracy over time.

3. **Automated Execution**: 
   - The prediction model is deployed on AWS infrastructure, leveraging services such as AWS Lambda, AWS S3, and AWS DynamoDB.
   - AWS Lambda functions are used to automate the execution of the prediction model on a daily basis.
   - Predictions are stored in AWS DynamoDB for tracking and analysis.

4. **Tracking Metrics**:
    - Different metrics are tracked to determine how successful the model is. This includes the accuracy of the predictions, as well as tracking how many units would be won based on odds from various sportsbooks.
