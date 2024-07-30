import requests, json, os, getpass, time
import requests.adapters

from concurrent.futures import ThreadPoolExecutor



from configuration import *


# Declare global variables
access_token = ''
THREAD_POOL = 2

# In order to download multiple module definitions, multiple HTTP requests have to be sent in paraller
# and connections should be reused in order to be more efficient with resources.
# To achieve this, I am using the solution from user5994461:
# https://stackoverflow.com/questions/2632520/what-is-the-fastest-way-to-send-100-000-http-requests-in-python
session = requests.Session()
session.mount('https://', requests.adapters.HTTPAdapter(pool_maxsize=THREAD_POOL,
                                                        max_retries=3,
                                                        pool_block=True))


def create_payload_for_access_token() -> dict:
    '''
    Create the payload that will be used as the body of the request sent to the Authentication URL.
    '''

    # Initialize the payload...
    payload = {}
    
    if GRANT_TYPE == PASSWORD: # ... for password grant type
        payload['grant_type'] = PASSWORD
        payload['username'] = input('Enter your Unqork username/email: ')
        payload['password'] = getpass.getpass('Enter your Unqork password: ')

    elif GRANT_TYPE == CLIENT_CREDENTIALS: # ... for client credentials grant type
        payload['grant_type'] = CLIENT_CREDENTIALS

    return payload


def get_access_token() -> str:
    '''
    Get the access token from the authentication URL.

    This function uses the grant type and proxies, if any, to return a String token.

    If 'password' grant type is used, the user will be prompted for the username and password.
    '''

    # Create the headers
    headers = {
        'Content-Type': 'application/json',
    }

    # Create the payload
    payload = create_payload_for_access_token()

    # Send the request
    response = requests.request("POST", AUTHENTICATION_URL, proxies=PROXIES, headers=headers, data=json.dumps(payload))
    
    # Raise an exception if the status code is not '200'
    response.raise_for_status()

    # Extract the access token
    json_access_token = json.loads(response.content.decode())
    return json_access_token['access_token']


def get_list_of_application_module_names_and_ids() -> dict:
    '''
    This method sends a request for the application module names and corresponding module ids.

    The method returns a dictionary with the following keys:
        'name': module name
        'id': module id
    '''

    # Create the headers
    headers = { 'Authorization': f"Bearer {access_token}" }

    # Send the request
    response = requests.request('GET', APPLICATION_MODULES_URL, proxies=PROXIES, headers=headers)

    # Raise an exception if the status code is not '200'
    response.raise_for_status()

    # Return the modules
    modules = json.loads(response.content.decode())
    return modules


def create_folder_directory(folder_path: str) -> None:
    '''
    This method creates a folder in thee specified path, if it does not exist.
    '''

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f'Created folder: {folder_path}')


def write_modules_to_a_text_file(modules: list) -> None:
    '''
    This method reads a list of module objects, 
    extracts the values of 'name' and 'id' keys from each object,
    and writes these values to a text file.

    This module will also create a folder SEARCH_OUTPUT_FOLDER_PATH, if it does not exist.
    The name of the text file can be updated by changing LIST_OF_MODULES_FILENAME_OUTPUT in the configuration.
    '''

    # Create directory for storing search results, if it does not exist
    create_folder_directory(SEARCH_OUTPUT_FOLDER_PATH)

    with open(f'./{SEARCH_OUTPUT_FOLDER_PATH}/{LIST_OF_MODULES_FILENAME_OUTPUT}', 'w') as f:
        for module in modules:
            f.write(module['name'] + '\n')
            f.write(module['id'] + '\n\n')


def download_module_definitions(modules: list) -> None:
    '''
    This method accepts a list of module objects.
    It will send a request to MODULE_DEF_BASE_URL for each module object, using the 'id' parameter.
    It will store each module definition response in its own separate json file.

    This module will also create a folder '{MODULE_DEFINITIONS_OUTPUT_PATH}_{APPLICATION_ID}', if it does not exist.

    Parameters:
    modules: list of module objects, each containing a value for the 'id' key.
    '''

    # Create directory for storing module definitions, if it does not exist
    folder_path = f'{MODULE_DEFINITIONS_OUTPUT_PATH}_{APPLICATION_ID}'
    create_folder_directory(folder_path)

    # Download each module definition
    with ThreadPoolExecutor(max_workers=THREAD_POOL) as executor:

        # list() will force the program to wait for all requests to complete
        for response in list(executor.map(download_module_definition, modules)):
            if response.status_code == 200:
                response_payload = json.loads(response.content.decode())
                module_id = response_payload['_id']
                module_name = response_payload['name']
                module_components = response_payload['components']

                with open(f'{folder_path}/{module_name}_{module_id}.json', 'w') as f:
                    json.dump(module_components, f, indent=4)

                print(f'Successfully downloaded the module definition for: {module_name}')


def download_module_definition(module: dict) -> requests.Response:
    '''
    This method sends an HTTP GET request to MODULE_DEF_BASE_URL using the 'id' key of the provided module dictionary.
    It returns the Response object.

    Parameters:
    module: a single module object containing a value for the 'id' key.
    '''

    # Create the headers
    headers = { 'Authorization': f'Bearer {access_token}' }

    # Create the module URL
    module_url = f'{MODULE_DEF_BASE_URL}/{module["id"]}'

    # Send the request
    response = session.get(module_url, proxies=PROXIES, headers=headers)

    # Handle non-OK '200' responses
    if response.status_code != 200:
        print(f'Failed to get a successfull response from: {module_url}')
    
    # The server is overloaded? Give it a break
    if 500 <= response.status_code < 600:
        time.sleep(5)

    return response


def main():
    '''
    This method runs when the file is run.
    '''
    
    # Get the access token
    global access_token
    access_token = get_access_token()
    print('Successfully retrieved access token.')

    # Get the list of all module names and module ids
    print(f'Getting the list of module names and ids for application with id: {APPLICATION_ID}...')
    modules = get_list_of_application_module_names_and_ids()
    print(f'Successfully retrieved information for {len(modules)} modules.')

    # Write the list of modules to a text file
    write_modules_to_a_text_file(modules)
    
    # Download the module definition for each module
    download_module_definitions(modules)


if __name__ == '__main__':
    main()