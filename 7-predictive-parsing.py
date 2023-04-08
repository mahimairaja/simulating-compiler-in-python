'''
Recursive Descent Parser :
Parse the string recursively with the help of parsing table, stack, 
input and the action you perform according to stack and input. 
'''

from typing import List

class PredictiveParser:
    def __init__(self, parsingTable : dict) -> None:
        self.parsing_table : dict = parsingTable
        self.startingSymbol_ : str = list(parsingTable.keys())[0]
        self.stack : List[str] = ['$', self.startingSymbol_]
        self.input : List[str] = ['$']
    
    def parseString(self, input_string : str):
        '''
        Syntax of the input string is verified by recursive parsing
        '''
        self.input : List[str] = self.input + input_string.split('.')
        open('output/7-predictive-parsing.txt', 'w').truncate()
        while True :
            curr_stack : str = ''.join(self.stack)
            curr_input : str = ''.join(self.input)
            print(f"{curr_stack :<10} {curr_input}")
            with open('output/7-predictive-parsing.txt', 'a') as f :
                f.write(f"{curr_stack :<10} {curr_input}\n")
            try :
                if self.input == ['$'] and self.stack == ['$'] :
                    # Accepting state
                    return True 
                elif self.input[-1] == self.stack[-1]:
                    # Cancelling condition
                    self.input.pop()
                    self.stack.pop()
                elif self.parsing_table[self.stack[-1]][self.input[-1]] == 'e':
                    # Epsilon condition
                    self.stack.pop()
                else :
                    # Non-Terminal in stack expands
                    exp : str = self.parsing_table[self.stack[-1]][self.input[-1]]
                    self.stack.pop()
                    self.stack = self.stack + exp.split('.')[::-1]
            except Exception as e:
                print(e)
                # Empty cell or error condition
                return False
            
Table ={'E' : {'id' : 'T.A', '(' : 'T.A',},
        'A' : {'+'  : '+.T.A', ')': 'e', '$' : 'e'},
        'T' : {'id' : 'F.B', '(' : 'B'},
        'B' : {'+'  : 'e' ,  '*': '*.F.B', ')':'e', '$':'e'},
        'F' : {'id' : 'id',  '(': '(.E.)'} 
        }

with open('input/7-predictive-parsing.txt', 'r') as f:
    inputString = f.read()

parser = PredictiveParser(parsingTable= Table)
result = parser.parseString(input_string=inputString)

string = inputString.replace('.','')
if result :
    print(f'✅ The string "{string}" parsed successfully')
else :
    print('❌ String failed to parse')