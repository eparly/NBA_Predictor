import React, { useEffect } from 'react'
import { getData } from '../../../services/apiService'
import teamColours from '../../../utils/teamColours'
import './../NbaLanding.css'

export interface GameData {
    date: string;
    gameId: number;
    homeTeam: string;
    awayTeam: string;
    predictions: {
      homeScore: number;
      awayScore: number;
      confidence: string;
    };
    odds: {
      homeML: number;
      awayML: number;
      spread: number;
    };
  }
  

const NBAPredictionsPage: React.FC = () => {
    const [predictions, setPredictions] = React.useState<any[]>([])
    const [error, setError] = React.useState<string | null>(null)

    const date = new Date(new Date().toLocaleDateString('en-US', {
        timeZone: 'America/New_York',
    })).toISOString().split('T')[0]
    console.log(date)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const result = await getData(`/predictions/${date}`)
                if (result.length === 0) {
                  throw new Error('No picks available for today')
              }
              setPredictions(result)
          } catch (error: any) {
              // console.log('Error fetching data: ', error)
              setError(error.message || "An unexpected error occurred")
          }
      }
      fetchData()
  }, [date])

  if (error) {
    return (
        <div className="error-card">
            <h2>No Predictions Available</h2>
            <p>There are currently no predictions for today. Predictions are generated around 9:00 AM each day.</p>
        </div>
    )
  }
    if (!predictions) {
        return <div>Loading...</div>
    }

    return (
        <div className='nba-landing'>
            <h1>NBA Predictions Page</h1>
            <div className="game-cards">
                {predictions.map((game: GameData) => (
                    <GameCard key={game.gameId} game={game} />
                ))}
            </div>
        </div>
    )
}

interface GameCardProps {
    game: GameData
}

export const GameCard: React.FC<GameCardProps> = ({ game }) => {
    const { homeTeam, awayTeam, predictions, odds } = game;

    const homeTeamColour = teamColours[homeTeam]
    const awayTeamColour = teamColours[awayTeam]
    return (
      <div className="game-card">
        <div className="teams">
                <span className="team" style={{ color: awayTeamColour }}>{awayTeam}</span> @ <span className="team" style={{color: homeTeamColour}}>{homeTeam}</span>
        </div>
        <div className="predictions">
          <p>
                    <strong>Prediction:</strong>{" "}
                    <span style={{ color: awayTeamColour }}>
                        {awayTeam}
                    </span>{" "}
                    {predictions.awayScore} -{" "}
                    <span style={{ color: homeTeamColour }}>
                        {homeTeam}
                    </span>{" "}
                    {predictions.homeScore}
          </p>
          <p>
            <strong>Confidence:</strong> {(parseFloat(predictions.confidence) * 100).toFixed(1)}%
          </p>
        </div>
        <div className="odds">
          <p>
            <strong>Home ML:</strong> {odds.homeML.toFixed(2)}
          </p>
          <p>
            <strong>Away ML:</strong> {odds.awayML.toFixed(2)}
          </p>
          <p>
            <strong>Spread (Home):</strong> {odds.spread}
          </p>
        </div>
      </div>
    );
  };

export default NBAPredictionsPage;