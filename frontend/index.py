import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def form_submission():
    with st.form("Resume and JD"):
        uploaded_file = st.file_uploader(label = 'Resume', type = ['.pdf', '.docx'], max_upload_size=5, accept_multiple_files = False)
        job_description = st.text_area(label = 'Job Description')
        submit_button = st.form_submit_button("Submit")
    if submit_button:
        if uploaded_file is None:
            st.warning("Please upload a resume")
            st.stop()
        if job_description.strip() == "":
            st.warning("Please fill in the field with a job decsription")
            st.stop()
        process_input(uploaded_file, job_description)


def process_input(uploaded_file: UploadedFile, job_description : str):
    api_url = os.getenv('API_URL')
    form_file = {"file": uploaded_file}
    form_data = {"job_description": job_description}
    try:
        with st.spinner("Processing", show_time=True):
            response = requests.post(api_url, files = form_file, data = form_data)
            data = response.json()
            if response.status_code == 200:
                st.success("API Call Successful!")
                st.markdown(data)
            else:
                st.error(icon="🚨", body = f"Error {response.status_code}: {data['detail']}")       
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Is api.py running?")


def main():
    st.title('AI Resume Reviewer')    
    st.set_page_config(page_title="AI Resume Reviewer by Kenny Truong")
    form_submission()


if __name__ == "__main__":
    main()       