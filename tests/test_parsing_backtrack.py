import unittest
from parsing.backtrack_parser import (
    BacktrackParser,
)
from parsing.lexer import ListLexerWithEqual


class BacktrackTestCase(unittest.TestCase):

    def test_backtrack_basic(self):

        list_lexer = ListLexerWithEqual("[a, b, c]")
        list_parser = BacktrackParser(list_lexer)
        list_parser.stat()

    def test_backtrack_equal(self):

        list_lexer = ListLexerWithEqual("[a, b=c]")
        list_parser = BacktrackParser(list_lexer)
        list_parser.stat()

    def test_backtrack_assign(self):

        list_lexer = ListLexerWithEqual("[a, b] = [c,d=f]")
        list_parser = BacktrackParser(list_lexer)
        list_parser.stat()


if __name__ == "__main__":
    unittest.main()
