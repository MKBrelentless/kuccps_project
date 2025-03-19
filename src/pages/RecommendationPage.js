import React, { useState, useEffect } from "react";
import axios from "axios";
import styled from "styled-components";

const Recommendation = () => {
  const [clusterPoints, setClusterPoints] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const apiUrl =
    process.env.REACT_APP_API_URL || "http://127.0.0.1:5000/recommend";

  useEffect(() => {
    console.log("API URL:", apiUrl);
  }, [apiUrl]);

  const fetchRecommendations = async () => {
    setError("");
    setLoading(true);
    setRecommendations([]);

    if (!clusterPoints) {
      setError("Please enter cluster points.");
      setLoading(false);
      return;
    }

    try {
      console.log("Sending request to:", apiUrl);
      const response = await axios.post(apiUrl, {
        cluster_points: parseFloat(clusterPoints),
      });

      console.log("API Response:", response.data);

      if (response.data.recommended_courses?.length > 0) {
        setRecommendations(response.data.recommended_courses);
      } else {
        setError("No recommendations found.");
      }
    } catch (error) {
      console.error("Error fetching recommendations:", error);
      setError("Failed to fetch recommendations. Check API connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <BackgroundContainer>
      <Content>
        <Title>AI Course Recommendation</Title>
        <Input
          type="number"
          placeholder="Enter your cluster points"
          value={clusterPoints}
          onChange={(e) => setClusterPoints(e.target.value)}
        />
        <Button onClick={fetchRecommendations} disabled={loading}>
          {loading ? "Fetching..." : "Get Recommendations"}
        </Button>

        {error && <ErrorMessage>{error}</ErrorMessage>}

        {recommendations.length > 0 && (
          <CourseList>
            {recommendations.map((course, index) => (
              <CourseItem key={index}>
                <CourseName>{course.course_name}</CourseName>
                <Cutoff>Cutoff: {course.cutoff_points}</Cutoff>
              </CourseItem>
            ))}
          </CourseList>
        )}
      </Content>
    </BackgroundContainer>
  );
};

export default Recommendation;

// ✅ Styled Components
const BackgroundContainer = styled.div`
  background: url("https://built-environment.uonbi.ac.ke/sites/built-environment.uonbi.ac.ke/files/2022-08/KUCCPs%20image.png")
    no-repeat center center/cover;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  filter: brightness(1.2);
`;

const Content = styled.div`
  background: rgba(255, 255, 255, 0.85);
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
  width: 400px;
`;

const Title = styled.h2`
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
`;

const Input = styled.input`
  padding: 0.75rem;
  font-size: 1rem;
  width: 100%;
  border: 1px solid #bdc3c7;
  border-radius: 5px;
  outline: none;
  margin-bottom: 1rem;
`;

const Button = styled.button`
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;

  &:hover {
    background: #2980b9;
  }

  &:disabled {
    background: #95a5a6;
    cursor: not-allowed;
  }
`;

const ErrorMessage = styled.p`
  color: red;
  margin-top: 1rem;
`;

const CourseList = styled.ul`
  list-style: none;
  padding: 0;
  background: white;
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
`;

const CourseItem = styled.li`
  font-size: 1.2rem;
  padding: 0.5rem;
  border-bottom: 1px solid #bdc3c7;
  display: flex;
  justify-content: space-between;

  &:last-child {
    border-bottom: none;
  }
`;

const CourseName = styled.span`
  font-weight: bold;
`;

const Cutoff = styled.span`
  color: #7f8c8d;
`;
