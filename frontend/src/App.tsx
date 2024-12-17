import './styles.css';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import Layout from "./components/Layout/Layout"
import Home from './pages/home/HomePage';
import ProjectsPage from './pages/projects/ProjectsPage';
import NBAPages from './pages/nba/NBAPage';
import HockeyAnalyticsPage from './pages/hockey/HockeyAnalyticsPage';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/projects" element={<ProjectsPage />} />
          <Route path="/nba/*" element={<NBAPages />} />
          <Route path="/hockey" element={<HockeyAnalyticsPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
