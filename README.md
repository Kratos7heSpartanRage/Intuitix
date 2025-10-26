# INTUITIX - AI-Powered Peer Review Platform

INTUITIX is an intelligent AI-powered platform designed to provide comprehensive analysis of written content and code. Leveraging advanced language models and sophisticated algorithms, INTUITIX offers detailed feedback, plagiarism detection, and quality assessment for academic, professional, and personal projects.

## 🚀 Features
### ✍️ Write-up Analysis 
1. Grammar Scoring: Detailed evaluation of grammatical accuracy and syntax
2. Clarity Assessment: Analysis of writing clarity and readability
3. Structure Evaluation: Assessment of logical flow and organization
4. Error Detection: Identification of spelling, tense, and article usage issues
5. Improvement Suggestions: Actionable recommendations for enhancement

### 💻 Code Review
1. Multi-language Support: Python, JavaScript, Java, C++, HTML, CSS, SQL, and more
2. Best Practices: Evaluation of code quality and adherence to language conventions
3. Bug Detection: Identification of logical errors and potential issues
4. Performance Suggestions: Recommendations for optimization and improvement
5. Readability Analysis: Assessment of code structure and documentation

### 🔍 Plagiarism Detection
1. Text Plagiarism: AI-powered analysis of written content originality
2. Code Plagiarism: Detection of copied code patterns and common implementations
3. Similarity Scoring: Dynamic plagiarism scores (0-100) with confidence levels
4. Source Identification: Potential source matching and pattern recognition
5.Risk Assessment: Comprehensive risk analysis with detailed indicators

### 📊 Smart Analytics
1. Real-time Scoring: Instant feedback with detailed metrics
2. Historical Tracking: Complete history of all analyses performed
3. Comparative Analysis: Side-by-side comparison of multiple submissions
4. Export Capabilities: Downloadable reports and analysis data

## 🛠️ Technology Stack
### Backend
1. FastAPI: High-performance Python web framework
2. SQLModel: Modern SQL database integration with SQLite
3. Groq API: Lightning-fast LLM inference
4. Pydantic: Data validation and serialization

### Frontend
1. Streamlit: Interactive web application framework
2. Pandas: Data manipulation and analysis
3. Requests: HTTP client for API communication

### AI/ML
1. Llama 3.1 8B Instant: Advanced language model for analysis
2. Custom Prompts: Optimized prompts for different analysis types
3. Dynamic Scoring: Intelligent scoring algorithms based on content characteristics

## 📦 Installation
### Prerequisites
Python 3.8+
Groq API Key (Free tier available)

### Quick Setup (5 minutes)
Clone or Download the Project

```
# If using git
git clone https://github.com/your-username/intuitix.git
cd intuitix

# Or simply create a folder and add the project files
```

Create Virtual Environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install Dependencies

```
pip install fastapi uvicorn sqlmodel groq streamlit requests pandas python-dotenv pymysql cryptography sqlalchemy
```

Environment Configuration
Create a .env file in the root directory:

```
DATABASE_URL=sqlite:///./reviews.db
GROQ_API_KEY=your_actual_groq_api_key_here
```

Initialize Database (Automatic)

```
# The database will be created automatically when you first run the application
# Or run manually:
python -c "from database import create_db_and_tables; create_db_and_tables()"
```

Start the Application

```
# Terminal 1 - Start Backend (FastAPI)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Start Frontend (Streamlit)
streamlit run app.py
```

Access the Application
1. Frontend: http://localhost:8501
2. Backend API: http://localhost:8000
3. API Documentation: http://localhost:8000/docs

## 🎯 Usage
### Quick Start
1. Open the Application in your browser at http://localhost:8501
2. Choose Analysis Type using the quick action buttons:

📝 Analyze Write-up

💻 Review Code

🔍 Check Text Plagiarism

⚡ Check Code Plagiarism

3. Submit Your Content:

4. Paste text/code directly into the text area, or upload files (.txt for text, any for code)

5. Select programming language for code analysis

6. Get Instant Results:

i. Real-time scoring and feedback
ii. Detailed error analysis
iii. Plagiarism risk assessment
iv. Improvement recommendations

## 📁 Project Structure

intuitix/
├── app.py                 # Streamlit frontend
├── main.py               # FastAPI backend
├── review_logic.py       # AI analysis logic
├── database.py           # Database configuration
├── models.py             # Data models
├── requirements.txt      # Dependencies
├── .env                 # Environment variables
└── reviews.db           # SQLite database (auto-created)

## 🔧 Configuration
### Environment Variables (.env)

```
DATABASE_URL=sqlite:///./reviews.db
GROQ_API_KEY=your_groq_api_key_here
```

### Getting Groq API Key
1. Visit https://console.groq.com
2. Sign up for free account
3. Generate API key
4. Add to your .env file

## 🗄️ Database
1. INTUITIX uses SQLite for simplicity and portability:
2. Automatic setup - no manual database creation needed
3. Single file - easy backup and sharing
4. Zero configuration - works out of the box
5. File location: [peer_reviews.db in project root

## 🚀 Deployment
Local Development
```
# Start both services
./start_services.sh
```
# Or manually:
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
streamlit run app.py
```
Production Deployment
For production, consider:

1. Docker containerization
2. PostgreSQL instead of SQLite
3. Environment-specific configurations
4. API key rotation

## 🐛 Troubleshooting
Common Issues

1. Port already in use

```
# Kill processes on ports 8000/8501
sudo fuser -k 8000/tcp
sudo fuser -k 8501/tcp
```

2. Module not found errors

```
pip install -r requirements.txt
```

3. Groq API errors

i. Verify API key in .env
ii. Check Groq service status
iii. Ensure proper internet connection

4. Database issues

```
# Reset database
rm reviews.db
python -c "from database import create_db_and_tables; create_db_and_tables()"
```

🙏 Acknowledgments
1. Groq for ultra-fast LLM inference
2. Streamlit for seamless web app development
3. FastAPI for robust backend API
4. SQLModel for elegant database integration
5. SQLite for zero-configuration data persistence

INTUITIX - Intelligent Analysis Made Simple 🚀

*Built for Udbhav'25 Hackathon - AI-Driven Peer Review Platform*
