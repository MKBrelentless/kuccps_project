import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { HomePage, RecommendationPage } from "./pages";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        {/* <Route path="/courses" element={<CourseList />} /> */}
        <Route path="/recommendations" element={<RecommendationPage />} />
      </Routes>
    </Router>
  );
}

export default App;
