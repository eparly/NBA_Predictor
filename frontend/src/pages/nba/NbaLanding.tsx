import React, { useEffect } from 'react';
import './NbaLanding.css';
import { getData } from '../../services/apiService';
import WinPercentageChart from '../../components/Chart/WinPercentageChart';
import UnitsChart from '../../components/Chart/UnitsChart';

const NbaLanding: React.FC = () => {
  const [record, setRecord] = React.useState<any>({})
  const [predictionRecordSummary, setPredictionRecordSummary] = React.useState<any>({})
  const [picksRecordSummary, setPicksRecordSummary] = React.useState<any>({})
  const [error, setError] = React.useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getData('/record?type=all')
        setRecord(result)
        setPredictionRecordSummary(result.preds[0])
        setPicksRecordSummary(result.picks[0])
      } catch (error) {
        console.log('Error fetching data: ', error)
        setError('Error fetching data')
      }
    }

    fetchData()
  }, [])
  
  if (error) {
    return <div>Error: {error}</div>
  }
  console.log(record)
  return (
    <div className="nba-landing">
      <h1>NBA Picks and Records</h1>
      <p className="intro">
        Welcome to the NBA Picks section! Here, you'll find my daily picks, recent results, and my overall record for the season.
      </p>
      
      {/* Record Summary Section */}
      {predictionRecordSummary.allTime ? (
        <div className="record-summary">
          <h2>Season Record - Predictions</h2>
          <p>Wins: {predictionRecordSummary.allTime.correct} | Losses: {predictionRecordSummary.allTime.total - predictionRecordSummary.allTime.correct}</p>
          <p>Winning Percentage: {(predictionRecordSummary.allTime.percentage * 100).toFixed(1)}%</p>
          <p>Units: {(predictionRecordSummary.allTime.units).toFixed(2)}</p>
          <h2>Season Record - Picks</h2>
          <p>Wins: {picksRecordSummary.allTime.correct} | Losses: {picksRecordSummary.allTime.total - picksRecordSummary.allTime.correct}</p>
          <p>Winning Percentage: {(picksRecordSummary.allTime.percentage * 100).toFixed(1)}%</p>
          <p>Units: {(picksRecordSummary.allTime.units).toFixed(2)}</p>
          <WinPercentageChart data={record} />
          <UnitsChart data={record} />
        </div>
        ): <p>Loading...</p>}
      

      {/* Navigation Links */}
      <div className="links">
        <a href="/nba/predictions">Daily Predictions</a>
        <a href="/nba/picks">Daily Picks</a>
        <a href="/nba/results">Results</a>
        <a href="/nba/record">Record</a>
      </div>

      {/* Disclaimer */}
      <p className="disclaimer">
        Disclaimer: This information is provided for entertainment purposes only. I am not responsible for any picks you may make. Please play responsibly.
      </p>
    </div>
  );
};

export default NbaLanding;
