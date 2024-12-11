import { Route, Routes } from "react-router-dom";
import NBAPicksPage from "./picks/NBAPicksPage";
import NBARecordPage from "./record/NBARecordPage";
import NBAResultsPage from "./results/NBAResults";
import NbaLanding from "./NbaLanding"


function NBAPages() {
    return (
        <Routes>
            <Route path="/" element={<NbaLanding />} />
            <Route path="/picks" element={<NBAPicksPage />} />
            <Route path="/results" element={<NBAResultsPage />} />
            <Route path="/record" element={<NBARecordPage />} />
        </Routes>
    );
}

export default NBAPages;