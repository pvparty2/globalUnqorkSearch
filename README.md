Background:
Unqork provides no efficient option to search for a keyword or keyphrase within all of the modules in an application.

The local search option, which is displayed on the right-hand side when a module is open, only searches component by component ids. It does not search for keyphrases used inside the components. For example, let's say I have a Data Workflow component called "dwfCool", and inside this component I have multiple operators: inputs, outputs, gateways, tables, operations, formulas, deicisions, etc.. Each operator can potentially have references to components located elsewhere in the module or even in other modules. The local search option will not be able to search for these occurrences.

The other search option offered by Unqork requires administrator access. This search option is called "Config Search", and it is located at: Settings > UDLC Toolkit > Build and Test > Config Search. The description for this search option states, "Request a search of your module definitions". When the user selects, "Use Tool", they are redirected to an intake form. The description on this intake form states that, "Once you have submitted this form, the request will be sent to the Data Analytics team and you will receive a report specifying exactly where in each module the text was found." The wait time? I do not know as I never tried this option.

Regardless, a search that takes any longer than a few seconds is inefficient. This solution attempts to replicate the "Config Search" option. This solution "allows you to search for any value within your module's configuration. The text could be things such as property names, labels, e-mails or URLs but also just about anything else you can think of." And it provides you a result in a few seconds.


Overview:
This solution will download module definitions for each module in an application. It will store each module definition as a Json file. (This download portion of the solution is a separate runnable that only has to be run once. In the future, as you edit your modules in Unqork, you might wish to re-download the module definitions so that your searches are accurate.) Then the solution will search a user's input value in each stored Json module definition. If there is a match, the solution will output (to the console): the path to the value, the matching value, and the name of the Json file (i.e., module name) where that value was found.


Getting Started:
This program is made up of 2 runnable and 1 configuration Python files.

The user should first update the configuration file by providing values for:
  - SUBDOMAIN
  - GRANT_TYPE (currently supports 'password' grant type. For 'client credentials', please feel free to implement the solution.)
  - HTTP_PROXY
  - HTTPS_PROXY
  - APPLICATION_ID

The rest of the configuration parameters can be left at their default values.

Steps:
1. Update configuration.py. See Getting Started section above.
2. The first runnable that should be executed is: download_all_module_definitions.py. This will download all module definitions in the specified application. As mentioned in the Overview section, this only has to be run once.
3. The second runnable is: search_for_keyword.py. Specify the value you wish to search for by modifying the 'target' argument of the get_paths(json_data, path="", target='your-search-value-here', exact=False) function in the main() method. If you want an exact match, change the 'exact' argument to True.
4. The program will output the search results to the console. See Overview section.

Errors:
You might run into some runtime issues. The biggest issue would be decoding a module definition that has some characters that are not utf-8 encoded. You can choose to remove, replace, or handle these characters.

