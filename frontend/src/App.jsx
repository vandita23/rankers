import { HashRouter, Routes, Route } from "react-router-dom";
import { AppProvider } from "./context/AppContext";
import TopBar from "./components/layout/TopBar";
import BottomNav from "./components/layout/BottomNav";
import Dashboard from "./pages/Dashboard";
import AskAI from "./pages/AskAI";
import DiseaseDetection from "./pages/DiseaseDetection";
import Weather from "./pages/Weather";
import Schemes from "./pages/Schemes";
import Profile from "./pages/Profile";

function App() {
  return (
    <AppProvider>
      <HashRouter>
        <div className="min-h-svh bg-soil-50">
          <TopBar />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/ask" element={<AskAI />} />
            <Route path="/disease" element={<DiseaseDetection />} />
            <Route path="/weather" element={<Weather />} />
            <Route path="/schemes" element={<Schemes />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
          <BottomNav />
        </div>
      </HashRouter>
    </AppProvider>
  );
}

export default App;
