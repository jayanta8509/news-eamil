import os
from dotenv import load_dotenv
import openai
import json
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please check your .env file.")

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

class EmailGenerator:
    def __init__(self):
        self.model = "gpt-4o-mini"  # Using GPT-4 for better email generation

    def generate_email(self, expert_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a personalized email template for an expert based on their information and topic
        
        Args:
            expert_data: Dictionary containing expert information (name, institution, topic, etc.)
            
        Returns:
            Dictionary with email template in the required format
        """
        try:
            # Construct prompt for email generation
            prompt = f"""
Using the information about this expert, create a personalized email template to request their commentary. Format your response as valid JSON.

Expert Information:
- Topic: {expert_data.get('topic', '')}
- Name: {expert_data.get('name', '')}
- Institution: {expert_data.get('institution', '')}
- Expertise: {expert_data.get('expertise', '')}
- Notable Work: {expert_data.get('notable_work', '')}
- Unique Perspective: {expert_data.get('unique_perspective', '')}
- Contact Method: {expert_data.get('contact_method', '')}
- Suggested Questions: {json.dumps(expert_data.get('suggested_questions', []))}
- Contact Info: {expert_data.get('contact_info', '')}

Craft a professional email with:
1. Clear subject line mentioning the news topic
2. Professional greeting with proper title and name
3. Concise introduction of purpose
4. Explanation of why their expertise is valuable
5. Clear 6-hour deadline
6. Their specialized questions
7. Requested format (brief, quotable paragraphs)
8. How their commentary will be used

Format your response in this JSON structure:
{{
  "email_templates": [
    {{
      "expert_name": "{expert_data.get('name', '')}",
      "topic": "{expert_data.get('topic', '')}",
      "subject": "Expert Commentary Request: [Topic] - Response Needed in 6 Hours",
      "greeting": "Dear [Title and Name],",
      "email_body": "Complete email body text here...",
      "signature": "Best regards, [Your Name] [Your Title] [Your Institution] [Your Contact Information]"
    }}
  ]
}}

Ensure the email is concise, professional, customized to the expert, and ready to send after review.

YOU MUST RETURN YOUR RESPONSE IN VALID JSON FORMAT ONLY.
            """

            # Get email template from OpenAI
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert email writer specializing in crafting professional outreach messages to academic experts for commentary requests."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000,
                response_format={"type": "json_object"}
            )

            # Parse the response
            email_template = json.loads(response.choices[0].message.content)
            
            return email_template

        except Exception as e:
            raise Exception(f"Error generating email template: {str(e)}")


def generate_expert_email(expert_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Helper function to generate an email template for an expert
    
    Args:
        expert_data: Dictionary containing expert information
        
    Returns:
        Dictionary with email template
    """
    email_generator = EmailGenerator()
    return email_generator.generate_email(expert_data)

