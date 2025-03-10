import React from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";

const courses = [
  { id: 1, name: "Computer Science" },
  { id: 2, name: "Software Engineering" },
  { id: 3, name: "Data Science" },
  { id: 4, name: "Artificial Intelligence" },
  { id: 5, name: "Cybersecurity" },
];

function HomePage() {
  return (
    <Container>
      <Title>Welcome to KUCCPS Course Recommender</Title>
      <CourseList>
        {courses.map((course) => (
          <CourseItem key={course.id}>
            {course.id}. {course.name}
          </CourseItem>
        ))}
      </CourseList>
      <StyledLink to="/recommendations">
        <Button>Go to Recommendation Page</Button>
      </StyledLink>
    </Container>
  );
}

export default HomePage;

const Container = styled.div`
  text-align: center;
  padding: 2rem;
  font-family: "Arial", sans-serif;
`;

const Title = styled.h1`
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
`;

const CourseList = styled.ul`
  list-style: none;
  padding: 0;
  max-width: 400px;
  margin: 0 auto;
  background: #ecf0f1;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
`;

const CourseItem = styled.li`
  font-size: 1.2rem;
  padding: 0.5rem;
  border-bottom: 1px solid #bdc3c7;
  &:last-child {
    border-bottom: none;
  }
`;

const StyledLink = styled(Link)`
  text-decoration: none;
`;

const Button = styled.button`
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  margin-top: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;

  &:hover {
    background: #2980b9;
  }
`;
