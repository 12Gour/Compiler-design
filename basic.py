########################################################################
# Constant 
########################################################################

digits ='0123456789' 
variables = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

########################################################################
# Error class
########################################################################

class Error:
    def __init__(self, pos_start, pos_end , error_name,details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    def as_string(self):
        result = f'{self.error_name}:{self.details}'
        result += f'line {self.pos_start.ln + 1}'
        return result
class IllegalCharacter(Error):
    def __init__(self,pos_start, pos_end ,details):
        super().__init__(pos_start, pos_end ,'Illegal Character',details)
        


#######################################################################
# POSITION
#######################################################################

class Position():
    def __init__(self, idx, ln, col):
        self.idx = idx
        self.ln = ln
        self.col = col
    


    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col += 0 
        
        return self
    

    def copy (self):
        return Position(self.idx, self.ln, self.col)

########################################################################
# TOKENS
########################################################################

TT_INT = 'TT_INT'
TT_FLOAT = 'TT_FLOAT'
TT_PLUS = 'TT_PLUS'
TT_MINUS = 'TT_MINUS'
TT_MUL = 'TT_MUL'
TT_DIV = 'TT_DIV'
TT_VAR = 'TT_VAR'



class Token:
    def __init__(self,type, value = None):
        self.type = type
        self.value = value
    
    # Representation of a token
    def __repr__(self):   
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

################################################################
# LEXER Class methods
################################################################

class Lexer:
    def __init__(self,text):
        self.text = text
        self.pos = Position(-1, 0, -1)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None  

    def make_token(self):
        tokens = []

        while self.current_char != None:
            if self.current_char.isspace(): 
                 self.advance()
            elif self.current_char in digits:  
                tokens.append(self.make_number())
            elif self.current_char in variables :
                tokens.append(self.make_variables())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            else:
                # return error message
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharacter(pos_start, self.pos, "'" + char + "'")

        return tokens, None
    
    # checking integer / floating point values
    def make_number(self):      
        num_str = ''
        dot_count = 0 

        while self.current_char != None and self.current_char in digits + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT,int(num_str))
        else:
            return Token(TT_FLOAT,float(num_str))
        
    # Identify characters
    def make_variables(self):
        variables_str = ''
        while self.current_char != None and self.current_char in variables :
            variables_str += self.current_char
            self.advance()   
        return Token(TT_VAR, str(variables_str))


########################################################################
# RUN Method
########################################################################
 
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_token()
    return tokens,error