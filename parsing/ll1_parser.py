from __future__ import annotations
from parsing.lexer import ListLexerWithEqual, Token, ListLexer, Lexer


class Parser:
    def __init__(self, input: Lexer):
        self.input = input  # 从词法分析器获取词法单元
        self.consume()  # 初始化 lookahead

    def match(self, type: str):
        """如果 lookahead 词法单元类型匹配 x，则消耗；否则报错。"""
        if self.lookahead.type == type:
            self.consume()
        else:
            raise ValueError(
                f"Expecting type: {type}; found {self.lookahead} with type {self.lookahead.type}"
            )

    def consume(self):
        """前进到下一个词法单元。"""
        try:
            self.lookahead = next(self.input)
        except StopIteration:
            self.lookahead = Token(self.input.EOF_TYPE, self.input.EOF)


class ListParser(Parser):
    def __init__(self, input: ListLexer):
        super().__init__(input)

    def list(self):
        """list : '[' elements ']' ; // match bracketed list"""
        self.match(self.input.LBRACK)
        self.elements()
        self.match(self.input.RBRACK)

    def elements(self):
        """elements : element (',' element)* ;"""
        self.element()
        while self.lookahead.type == self.input.COMMA:
            self.match(self.input.COMMA)
            self.element()

    def element(self):
        """element : name | list ; // element is name or nested list"""
        if self.lookahead.type == self.input.NAME:
            self.match(self.input.NAME)
        elif self.lookahead.type == self.input.LBRACK:
            self.list()
        else:
            raise ValueError(f"Expecting name or list; found {self.lookahead}")


class ListParserWithEqual(ListParser):
    def element(self):
        if self.lookahead.type == self.input.NAME:
            self.match(self.input.NAME)
            if self.lookahead.type == self.input.EQUALS:
                self.match(self.input.EQUALS)
                self.element()
        elif self.lookahead.type == self.input.LBRACK:
            self.list()
        else:
            raise ValueError(f"Expecting name or list; found {self.lookahead}")
