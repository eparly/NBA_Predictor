import { Route, Routes } from "react-router-dom";
import NBAPredictionsPage from "./predictions/NbaPredictionsPage";
import NbaLanding from "./NbaLanding";
import PicksPage from "./picks/NBAPicksPage";


function NBAPages() {
    return (
        <Routes>
            <Route path="/" element={<NbaLanding />} />
            <Route path="/predictions" element={<NBAPredictionsPage />} />
            <Route path="/picks" element={<PicksPage />} />
        </Routes>
    );
}

export default NBAPages;