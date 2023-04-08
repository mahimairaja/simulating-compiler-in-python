# To catagorize the leximes under the below catagory.
# Keywords 
# Operators
# Identifier = (letter)(letter | digit)* 
# Constants  / Literals
# Punctuations / Separators

from typing import List 
import re

class Tokenizer :
    def __init__(self, filepath) -> None:
        self.programlines = self.readInput(filepath)
        
    def readInput(self, filepath : str) -> List[str]:
        '''
        To read the input source program from a text file
        '''
        with open(filepath, 'r') as f :
            programlines = f.readlines()
            programlines = [line.replace("\n", "").strip() for line in programlines]
            programlines = [line.split() for line in programlines]
            return programlines
    
    def start_scanning(self, outputFile) -> None :
        '''
        Scans and write the output to a file
        '''
        open(outputFile, 'w').truncate()
        for lines in self.programlines :
            for word in lines :
                token = self.scan(word)
                line = f'< {token[1]}, {token[0]} > \n' 
                self.writeOutput(filepath=outputFile, line=line)
    
    def scan(self, lex : str) -> bool:
        '''
        Actual scanning lexical analysis happens here         
        '''
        keywords : List[str] = ["main","int", "float", "double", "long", \
                "short", "string", "char", "if", "else", "while", \
                "do","break","continue"]
        operators : List[str] = ["+", "-","*","/","<",">","=","|","&"]
        punctuations : List[str] = ["{", "}","(",")",";","[","]",".","&"]
        identifers = r'\b[A-Za-z_][A-Za-z0-9_]*\b'
        constants = r'\b[0-9][0-9]*\b'
        if lex in keywords :
            return [lex , 'Keyword'] 
        elif lex in operators :
            return [lex , 'Operator'] 
        elif lex in punctuations :
            return [lex, 'Punctuation']
        elif re.findall(identifers, lex) :
            return [lex, 'Identifier']
        elif re.findall(constants, lex):
            return [lex, 'Constant']
    
    def writeOutput(self, filepath : str, line : str) -> None :
        '''
        To write the output to a file
        '''
        with open(filepath, 'a') as f :
            f.write(line)

if __name__ == '__main__' :
    scanner = Tokenizer(filepath='input/1-token-separation.txt')
    scanner.start_scanning('output/1-token-separation.txt')