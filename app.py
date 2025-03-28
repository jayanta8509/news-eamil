from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
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
    description="API for news analysis, expert finding, and email generation",
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

# Pydantic models for input and response
class NewsStory(BaseModel):
    headline: str
    summary: str
    significance: str
    key_entities: List[str]
    commentary_note: str

class ExpertInput(BaseModel):
    topic: str
    name: str
    institution: str
    expertise: str
    notable_work: str
    unique_perspective: str
    contact_method: str
    suggested_questions: List[str]
    contact_info: str

class NewsQueryInput(BaseModel):
    category: str

class TopicInput(BaseModel):
    topic_id: int
    headline: str
    summary: str
    need_for_commentary: str
    expert_angles: List[str]

async def fetch_news_by_category(category: str):
    """
    Fetch news data based on a specific category
    """
    try:
        # Configure SerpAPI search
        params = {
            "engine": "google",
            "q": category,
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

@app.post("/news/analysis/category")
async def analyze_news_by_category(query: NewsQueryInput):
    """
    Get news stories by category and analyze them for expert commentary topics.
    Uses AI to select the top 3 topics that would benefit from expert commentary.
    
    Example categories:
    - "sports news"
    - "business or finance news"
    - "European news"
    - "tabloid or sensational news"
    - "legal news"
    """
    try:
        # Import the analyzer
        from agent import analyze_news_stories
        
        # Fetch news data for the specified category
        news_data = await fetch_news_by_category(query.category)
        
        # Analyze the news
        analysis = analyze_news_stories(news_data)
        
        return {"output": analysis, "status": "success", "status_code": 200}
    
    except Exception as e:
        print(f"API Error in /news/analysis/category: {str(e)}")
        return {
            "output": {
                "selected_topics": [],
                "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            },
            "status": "error",
            "status_code": 500,
            "error": str(e)
        }

@app.post("/email/generate", response_model=Dict[str, Any])
async def generate_email_template(expert_data: ExpertInput):
    """
    Generate a personalized email template for an expert based on their information.
    """
    try:
        # Import the email generator
        from email_agent import generate_expert_email
        
        # Convert Pydantic model to dictionary
        expert_dict = expert_data.dict()
        
        # Generate email template
        email_template = generate_expert_email(expert_dict)
        
        return email_template
    
    except Exception as e:
        print(f"API Error in /email/generate: {str(e)}")
        return {
            "email_templates": [
                {
                    "expert_name": expert_data.name,
                    "topic": expert_data.topic,
                    "subject": f"Expert Commentary Request: {expert_data.topic} - Response Needed in 6 Hours",
                    "greeting": f"Dear {expert_data.name},",
                    "email_body": f"Error generating email: {str(e)}",
                    "signature": "Best regards,\nNews Analysis Team\nsupport@example.com\n(123) 456-7890"
                }
            ],
            "status": "error",
            "status_code": 500
        }

@app.post("/news/experts/topic", response_model=Dict[str, Any])
async def get_experts_for_topic(topic: TopicInput):
    """
    Get expert recommendations for a specific topic provided directly by the user.
    
    This allows skipping the news fetching and analysis steps when you already have a topic.
    """
    try:
        # Import the necessary function
        from expert_finder import find_experts_for_single_topic
        
        # Convert Pydantic model to dictionary
        topic_dict = topic.dict()
        
        # Print input for debugging
        # print(f"Topic received: {topic_dict}")
        
        # Find experts for the specific topic
        experts_data = find_experts_for_single_topic(topic_dict)
        
        # Check if there was an error flag in the response
        if experts_data.get("error", False):
            print("Error flag detected in experts_data")
            return {
                "output": experts_data,
                "status": "error",
                "status_code": 500,
                "error_message": "Failed to get experts. Check server logs for details."
            }
        
        # Validate the response before returning
        if not experts_data or not isinstance(experts_data, dict):
            print("Invalid response format received")
            return {
                "output": {
                    "expert_recommendations": [
                        {
                            "topic_id": topic_dict.get("topic_id", 1),
                            "topic": topic_dict.get("headline", "Error"),
                            "experts": [
                                {
                                    "name": "API Error",
                                    "institution": "Please try again later",
                                    "expertise": "An error occurred processing your request",
                                    "notable_work": "N/A",
                                    "unique_perspective": "N/A",
                                    "contact_method": "N/A",
                                    "suggested_questions": [],
                                    "contact_info": "support@example.com"
                                }
                            ]
                        }
                    ]
                },
                "status": "error",
                "status_code": 500
            }
        
        return {"output": experts_data, "status": "success", "status_code": 200}
    
    except Exception as e:
        print(f"API Error in /news/experts/topic: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return {
            "output": {
                "expert_recommendations": [
                    {
                        "topic_id": topic.topic_id,
                        "topic": topic.headline,
                        "experts": [
                            {
                                "name": "API Error",
                                "institution": "Please try again later",
                                "expertise": f"Error: {str(e)}",
                                "notable_work": "N/A",
                                "unique_perspective": "N/A",
                                "contact_method": "N/A",
                                "suggested_questions": [],
                                "contact_info": "support@example.com"
                            }
                        ]
                    }
                ]
            },
            "status": "error",
            "status_code": 500
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 