import os
import zipfile
import mysql.connector
from pdfminer.high_level import extract_text

# Database Connection
def connect_db():
    """Establishes a connection to the MySQL database."""
    conn = mysql.connector.connect(
        host="localhost",  # Change to your MySQL server
        user="root",  # Replace with your DB username
        password="ostin",  # Replace with your DB password
        database="kuccps_db"  # Ensure the database exists
    )
    return conn

# Ensure Database Tables Exist
def setup_database():
    """Creates the required tables if they do not exist."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Create table for PDFs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pdf_entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            content LONGTEXT NOT NULL
        )
    """)
    
    # Create table for course requirements
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_requirements (
            id INT AUTO_INCREMENT PRIMARY KEY,
            course_name VARCHAR(255) NOT NULL,
            subject_requirements TEXT NOT NULL
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database setup completed.")

# Ensure ZIP Extraction
def extract_zip_if_needed(zip_path, extract_to):
    """Extracts ZIP file if it's not already extracted."""
    if os.path.isfile(zip_path):
        print(f"📂 ZIP file found: {zip_path}. Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✅ Extraction complete. PDFs saved in: {extract_to}")
    else:
        print(f"❌ No ZIP file found at: {zip_path}")

# Process PDFs and Insert Data
def process_pdfs_and_insert_data(pdf_folder):
    """Reads PDFs from a folder and inserts extracted text into the database."""
    if not os.path.isdir(pdf_folder):
        print(f"❌ Error: PDF folder not found: {pdf_folder}")
        return

    conn = connect_db()
    cursor = conn.cursor()

    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"📖 Processing {filename}...")

            try:
                text = extract_text(pdf_path)  # Extract text from PDF
                cursor.execute("INSERT INTO pdf_entries (filename, content) VALUES (%s, %s)", (filename, text))
                conn.commit()
                print(f"✅ {filename} inserted into database.")
            except Exception as e:
                print(f"⚠️ Error processing {filename}: {e}")

    cursor.close()
    conn.close()
    print("✅ All PDFs processed successfully.")

# Define Paths
base_dir = r"C:\\Users\\austi\\Desktop\\PROJECT"
zip_path = os.path.join(base_dir, "Desktop.zip")
pdf_folder = os.path.join(base_dir, "pdfs")

# Set up the database
setup_database()

# Extract ZIP if necessary
extract_zip_if_needed(zip_path, pdf_folder)

# Process PDFs
process_pdfs_and_insert_data(pdf_folder)
