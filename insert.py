import fitz  # PyMuPDF
import zipfile
import os
import re
import json
import statistics  # For calculating the mean

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

# **Step 3: Process Each PDF**
course_cutoff_data = []  # List to store extracted course details

for filename in os.listdir(extract_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(extract_path, filename)
        print(f"📄 Processing: {filename}")
        
        text = extract_text_from_pdf(pdf_path)
        lines = text.split("\n")
        
        current_university = None
        current_course = None
        cutoff_values = []  # List to store cutoff values for the current course

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Debug: Print the current line
            print(f"Processing Line: {line}")

            # Detect university names
            university_match = re.search(r"(\b[A-Z\s]+UNIVERSITY\b|\bCOLLEGE OF [A-Z\s]+\b)", line)
            if university_match:
                current_university = university_match.group(1).strip()
                print(f"✅ Detected University: {current_university}")  # Debugging

            # Detect course names (broadened regex pattern)
            course_match = re.match(r"^(DIPLOMA|BACHELOR|CERTIFICATE)\s+(IN|OF)\s+.+", line, re.IGNORECASE)
            if course_match:
                # Save the previous course and its mean cutoff (if any)
                if current_university and current_course and cutoff_values:
                    mean_cutoff = statistics.mean(cutoff_values)  # Calculate mean cutoff
                    course_cutoff_data.append({
                        "university": current_university,
                        "course": current_course,
                        "cutoff_points": mean_cutoff
                    })
                    print(f"✅ Saved Course: {current_course} with Mean Cutoff: {mean_cutoff} for University: {current_university}")  # Debugging
                
                # Reset for the next course
                current_course = line
                cutoff_values = []  # Reset cutoff values for the next course
                print(f"✅ Detected Course: {current_course}")  # Debugging

            # Detect cutoff points (improved regex pattern for digits)
            cutoff_match = re.search(r"(\b\d{1,2}\.\d{1,2}\b)", line)
            if cutoff_match:
                cutoff_value = float(cutoff_match.group(1))  # Convert to float
                cutoff_values.append(cutoff_value)  # Add to the list of cutoff values
                print(f"✅ Detected Cutoff Value: {cutoff_value}")  # Debugging

        # Save the last course and its mean cutoff (if any)
        if current_university and current_course and cutoff_values:
            mean_cutoff = statistics.mean(cutoff_values)  # Calculate mean cutoff
            course_cutoff_data.append({
                "university": current_university,
                "course": current_course,
                "cutoff_points": mean_cutoff
            })
            print(f"✅ Saved Course: {current_course} with Mean Cutoff: {mean_cutoff} for University: {current_university}")  # Debugging

# **Step 4: Save Data**
output_file = os.path.join(os.getcwd(), "course_cutoff_data.json")
with open(output_file, "w") as f:
    json.dump(course_cutoff_data, f, indent=4)

print(f"\n✅ Course cutoff data saved to: {output_file}")