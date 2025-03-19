from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/recommend', methods=['POST'])
def recommend_courses():
    try:
        data = request.get_json()
        cluster_points = data.get("cluster_points")

        # Mockup recommended courses (Replace with real DB query)
        recommended_courses = [
            {"course_name": "Computer Science", "cutoff_points": 32},
            {"course_name": "Mechanical Engineering", "cutoff_points": 29},
            {"course_name": "Medicine", "cutoff_points": 35}
        ]

        # Filter courses based on cutoff points
        filtered_courses = [course for course in recommended_courses if cluster_points >= course["cutoff_points"]]

        return jsonify({"recommended_courses": filtered_courses})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
