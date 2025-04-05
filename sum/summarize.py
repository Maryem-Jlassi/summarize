import json
import requests
from typing import Optional

BASE_API_URL = "http://127.0.0.1:7860"  # Update if your API URL differs
FLOW_ID = "9960bfb7-b5ea-443b-8e4e-244837962554"
ENDPOINT = ""  # Set endpoint name here if applicable

# Optional tweaks for the flow
TWEAKS = {
    "ChatInput-7OjqK": {},
    "ChatOutput-fAR1p": {},
    "Prompt-g4Jw9": {},
    "OllamaModel-rqdCY": {}
}

def run_flow(
    message: str,
    endpoint: str = ENDPOINT or FLOW_ID,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    api_key: Optional[str] = None
) -> dict:
    """
    Sends a message to the LangFlow API and retrieves the response.

    :param message: Input message for the flow
    :param endpoint: Flow endpoint or ID
    :param output_type: Type of the output (default is "chat")
    :param input_type: Type of the input (default is "chat")
    :param tweaks: Optional tweaks to customize the flow
    :param api_key: API key for authentication (if required)
    :return: Response from the LangFlow API as a dictionary
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    if tweaks:
        payload["tweaks"] = tweaks

    headers = {"x-api-key": api_key} if api_key else None

    response = requests.post(api_url, json=payload, headers=headers)

    # Check if the response is successful
    if response.status_code != 200:
        raise RuntimeError(f"Error {response.status_code}: {response.text}")

    return response.json()

# Example usage
if __name__ == "__main__":  # Corrected name check
    message = "This is a document about the human brain of a patient. Summarize and explain."
    try:
        response = run_flow(message=message)
        print("Response from LangFlow:")
        print(json.dumps(response, indent=2))
    except Exception as e:
        print(f"An error occurred: {e}")


result = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "")
print("Processed Output:", result)
