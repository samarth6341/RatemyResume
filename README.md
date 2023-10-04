# ratemyresume



RateMyResume
RateMyResume is a web application designed to provide AI-generated feedback on resumes. Users can upload their resumes, and optionally provide a job description, to receive tailored feedback and suggestions for improvement.

Features
AI-Powered Feedback: Uses Google's Generative AI to analyze resumes and provide feedback.
PDF Support: Users can upload their resumes in PDF format.
Job Description Analysis: Users can provide a job description to get feedback tailored to a specific job role.
Personal Info Sanitization: The application ensures that personal information like email addresses, phone numbers, and links are sanitized before processing.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/samarth6341/ratemyresume.git
Navigate to the repository directory:

bash
Copy code
cd ratemyresume
Install the required Python libraries:

Copy code
pip install -r requirements.txt
Usage
Run the Streamlit application:

arduino
Copy code
streamlit run appCOPY.py
Open the provided link in your web browser.

Upload your resume in PDF format.

(Optional) Provide a job description to get tailored feedback.

Click on "Process PDF" to receive feedback.

Dependencies
streamlit: For creating the web interface.
google-generativeai: For generating feedback on the resume.
PyMuPDF: For reading PDF files.
Author
Samarth Saraogi - A final year engineering student with a passion for building apps with AI/Computer Vision.

GitHub
LinkedIn
License
This project is open-source. Feel free to fork, modify, and use as you see fit.

You can add this README to the root directory of the repository to provide users with information about the project, its features, and how to use it.
