'''
Macro-Processor used to expand the macros on compile time 
Macros are expanded before compiling the source code 
'''

import re 
from typing import List
from warnings import filterwarnings
filterwarnings('ignore')

class MacroProcessor:
    def __init__(self, inputFile) -> None:
        self.sourceCode = self.readInput(inputFile)
        self.def_index : List[str] = []
        self.var_index : List[str] = []
    
    def execute(self, outputPath) :
        '''
        Responisible for overall processing
        '''
        self.expandVariable()
        self.expandFunction()
        self.removeDefinition()
        for line in self.sourceCode :
            print(' '.join(line))
        
        open('output/3-macro-processor.txt','w').truncate()
        for line in self.sourceCode :
            self.writeOutput(outputPath, ''.join(line) + '\n')
    
    
    def findVariable(self,) -> dict :
        '''
        Finds the macro definition and macro body and 
        returns the hash map with definition and body
        '''
        pattern : re.Pattern = re.compile(r'#\sdefine\s+(\w+)\s+([0-9].[0-9]*)')
        variable_map : dict = {}
        for idx, line in enumerate(self.sourceCode) :
            str_line : str = ' '.join(line)
            if pattern.search(str_line) != None :
                pattern_match = pattern.search(str_line)
                identifier : str = pattern_match.group(1)
                constant : str = pattern_match.group(2)
                variable_map[identifier] : str = constant
                self.var_index.append(idx)
        return variable_map
    
    def expandVariable(self, ) -> None :
        '''
        Expands the macro call using the retrived hash map
        '''
        variable_map : dict = self.findVariable()
        variable_names : List[str] = list(variable_map.keys())
        for name in variable_names :
            for idx, line in enumerate(self.sourceCode) :
                if  name in line and '#' not in line :
                    self.sourceCode[idx] : List[str] = [variable_map[name] if word == name \
                                            else word for word in line]
    
    def findFunction(self, ) -> int :
        '''
        Finds the macro function definition and macro body and 
        returns the definition name, definition parameter, definiton expansion
        '''
        def_pattern : re.Pattern = re.compile(r'#\sdefine\s+(\w+)\s+\((.*)\)\s+{(.*)}')
        function_names : List[str] = []
        function_parameters : List[str] = []
        function_expansion : List[str] = []
        
        for idx, line in enumerate(self.sourceCode) :
            str_line : str = ' '.join(line)
            if def_pattern.search(str_line) != None :
                pattern_match : re.Match  = def_pattern.search(str_line) 
                
                fun_name : str = pattern_match.group(1)
                function_names.append(fun_name)
                
                fun_para : List[str] = [args.strip() for args in pattern_match.group(2).split(',')]
                function_parameters.append(fun_para)
                
                fun_expan : str = pattern_match.group(3)
                function_expansion.append(fun_expan)
                
                self.def_index.append(idx)
        return function_names, function_parameters, function_expansion
    
    def mapFunction(self) -> dict:
        '''
        Using the retrived defintion generates a hash map
        '''
        function_names, function_parameters, function_expansion = self.findFunction()
        count : int = 0
        variable_map : dict = {}
        result : dict = {}
        try :
            for idx, line in enumerate(self.sourceCode) :
                str_line : str = ' '.join(line)
                def_pattern : re.Pattern = re.compile(r'{}\s\(\s([\w\s,]+)\s\)\s;'.format(function_names[count]))
                if def_pattern.search(str_line) != None :
                    pattern_match : re.Match = def_pattern.search(str_line)
                    params : List[str] = pattern_match.group(1).split(',')
                    params : List[str] = [arg.strip() for arg in params]
                    variable_map[function_names[count]] = dict(zip(function_parameters[count], params))
                    
                    call_expansion = self.replaceArgument(variable_map, function_names, function_expansion, count)
                    
                    result[function_names[count]] = call_expansion
                    count += 1
        except Exception as e :
            pass
        return result
    
    def replaceArgument(self,variable_map, function_names, function_expansion, count) -> str :
        '''
        Using the mapping hash map and macro definion body it 
        replaces the actual parameters.
        '''
        call_expansion : str = ''.join(variable_map[function_names[count]][char] \
                    if char in variable_map[function_names[count]] \
                    else char for char in function_expansion[count])
        return call_expansion.strip()
    
    def expandFunction(self, )-> None :
        '''
        The macro definition with replaced paramters is then 
        replaced in the palce of macro call 
        '''
        functions : dict = self.mapFunction()
        function_keys : List[str] = list(functions.keys())
        for term in function_keys :
            for idx, line in enumerate(self.sourceCode) :
                if term in line and '#' not in line :
                    self.sourceCode[idx] : List[str] = functions[term]
    
    def removeDefinition(self) -> None:
        '''
        To remove the macro defintion statement
        '''
        self.sourceCode : List[str] =  [self.sourceCode[i] for i in range(len(self.sourceCode)) if i not in self.var_index]
        self.sourceCode : List[str] =  [self.sourceCode[i] for i in range(len(self.sourceCode)) if i not in self.def_index]
    
    def readInput(self, filePath) -> List[str] :
        '''
        To read a input of c/c++ code from a text file
        '''
        with open(filePath, 'r') as f :
            programLines : List[str] = f.readlines()
            programLines : List[str] = [line.replace('\n','').strip() for line in programLines]
            programLines : List[str] = [line.split() for line in programLines]
        return programLines
    
    def writeOutput(self, path, data) -> None :
        '''
        Writes the expanded code to a text file.
        '''
        with open(path, 'a') as f :
            f.write(data)

processor = MacroProcessor('input/3-macro-processor.txt')
processor.execute('output/3-macro-processor.txt')
