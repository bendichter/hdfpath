import sys
import logging
import ply.lex
from jsonpath_ng.exceptions import JsonPathLexerError

logger = logging.getLogger(__name__)

class HDFPathLexer:
    '''
    A Lexical analyzer for HDFPath.
    '''

    def __init__(self, debug=False):
        self.debug = debug
        if self.__doc__ is None:
            raise JsonPathLexerError('Docstrings have been removed! By design of PLY, HDFPath requires docstrings. You must not use PYTHONOPTIMIZE=2 or python -OO.')

    def tokenize(self, string):
        '''
        Maps a string to an iterator over tokens. [char] -> [token]
        '''
        new_lexer = ply.lex.lex(module=self, debug=self.debug, errorlog=logger)
        new_lexer.latest_newline = 0
        new_lexer.input(string)

        while True:
            t = new_lexer.token()
            if t is None:
                break
            t.col = t.lexpos - new_lexer.latest_newline
            yield t

    # ============== PLY Lexer specification ==================

    literals = ['/', '$', '[', ']', '=', '@']

    tokens = ['SLASH', 'DOLLAR', 'LBRACKET', 'RBRACKET', 'EQUALS', 'ATTR', 'NUMBER', 'ID', 'STRING']

    t_ignore = ' \t'

    def t_SLASH(self, t):
        r'/'
        return t

    def t_DOLLAR(self, t):
        r'\$'
        return t

    def t_LBRACKET(self, t):
        r'\['
        return t

    def t_RBRACKET(self, t):
        r'\]'
        return t

    def t_EQUALS(self, t):
        r'=='
        return t

    def t_ATTR(self, t):
        r'\.attrs'
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r"'([^\\']+|\\.)+'"
        t.value = t.value[1:-1]  # Remove quotes
        return t

    def t_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        t.lexer.latest_newline = t.lexpos

    def t_error(self, t):
        raise JsonPathLexerError(f'Error on line {t.lexer.lineno}, col {t.lexpos - t.lexer.latest_newline}: Unexpected character: {t.value[0]}')

if __name__ == '__main__':
    logging.basicConfig()
    lexer = HDFPathLexer(debug=True)
    for token in lexer.tokenize(sys.stdin.read()):
        print(f'{token.value} ({token.type})')
