import unittest
from parsing.lexer import ListLexer, ListLexerWithEqual


class ListLexerTestCase(unittest.TestCase):
    def test_list_lexer(self):
        lexer = ListLexer("[a, b ,,]")
        tokens = [str(token) for token in lexer]
        expected = [
            "<'[','LBRACK'>",
            "<'a','NAME'>",
            "<',','COMMA'>",
            "<'b','NAME'>",
            "<',','COMMA'>",
            "<',','COMMA'>",
            "<']','RBRACK'>",
        ]
        self.assertEqual(tokens, expected)

    def test_list_lexer_with_equal(self):
        lexer_we = ListLexerWithEqual("[a, b=c]")
        tokens_we = [str(token) for token in lexer_we]
        expected = [
            "<'[','LBRACK'>",
            "<'a','NAME'>",
            "<',','COMMA'>",
            "<'b','NAME'>",
            "<'=','EQUALS'>",
            "<'c','NAME'>",
            "<']','RBRACK'>",
        ]
        self.assertEqual(tokens_we, expected)


if __name__ == "__main__":
    unittest.main()
