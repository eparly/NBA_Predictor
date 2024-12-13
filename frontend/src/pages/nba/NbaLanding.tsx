import React, { useEffect } from 'react';
import './NbaLanding.css';
import { getData } from '../../services/apiService';

const NbaLanding: React.FC = () => {
  const [recordSummary, setRecordSummary] = React.useState<any>({})
  const [error, setError] = React.useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getData('/record')
        setRecordSummary(result[0])
        console.log('recordSummary: ', recordSummary)
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

  return (
    <div className="nba-landing">
      <h1>NBA Picks and Records</h1>
      <p className="intro">
        Welcome to the NBA Picks section! Here, you'll find my daily picks, recent results, and my overall record for the season.
      </p>
      
      {/* Record Summary Section */}
      {recordSummary.allTime ? (
        <div className="record-summary">
          <h2>Season Record</h2>
          <p>Wins: {recordSummary.allTime.correct} | Losses: {recordSummary.allTime.total - recordSummary.allTime.correct}</p>
          <p>Winning Percentage: {(recordSummary.allTime.percentage * 100).toFixed(1)}%</p>
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
