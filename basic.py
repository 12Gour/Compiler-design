########################################################################
# Constant 
########################################################################

digits ='0123456789' 

########################################################################
# Error class
########################################################################

class Error:
    def __init__(self,error_name,details):
        self.error_name = error_name
        self.details = details
    def as_string(self):
        result = f'{self.error_name}:{self.details}'
        return result
class IllegalCharacter(Error):
    def __init__(self,details):
        super().__init__('Illegal Character',details)
        
        

########################################################################
# TOKENS
########################################################################

TT_INT = 'TT_INT'
TT_FLOAT = 'TT_FLOAT'
TT_PLUS = 'TT_PLUS'
TT_MINUS = 'TT_MINUS'
TT_MUL = 'TT_MUL'
TT_DIV = 'TT_DIV'

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
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None  

    def make_token(self):
        tokens = []

        while self.current_char != None:
            if self.current_char.isspace():  # seperate token for whitespace
                self.advance()
            elif self.current_char in digits:  
                tokens.append(self.make_number())
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
                char = self.current_char
                self.advance()
                return [], IllegalCharacter("'" + char + "'")

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
        

########################################################################
# RUN Method
########################################################################

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_token()
    return tokens,error