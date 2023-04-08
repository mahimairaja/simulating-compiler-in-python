class DeterministicFiniteAutomata:
    def __init__(self, initial, final, dfa_table) -> None:
        self.initialQ : str = initial
        self.finalQ : set = final
        self.transTable : dict = dfa_table
    
    def verifyString(self, inputString) -> bool :
        '''
        Multiple transitions were caried on through 
        input string, till it reaches one of a final state
        '''
        currQ = self.initialQ 
        for symbol in inputString :
            try :
                print(currQ)
                currQ = self.transTable[currQ][symbol]
                print(f"{symbol} => {currQ}")
            except KeyError as e:
                print('Key error')
                return False 
        if currQ in self.finalQ :
            return True
        else :
            return False 


initial_state = 'q0'
final_states = {'q0'}
table = {'q0': {'0': 'q1', '1': 'q0'}, 
        'q1': {'0': 'q0', '1': 'q1'}}
machine = DeterministicFiniteAutomata(initial=initial_state,
                                    final= final_states,
                                    dfa_table=table)

# Sample string - 001 ( Belongs to the lang )
input_string = input("Enter a string - from {0, 1} :\n")
result = machine.verifyString(inputString=input_string)

if result :
    print(f'✅ The string "{input_string}" is a part of given language')
else :
    print('❌ String does not belong to the language')
    
'''
Sample input string - 001
'''