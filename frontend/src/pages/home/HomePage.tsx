import React from 'react';
import './HomePage.css';

function Home() {
  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>Welcome to My Portfolio</h1>
                <p>
                    Hi, I'm Ethan Parliament, a passionate Computer Engineering student specializing in AI and ML. I love sports analytics, specifically hockey and basketball.
                  </p>  
                <p>
                    I've written and presented multiple research papers on hockey analytics through LINHAC - check them out on my projects page!
                  </p>
                  <a href="/hockey" className="cta-button">Hockey Analytics</a>
                <p>
                    I'm also a big fan of the NBA and have created different analytical models used to predict the winner of NBA games. You can check out my picks daily and track my progress on my NBA page! 
                  </p>
                  <a href="nba" className="cta-button">NBA Predictions</a>
        </div>
      </section>
    </div>
  );
}

export default Home;
