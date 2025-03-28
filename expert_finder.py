import os
from dotenv import load_dotenv
import openai
from typing import List, Dict
import json
from datetime import datetime
import traceback  # Add for detailed error tracing

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
        self.model = "gpt-4o-mini"  # Using a more available model

    def find_experts_for_topic(self, topic: Dict) -> Dict:
        """
        Find expert recommendations for a single news topic
        """
        try:
            # print(f"Finding experts for topic: {topic.get('headline', 'Unknown Topic')}")
            # print(f"Using OpenAI model: {self.model}")
            # print(f"OpenAI API key is {'set' if openai.api_key else 'NOT SET'}")
            
            # Check if OpenAI API key is valid
            if not openai.api_key or len(openai.api_key) < 10:
                raise ValueError("OpenAI API key is missing or invalid. Please check your .env file.")
                
            # Prepare the prompt for OpenAI
            prompt = f"""
            For the following news topic, identify 3 specific academic experts who would be ideal candidates to provide valuable commentary. Format your response as valid JSON.

            Find exactly 3 experts who meet these criteria:
            - Have demonstrated expertise directly relevant to the specific news topic
            - Hold academic credentials or research positions at universities or research institutions
            - Have published work, given interviews, or made public statements on similar issues
            - Represent diverse perspectives and institutions

            Return your response in this JSON structure:
            {{
              "expert_recommendations": [
                {{
                  "topic_id": {topic.get("topic_id", 1)},
                  "topic": "{topic.get("headline", "")}",
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
              ]
            }}

            CRITICAL INSTRUCTIONS:
            1. Use the EXACT headline from the input topic
            2. For each expert, draw questions from the topic's expert_angles when available
            3. Ensure expert perspectives are diverse and relevant
            4. For contact_info, generate a realistic academic email address based on the expert's name and institution
            5. Focus on real experts with verifiable credentials and relevant expertise
            6. Ensure the final output is valid, parseable JSON

            Input topic:
            {json.dumps(topic, indent=2)}

            YOU MUST RETURN YOUR RESPONSE IN VALID JSON FORMAT ONLY.
            """

            # Get expert recommendations from OpenAI
            print("Sending request to OpenAI API...")
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
            print("Received response from OpenAI API.")

            # Parse the response
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response received from OpenAI API")
                
            print("Parsing JSON response...")
            experts_data = json.loads(content)
            print("Successfully parsed JSON response.")
            
            # Validate the output structure
            if "expert_recommendations" not in experts_data:
                print("Warning: expert_recommendations field missing from OpenAI response.")
                # Create a default structure if the expected structure is missing
                experts_data = {
                    "expert_recommendations": [
                        {
                            "topic_id": topic.get("topic_id", 1),
                            "topic": topic.get("headline", ""),
                            "experts": []
                        }
                    ]
                }
            
            return experts_data

        except openai.error.AuthenticationError as e:
            error_msg = "OpenAI API authentication error. Please check your API key."
            print(f"ERROR: {error_msg}")
            print(f"Original error: {str(e)}")
            return {
                "error": True,
                "expert_recommendations": [
                    {
                        "topic_id": topic.get("topic_id", 1),
                        "topic": topic.get("headline", ""),
                        "experts": [
                            {
                                "name": "API Authentication Error",
                                "institution": "Please check your OpenAI API key",
                                "expertise": error_msg,
                                "notable_work": "N/A",
                                "unique_perspective": "N/A",
                                "contact_method": "N/A",
                                "suggested_questions": [],
                                "contact_info": "support@example.com"
                            }
                        ]
                    }
                ]
            }
            
        except openai.error.RateLimitError as e:
            error_msg = "OpenAI API rate limit exceeded. Please try again later."
            print(f"ERROR: {error_msg}")
            print(f"Original error: {str(e)}")
            return {
                "error": True,
                "expert_recommendations": [
                    {
                        "topic_id": topic.get("topic_id", 1),
                        "topic": topic.get("headline", ""),
                        "experts": [
                            {
                                "name": "API Rate Limit Error",
                                "institution": "Please try again later",
                                "expertise": error_msg,
                                "notable_work": "N/A",
                                "unique_perspective": "N/A",
                                "contact_method": "N/A",
                                "suggested_questions": [],
                                "contact_info": "support@example.com"
                            }
                        ]
                    }
                ]
            }
            
        except Exception as e:
            # Get detailed error info
            error_type = type(e).__name__
            stack_trace = traceback.format_exc()
            error_msg = f"{error_type}: {str(e)}"
            
            # Log the error with full details
            print(f"ERROR finding experts for topic: {error_msg}")
            print(f"Stack trace: {stack_trace}")
            
            # Return a valid fallback response
            return {
                "error": True,
                "expert_recommendations": [
                    {
                        "topic_id": topic.get("topic_id", 1),
                        "topic": topic.get("headline", ""),
                        "experts": [
                            {
                                "name": "Error fetching experts",
                                "institution": "Please try again later",
                                "expertise": f"API error: {error_msg}",
                                "notable_work": "N/A",
                                "unique_perspective": "N/A",
                                "contact_method": "N/A",
                                "suggested_questions": [],
                                "contact_info": "support@example.com"
                            }
                        ]
                    }
                ]
            }

def find_experts_for_single_topic(topic: Dict) -> Dict:
    """
    Function to find expert recommendations for a single topic
    """
    try:
        print(f"Initiating expert finder for topic: {topic.get('headline', 'Unknown')}")
        finder = ExpertFinder()
        experts_data = finder.find_experts_for_topic(topic)
        
        if not experts_data:
            raise ValueError("No expert data was returned")
            
        # Check if there was an error
        if experts_data.get("error", False):
            print("Error flag found in experts_data")
            return experts_data
            
        return experts_data
    except Exception as e:
        stack_trace = traceback.format_exc()
        print(f"ERROR in find_experts_for_single_topic: {str(e)}")
        print(f"Stack trace: {stack_trace}")
        # Return a fallback response
        return {
            "error": True,
            "expert_recommendations": [
                {
                    "topic_id": topic.get("topic_id", 1),
                    "topic": topic.get("headline", ""),
                    "experts": [
                        {
                            "name": "Error fetching experts",
                            "institution": "Please try again later",
                            "expertise": f"Function error: {str(e)}",
                            "notable_work": "N/A",
                            "unique_perspective": "N/A",
                            "contact_method": "N/A",
                            "suggested_questions": [],
                            "contact_info": "support@example.com"
                        }
                    ]
                }
            ]
        }

if __name__ == "__main__":
    # Example usage
    from agent import analyze_news_stories
    from app import fetch_news_data
    
    async def test_expert_finder():
        # Fetch news data
        news_data = await fetch_news_data()
        
        # Analyze the news
        news_analysis = analyze_news_stories(news_data)

    import asyncio
    asyncio.run(test_expert_finder()) 