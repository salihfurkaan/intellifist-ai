from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from bs_scraper import scrape_through_hs

app = FastAPI()

class Question(BaseModel):
    number: str
    full_text: str
    options: List[str]

class ScraperRequest(BaseModel):
    grade: str
    lesson: str
    topic: str

@app.post("/scrape", response_model=List[Question])
async def scrape_questions(request: ScraperRequest):
    try:
        results = scrape_through_hs(request.grade, request.lesson, request.topic)
        if not results:
            raise HTTPException(status_code=404, detail="No questions found")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the TestKolik Scraper API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
