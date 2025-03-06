import requests
from bs4 import BeautifulSoup
import re
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables and initialize client at the top



load_dotenv()


# Use this for deployment
if st.secrets.get("GROQ_API_KEY"):
    api_key = st.secrets["GROQ_API_KEY"]
else:
    # Fallback for local development
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=api_key,  # Works both locally and in production
    base_url="https://api.groq.com/openai/v1"
)


def scrape_job_details(url):
    try:
        job_data = basic_scrape(url)
        
        if not job_data.get('company') or not job_data.get('role'):
            job_data = llm_scrape_fallback(url)
            
        return job_data
        
    except Exception as e:
        return {"error": f"Scraping failed: {str(e)}"}

def basic_scrape(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if "linkedin.com" in url:
            container = soup.find('main', class_='main')
            return {
                "role": container.find('h1').text.strip() if container else None,
                "company": container.find('a', class_='topcard__org-name-link').text.strip() if container else None,
                "description": soup.find('div', class_='description__text').text.strip() if soup else None
            }
            
        elif "indeed.com" in url:
            return {
                "role": soup.find('h1', class_='jobsearch-JobInfoHeader-title').text.strip(),
                "company": soup.find('div', class_='jobsearch-CompanyInfoContainer').text.split('\n')[0].strip(),
                "description": soup.find('div', id='jobDescriptionText').text.strip()
            }
            
        return llm_scrape_fallback(url)
        
    except:
        return {}

def llm_scrape_fallback(url):
    try:
        loader = WebBaseLoader(url)
        page_data = loader.load()[0].page_content[:5000]
        
        prompt = PromptTemplate.from_template("""
        **Website Content**: {page_data}
        
        Extract these fields STRICTLY as JSON:
        {{
            "role": "Job title (exact match)",
            "company": "Company name (official name)",
            "skills": ["list", "of", "technical", "skills"],
            "description": "Full job description (min 200 characters)"
        }}
        
        RULES:
        1. NEVER use "Not specified" - find the actual value
        2. Company name MUST appear in the page text
        3. If unsure, make educated guesses
        """)
        
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt.format(page_data=page_data)}],
            temperature=0.3,
            response_format={"type": "json_object"},
            max_tokens=500
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        return {"error": str(e)}
    
    

# Streamlit UI
st.set_page_config(page_title="AI Email Generator", page_icon="✉️")

st.markdown("""
<style>
    .stTextInput input { border: 2px solid #4CAF50 !important; border-radius: 5px; }
    .stButton>button { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 8px; }
    .stSpinner>div { border-top-color: #4CAF50; }
    h1 { color: #2d3436; }
    .stDownloadButton>button { background-color: #2d3436 !important; }
</style>
""", unsafe_allow_html=True)

st.title("AI-Powered Job Application Email Generator")
st.write("Paste a job URL and recipient details to generate a personalized email!")

with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        job_url = st.text_input("Job Posting URL*", placeholder="https://linkedin.com/jobs/123")
    with col2:
        recipient_name = st.text_input("Recipient Name*", placeholder="John Doe")
    recipient_role = st.text_input("Recipient Role*", placeholder="Hiring Manager")
    
    with st.expander("➕ Add Your Details (Optional)"):
        your_name = st.text_input("Your Name", placeholder="Alex Smith")
        your_skills = st.text_input("Relevant Skills", placeholder="Python, Project Management")

    #-------------
        col3, col4 = st.columns(2)
    with col3:
        email_tone = st.selectbox(
            "📝 Email Tone",
            ["Professional", "Friendly", "Formal"],
            index=0
        )
    with col4:
        email_length = st.select_slider(
            "🔠 Email Length",
            options=["Short", "Medium", "Long"],
            value="Medium"
        )
    # ==========================
    
    submit_button = st.form_submit_button("✨ Generate Email")

if submit_button:
    if not job_url or not recipient_name or not recipient_role:
        st.error("Please fill all required fields (*)")
    else:
        with st.spinner("Generating email..."):
            try:
                job_details = scrape_job_details(job_url)
        
                if "error" in job_details:
                    st.error(f"Scraping Error: {job_details['error']}")
                    st.stop()
            
                required_fields = {
                    'role': "Job Title",
                    'company': "Company Name",
                    'description': "Job Description"
                }
        
                errors = []
                for field, name in required_fields.items():
                    value = job_details.get(field, "").lower().strip()
                    if not value or "not found" in value or "not specified" in value:
                        errors.append(f"Missing {name} in job post")
                
                if errors:
                    st.error(" | ".join(errors))
                    st.stop()

                job_details['role'] = job_details['role'].split('|')[0].split('-')[0].strip()
                job_details['company'] = job_details['company'].split('·')[0].strip()

                # Safely handle optional fields
                skills = job_details.get('skills', [])
                experience = job_details.get('experience', 'Not specified')

                prompt = f"""
                **Objective**: Create a job application email that demonstrates strong skill alignment between candidate and position.

                **Job Analysis Requirements**:
                1. Carefully analyze this job description for sections titled:
                   - "Qualifications"
                   - "Skills Required" 
                   - "Requirements"
                   - "Technical Skills"
                   - "What We're Looking For"
                2. Extract ALL technical/hard skills and tools mentioned (prioritize repeated terms)
                3. Identify 3-5 CORE requirements (e.g., "Python", "AWS", "Agile methodologies")

                **Candidate Profile**:
                - My Skills: {your_skills or 'Not provided'}
                - Relevant Experience: {experience or 'Not specified'}

                **Email Composition Rules**:
                1. STRUCTURE:
                   - Opening: Express enthusiasm for specific role aspects
                   - Skill Matching: Create bullet points matching 3-4 JD requirements with my skills
                   - Experience Proof: Add 1 brief achievement statement per matched skill
                   - Closing: Request next steps

                2. Match Priorities:
                   a) Direct tool/technology matches (Python → Python)
                   b) Conceptual matches (Problem solving → Analytical skills)
                   c) Transferable skills (Team leadership → Project management)

                3. Style Guidelines:
                   - Tone: {email_tone} {"(use 1-2 emojis in subject line)" if email_tone == "Friendly" else ""}
                   - Length: {email_length} ({160 if email_length=="Short" else 220 if email_length=="Medium" else 300} words)
                   - Use industry-specific terminology from JD
                   - Mirror language from skills section ("We require Python" → "My Python experience...")
                   - Keep paragraphs under 3 lines
                   - Use active voice and metrics when possible

                **Example Structure**:
                "Having developed [SKILL 1] experience through [CONTEXT], 
                I successfully [ACHIEVEMENT]. This aligns with your need for [JD REQUIREMENT]..."

                **Job Details**:
                - Role: {job_details['role']}
                - Company: {job_details['company']}
                - Key Requirements: {', '.join(skills[:10]) if skills else 'Analyze JD text directly'}
                """

# Keep the rest of your code the same

                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=350
                )

                generated_email = response.choices[0].message.content
                st.subheader("Generated Email")
                st.markdown(f"```\n{generated_email}\n```")

                col1, col2, _ = st.columns([1,1,3])
                with col1:
                    st.download_button(
                        "📥 Download Email",
                        generated_email,
                        file_name="job_application_email.txt"
                    )
                with col2:
                    if st.button("🔄 Regenerate"):
                        st.rerun()
                # ======== EMAIL HISTORY ========
                # Initialize once at app start (NOT inside submit block)
                if 'history' not in st.session_state:
                    st.session_state.history = []

                # Add to history
                st.session_state.history.append({
                    "email": generated_email,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "job": job_details['role']
                })

                # Display history
                with st.expander("📜 Last 3 Generated Emails"):
                    for entry in st.session_state.history[-3:]:
                        st.markdown(f"**{entry['job']}** ({entry['timestamp']})")
                        st.code(entry['email'])
                        st.divider()
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")