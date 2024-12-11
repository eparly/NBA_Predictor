import React, { useEffect } from 'react'
import { getData } from '../../../services/apiService'

const NBAPicksPage: React.FC = () => {
    const [picks, setPicks] = React.useState<any[]>([])
    const [loading, setLoading] = React.useState<boolean>(true)
    const [error, setError] = React.useState<string | null>(null)

    const date = new Date().toISOString().split('T')[0]

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
        <div>
            <h1>NBA Picks Page</h1>
            <ul>
                {picks.map((pick) => (
                    <li key={pick.gameId}>
                        <div>{pick.gameId}</div>
                        <div>{pick.homeTeam} vs {pick.awayTeam}</div>
                        <div>{pick.prediction}</div>
                    </li>
                ))}
            </ul>
        </div>
    )
}

// function NBAPicksPage() {
//     return (
//         <div>
//             <h1>NBA Picks Page</h1>
//         </div>
//     );
// }

export default NBAPicksPage;