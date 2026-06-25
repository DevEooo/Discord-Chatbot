import os
from dotenv import load_dotenv
from google import genai 
from src.utils.chunks import split_into_chunks

load_dotenv()

base_directory = os.path.dirname(os.path.abspath(__file__))
prompt_path = os.path.join(base_directory, "prompts", "prompt.txt")

try:
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt_instruction = file.read().strip()
except FileNotFoundError:
    print("Prompt.txt is missing.")
    
ai_client = genai.Client(api_key=os.getenv('llm_credential'))

async def get_response(contents: list) -> list[str]:
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=genai.types.GenerateContentConfig(
                system_instruction = prompt_instruction
            )
        )
        
        return split_into_chunks(response.text)

    except Exception as e:
        print(f"An error occurred: {e}")
        return ["Apologies, there's an error processing to LLM."]