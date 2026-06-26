from pathlib import Path
from termSearching import term_searching

#looping through all files and writing the output in a new file
def main():
    with open('output for RACISM.txt', 'w', encoding="utf-8") as outfile:
        for file in Path('data').glob('*.txt'):
            result= term_searching(file)
            outfile.write(result)
    outfile.close()

main()

