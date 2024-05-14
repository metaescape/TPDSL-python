import unittest
from parsing.ll1_parser import (
    ListParser,
    ListParserWithEqual,
)
from parsing.lexer import ListLexer, ListLexerWithEqual


class ListLexerTestCase(unittest.TestCase):
    def test_list_lexer(self):

        list_lexer = ListLexer("[a, b]")
        list_parser = ListParser(list_lexer)
        list_parser.list()

    def test_list_lexer_with_equal(self):

        list_lexer = ListLexerWithEqual("[a, b=c]")
        list_parser = ListParserWithEqual(list_lexer)
        list_parser.list()


if __name__ == "__main__":
    unittest.main()
