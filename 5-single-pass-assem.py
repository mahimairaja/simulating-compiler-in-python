from typing import List


class SinglePassAssembler :
    def __init__(self) -> None:
        self.start_addr : hex = None
        self.location_counter : hex = None # Used to track the size of program.
        
        self.program_name : str = ''
        self.program_size : hex = 0
        
        self.object_code : List[hex] = []
        
        self.text_record : str = ''
        self.text_size : hex = 0
        
    
    def assembleCode(self, ) -> str :
        '''
        Using the source code, optab and symtab generates the 
        object program code.
        '''
        sourceCode = self.readInput('input/5-single-pass-assem.txt')
        optTab = dict(self.readInput('input/5-op-tab.txt'))
        symTab = dict(self.readInput('input/5-sym-tab.txt'))
        
        for line in sourceCode :
            for idx, word in enumerate(line):
                if word == 'START' :
                    self.program_name : str = line[idx - 1]
                    self.start_addr : str = line[idx + 1]
                    int_start_add : int = int(self.start_addr, 16)
                    self.location_counter : hex = hex(int_start_add)[2:]
                elif word in list(optTab.keys()):
                    opt : str = str(optTab[word]).rjust(2,'0')
                elif word in list(symTab.keys()) :
                    if idx != 0 :
                        sym : str = str(symTab[word]).rjust(4, '0')
                        objCode : str = opt + sym
                        if objCode != '':
                            self.object_code.append(objCode)
            if 'START' not in line and 'END' not in line :
                int_num : int = int(self.location_counter, 16) + 3
                self.location_counter : hex = hex(int_num)[2:]

        self.program_size : int = int(self.location_counter, 16) - int(self.start_addr, 16)
        self.program_size : str = str(hex(self.program_size)[2:]).rjust(2, '0')
        
        self.text_size = hex(len(''.join(self.object_code))//2 )[2:]
        
        for code in self.object_code :
            self.text_record = self.text_record + '^' + code
        
        result =  f'''H^{self.program_name}^{self.start_addr}^{self.program_size}
T^{str(self.start_addr).rjust(6,'0')}^{str(self.text_size).rjust(2,'0')}{self.text_record}
E^{str(self.start_addr).rjust(6,'0')}'''

        self.writeOutput('output/5-single-pass-assem.txt', result)
        return result
        
    def readInput(self, filepath) -> List[str] :
        '''
        To read the data from a text file
        '''
        with open(filepath, 'r') as f :
            programLines : List[str] = f.readlines()
            programLines : List[str] = [line.replace('\n','').strip() for line in programLines]
            programLines : List[str] = [line.split() for line in programLines]
        return programLines
    
    def writeOutput(self, filepath, data) -> None :
        '''
        To write the output to a text file
        '''
        with open(filepath, 'w') as f :
            f.write(data)
        
assembler = SinglePassAssembler()
result : str = assembler.assembleCode()
print(result)