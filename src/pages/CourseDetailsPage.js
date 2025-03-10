import React from "react";
import { useParams } from "react-router-dom";

const CourseDetails = () => {
  const { id } = useParams();

  return (
    <div className="p-10">
      <h2 className="text-2xl font-bold">Course Details</h2>
      <p className="mt-4">Details for course ID: {id}</p>
    </div>
  );
};

export default CourseDetails;
