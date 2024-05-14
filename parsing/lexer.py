"""
Pattern 1: Lexer from "Language Implementation Patterns" by Terence Parr
"""


class Token:
    def __init__(self, type: str, text: str):
        self.type = type
        self.text = text

    def __repr__(self):
        return f"<'{self.text}','{self.type}'>"


class Lexer:
    """
    A Abstract Lexert class
    """

    def __init__(self, input: str):
        self.input = input

        # string with < > is the token and the string without < > is the token type
        self.T = {"<NA>": "NA", "<EOF>": "EOF"}  # token: type
        self.EOF = "<EOF>"
        self.EOF_TYPE = self.T["<EOF>"]
        self.p = 0  # Index into input of current character
        self.c = self.input[self.p] if self.input else self.EOF

    def consume(self):
        """Move one character, and consume it."""
        self.p += 1
        if self.p >= len(self.input):
            self.c = self.EOF
        else:
            self.c = self.input[self.p]

    def get_type(self, token):
        """get the token type from token name."""
        return self.T[token]

    def __next__(self):
        raise NotImplementedError


class ListLexer(Lexer):
    """
    A lexer for the list grammar:

    // START: lexer
    NAME     : LETTER+ ;                 // name is sequence of >=1 letter
    LETTER   : 'a'..'z'|'A'..'Z';        // define what a letter is
    WS       : (' '|'\t'|'\n'|'\r')+ {skip();} ; // throw out whitespace
    // END: lexer
    """

    def __init__(self, input: str):

        super().__init__(input)
        self.extra_T = {
            ",": "COMMA",
            "[": "LBRACK",
            "]": "RBRACK",
        }
        self.NAME = "NAME"
        self.COMMA = "COMMA"
        self.LBRACK = "LBRACK"
        self.RBRACK = "RBRACK"
        self.T.update(self.extra_T)

    def is_letter(self):
        return len(self.c) == 1 and self.c.isalpha()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            if self.c == self.EOF:
                raise StopIteration
            elif self.c in [" ", "\t", "\n", "\r"]:
                self.ws()
            elif self.c in self.extra_T:
                result = Token(self.get_type(self.c), self.c)
                self.consume()
                return result
            else:
                if self.is_letter():  # only chech first character
                    return self.name()
                raise ValueError(f"Invalid character: {self.c}")

    def name(self):
        buf = []
        buf.append(self.c)  # do while
        self.consume()
        while self.is_letter():
            buf.append(self.c)
            self.consume()
        return Token("NAME", "".join(buf))

    def ws(self):
        while self.c in [" ", "\t", "\n", "\r"]:
            self.consume()


class ListLexerWithEqual(ListLexer):
    def __init__(self, input: str):
        super().__init__(input)
        self.extra_T.update({"=": "EQUALS"})
        self.EQUALS = "EQUALS"
        self.T.update(self.extra_T)


if __name__ == "__main__":
    lexer = self.input("[a, b ,,]")
    for token in lexer:
        print(token)

    lexer_we = ListLexerWithEqual("[a, b=c]")
    for token in lexer_we:
        print(token)
