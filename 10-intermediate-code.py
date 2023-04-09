'''
Intermediate code generation - To convert the source
program into three address code format 
To the right side :
    Operator  |  Arg_1  | Arg_2
'''

import re
from typing import List

class IntermediateCodeGenerator :
    def __init__(self, filepath) -> None:
        self.stack : List[str] = []
        self.opertors : List[str] = ['+','-','*','/']
        self.user_input : str = self.readInput(filepath)
        self.statement : List[str] = re.split('([+-/*])', self.user_input)
        self.temp_count : int = 1
        
    def codeGenerator(self) -> bool:
        '''
        It splits the program into 3 elements each and iterate
        till every part gets converted to three address code.
        '''
        while len(self.statement) > 1 :
            self.compare()
            if len(self.statement) == 1 :
                self.displayOutput(filepath='output/10-inter-code.txt',)
                return True
        if len(self.statement) != 1 :
            return False
        
    def readInput(self, filepath) -> str :
        '''
        To read the input source program from a text file.
        '''
        with open(filepath, 'r') as f :
            data = f.read()
            return data
        
    def compare(self, ) -> None:
        '''
        It splits the statement to each 3 element and
        adds to an stack
        '''
        for word in self.statement :
            if word in self.opertors :
                self.stack.append(''.join(self.statement[:3]))
                self.statement.pop(0)
                self.statement.pop(0)
                self.statement[0] = 't' + str(self.temp_count)
                self.temp_count += 1
                
    def displayOutput(self, filepath)-> None :
        '''
        To print the result in console
        '''
        k_times : int = 1
        open(filepath, 'w').truncate()
        for no_of_times in range(len(self.stack)) :
            print('t'+str(k_times)+' = '+self.stack[no_of_times])
            self.writeOutput(filepath, 't'+str(k_times)+' = '+self.stack[no_of_times]+'\n')
            k_times += 1
    
    def writeOutput(self,filepath, data) -> None :
        '''
        To write the three address to a files
        '''
        with open(filepath, 'a') as f:
            f.write(data)


generator = IntermediateCodeGenerator('input/10-inter-code.txt')
result = generator.codeGenerator()

if result :
    print(f"\n✅Three address code for {generator.user_input} has genearated successfully ✅")
else :
    print(f'❌Unable to process the your input : {generator.user_input}')