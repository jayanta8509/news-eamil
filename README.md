# News Analysis API with Expert Recommendations

This FastAPI application fetches and structures news stories from the past 24 hours using SerpAPI, analyzes them to identify important topics, and recommends experts for each topic.

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your API keys:
```
SERPAPI_KEY=your_serpapi_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Application

Start the server:
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /news

Fetches news stories from the past 24 hours.

### POST /fetch-news

Alternative endpoint to fetch news using POST method.

### GET /news/analysis

Analyzes news stories and identifies the top 3 topics that would benefit from expert commentary. This uses an AI model to evaluate topics based on complexity, public interest, timeliness, impact, and controversy.

Response format:
```json
{
  "selected_topics": [
    {
      "headline": "Topic headline",
      "summary": "2-3 sentence summary",
      "need_for_commentary": "Why this topic needs expert input",
      "expert_angles": ["Specific question 1", "Specific question 2"]
    }
  ],
  "analysis_timestamp": "2023-05-18 12:34:56.789012"
}
```

### GET /news/experts

Finds expert recommendations for the top news topics. This endpoint:
1. Fetches news stories
2. Analyzes them to identify important topics
3. Recommends 3 experts for each topic

Response format:
```json
{
  "expert_recommendations": [
    {
      "topic_id": 1,
      "topic": "Topic headline",
      "experts": [
        {
          "name": "Expert Name",
          "institution": "University or Organization",
          "expertise": "Relevant field of expertise",
          "notable_work": "Publications or achievements",
          "unique_perspective": "What makes their view valuable",
          "contact_method": "How to reach them",
          "suggested_questions": ["Question 1", "Question 2"],
          "contact_info": "expert.name@institution.edu"
        }
      ]
    }
  ]
}
```

### POST /email/generate

Generates a personalized email template for requesting expert commentary. This endpoint:
1. Takes expert information as input
2. Creates a professional email template with a clear deadline and specific questions
3. Returns a formatted email ready to be sent

Request Body:
```json
{
  "topic": "News topic headline",
  "name": "Dr. Expert Name",
  "institution": "University Name",
  "expertise": "Field of expertise",
  "notable_work": "Publications or achievements",
  "unique_perspective": "What makes their view valuable",
  "contact_method": "How to reach them",
  "suggested_questions": ["Question 1", "Question 2"],
  "contact_info": "expert.name@institution.edu"
}
```

Response format:
```json
{
  "email_templates": [
    {
      "expert_name": "Dr. Expert Name",
      "topic": "News topic headline",
      "subject": "Expert Commentary Request: News topic headline - Response Needed in 6 Hours",
      "greeting": "Dear Dr. Name,",
      "email_body": "Professional email body with questions and deadline...",
      "signature": "Best regards,\nEditor Name\nPosition, Organization\nemail@organization.com\n(123) 456-7890"
    }
  ]
}
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 