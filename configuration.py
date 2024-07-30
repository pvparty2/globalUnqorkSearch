# REFERENCE: https://developers.unqork.io/

# Subdomain - For example, if your subdomain is xyzfinancial, you would use the prefix https://xyzfinancial.unqork.io/api/1.0
SUBDOMAIN = 'your-domain-here'

# Base URL
BASE_URL = f'https://{SUBDOMAIN}.unqork.io/api/1.0' # Do not modify

# Password or client credentials
PASSWORD = 'password' # Do not modify
CLIENT_CREDENTIALS = 'client_credentials' # Do not modify

# The grant type can only be 1 of the following: ['password', 'client_credentials']
# I have never used client credentials. This option is not implemented. 
# In order to implement client credential option, please edit create_payload_for_access_token().
GRANT_TYPE = PASSWORD

# Authentication URL - In order to utilize any of the API resources, you must first retrieve an access token by POSTing your credentials to the access token URL
AUTHENTICATION_URL = f'{BASE_URL}/oauth2/access_token' # Do not modify

# Proxies - Leave these parameters empty strings if proxies should not be used.
HTTP_PROXY = ''
HTTPS_PROXY = ''
PROXIES = {'http': HTTP_PROXY, 'https': HTTPS_PROXY, } # Do not modify

# Application ID
APPLICATION_ID = 'your-application-id-here'
APPLICATION_MODULES_URL = f'https://{SUBDOMAIN}.unqork.io/api/1.0/applications/{APPLICATION_ID}/modules' # Do not modify

# Module Definition Base URL - If your module id is 66a66666a6aa6a6666a66666, then your final URL endpoint is https://{SUBDOMAIN}.unqork.io/fbu/form/66a66666a6aa6a6666a66666
MODULE_DEF_BASE_URL = 'https://{SUBDOMAIN}.unqork.io/fbu/form/' # Do not modify

# Output
LIST_OF_MODULES_FILENAME_OUTPUT = 'list_of_modules.txt'
SEARCH_OUTPUT_FOLDER_PATH = 'searchResults'
MODULE_DEFINITIONS_OUTPUT_PATH = f'{SEARCH_OUTPUT_FOLDER_PATH}/moduleDefinitions'