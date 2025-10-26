from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from database import create_db_and_tables, engine
from models import ReviewResult
from review_logic import analyze_writeup, analyze_code, check_plagiarism, check_code_plagiarism
import json
from pydantic import BaseModel
from typing import Optional, Literal

app = FastAPI(title="AI Peer Review API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins (e.g., your Streamlit app)
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

class PlagiarismRequest(BaseModel):
    text: str
    filename: str = "text_input"
    language: Optional[str] = None  # For code plagiarism

@app.post("/review/writeup")
async def review_writeup_endpoint(
    text: Optional[str] = Form(None), 
    file: Optional[UploadFile] = File(None)
):
    file_text = ""
    filename = "text_input"

    try:
        if file:
            file_text = (await file.read()).decode("utf-8")
            filename = file.filename if file.filename else "uploaded_file.txt"
        elif text:
            file_text = text
            # filename is already "text_input"
        else:
            raise HTTPException(status_code=400, detail="No text or file provided")

        # 1. Analyze text using the new logic
        result = analyze_writeup(file_text)

        # 2. Save to DB
        with Session(engine) as session:
            review_entry = ReviewResult(
                filename=filename,
                review_type="writeup",
                scores=json.dumps(result["scores"]), # Store scores as JSON string
                feedback=result["overall_feedback"],
                full_response=json.dumps(result) # Store the full JSON response
            )
            session.add(review_entry)
            session.commit()
            session.refresh(review_entry)
        
        return {"status": "success", "feedback": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/review/code")
async def review_code_endpoint(
    language: str = Form(...),
    code: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    code_text = ""
    filename = "code_input"

    try:
        if file:
            code_text = (await file.read()).decode("utf-8")
            filename = file.filename if file.filename else f"uploaded_code.{language.lower()}"
        elif code:
            code_text = code
            filename = f"code_input.{language.lower()}"
        else:
            raise HTTPException(status_code=400, detail="No code or file provided")
        
        # 1. Analyze code - this returns a string, not a dict!
        feedback_text = analyze_code(code_text, language)

        # 2. Save to DB - use the string directly for feedback
        with Session(engine) as session:
            review_entry = ReviewResult(
                filename=filename,
                review_type="code",
                scores=json.dumps({}), # No scores for code review
                feedback=feedback_text,  # Use the string directly
                full_response=json.dumps({"feedback": feedback_text})
            )
            session.add(review_entry)
            session.commit()
            session.refresh(review_entry)

        return {"status": "success", "feedback": {"feedback": feedback_text}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/review/plagiarism")
async def check_plagiarism_endpoint(request: PlagiarismRequest):
    try:
        # 1. Check plagiarism
        result = check_plagiarism(request.text)

        # 2. Save to DB with plagiarism score
        with Session(engine) as session:
            review_entry = ReviewResult(
                filename=request.filename,
                review_type="plagiarism",
                scores=json.dumps({
                    "plagiarism_score": result.get("plagiarism_score", 0), 
                    "confidence": result.get("confidence", "Unknown"),
                    "source_count": len(result.get("sources", []))
                }),
                feedback=result["summary"],
                full_response=json.dumps(result)
            )
            session.add(review_entry)
            session.commit()
            session.refresh(review_entry)

        return {"status": "success", "feedback": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/review/code_plagiarism")
async def check_code_plagiarism_endpoint(request: PlagiarismRequest):
    try:
        language = request.language if request.language else "Unknown"
        
        # 1. Check code plagiarism
        result = check_code_plagiarism(request.text, language)

        # 2. Save to DB with plagiarism score
        with Session(engine) as session:
            review_entry = ReviewResult(
                filename=request.filename,
                review_type="code_plagiarism",
                scores=json.dumps({
                    "plagiarism_score": result.get("plagiarism_score", 0), 
                    "confidence": result.get("confidence", "Unknown"),
                    "source_count": len(result.get("sources", [])),
                    "indicator_count": len(result.get("indicators", []))
                }),
                feedback=result["summary"],
                full_response=json.dumps(result)
            )
            session.add(review_entry)
            session.commit()
            session.refresh(review_entry)

        return {"status": "success", "feedback": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_all_reviews():
    """
    Get all past review results.
    """
    with Session(engine) as session:
        reviews = session.exec(select(ReviewResult)).all()
        return reviews

@app.get("/")
def read_root():
    return {"message": "AI Peer Review API is running!", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}