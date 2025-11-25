import os
from dotenv import load_dotenv
from google import genai

import sys
def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if len(sys.argv) < 2:
        print("i need a prompt")
        sys.exit(1)
    prompte = sys.argv[1]

    response = client.models.generate_content(model="gemini-2.0-flash", 
        contents=prompte
    )

    print(response.text)

    print(response.usage_metadata.prompt_token_count)
    print(response.usage_metadata.candidates_token_count)
    print(sys.argv)

main()
