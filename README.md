# News Analysis API with Expert Recommendations

This FastAPI application provides four main services:
1. Fetching the top news stories from the last 24 hours
2. Analyzing news stories from specific categories to identify important topics
3. Finding academic experts for specific topics
4. Generating professional email templates to contact these experts

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

### GET /news/top

Fetches and analyzes the top 3 general news stories from the last 24 hours. This endpoint provides a simple way to get analyzed topics ready for expert commentary without needing to specify a category.

Response format:
```json
{
  "output": {
    "selected_topics": [
      {
        "topic_id": 1,
        "headline": "Prince Harry wins tabloid legal battle",
        "summary": "The Duke of Sussex achieved a significant legal victory against British tabloids, resulting in public apologies and financial compensation. This event highlights ongoing issues of privacy and media ethics.",
        "need_for_commentary": "This topic needs expert input to analyze the implications of this legal battle on media practices and the rights of public figures.",
        "expert_angles": [
          "What does this case signify about the evolving relationship between celebrities and the media?",
          "How might this ruling influence future media regulations and journalistic ethics?"
        ]
      },
      {
        "topic_id": 2,
        "headline": "Effects of Tabloid on Information Processing and Evaluative Responses",
        "summary": "A recent study investigates how the presentation of tabloid news affects viewer engagement and response. This research sheds light on the broader implications of media consumption.",
        "need_for_commentary": "Expert analysis is essential to contextualize these findings within the current media landscape and their effects on public perception.",
        "expert_angles": [
          "How do tabloid formats impact audience understanding of important news events?",
          "What are the potential long-term effects of tabloid journalism on public discourse?"
        ]
      },
      {
        "topic_id": 3,
        "headline": "Tabloid Journalism and Its Global Impact",
        "summary": "The rise of tabloid journalism represents a shift in how news is consumed worldwide, often prioritizing sensationalism over factual reporting. This trend raises questions about media responsibility.",
        "need_for_commentary": "This topic requires expert insights to discuss the implications of sensationalist journalism on democracy and informed citizenship.",
        "expert_angles": [
          "What are the societal consequences of the shift towards sensationalism in journalism?",
          "How can consumers critically engage with tabloid news to mitigate misinformation?"
        ]
      }
    ],
    "analysis_timestamp": "2025-04-01 14:26:06.316866"
  },
  "status": "success",
  "status_code": 200
}
```

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
- "showbiz world" (celebrities, music, Hollywood)
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

### POST /format-simple-email

A simplified endpoint that formats a basic email with minimal input requirements.

Request Body:
```json
{
  "subject": "Trump's Executive Order on Voting Requirements",
  "body": "The executive order regarding proof of citizenship for voter registration raises serious constitutional questions. The 24th Amendment prohibits poll taxes in federal elections, and courts have generally viewed documentation requirements that impose costs on voters as potentially unconstitutional barriers. Additionally, the National Voter Registration Act established specific procedures for voter registration that may conflict with this order. States maintain primary authority over voting procedures, creating a complex federalism issue.",
  "name": "Dr. Richard Hasen"
}
```

This endpoint requires only three fields:
- `subject`: The email subject line
- `body`: The raw content to be formatted (include all necessary information here)
- `name`: The name of the expert

The API will automatically analyze the body content and extract any information about media outlets, editors, etc. if present. Everything needed for formatting should be included in the body field.

Response format:
```json
{
  "formatted_email": {
    "subject": "Trump's Executive Order on Voting Requirements",
    "greeting": "Dear Editor,",
    "introduction": "I am pleased to share expert commentary from Dr. Richard Hasen regarding the recent executive order on voting requirements. His analysis provides valuable insights into the constitutional implications of this policy change.",
    "formatted_body": "\"The executive order regarding proof of citizenship for voter registration raises serious constitutional questions,\" explains Dr. Hasen. \"The 24th Amendment prohibits poll taxes in federal elections, and courts have generally viewed documentation requirements that impose costs on voters as potentially unconstitutional barriers.\"\n\n\"Additionally, the National Voter Registration Act established specific procedures for voter registration that may conflict with this order,\" Dr. Hasen notes. \"States maintain primary authority over voting procedures, creating a complex federalism issue.\"",
    "closing": "Best regards,\nNews Analysis Team\ncontact@newsanalysis.com"
  },
  "word_count": 102,
  "key_points": [
    "Constitutional concerns regarding the 24th Amendment",
    "Potential conflicts with the National Voter Registration Act",
    "Federalism issues with state vs. federal authority"
  ],
  "status": "success",
  "status_code": 200
}
```

This endpoint takes raw content and formats it into a professional email with proper attribution, quotations, and structure.

## Error Handling

All endpoints include robust error handling and will return formatted error responses rather than failing with HTTP errors. This makes error handling more predictable on the client side.

## Technology Stack

- FastAPI: API framework
- OpenAI API: For news analysis, expert recommendations, and email generation
- SerpAPI: For fetching news stories in specific categories 