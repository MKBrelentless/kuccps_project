import mysql.connector
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

def connect_db():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ostin",
        database="kuccps_db"
    )

def get_course_data():
    """Fetches course data from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, cutoff_points FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return pd.DataFrame(courses, columns=["id", "name", "cutoff_points"])

def train_model():
    """Trains a KNN model based on course cutoff points."""
    df = get_course_data()
    if df.empty:
        print("❌ No data available in the courses table.")
        return None, None
    
    X = df[['cutoff_points']].values  # Corrected column name
    y = df['id'].values
    
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)
    print("✅ KNN Model trained successfully.")
    return knn, df

def recommend_course(knn_model, df, student_score):
    """Recommends a course based on student's cluster points."""
    if knn_model is None:
        return "❌ Model is not trained."
    
    predicted_course_id = knn_model.predict([[student_score]])[0]
    course = df[df['id'] == predicted_course_id]
    
    if not course.empty:
        return course.iloc[0]['name']
    return "❌ No matching course found."

# Train the model
knn_model, course_df = train_model()

# Example: Predict a course for a student with 48 cluster points
if knn_model:
    student_score = 48
    recommendation = recommend_course(knn_model, course_df, student_score)
    print(f"🎓 Recommended Course: {recommendation}")
