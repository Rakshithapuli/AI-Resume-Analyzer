import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Load Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")

# App Title
st.title("🤖 AI Resume Analyzer")
st.write("Upload your resume and compare it with a job description.")

# Upload Resume
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# Job Description Input
job_description = st.text_area(
    "Paste Job Description"
)

# Process Resume
if uploaded_file and job_description:

    reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text

    if st.button("Analyze Resume"):

        prompt = f"""
        You are an ATS Resume Analyzer.

        Analyze the following resume against the job description.

        Resume:
        {resume_text}

        Job Description:
        {job_description}

        Provide:

        1. Match Percentage
        2. Matching Skills
        3. Missing Skills
        4. Resume Improvement Suggestions
        5. Final Verdict
        """

        try:
            with st.spinner("Analyzing Resume..."):
                response = model.generate_content(prompt)

            st.subheader("📊 Analysis Result")

            st.write(response.text)

            # Download Report
            st.download_button(
                label="📥 Download Report",
                data=response.text,
                file_name="resume_analysis.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {e}")