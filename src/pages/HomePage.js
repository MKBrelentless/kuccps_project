import React from "react";
import { Link } from "react-router-dom";

function HomePage() {
  return (
    <div>
      <h1>Welcome to KUCCPS Course Recommender</h1>
      <Link to="/recommendation">
        <button>Go to Recommendation Page</button>
      </Link>
    </div>
  );
}

export default HomePage;
