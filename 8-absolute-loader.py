from typing import List
import re

class AbsoluteLoader :
    def __init__(self, filepath : str) -> None:
        self.sourceCode_ : List[str] = self.readInput(filepath)
    
    def readInput(self, path : str) -> List[str]:
        '''
        To read the input object program of a 
        assembler from a text file
        '''
        with open(path,'r') as f:
            programcode = f.readlines()
            programcode = [x.replace('\n','').strip() for x in programcode]
            programcode = [x.split('^') for x in programcode]
        return programcode
    
    def loadProgram(self, progName) -> bool:
        '''
        Extracts the program address and maps with each single
        byte of data in a sequence according to address pair.
        '''
        output_path = 'output/8-abs-loader.txt'
        if self.sourceCode_[0][1] != progName :
            return False
        open('output/8-abs-loader.txt', 'w').truncate()
        for idx, record in enumerate(self.sourceCode_):
            if record[0] == 'T' :
                for jdx, word in enumerate(record):
                    hex_pattern = re.compile(r'^[A-Fa-f0-9]{2}$')
                    if re.search(hex_pattern, word) :
                        start_address = record[jdx - 1]
                        curr_address = int(start_address)
                        objectCode = record[jdx+1 : ]
                objectCodeStack = ''.join(objectCode)
                objectCodeStack = re.findall('..', objectCodeStack) # Splits into object program to each single byte
                for code in objectCodeStack:
                    print(f'{curr_address:06d} {code}')
                    self.writeOutput(output_path, f'{curr_address:06d} {code}\n')
                    curr_address = curr_address + 1
        return True
    
    def writeOutput(self, filepath, content)-> None :
        '''
        Writes the loaded program to a text file.
        '''
        with open(filepath, 'a') as f :
            f.write(content)

loader = AbsoluteLoader(filepath='input/8-abs-loader.txt')

program_name = input("Enter the program name : \n")
loaded = loader.loadProgram(program_name)

if loaded is True : 
    print("✅ Absolute loader loaded the assembler program Successfully")
else :
    print('❌ The entered program name is invalid')