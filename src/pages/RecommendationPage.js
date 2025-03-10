import React, { useState, useEffect } from "react";
import axios from "axios";

const Recommendation = () => {
  const [clusterPoints, setClusterPoints] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState("");

  // API URL from environment variables
  const apiUrl = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000/recommend";

  useEffect(() => {
    console.log("API URL:", apiUrl);
  }, []);

  const fetchRecommendations = async () => {
    setError(""); // Reset error message

    if (!clusterPoints) {
      setError("Please enter cluster points.");
      return;
    }

    try {
      console.log("Sending request to:", apiUrl);
      const response = await axios.post(apiUrl, { cluster_points: parseFloat(clusterPoints) });

      console.log("API Response:", response.data);

      if (response.data.recommended_courses) {
        setRecommendations(response.data.recommended_courses);
      } else {
        setRecommendations([]);
        setError("No recommendations found.");
      }
    } catch (error) {
      console.error("Error fetching recommendations:", error);
      setError("Failed to fetch recommendations. Check API connection.");
    }
  };

  return (
    <div>
      <h2>Course Recommendation</h2>
      <input
        type="number"
        placeholder="Enter your cluster points"
        value={clusterPoints}
        onChange={(e) => setClusterPoints(e.target.value)}
      />
      <button onClick={fetchRecommendations}>Get Recommendations</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {recommendations.map((course, index) => (
          <li key={index}>
            {course.course_name} (Cutoff: {course.cutoff_points})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Recommendation;
