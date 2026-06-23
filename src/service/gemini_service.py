import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
llmCreds = os.getenv('llm_credential')

ai_client = genai.Client(api_key=llmCreds)

async def get_response(prompt: str) -> list[str]:
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        answer = response.text
        
        # Chunking the response is necessary here, since discord has a response limit to 2.000 chars. if the limit reached, HTTP 400 Bad Request (Error Code: 50035) error would happen.
        chunk_size = 1900
        
        return [answer[i:i+chunk_size] for i in range(0, len(answer), chunk_size)]

    except Exception as e:
        print(f"An error occurred: {e}")
        return ["Apologies, there's an error processing to LLM."]