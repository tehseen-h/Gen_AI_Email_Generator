# 📧 Generative-AI LLM-Driven Career Outreach Automation  

**Automate personalized job application emails with AI!**  
*Save hours by letting AI craft tailored emails that match job descriptions to your skills.*  

🌐 **Live Demo**: [Try it here!](https://gen-ai-email-generator-tehseen-h.streamlit.app/)  

---

## ✨ Features  
- **🔗 Job Link Analysis**: Paste a job posting URL (LinkedIn/company career page), and the app extracts key details like job title, company, and requirements.  
- **🤖 AI-Powered Email Generation**: Uses Groq's Llama3-70B model to write professional emails that align your skills with the job description.  
- **🎨 Customizable Tone**: Choose between *Professional*, *Friendly*, or *Formal* email styles.
- **📜 Email History: Keep track of your last generated emails with timestamps.
- **📥 Download & Regenerate**: Download the email as a text file or regenerate for new variations.  
- **🔒 Secure**: API keys protected via Streamlit Secrets.  

---

## 🛠️ How It Works  
1. **Input**: User provides a job URL and recipient details.  
2. **Web Scraping**: Extracts job title, company, skills, and description from the URL.  
3. **AI Processing**: Matches your skills to the job requirements using LLM.  
4. **Output**: Generates a polished email ready to send!  

---

## 🚀 Quick Start  
### Prerequisites  
- Python 3.8+  
- Groq API Key

### Installation  
```bash  
git clone https://github.com/yourusername/gen-ai-email-generator.git  
cd gen-ai-email-generator  
pip install -r requirements.txt


## How It Works
###Job Details Scraping:

- The app uses basic HTML scraping for job postings from platforms like LinkedIn and Indeed.
- If critical information is missing (e.g., company name or role), it triggers an LLM-based fallback using the LangChain community loader to extract relevant details.

###Email Generation:

- A dynamic prompt is created using the scraped data along with your provided candidate details (skills, name, etc.).
- The language model processes the prompt to generate a personalized email that matches the job description and your profile.

###User Interface:

- Built using Streamlit, the app provides an interactive form for input.
- Features include a custom styled UI, download button for saving emails, and a history section displaying your last three generated emails.

##Tech Stack
- Python 🐍
- Streamlit: For creating the interactive UI.
- BeautifulSoup & Requests: For web scraping.
- LangChain: For prompt templating and output parsing.
- OpenAI: Powered by the OpenAI API (via GROQ endpoint).
- dotenv: To manage environment variables.
