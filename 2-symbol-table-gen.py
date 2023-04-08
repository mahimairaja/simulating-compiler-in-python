# Symbol Table  
# id | datatype | input_value | return_type | arguments

# Generate symbol table for 
# Simple definitions and function calls

import pandas as pd
import re
from typing import List

class SymbolTable:
    def __init__(self, inputPath) -> None:
        self.data : dict = {'id' : [] ,
                    'datatype'   : [] ,
                    'input_value': [] ,
                    'return_type': [] , 
                    'arguments'  : [] }
        self.dataKeys : List[str] = list(self.data.keys())
        self.dataTypes : List[str] = ['string','char','int','float','short','long','double']
        self.currType : str = ''
        self.symTab : List[str] = ['null'] * 5
        self.souceCode : List[str] = self.readInput(inputPath)
    
    def readInput(self, filepath) -> List[str]:
        '''
        To read the input source program from a text file
        '''
        with open(filepath, 'r') as f:
            programLines : List[str] = f.readlines()
            programLines : List[str] = [line.replace('\n', '').strip() for line in programLines]
            programLines : List[str] = [line.split() for line in programLines]
        return programLines
    
    def generate(self,) -> dict:
        '''
        Actual Symbol Table generation
        '''
        for line in self.souceCode :
            self.symTab : List[str] = ['null'] * 5
            for idx, token in enumerate(line) :
                if token in self.dataTypes  : 
                    try :
                        if not (line[idx - 1] == '(' or line[idx - 1] == ','):
                            self.currType = self.symTab[1] = token
                            self.symTab[0] : str = line[idx + 1]
                    except IndentationError :
                        pass
                elif token == ',' :
                    if not line[idx + 1] in self.dataTypes :
                        for index in range(len(self.symTab)) :
                            self.data.get(self.dataKeys[index]).append(self.symTab[index])
                        self.symTab[0] = line[idx + 1]
                elif token == '=' :
                    value = line[idx + 1]
                    if self.currType == 'char' or self.currType == 'string' :
                        value : str = value[1 : -1]
                    self.symTab[2] : str = value
                elif token == '(' :
                    self.symTab[3] = self.currType
                    arguments = line[idx + 1 : line.index(')')]     
                    arguments = ''.join(arguments)
                    self.symTab[4] = arguments
                elif token == ')' :
                    self.symTab[1] = 'null'
            for index in range(len(self.symTab)) :
                self.data.get(self.dataKeys[index]).append(self.symTab[index])  
        return self.data
    
    def getSymbolTable(self,) -> pd.DataFrame:
        '''
        To get the symbol table as dataframe
        '''
        data : dict = self.generate()
        df : pd.DataFrame = pd.DataFrame(data)
        return df 
    
    def writeOutput(self, filepath : str) -> pd.DataFrame :
        '''
        To write the dataframe into a txt file
        '''
        with open(filepath, 'w') as f :
            dataframe = self.getSymbolTable()
            f.write(dataframe.to_string())
        return dataframe



if __name__ == '__main__':
    generator = SymbolTable('input/2-symbol-table.txt')
    result = generator.writeOutput('output/2-symbol-table.txt')

    print(result)

