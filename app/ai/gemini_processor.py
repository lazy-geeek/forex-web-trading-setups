import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()

openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.getenv("OPENROUTER_API_KEY")

PROMPT_TEMPLATE = """Analyze this trading setup text:
{text}

Extract structured JSON with:
- entry_price (number)
- stop_loss (number)
- take_profit (number)
- risk_reward_ratio (number)
- confidence_score (1-5)"""


def process_setups(raw_data):
    processed_setups = []
    for item in raw_data:
        prompt = PROMPT_TEMPLATE.format(text=item["content"])
        try:
            response = openai.ChatCompletion.create(
                model="google/gemini-pro",
                messages=[
                    {"role": "user", "content": prompt},
                ],
                headers={
                    "HTTP-Referer": "http://localhost:5000",  # Replace with your actual app URL
                    "X-Title": "Forex Setup Finder",
                },
            )
            try:
                print(
                    "Debug: Gemini API raw response:",
                    response.choices[0].message.content,
                )
                parsed_response = json.loads(response.choices[0].message.content)
                print("Debug: Parsed JSON response:", parsed_response)
                parsed_response["site"] = item["site"]  # Add the site information
                processed_setups.append(parsed_response)
            except json.JSONDecodeError as e:
                print(
                    "Error decoding JSON from Gemini response:",
                    response.choices[0].message.content,
                    "Exception:",
                    e,
                )
                continue

        except Exception as e:
            print(f"Error processing with Gemini: {e}")
            continue
    return processed_setups
