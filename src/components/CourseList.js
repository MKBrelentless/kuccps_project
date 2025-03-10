import React from "react";

export const courses = [
  { id: '1', name: 'Soen' },
  { id: 'q1', name: 'Computer' },
  { id: '1w', name: 'Science' },
  { id: '1r', name: 'Math' },
]

const CourseList = () => {
  return (
    <div className="p-10">
      <h2 className="text-2xl font-bold">Available Courses</h2>
      <p className="mt-4">List of KUCCPS courses will appear here.</p>
      {courses.map((course) => (
       <p key={course.id}>{course.name}</p> ))}
    </div>
  );
};

export default CourseList;
