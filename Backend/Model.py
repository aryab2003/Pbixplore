from google import genai
import json

client = genai.Client(api_key="AIzaSyCPg_1DVkfpX6QLcVaoFJENOQyF3zRlKEQ")

def process_json_data(json_data):
    """
    Function to process JSON data using the Google GenAI API.
    """
    try:
        # Convert JSON data to a string
        json_data_str = json.dumps(json_data, indent=4)

        # Generate content using the GenAI API
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=(
                "Provide suggestions regarding optimisation, which columns must be used, "
                "which columns can be ignored, GUI improvement, and how to speed up only based on json provided: \n" + json_data_str
            )
        )

        # Print the response from the API
        print("API Response:")
        print(response.text)

        # Optionally, return the response for further use
        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")