from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import json
import requests
import base64

load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv('AZURE_OPENAI_API_KEY')

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_APIM_ENDPOINT"),
    api_key=os.getenv("AZURE_APIM_API_KEY"),
    api_version="2023-12-01-preview",
)

VALID_REGIONS = {"west-us", "east-us"}

def validate_bgpas_number(number):
    return len(number) == 5 and number.isdigit()

def validate_region(region):
    return region.lower() in VALID_REGIONS

def get_user_input(prompt, validation_func):
    user_input = input(prompt) or "Y"
    while not validation_func(user_input):
        print("Invalid input.")
        user_input = input(prompt) or "Y"
    return user_input

def convert_to_json(data):
    return json.dumps(data)

def send_to_azure_devops_api(json_data):
    # Add your code here to send the JSON data to the Azure DevOps API
    pass

def main():
    completion = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
    )
    print(completion.choices[0].message.content.strip())

    # Get user ID from user input
    user_id = get_user_input("Enter your User ID: ", lambda x: True)
    print(f"You entered User ID: {user_id}")

    # Validate BGPAS Number
    bgpas_number = get_user_input("Enter your BGPAS Number (5 numeric digits): ", validate_bgpas_number)
    if not validate_bgpas_number(bgpas_number):
        print("Invalid BGPAS Number. It should be 5 numeric digits.")
        return

    # Validate Region
    region = get_user_input("Enter your Region (east-us or west-us): ", validate_region)
    if not validate_region(region):
        print("Invalid Region. It should be either 'east-us' or 'west-us'.")
        return

    # Summary of inputs
    print(f"Summary of your inputs:\nUser ID: {user_id}\nBGPAS Number: {bgpas_number}\nRegion: {region}")
    confirmation = get_user_input("Confirm? (Y/n): ", lambda x: x.lower() in {"y", "n", ""})
    if confirmation.lower() == "n":
        print("Aborted by user.")
        return
    # Convert inputs to JSON
    data = {
        "User ID": user_id,
        "BGPAS Number": bgpas_number,
        "Region": region
    }
    json_data = convert_to_json(data)
    print(f"JSON data to be sent to Azure DevOps API: {json_data}")

    # Send the JSON data to the Azure DevOps API
    send_to_azure_devops_api(json_data)


def send_to_azure_devops_api(json_data):
    organization = "contoso-jml"
    project = "vidbot-teams"
    type = "task"  # or whatever type of work item you want to create
    
    url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/${type}?api-version=6.0"
    pat = os.getenv("AZURE_DEVOPS_PERSONAL_ACCESS_TOKEN")
    headers = {
        "Content-Type": "application/json-patch+json",
        "Authorization": "Basic " + base64.b64encode((":{}".format(pat)).encode()).decode()
    }

    # Format the data for the Azure DevOps API
    data = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "from": None,
            "value": "Vidbot Test Task"
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": json_data
        }
    ]

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Data successfully sent to Azure DevOps API.")
    else:
        print(f"Failed to send data to Azure DevOps API. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
