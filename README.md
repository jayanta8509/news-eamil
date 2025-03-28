# News Analysis API with Expert Recommendations

This FastAPI application provides three main services:
1. Analyzing news stories from specific categories to identify important topics
2. Finding academic experts for specific topics
3. Generating professional email templates to contact these experts

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

### POST /news/analysis/category

Analyzes news stories from a specific category and identifies the top 3 topics that would benefit from expert commentary.

Request Body:
```json
{
  "category": "sports news"
}
```

Example categories:
- "sports news"
- "business or finance news"
- "European news"
- "tabloid or sensational news"
- "legal news"

Response format:
```json
{
  "output": {
    "selected_topics": [
      {
        "topic_id": 1,
        "headline": "Topic headline",
        "summary": "2-3 sentence summary",
        "need_for_commentary": "Why this topic needs expert input",
        "expert_angles": ["Specific question 1", "Specific question 2"]
      }
    ],
    "analysis_timestamp": "2023-05-18 12:34:56.789012"
  },
  "status": "success", 
  "status_code": 200
}
```

### POST /news/experts/topic

Finds expert recommendations for a single specific topic without needing to fetch and analyze news first.

Request Body:
```json
{
  "topic_id": 1,
  "headline": "Duke back in Elite 8 behind Flagg's 30-point clinic",
  "summary": "Duke's Cooper Flagg delivered an impressive performance against Arizona...",
  "need_for_commentary": "This topic requires expert commentary to analyze...",
  "expert_angles": [
    "What are the long-term effects of standout performances on a player's draft stock?",
    "How do coaching strategies adapt to players with such exceptional skills?"
  ]
}
```

Response format:
```json
{
  "output": {
    "expert_recommendations": [
      {
        "topic_id": 1,
        "topic": "Duke back in Elite 8 behind Flagg's 30-point clinic",
        "experts": [
          {
            "name": "Dr. John Smith, Professor of Sports Science",
            "institution": "University of North Carolina",
            "expertise": "Athlete performance and sports psychology",
            "notable_work": "Published research on athlete performance under pressure",
            "unique_perspective": "Combines sports science with psychology to understand peak performance",
            "contact_method": "via university department",
            "suggested_questions": [
              "What are the key factors that contribute to an athlete's peak performance in critical games?",
              "How does the coaching strategy adapt in high-pressure situations like the Elite 8?"
            ],
            "contact_info": "john.smith@unc.edu"
          },
          // Additional experts...
        ]
      }
    ]
  },
  "status": "success",
  "status_code": 200
}
```

### POST /email/generate

Generates a personalized email template for requesting expert commentary.

Request Body:
```json
{
  "topic": "Trump's new executive order could upend voting",
  "name": "Dr. Richard Hasen",
  "institution": "University of California, Irvine",
  "expertise": "Election law and voter access",
  "notable_work": "Author of 'The Voting Wars' and commentator on election integrity",
  "unique_perspective": "Focuses on the legal and practical challenges of voting regulations",
  "contact_method": "via university department",
  "suggested_questions": [
    "How could this executive order affect voter turnout and access to the polls?",
    "What are the constitutional challenges that could arise from this order?"
  ],
  "contact_info": "richard.hasen@uci.edu"
}
```

Response format:
```json
{
  "email_templates": [
    {
      "expert_name": "Dr. Richard Hasen",
      "topic": "Trump's new executive order could upend voting",
      "subject": "Expert Commentary Request: Trump's New Executive Order Could Upend Voting - Response Needed in 6 Hours",
      "greeting": "Dear Dr. Hasen,",
      "email_body": "Professional email body with questions and deadline...",
      "signature": "Best regards,\nEditor Name\nPosition, Organization\nemail@organization.com\n(123) 456-7890"
    }
  ]
}
```

## Error Handling

All endpoints include robust error handling and will return formatted error responses rather than failing with HTTP errors. This makes error handling more predictable on the client side.

## Technology Stack

- FastAPI: API framework
- OpenAI API: For news analysis, expert recommendations, and email generation
- SerpAPI: For fetching news stories in specific categories 