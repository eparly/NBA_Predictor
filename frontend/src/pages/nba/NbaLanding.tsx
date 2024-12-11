import React, { useEffect } from 'react';
import './NbaLanding.css';
import teamColours from '../../utils/teamColours';
import { getData } from '../../services/apiService';
import { GameCard, GameData } from './picks/NBAPicksPage';

const NbaLanding: React.FC = () => {
  const [picks, setPicks] = React.useState<any[]>([])
  const [recordSummary, setRecordSummary] = React.useState<any>({})
  const [loading, setLoading] = React.useState<boolean>(true)
  const [error, setError] = React.useState<string | null>(null)

  // const date = new Date().toISOString().split('T')[0]
  const date = '2024-12-07'
  
  useEffect(() => {
      console.log('here')
      const fetchData = async () => {
          try {
            const result = await getData(`/predictions/${date}`)
            setPicks(result)
            console.log('picks: ', picks)
          }
          catch (error) {
            console.log('Error fetching data: ', error)
            setError('Error fetching data')
          }
      }

      fetchData()
  }, [])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getData('/record')
        setRecordSummary(result)
      } catch (error) {
        console.log('Error fetching data: ', error)
        setError('Error fetching data')
      }
    }

    fetchData()
  }, [])

  const featuredPick: GameData = picks[0]

  
  if (error) {
    return <div>Error: {error}</div>
  }
  if (!picks) {
    return <div>Loading...</div>
  }

  return (
    <div className="nba-landing">
      <h1>NBA Picks and Records</h1>
      <p className="intro">
        Welcome to the NBA Picks section! Here, you'll find my daily picks, recent results, and my overall record for the season.
      </p>
      
      {/* Featured Pick Section */}
      {picks.length > 0 && featuredPick ? (
        <div className="featured-pick">
          <h2>Featured Pick</h2>
          <div className="featured-pick-card">
            <GameCard key={featuredPick.gameId} game={featuredPick} />
          </div>
        </div>
      ) : <p>Loading...</p>}
      
      {/* Record Summary Section */}
      <div className="record-summary">
        <h2>Season Record</h2>
        <p>Wins: {recordSummary.wins} | Losses: {recordSummary.losses}</p>
      </div>

      {/* Navigation Links */}
      <div className="links">
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
