from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Get SerpAPI key from environment
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
if not SERPAPI_KEY:
    raise ValueError("SERPAPI_KEY environment variable is not set. Please check your .env file.")

app = FastAPI(
    title="News Analysis API",
    description="API to fetch and analyze news from the past 24 hours",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for response
class NewsStory(BaseModel):
    headline: str
    summary: str
    significance: str
    key_entities: List[str]
    commentary_note: str

class NewsResponse(BaseModel):
    output: dict

async def fetch_news_data():
    """
    Common function to fetch news data
    """
    try:
        # Configure SerpAPI search
        params = {
            "engine": "google",
            "q": "news",
            "tbm": "nws",
            "api_key": SERPAPI_KEY,
            "time": "d1",  # Last 24 hours
            "num": 3  # Number of results
        }

        # Perform search
        search = GoogleSearch(params)
        results = search.get_dict()

        # Process and structure news stories
        news_stories = []
        if "news_results" in results:
            for story in results["news_results"]:
                # Extract key entities (organizations and people mentioned)
                key_entities = []
                if "source" in story:
                    key_entities.append(story["source"])
                
                # Create structured news story
                news_story = NewsStory(
                    headline=story.get("title", ""),
                    summary=story.get("snippet", ""),
                    significance="This story is significant as it represents current developments in important global events.",
                    key_entities=key_entities,
                    commentary_note="Expert analysis would provide deeper insights into the implications and potential developments."
                )
                news_stories.append(news_story)

        # Format response according to required structure
        response = [{
            "output": {
                "news_stories": [story.dict() for story in news_stories]
            }
        }]

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news", response_model=List[NewsResponse])
async def get_news():
    """
    Get news stories from the past 24 hours using GET method.
    """
    return await fetch_news_data()

@app.get("/news/analysis")
async def get_news_analysis():
    """
    Get news stories and analyze them for expert commentary topics.
    Uses AI to select the top 3 topics that would benefit from expert commentary.
    """
    try:
        # Import the analyzer
        from agent import analyze_news_stories
        
        # Fetch news data
        news_data = await fetch_news_data()
        
        # Analyze the news
        analysis = analyze_news_stories(news_data)
        
        # return analysis
        return [analysis, {"status":"success","status_code":200}]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news/experts")
async def get_expert_recommendations():
    """
    Get expert recommendations for news topics.
    First analyzes news to find important topics, then finds experts for those topics.
    """
    try:
        # Import the necessary functions
        from agent import analyze_news_stories
        from expert_finder import find_experts_for_topics
        
        # Fetch news data
        news_data = await fetch_news_data()
        
        # Step 1: Analyze the news to identify topics
        news_analysis = analyze_news_stories(news_data)
        
        # Step 2: Find experts for those topics
        experts_data = find_experts_for_topics(news_analysis)
        
        # Return as a list for consistent response format
        return [experts_data, {"status":"success","status_code":200}]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 