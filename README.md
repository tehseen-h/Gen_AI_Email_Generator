# 📧 Generative-AI LLM-Driven Career Outreach Automation  

**Automate personalized job application emails with AI!**  
*Save hours by letting AI craft tailored emails that match job descriptions to your skills.*  

🌐 **Live Demo**: [Try it here!](https://gen-ai-email-generator-tehseen-h.streamlit.app/)  

---

## ✨ Features  
- **🔗 Job Link Analysis**: Paste a job posting URL (LinkedIn/Indeed), and the app extracts key details like job title, company, and requirements.  
- **🤖 AI-Powered Email Generation**: Uses Groq's Llama3-70B model to write professional emails that align your skills with the job description.  
- **🎨 Customizable Tone**: Choose between *Professional*, *Friendly*, or *Formal* email styles.  
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
- Groq API Key ([Get yours here](https://console.groq.com/keys))  

### Installation  
```bash  
git clone https://github.com/yourusername/gen-ai-email-generator.git  
cd gen-ai-email-generator  
pip install -r requirements.txt  
