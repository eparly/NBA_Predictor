import React from 'react';
import './NbaLanding.css';

const NbaLanding: React.FC = () => {
  // Mock data for featured pick and record summary
  const featuredPick = {
    game: "Lakers vs. Warriors",
    pick: "Lakers -4.5",
    confidence: "High"
  };

  const recordSummary = {
    wins: 42,
    losses: 18
  };

  // Placeholder for API call to fetch featured pick data
  // Uncomment and modify when API is available
  // useEffect(() => {
  //   fetch('/api/featuredPick')
  //     .then(response => response.json())
  //     .then(data => setFeaturedPick(data))
  //     .catch(error => console.error("Error fetching featured pick:", error));
  // }, []);

  // Placeholder for API call to fetch record summary data
  // Uncomment and modify when API is available
  // useEffect(() => {
  //   fetch('/api/recordSummary')
  //     .then(response => response.json())
  //     .then(data => setRecordSummary(data))
  //     .catch(error => console.error("Error fetching record summary:", error));
  // }, []);

  return (
    <div className="nba-landing">
      <h1>NBA Picks and Records</h1>
      <p className="intro">
        Welcome to the NBA Picks section! Here, you'll find my daily picks, recent results, and my overall record for the season.
      </p>
      
      {/* Featured Pick Section */}
      <div className="featured-pick">
        <h2>Featured Pick</h2>
        <p><strong>Game:</strong> {featuredPick.game}</p>
        <p><strong>Pick:</strong> {featuredPick.pick}</p>
        <p><strong>Confidence:</strong> {featuredPick.confidence}</p>
      </div>
      
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
