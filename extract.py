import fitz  # PyMuPDF
import zipfile
import os
import re
import json
import statistics  # For calculating the mean
import mysql.connector  # MySQL connection

# **Step 1: Extract ZIP file**
zip_path = r"C:\Users\austi\Desktop\PROJECT\Desktop.zip"
extract_path = r"C:\Users\austi\Desktop\app\kuccps_pdfs"

if not os.path.exists(extract_path):
    os.makedirs(extract_path)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print(f"✅ Extracted PDFs to: {extract_path}")

# **Step 2: Extract Text from PDFs**
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

# **Step 3: Database Setup**
def setup_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ostin",
        database="kuccps_db"
    )
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS universities (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) UNIQUE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        university_id INT,
        name VARCHAR(255),
        cutoff_points FLOAT,
        FOREIGN KEY (university_id) REFERENCES universities (id),
        UNIQUE(university_id, name)
    )
    """)
    
    conn.commit()
    return conn, cursor

# **Step 4: Process Each PDF and Insert Data**
def process_pdfs_and_insert_data(extract_path, conn, cursor):
    course_cutoff_data = []  # List to store extracted course details
    
    for filename in os.listdir(extract_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(extract_path, filename)
            print(f"📄 Processing: {filename}")
            
            text = extract_text_from_pdf(pdf_path)
            lines = text.split("\n")
            
            current_university = None
            current_course = None
            cutoff_values = []

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Detect university names
                university_match = re.search(r"(\b[A-Z\s]+UNIVERSITY\b|\bCOLLEGE OF [A-Z\s]+\b)", line)
                if university_match:
                    current_university = university_match.group(1).strip()
                    print(f"✅ Detected University: {current_university}")
                    
                    # Insert university into database if it doesn't exist
                    try:
                        cursor.execute("INSERT IGNORE INTO universities (name) VALUES (%s)", (current_university,))
                        conn.commit()
                    except Exception as e:
                        print(f"⚠️ Error inserting university: {e}")

                # Detect course names
                course_match = re.match(r"^(DIPLOMA|BACHELOR|CERTIFICATE|MASTER'S|PHD)\s+.+", line, re.IGNORECASE)
                if course_match:
                    # Save previous course if valid
                    if current_university and current_course and cutoff_values:
                        mean_cutoff = statistics.mean(cutoff_values)
                        course_cutoff_data.append({
                            "university": current_university,
                            "course": current_course,
                            "cutoff_points": mean_cutoff
                        })
                        
                        try:
                            cursor.execute("SELECT id FROM universities WHERE name = %s", (current_university,))
                            result = cursor.fetchone()
                            if result:
                                university_id = result[0]
                                cursor.execute("""
                                INSERT INTO courses (university_id, name, cutoff_points) 
                                VALUES (%s, %s, %s)
                                ON DUPLICATE KEY UPDATE cutoff_points = %s
                                """, (university_id, current_course, mean_cutoff, mean_cutoff))
                                conn.commit()
                        except Exception as e:
                            print(f"⚠️ Error inserting course {current_course}: {e}")
                    
                    current_course = line
                    cutoff_values = []
                    print(f"✅ Detected Course: {current_course}")

                # Detect cutoff points
                cutoff_match = re.search(r"(\b\d{1,2}\.\d{1,2}\b)", line)
                if cutoff_match:
                    cutoff_value = float(cutoff_match.group(1))
                    cutoff_values.append(cutoff_value)
                    print(f"✅ Detected Cutoff Value: {cutoff_value}")

            # Save the last course
            if current_university and current_course and cutoff_values:
                mean_cutoff = statistics.mean(cutoff_values)
                course_cutoff_data.append({
                    "university": current_university,
                    "course": current_course,
                    "cutoff_points": mean_cutoff
                })
                
                try:
                    cursor.execute("SELECT id FROM universities WHERE name = %s", (current_university,))
                    result = cursor.fetchone()
                    if result:
                        university_id = result[0]
                        cursor.execute("""
                        INSERT INTO courses (university_id, name, cutoff_points) 
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE cutoff_points = %s
                        """, (university_id, current_course, mean_cutoff, mean_cutoff))
                        conn.commit()
                except Exception as e:
                    print(f"⚠️ Error inserting last course {current_course}: {e}")
    
    return course_cutoff_data

# **Step 5: Main Execution**
def main():
    conn, cursor = setup_database()
    try:
        course_cutoff_data = process_pdfs_and_insert_data(extract_path, conn, cursor)
        
        output_file = os.path.join(os.getcwd(), "course_cutoff_data.json")
        with open(output_file, "w") as f:
            json.dump(course_cutoff_data, f, indent=4)
        print(f"\n✅ Course cutoff data saved to: {output_file}")
        
        cursor.execute("SELECT COUNT(*) FROM universities")
        print(f"📊 Universities Count: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM courses")
        print(f"📊 Courses Count: {cursor.fetchone()[0]}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()
        print("\n✅ Database connection closed")

if __name__ == "__main__":
    main()
