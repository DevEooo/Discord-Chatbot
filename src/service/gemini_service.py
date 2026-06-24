import os
from dotenv import load_dotenv
from google import genai
from src.utils.chunks import split_into_chunks

load_dotenv()
ai_client = genai.Client(api_key=os.getenv('llm_credential'))

async def get_response(prompt: str) -> list[str]:
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        return split_into_chunks(response.text)

    except Exception as e:
        print(f"An error occurred: {e}")
        return ["Apologies, there's an error processing to LLM."]