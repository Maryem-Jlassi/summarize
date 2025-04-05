import json
import requests
import warnings
from typing import Optional

try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

BASE_API_URL = "http://127.0.0.1:7860"  # Update if your API URL differs
FLOW_ID = "ad43a4f8-0617-48db-b716-0d046524f2bb"
ENDPOINT = ""  # Set endpoint name here if applicable

# Optional tweaks for the flow
TWEAKS = {
    "Prompt-f6IVu": {},
    "ChatInput-MZjeQ": {},
    "ChatOutput-pRNwH": {},
    "Prompt-HekJ4": {},
    "TavilyAISearch-KFmOe": {},
    "Agent-BJmFC": {},
    "Prompt-yE8qm": {},
    "Prompt-7iw6U": {},
    "OllamaModel-yVGGF": {},
    "OllamaModel-g2Nmk": {}
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

def upload_file_to_flow(file_path: str, components: list, tweaks: Optional[dict] = None) -> dict:
    """
    Uploads a file to the LangFlow API.

    :param file_path: Path to the file to upload
    :param components: List of components to upload the file to
    :param tweaks: Optional tweaks to customize the flow
    :return: Updated tweaks dictionary
    """
    if not upload_file:
        raise ImportError("Langflow is not installed. Please install it to use the upload_file function.")

    return upload_file(
        file_path=file_path,
        host=BASE_API_URL,
        flow_id=ENDPOINT or FLOW_ID,
        components=components,
        tweaks=tweaks
    )

# Example usage
if __name__ == "__main__":
    message = "This is a document about the human brain of a patient. Summarize and explain."
    try:
        tweaks = TWEAKS
        # Uncomment the lines below to use file upload functionality
        # file_path = "path_to_your_file"
        # components = ["your_component_name"]
        # tweaks = upload_file_to_flow(file_path, components, tweaks)

        response = run_flow(message=message, tweaks=tweaks)
        print("Response from LangFlow:")
        print(json.dumps(response, indent=2))

        # Extract and print processed output
        result = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "")
        print("Processed Output:", result)
    except Exception as e:
        print(f"An error occurred: {e}")
