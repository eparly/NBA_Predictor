import { useEffect, useState } from "react"
import { getData } from "../../../services/apiService"
import PickCard from "./PickCard"
import './PicksPage.css'

const PicksPage: React.FC = () => {
    const [picks, setPicks] = useState<any[]>([])
    const [error, setError] = useState<string | null>(null)

    const date = new Date(new Date().toLocaleDateString('en-US', {
        timeZone: 'America/New_York',
    })).toISOString().split('T')[0]
    // const date = '2024-12-07'


    useEffect(() => {
        const fetchData = async () => {
            try {
                const result = await getData(`/picks/value/${date}`)
                if (result.length === 0) {
                    throw new Error('No picks available for today')
                }
                setPicks(result)
            } catch (error: any) {
                // console.log('Error fetching data: ', error)
                setError(error.message || "An unexpected error occurred")
            }
        }
        fetchData()
    }, [])

    if (error) {
        return (
            <div className="error-card">
                <h2>No Picks Available</h2>
                <p>There are currently no picks for today. Picks are generated around 9:00 AM each day. Due to the way picks are generated, there may not be any picks for the NBA games today</p>
            </div>
        )
    }
    if (!picks) {
        return <div>Loading...</div>
    }
    return (
        <div className="picks-page">
            <h1>NBA Picks</h1>
            <p>
                Picks are generated daily around 9:00 AM, and are based on the predictions made,
                and the odds from sportsbooks
                These picks may not match up with the predictions exactly,
                but are designed to maximize the value of each pick.
            </p>
            <div className="picks-grid">
                {picks.map((pick) => (
                    console.log(pick),
                    <PickCard key={pick.gameId} pickData={pick} />
                ))}
            </div>
        </div>
    )
}

export default PicksPage