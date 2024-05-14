import unittest
from parsing.llk_parser import (
    LookaheadParser,
)
from parsing.lexer import ListLexerWithEqual


class LLKTestCase(unittest.TestCase):

    def test_list_lexer_with_equal(self):

        list_lexer = ListLexerWithEqual("[a, b=c]")
        list_parser = LookaheadParser(list_lexer)
        list_parser.list()


if __name__ == "__main__":
    unittest.main()
