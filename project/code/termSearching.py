import re
from colorama import Fore, Style

def term_searching(file):
    #opening a file
    with open(file, 'r', encoding='utf-8') as f:
        text= f.read()

    # splitting file into lines
    lines = text.split('.')

    #getting a term from input
    #term=input(f"Enter the term you want to search for in {file}: ")

    #or directly
    term = r"ρατσισμός"
    pattern = r'ρατσισ.*\b'

    #initialize an empty list to be returned and saved in the output file
    results = []

    #dictionary with frequencies
    freqdict = {}

    # searching for term and returning the line it was found in (ONLY IN THE TERMINAL)
    for i, line in enumerate(lines):
        try:
            if re.search(pattern, line, re.IGNORECASE):
                print('\n', i, line)
                freqdict[pattern] = freqdict.get(pattern, 0) + 1

        #handling exceptions
        except KeyError:
            statement = f'Term not found in {file}'
            print(statement)
            
    #printing how many times the term was found
    dict_result= (Fore.GREEN + f"\n\n\tTerm '{term}' found {freqdict[pattern]} times in {file}" + Style.RESET_ALL)
    print(dict_result)
    results.append(dict_result)


    # closing file
    f.close()

    return "\n".join(results)


#term_searching('data/1989.txt')
