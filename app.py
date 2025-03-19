from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend API requests

# Database Connection Function
def connect_db():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ostin",
        database="kuccps_db"
    )

# Train AI Model
def train_model():
    """Trains a KNN model based on course data."""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, cutoff_points FROM courses")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()

    if not courses:
        print("⚠️ No course data found in the database.")
        return None, None

    df = pd.DataFrame(courses)
    X = df[['cutoff_points']].values
    y = df[['id']].values.ravel()

    knn_model = KNeighborsClassifier(n_neighbors=5)
    knn_model.fit(X, y)
    return knn_model, df

# Load the trained model
knn_model, course_df = train_model()

# API Endpoint for Course Recommendation
@app.route("/recommend", methods=["POST"])
def recommend_courses():
    """Recommends courses based on user input cluster points."""
    data = request.json
    cluster_points = data.get("cluster_points")

    if cluster_points is None:
        return jsonify({"error": "Missing cluster_points field"}), 400

    if knn_model is None or course_df is None:
        return jsonify({"error": "AI model is not trained yet"}), 500

    # Get 5 closest course matches
    distances, indices = knn_model.kneighbors([[cluster_points]])

    recommended_courses = []
    for index in indices[0]:
        course = course_df.iloc[index]
        recommended_courses.append({
            "course_name": course["name"],
            "cutoff_points": course["cutoff_points"]
        })

    return jsonify({"recommended_courses": recommended_courses})

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
