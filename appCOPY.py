import streamlit as st
import google.generativeai as palm
import fitz  # PyMuPDF library
import re

palm.configure(api_key="AIzaSyCB4uoFy4QUTvsnEyL7R8pRje8wgdGZ8u8")

defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.5,
    'candidate_count': 1,
    'top_k': 30,                            
    'top_p': 0.95,
    'max_output_tokens': 1024,
    'stop_sequences': [],
    'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
    }

def fix(text,job_description):
    
    withoutjd=f"""
    You are a top hiring manager
    Resume:{text}

    Give the feedback specific to this resume
    rewrite the sentences to make them more concise and clear
    quantify impact where possible. do not assume data for qauntification
    For example

    Managed a team of software developers.-> Managed a team of [x] software developers, overseeing key projects that were delivered ahead of schedule by an average of [y] weeks.
    Responsible for increasing sales.-> Increased quarterly sales by [20%], resulting in an additional [$500,000] in revenue.

   

        



    OUTPUT FORMAT
    1.Specific Feedback for the resume
    [output]
    
    2.Rephrasing Suggestions
    [old sentence->new sentence] format

    """

    withjd=prompt = f"""You are a top hiring manager
Read the given resume 
{text}

If this resume is submitted for the following Job Description 

 {job_description}

What changes would you suggest, and what what will you say is missing
Give the feedback specific to this resume. 
OUTPUT FORMAT
**General Feedback**

"General Feedback about the resume, including resume language, relevance to given Job Description."
"Skills Missing":
"Feedback about missing skills for the job description"

EXAMPLE
I would also suggest adding the following skills to your resume: 
 
* [SKILL 1]
* [SKILL 2]
Suggested Rephrasing
"sentence in the resume"->"better phrasing of sentence"
    quantify impact where possible. do not assume data for qauntification
    For example

    Managed a team of software developers.-> Managed a team of [x] software developers, overseeing key projects that were delivered ahead of schedule by an average of [y] weeks.
    Responsible for increasing sales.-> Increased quarterly sales by [20%], resulting in an additional [$500,000] in revenue.
for example
* "Devised a Image Classification model to be applied in Industrial Systems" -> "Developed an image classification model to detect when analog gauge readings exceed safe limits and actuate a contingency response" 



"""

    prompt=withjd if job_description else withoutjd

    response = palm.generate_text(
    **defaults,
    prompt=prompt
    )
    question_list=response.result
    
    return response.result





def remove_personal_info(text,job_description):
    # Regular expression patterns
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    phone_pattern = r'\b\d{3}[-\s]?\d{3}[-\s]?\d{4}\b'
    link_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # Remove email addresses
    text = re.sub(email_pattern, 'eml@ad.com', text)

    # Remove phone numbers
    text = re.sub(phone_pattern, '09', text)

    # Remove links
    text = re.sub(link_pattern, 's.l.com', text)

    return fix(text,job_description)


    # sanitized_resume = remove_personal_info(resume_text)
    # print(sanitized_resume)






def read_pdf(file,job_description):
    text = ""
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()
    pdf_document.close()
    #TESTING
    return remove_personal_info(text,job_description)
    #return fix(text,job_description)                                         #CHANGE AFTER TESTING

def main():
    #st.set_theme('light')
    st.set_page_config(page_title="Resume Fixer", page_icon="🔨", layout="wide")

    # Sidebar (Navigation)
    menu = ["Home", "About the Author"]
    choice = st.sidebar.selectbox("Select Page", menu)

    if choice == "Home":
        home_page()
    elif choice == "About the Author":
        about_page()

def home_page():
    st.title("Resume :handshake: Job Description")
    st.write("Get resume feedback and job description suggestions from an AI model. This app uses the [Generative AI API](https://developers.generativeai.google/products/palm) from Google.")
    uploaded_file = st.file_uploader("Upload your Resume", type=["pdf"])
    on = st.toggle('Activate feature')

    if on:
        st.subheader("Job Description:")
        job_description = st.text_area("Paste or type the job description here")
        st.info("Paste the qualifications/skills mentioned in the job description above. Do not include company history, location, etc.")
    else:
        job_description=None
   
    if uploaded_file is not None:
        if st.button("Process PDF"):
            st.subheader("Resume Feedback:")
            try:
                pdf_text = read_pdf(uploaded_file, job_description)
                st.write(pdf_text)
            except:
                st.error("Error reading the PDF. Please make sure it's a valid PDF document.")

def about_page():
    st.title("About the Author")
    st.write("Hi. This is Samarth. I am a final year engineering student. I build apps with AI/Computer Vision. Feel free to reach out to me for any queries/suggestions about this project.")
    st.markdown("[GitHub](https://github.com/samarth6341/)")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/samarth-saraogi/)")

if __name__ == "__main__":
    main()