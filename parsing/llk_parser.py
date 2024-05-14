from __future__ import annotations

from parsing.lexer import ListLexerWithEqual, Token


class Parser:
    def __init__(self, input_lexer, k=2):
        self.input = input_lexer  # 从词法分析器获取词法单元
        self.k = k  # 前瞻符号的数量
        self.lookahead = [None] * k  # 创建前瞻缓冲区
        self.p = 0  # 循环索引，指向下一个要填充的令牌位置
        for _ in range(k):  # 填充缓冲区
            self.consume()

    def consume(self):
        try:
            self.lookahead[self.p] = next(self.input)
        except StopIteration:
            self.lookahead[self.p] = Token(self.input.EOF_TYPE, self.input.EOF)
        self.p = (self.p + 1) % self.k  # 循环递增索引

    def __getitem__(self, i):
        """允许使用索引操作获取第 i 个 token 。"""
        if isinstance(i, slice):
            # 支持切片操作
            return [
                self.lookahead[(self.p + idx) % self.k]
                for idx in range(i.start or 0, i.stop or self.k, i.step or 1)
            ]
        else:
            return self.lookahead[(self.p + i) % self.k]

    def match(self, type: str):
        """匹配预期的令牌类型。"""
        if self[0].type == type:
            self.consume()
        else:
            raise ValueError(
                f"Expecting type: {self[0].type}; found {self[0]} with type {self[1].type}"
            )


class LookaheadParser(Parser):
    def __init__(self, input: self.input):
        super().__init__(input)

    def list(self):
        """list : '[' elements ']' ; // match bracketed list"""
        self.match(self.input.LBRACK)
        self.elements()
        self.match(self.input.RBRACK)

    def elements(self):
        """elements : element (',' element)* ;"""
        self.element()
        while self[0].type == self.input.COMMA:
            self.match(self.input.COMMA)
            self.element()

    def element(self):
        """element : name | list ; // element is name or nested list"""
        if (
            self[0].type == self.input.NAME
            and self[1].type == self.input.EQUALS
        ):
            self.match(self.input.NAME)
            self.match(self.input.EQUALS)
            self.match(self.input.NAME)

        elif self[0].type == self.input.NAME:
            self.match(self.input.NAME)
        elif self[0].type == self.input.LBRACK:
            self.list()
        else:
            raise ValueError(f"Expecting name or list; found {self.lookahead}")
