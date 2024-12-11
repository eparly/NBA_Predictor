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
  

const NBAPicksPage: React.FC = () => {
    const [picks, setPicks] = React.useState<any[]>([])
    const [loading, setLoading] = React.useState<boolean>(true)
    const [error, setError] = React.useState<string | null>(null)

    // const date = new Date().toISOString().split('T')[0]
    const date = '2024-12-07'

    useEffect(() => {
        const fetchData = async () => {
            try {
                const result = await getData(`/predictions/${date}`)
                setPicks(result)
            }
            catch (error) {
                console.log('Error fetching data: ', error)
                setError('Error fetching data')
            }
        }

        fetchData()
    }, [])

    if (error) {
        return <div>Error: {error}</div>
    }
    if (!picks) {
        return <div>Loading...</div>
    }

    return (
        <div className='nba-landing'>
            <h1>NBA Picks Page</h1>
            <div className="game-cards">
                {picks.map((game: GameData) => (
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
    const { date, homeTeam, awayTeam, predictions, odds } = game;

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
  

// function NBAPicksPage() {
//     return (
//         <div>
//             <h1>NBA Picks Page</h1>
//         </div>
//     );
// }

export default NBAPicksPage;