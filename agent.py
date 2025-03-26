import os
from dotenv import load_dotenv
import openai
from typing import List, Dict
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please check your .env file.")

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

class NewsAnalyzer:
    def __init__(self):
        self.model = "gpt-4o-mini"  # Using GPT-4 for better analysis

    def analyze_news(self, news_data: List[Dict]) -> Dict:
        """
        Analyze news stories and select top 3 topics for expert commentary
        """
        try:
            # Extract news stories from the input data
            news_stories = news_data[0]["output"]["news_stories"]
            
            # Prepare the prompt for OpenAI
            prompt = f"""
            Based on the news stories JSON provided, select the top 3 news topics that would most benefit from academic expert commentary for media outlets.

            If news stories are available, your task is to:

            1. Evaluate each news story using these criteria:
               - Complexity (requires expert knowledge to fully understand)
               - Public interest (generates significant questions or concerns)
               - Timeliness (relevant to current discourse)
               - Impact (affects many people or has significant consequences)
               - Controversy (involves multiple perspectives or interpretations)

            2. Select exactly 3 news topics that best meet these criteria

            3. Format your response as a valid JSON with the following structure:
            {{
              "selected_topics": [
                {{
                  "topic_id": 1,
                  "headline": "Topic headline",
                  "summary": "2-3 sentence summary",
                  "need_for_commentary": "Why this topic needs expert input",
                  "expert_angles": ["Specific question 1", "Specific question 2"]
                }}
              ]
            }}

            4. Prioritize topics that are:
               - Complex enough to require expert interpretation
               - Current and timely (happening within the past 24 hours)
               - Likely to remain relevant for at least the next few days
               - Of interest to multiple media outlets

            5. Avoid selecting topics that:
               - Are primarily opinion-based with little factual substance
               - Are too specialized for general media interest
               - Have already been extensively covered by experts
               - Are politically divisive without substantive policy elements

            6. Add a topic_id field to each topic (1, 2, 3)

            News Stories:
            {json.dumps(news_stories, indent=2)}

            YOU MUST RETURN YOUR RESPONSE IN VALID JSON FORMAT ONLY.
            """

            # Get analysis from OpenAI
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert news analyst specializing in identifying topics that would benefit from academic expert commentary."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=5000,
                response_format={"type": "json_object"}
            )

            # Parse the response
            analysis = json.loads(response.choices[0].message.content)
            
            return analysis

        except Exception as e:
            raise Exception(f"Error analyzing news: {str(e)}")

def analyze_news_stories(news_data: List[Dict]) -> Dict:
    """
    Main function to analyze news stories and get expert commentary recommendations
    """
    analyzer = NewsAnalyzer()
    analysis = analyzer.analyze_news(news_data)
    
    # Add timestamp
    analysis["analysis_timestamp"] = str(datetime.now())
    
    return analysis

if __name__ == "__main__":
    # Example usage
    from app import fetch_news_data
    
    async def test_analysis():
        # Fetch news data
        news_data = await fetch_news_data()
        
        # Analyze the news
        analysis = analyze_news_stories(news_data)
        
        # Print results
        print(json.dumps(analysis, indent=2))

    import asyncio
    asyncio.run(test_analysis()) 