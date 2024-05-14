from parsing.lexer import ListLexerWithEqual, Token, Lexer


# NoViableAltException
class NoViableAltException(Exception):
    pass


# RecognitionException
class RecognitionException(Exception):
    pass


class MismatchedTokenException(Exception):
    pass


class Parser:
    def __init__(self, input: ListLexerWithEqual) -> None:
        self.input = input
        self.stack = []  # stack to store markers
        self.buffer = []  # lookahead buffer
        self.p = 0  # index of first lookahead token

    def match(self, type: str):
        if self[0].type == type:
            self._consume()
        else:
            raise RecognitionException(
                f"Expecting type: {type}; found {self[0]} with type {self[0].type}"
            )

    def _consume(self):
        self.p += 1
        if self.p == len(self.buffer) and len(self.stack) == 0:
            self.buffer.clear()
            self.p = 0

    def __getitem__(self, i):
        """允许使用索引操作获取第 i 个前瞻令牌。"""
        if isinstance(i, slice):
            # 支持切片操作
            if i.stop is None:
                raise ValueError("stop index must be specified")
            self.sync(i.stop - 1)
            return [
                self.buffer[self.p + idx]
                for idx in range(i.start or 0, i.stop, i.step or 1)
            ]
        else:
            self.sync(i)
            return self.buffer[self.p + i]

    def sync(self, i):
        end = self.p + i
        n = len(self.buffer)
        for _ in range(n, end + 1):
            try:
                next_token = next(self.input)
            except StopIteration:
                next_token = Token(self.input.EOF_TYPE, self.input.EOF)
            self.buffer.append(next_token)

    def mark(self):
        self.stack.append(self.p)

    def release(self):
        self.p = self.stack.pop()

    def is_speculating(self):
        return len(self.stack) > 0


class BacktrackParser(Parser):
    def __init__(self, input):
        super().__init__(input)

    def stat(self):
        # attempt alternative 1: list EOF
        if self.speculate_stat_alt1():
            self.list()
            self.match(self.input.EOF_TYPE)
        # attempt alternative 2: assign EOF
        elif self.speculate_stat_alt2():
            self.assign()
            self.match(self.input.EOF_TYPE)
        # must be an error; neither matched; LT(1) is lookahead token 1
        else:
            raise NoViableAltException("expecting stat found " + str(self[1]))

    def speculate_stat_alt1(self):
        success = True
        self.mark()  # mark this spot in input so we can rewind
        try:
            self.list()
            self.match(self.input.EOF_TYPE)
        except RecognitionException:
            success = False
        self.release()  # either way, rewind to where we were
        return success

    def speculate_stat_alt2(self):
        success = True
        self.mark()  # mark this spot in input so we can rewind
        try:
            self.assign()
            self.match(self.input.EOF_TYPE)
        except RecognitionException:
            success = False
        self.release()  # either way, rewind to where we were
        return success

    def assign(self):
        self.list()
        self.match(self.input.EQUALS)
        self.list()

    def list(self):
        self.match(self.input.LBRACK)
        self.elements()
        self.match(self.input.RBRACK)

    def elements(self):
        self.element()
        while self[0].type == self.input.COMMA:
            self.match(self.input.COMMA)
            self.element()

    def element(self):
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
            raise RecognitionException(
                "expecting element found " + str(self[0])
            )
