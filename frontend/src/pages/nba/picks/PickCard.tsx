import React from 'react';
import teamColours from '../../../utils/teamColours';
import './PickCard.css';

interface PickData {
    date: string;
    gameId: number;
    hometeam: string;
    awayTeam: string;
    actualOdds: number;
    impliedOdds: number;
    edge: number;
    pick: string;
}

interface PickCardProps {
    pickData: PickData;
}

const PickCard: React.FC<PickCardProps> = ({ pickData }) => {
    const { hometeam, awayTeam, actualOdds, pick } = pickData;

    const homeColour = teamColours[hometeam] || '#ccc';
    const awayColour = teamColours[awayTeam] || '#ccc';

    return (
        <div className="pick-card">
            <div className="team-section">
                <div className="team" style={{ backgroundColor: homeColour }}>
                    <span>{hometeam}</span>
                </div>
                <div className='vs'>vs</div>
                <div className="team" style={{ backgroundColor: awayColour }}>
                    <span>{awayTeam}</span>
                </div>
            </div>
            <div className="pick-details">
                <p>
                    <strong>Pick: {pick}</strong>
                </p>
                <p>
                    <strong>Odds: {actualOdds.toFixed(2)}</strong>
                </p>
            </div>
        </div>
    );
};

export default PickCard;
