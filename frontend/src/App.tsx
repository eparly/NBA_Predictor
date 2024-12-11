import './styles.css';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import Home from './pages/home/HomePage';
import ProjectsPage from './pages/projects/ProjectsPage';
import NBAPages from './pages/nba/NBAPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/projects" element={<ProjectsPage />} />
        <Route path="/nba/*" element={<NBAPages />} />
      </Routes>
    </Router>
  );
}

export default App;
