from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load API key
load_dotenv() 
print("API KEY LOADED:", os.getenv("GEMINI_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["http://localhost:5173"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QueryRequest(BaseModel):
    query: str

# Education keywords
EDUCATION_KEYWORDS = [
    "college", "school", "degree", "university", "fees", "exam", "course",
    "admission", "student", "syllabus", "placement", "results", "bengaluru",
    "education", "tution", "marks", "ug", "pg", "scholarship"
]

def is_education_query(query: str) -> bool:
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in EDUCATION_KEYWORDS)

@app.post("/ask")
async def ask_question(request: QueryRequest):
    query = request.query

    # Sector filter
    if not is_education_query(query):
        return {"response": "Sorry, I only answer education-related questions."}

    # Prompt Gemini as Education Expert
    prompt = f"""
You are an expert chatbot that ONLY answers about education in India.
Answer concisely (3-4 lines) unless detailed explanation is explicitly requested.
If the question is unrelated, reply: "Sorry, I only answer education-related questions."

Question: {query}
"""



    model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro" for higher accuracy
    response = model.generate_content(prompt)

    return {"response": response.text}
