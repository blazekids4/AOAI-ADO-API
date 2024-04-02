# README.md

## Introduction

This Python script is designed to interact with the Azure OpenAI API and Azure DevOps API. 
It serves as a bridge between the user and these APIs, allowing the user to input data via the command line, which is then validated and sent to the Azure DevOps API. 
The script leverages the power of the Azure OpenAI API to generate chat completions, providing a user-friendly interface for data input and manipulation.

## Prerequisites

Before running this script, ensure you have the following:

1. Python: The script is written in Python. Ensure you have Python 3.9 or later installed on your machine. You can download Python from the official website.

2. Required Python Libraries: This script uses several Python libraries such as dotenv for loading environment variables, requests for making HTTP requests, connecting to the LLM via Azure OpenAI, and json for handling JSON data. You can install these libraries using pip:

    ```cli
    pip install python-dotenv requests openai
    ```

3. Azure OpenAI API Key: You need an API key from Azure OpenAI to interact with the chat model. You can obtain this key from the Azure portal.

4. Azure DevOps Personal Access Token (PAT): To send data to the Azure DevOps API, you need a Personal Access Token. You can create one in the Azure DevOps portal.

5. .env File: This script loads environment variables from a .env file. Ensure you have this file in the same directory as your script. The file should contain your Azure OpenAI API key and Azure DevOps PAT:

    ```.env
    AZURE_OPENAI_API_KEY=your_openai_api_key
    AZURE_DEVOPS_PAT=your_azure_devops_pat
    ```

6. Azure DevOps Organization and Project: The script sends data to a specific Azure DevOps organization and project. Ensure you have the name of your organization and project.

Once you have all the prerequisites in place, you can proceed to set up and run the script.

## Setup

The script uses the dotenv module to load environment variables from a .env file. This file should be located in the same directory as your script. The environment variables include:

- AZURE_OPENAI_API_KEY: Your Azure OpenAI API key. This is used to authenticate your requests to the Azure OpenAI API.
- AZURE_DEVOPS_PAT: Your Azure DevOps Personal Access Token. This is used to authenticate your requests to the Azure DevOps API.

Here's a sample .env file:

```python
from dotenv import load_dotenv
load_dotenv()
```
Replace your_openai_api_key and your_azure_devops_pat with your actual keys.

## OpenAI Client Initialization

The script initializes an AzureOpenAI client with the Azure endpoint, API key, and API version.

```python
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_APIM_ENDPOINT"),
    api_key=os.getenvAZURE_APIM_API_KEY"),
    api_version="2023-12-01-preview",
)
```

## Input Validation

The script includes two validation functions: validate_bgpas_number and validate_region.

validate_bgpas_number checks if a number is exactly 5 digits long and consists only of digits.

```python
def validate_bgpas_number(number):
    return len(number) == 5 and number.isdigit()
```

validate_region checks if a region is either "west-us" or "east-us".

```python
VALID_REGIONS = {"west-us", "east-us"}

def validate_region(region):
    return region.lower() in VALID_REGIONS
```

## Sending Data to Azure DevOps API

The send_to_azure_devops_api function is responsible for sending the user input data to the Azure DevOps API. 
This function takes the JSON data as an argument.

```python
def send_to_azure_devops_api(json_data):
    # Code here
```

The function first sets up the necessary variables for the API request. 
This includes the organization, project, and type of work item to be created. 
The URL for the API request is constructed using these variables.

```python
organization = "contoso-jml"
project = "vidbot-teams"
type = "task"  # or whatever type of work item you want to create

url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/${type}?api-version=6.0"
```

Next, the function retrieves the Azure DevOps Personal Access Token (PAT) from the environment variables and sets up the headers for the API request. 
The PAT is encoded in base64 format and included in the Authorization header.

```python
pat = os.getenv("AZURE_DEVOPS_PERSONAL_ACCESS_TOKEN")
headers = {
    "Content-Type": "application/json-patch+json",
    "Authorization": "Basic " + base64.b64encode((":{}".format(pat)).encode()).decode()
}
```

The function then formats the data for the Azure DevOps API. 
The data is structured as a list of dictionaries, each representing an operation to be performed on the work item.

```python
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
```

Finally, the function sends a POST request to the Azure DevOps API with the URL, headers, and data. 
It checks the status code of the response to determine whether the request was successful.

```python
response = requests.post(url, headers=headers, json=data)
if response.status_code == 200:
    print("Data successfully sent to Azure DevOps API.")
else:
    print(f"Failed to send data to Azure DevOps API. Status code: {response.status_code}")
```

## Main Function

The main function is the entry point of the script. It first creates a chat completion with the OpenAI API and prints the response.

```python
completion = client.chat.completions.create(
    model="gpt-35-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
print(completion.choices[0].message.content.strip())
```

The function then prompts the user for their User ID, BGPAS Number, and Region, and validates the inputs. 
If the inputs are valid, the function asks the user to confirm. 
If the user confirms, the function converts the inputs to JSON and sends the JSON data to the Azure DevOps API using the send_to_azure_devops_api function.

```python
# Code for getting and validating user input here

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
```

The main function is called when the script is run as a standalone program.

```python
if __name__ == "__main__":
    main()
```

## Running the Script

To run the script, navigate to the directory containing the script in your terminal and run the following command:

```cli
python script_name.py
```

Replace script_name.py with the actual name of your script.

The script will prompt you for your User ID, BGPAS Number, and Region.

Enter these values when prompted.

## Results in Azure DevOps
![image](https://github.com/blazekids4/AOAI-ADO-API/assets/45666337/a988730d-0fd7-4f37-bd4e-a5736fd5f121)


## Error Handling

The script includes basic error handling. If an error occurs while sending data to the Azure DevOps API, the script will print an error message with the status code of the response.
If the status code is not 200, this means that the request was not successful. Check the Azure DevOps API documentation for more information on what each status code means.

Additionally, the script validates the user input for the BGPAS Number and Region.
If the input is not valid, the script will print an error message and prompt the user to enter the information again.

## Conclusion

This script provides a basic example of how to interact with the Azure OpenAI API and Azure DevOps API. 

After running the script, you can check your Azure DevOps project to see the new work item that was created.

If you want to extend the script, you could add more fields to the work item, such as the Assigned To field or the Priority field. 

You could also modify the script to interact with other APIs, or to perform different operations on the Azure DevOps API, such as updating or deleting work items.

## Reference Documentation

- Azure DevOps Services REST API Reference:  https://learn.microsoft.com/en-us/rest/api/azure/devops/?view=azure-devops-rest-7.2
  
- Work Items/Create:  https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/create?view=azure-devops-rest-7.1&tabs=HTTP

