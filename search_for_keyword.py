import json, re, os

from configuration import *

'''The recursive solution to search JSON files was obtained from https://stackoverflow.com/questions/73168515/find-nested-json-path-with-key-using-python

The original method used below to search a JSON object for a value:
def get_paths(source, key="", target = None):
    if isinstance(source, dict):
        for source_key, source_value in source.items():
            tmp_key = f"{key}.{source_key}" if key else source_key
            if source_key == target:
                yield tmp_key, source_value, source.get('_type')
            else:
                yield from get_paths(source_value, tmp_key, target)
    elif isinstance(source, (list, tuple, set, frozenset)):
        for index, value in enumerate(source):
            yield from get_paths(value, f"{key}[{index}]", target)'''


# Discard any matching value whose character length is over 10000.
# Why? Because sometimes people test large data objects by placing them in default values of hidden components
# and then forgetting to remove them.
VALUE_CUTOFF = 10000

# The directory to all the module definitions.
BASE_DIR = f'{MODULE_DEFINITIONS_OUTPUT_PATH}_{APPLICATION_ID}'

# Regex for 'components', a common reoccuring keyword in module definitions.
# This is used to build the path for a value.
# The "component" key in the Json object will be replaced with the actual component name when building out the path to a keyword/keyphrase.
re_components = re.compile('components$')


def get_paths(source: dict, path="", target=None, exact=False):
    '''
    This method searches a dictionary object (i.e., Json) for all occurrences of a specified target keyword/keyphrase.
    It yields a list of (path, value) pairs.
    The path is the location in the source where the value was found.
    The value is the actual value stored at the end of that path.

    Parameters:
    source - dictionary object that contains key-value pairs, i.e. Json object.
    path - the prefix to every path.
    target - the keyword/keyphrase value to search the source object for.
    exact - specifies whether the search should be a partial or exact match.
    '''

    if isinstance(source, dict):
        if re_components.search(path):
            path = re.sub('components$', source['key'], path)
        elif 'key' in source:
            path = f'{path}->{source["key"]}'

        for source_key, source_value in source.items():
            temp_path = f"{path}->{source_key}" if path else source_key
            if isinstance(source_value, str):
                if exact and target == source_value:
                    source_value = source_value[:VALUE_CUTOFF] if len(source_value) > VALUE_CUTOFF else source_value
                    yield temp_path, source_value
                elif not exact and target in source_value:
                    source_value = source_value[:VALUE_CUTOFF] if len(source_value) > VALUE_CUTOFF else source_value
                    yield temp_path, source_value
            else:
                yield from get_paths(source_value, temp_path, target, exact)
    elif isinstance(source, (list, tuple, set, frozenset)):
        for index, value in enumerate(source):
            yield from get_paths(value, f"{path}", target, exact)


def get_unique_locations(locations: list) -> list:
    '''
    This method combines paths that are the same across multiple module definitions.

    For example, when a module inherits another module, 
    the parent module will have a path to a keyword that is the same as the path found in the child module.
    '''

    unique_locations = []
    for location in locations:

        if len(location[1]) >= VALUE_CUTOFF:
            continue

        path = location[0]
        matched = False

        for i, u_location in enumerate(unique_locations):
            u_path = u_location[0]
            if u_path in path:
                matched = True
                u_location[2] += location[2] # Append the filename
                break
            elif path in u_path:
                matched = True
                location[2] += u_location[2] # Append the filename
                unique_locations[i] = location
                break
        
        if matched:
            continue
        
        unique_locations.append(location)

    return unique_locations

def print_prettily(locations: list):
    '''
    Print path, key, and filenames from each location.
    '''
    for location in locations:

        print('-' * 100)
        print(location[0] + '\n')
        print(location[1] + '\n')
        for filename in location[2]:
            print(filename)



def main():
    '''
    This method runs when the file is run.
    '''

    locations = []

    for filename in os.listdir(BASE_DIR):
        if os.stat(f'{BASE_DIR}/{filename}').st_size == 0:
            continue

        with open(f'{BASE_DIR}/{filename}', 'r') as f:
            json_data = json.loads(f.read())
            
            paths = get_paths(json_data, path="", target='dynamicGrid', exact=False) # Enter your target keyword/keyphrase to search by. If you want an exact search, set exact to True.
            for path in paths:
                location = []
                location.append(path[0])
                location.append(path[1])
                location.append([filename])
                locations.append(location)

    unique_locations = get_unique_locations(locations)
    print_prettily(unique_locations)


if __name__ == '__main__':
    main()