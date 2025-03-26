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

class ExpertFinder:
    def __init__(self):
        self.model = "gpt-4o"  # Using GPT-4 for better expert recommendations

    def find_experts(self, news_analysis: Dict) -> Dict:
        """
        Find expert recommendations for each news topic identified
        """
        try:
            # Prepare the prompt for OpenAI
            prompt = f"""
            For each of the 3 news topics previously identified in the JSON, identify 3 specific academic experts who would be ideal candidates to provide valuable commentary. Format your response as valid JSON.

            For each topic in the input JSON's selected_topics array, find exactly 3 experts who meet these criteria:
            - Have demonstrated expertise directly relevant to the specific news topic
            - Hold academic credentials or research positions at universities or research institutions
            - Have published work, given interviews, or made public statements on similar issues
            - Represent diverse perspectives and institutions

            Return your response in this JSON structure:
            {{
              "expert_recommendations": [
                {{
                  "topic_id": 1,
                  "topic": "EXACT headline from the input topic",
                  "experts": [
                    {{
                      "name": "Full name and title",
                      "institution": "Current academic institution",
                      "expertise": "Specific area and relevance to the topic",
                      "notable_work": "Brief mention of relevant work or appearances",
                      "unique_perspective": "What specific angle they bring to the topic",
                      "contact_method": "Preferred contact method (e.g., 'via university department')",
                      "suggested_questions": ["Question 1", "Question 2"],
                      "contact_info": "Expert's email in format firstname.lastname@institution.edu"
                    }},
                    // Expert 2 structure (same fields)
                    // Expert 3 structure (same fields)
                  ]
                }}
                // Additional topics follow the same structure
              ]
            }}

            CRITICAL INSTRUCTIONS:
            1. Use EXACT headlines from the input topics
            2. For each expert, draw questions from the topic's expert_angles when available
            3. Ensure expert perspectives are diverse and relevant
            4. For contact_info, generate a realistic academic email address based on the expert's name and institution
            5. Add topic_id field to each topic
            6. Focus on real experts with verifiable credentials and relevant expertise
            7. Ensure the final output is valid, parseable JSON

            Input JSON:
            {json.dumps(news_analysis, indent=2)}

            YOU MUST RETURN YOUR RESPONSE IN VALID JSON FORMAT ONLY.
            """

            # Get expert recommendations from OpenAI
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert researcher specializing in identifying academic experts for news commentary."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=5000,
                response_format={"type": "json_object"}
            )

            # Parse the response
            experts_data = json.loads(response.choices[0].message.content)
            
            return experts_data

        except Exception as e:
            raise Exception(f"Error finding experts: {str(e)}")

def find_experts_for_topics(news_analysis: Dict) -> Dict:
    """
    Main function to find expert recommendations for news topics
    """
    finder = ExpertFinder()
    experts_data = finder.find_experts(news_analysis)
    
    # Format for the required output structure
    formatted_output = {
        "output": experts_data
    }
    
    return formatted_output

if __name__ == "__main__":
    # Example usage
    from agent import analyze_news_stories
    from app import fetch_news_data
    
    async def test_expert_finder():
        # Fetch news data
        news_data = await fetch_news_data()
        
        # Analyze the news
        news_analysis = analyze_news_stories(news_data)
        
        # Find experts for the analyzed topics
        experts_data = find_experts_for_topics(news_analysis)
        
        # Print results
        print(json.dumps([experts_data], indent=2))

    import asyncio
    asyncio.run(test_expert_finder()) 