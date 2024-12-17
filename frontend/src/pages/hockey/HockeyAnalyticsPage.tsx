import React from 'react';
import './HockeyAnalyticsPage.css';

const HockeyAnalyticsPage: React.FC = () => {
    const [selectedPaper, setSelectedPaper] = React.useState<string | null>(null);

    const papers = [
        {
            title: "The Effect of Shot Location on Rebound Quality",
            description:
                "This paper examines the impact that shot location has on generating rebounds with high-quality scoring chances. Methods to measure rebound quality are discussed, as well as how shooting from different locations on the ice can maximize rebound chances. Presented at LINHAC 2022, this paper won the student competition for hockey analytics.",
            file: '/pdfs/LINHAC22.pdf',
        },
        {
            title: "Defensive Zone Puck Battles and Breakout Success",
            description:
                "This paper explores the locations of defensive zone battles and how winning them impacts a team's ability to break out of their zone. Metrics like breakout success rates, cumulative xG, and time of possession are discussed. Presented at LINHAC 2023, it won the student competition for hockey analytics.",
            file: '/pdfs/LINHAC23.pdf',
        },
        {
            title: "Decision Making in the Neutral Zone and its Impact on Possession Value",
            description:
                "This paper analyzes decisions made by players with the puck in the neutral zone, such as passing or skating, and how these decisions impact possession value. The location of the action significantly influences the value of the possession. Presented at LINHAC 2024.",
            file: '/pdfs/LINHAC24.pdf',
        },
    ];

    return (
        <div className="hockey-analytics-container">
            <h1>Hockey Analytics</h1>
            <p className="intro">
                I've written and presented multiple research papers on hockey analytics through Linköping Hockey Analytics Conference (LINHAC). Check them out below, click to read the paper!
            </p>
            <div className="papers-list">
                {papers.map((paper, index) => (
                    <div
                        key={index}
                        className="paper-card"
                        onClick={() => setSelectedPaper(paper.file)}
                    >
                        <h2>{paper.title}</h2>
                        <p>{paper.description}</p>
                    </div>
                ))}
            </div>
            {selectedPaper && (
                <div className="modal" onClick={() => setSelectedPaper(null)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <button className="close-button" onClick={() => setSelectedPaper(null)}>
                            &times;
                        </button>
                        <iframe src={selectedPaper} title="Research Paper" className="pdf-viewer"></iframe>
                    </div>
                </div>
            )}
        </div>
    );
};

export default HockeyAnalyticsPage;
