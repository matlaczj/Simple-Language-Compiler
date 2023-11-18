# type: ignore
from lexer import *


class Parser:
    def __init__(self, source):
        self.tokens = None
        self.token_index = -1
        self.current_token = None
        self.tokenize(source)
        self.if_reached_eof = False
        print(f"-> initialized parser with {len(self.tokens)} tokens")
        print(f"token index: {self.token_index}, current token: {self.current_token}")

    def tokenize(self, source):
        lxr = Lexer(source)
        lxr.tokenize()
        self.tokens = lxr.tokens
        print("-> tokenization finished")

    def current_token_details(self):
        return f"token: {self.current_token.ttype}, value: {self.current_token.value}, line: {self.current_token.line}, column: {self.current_token.column}"

    def current_token_type(self):
        return self.current_token.ttype if self.current_token else None

    def advance(self):
        print(f"-> advancing from {self.current_token_type()}", end=" ")
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None
        print(f"to {self.current_token_type()}")
        if self.current_token_type() == "TOKEN_EOF":
            print("-> reached EOF")
            self.if_reached_eof = True

    def consume(self, token_type):
        print(f"-> consuming {token_type}", end=":")
        if self.current_token is not None and self.current_token.ttype == token_type:
            print(f"{self.current_token.value}")
            self.advance()
        else:
            raise SyntaxError(
                f"Expected {token_type}, but found {self.current_token_details()}"
            )

    # <STYLESHEET> ::= <rule> | <rule> <STYLESHEET>
    def parse(self):
        print("-> began parsing")
        self.advance()
        while self.current_token is not None and self.if_reached_eof is False:
            self.parse_rule()

    # <rule> ::= <selectors> <INDENT> <declarations> <DEDENT>
    def parse_rule(self):
        print("-> parsing rule")
        self.parse_selectors()
        self.consume("TOKEN_INDENT")
        self.parse_declarations()
        self.consume("TOKEN_DEDENT")

    # <selectors> ::= <selector> | <selector> "," <selectors>
    def parse_selectors(self):
        print("-> parsing selectors")
        self.parse_selector()
        if self.current_token.ttype == "TOKEN_COMMA":
            self.consume("TOKEN_COMMA")
            self.parse_selectors()

    # <selector> ::= <simple_selector> | <simple_selector> <combinator> <simple_selector>
    # <selector> ::= <simple_selector> ":" <selector_keyword>
    def parse_selector(self):
        print("-> parsing selector")
        self.parse_simple_selector()
        if self.current_token.ttype in dict(COMBINATOR_PATTERNS):
            self.parse_combinator()
            self.parse_simple_selector()
        if self.current_token.ttype == "TOKEN_COLON":
            self.consume("TOKEN_COLON")
            self.consume("TOKEN_SELECTOR_KEYWORD")

    # <simple_selector> ::= "#" <IDENTIFIER> | "." <IDENTIFIER> | ":" <IDENTIFIER> | "*" | <IDENTIFIER>
    def parse_simple_selector(self):
        print("-> parsing simple selector")
        if self.current_token.ttype == "TOKEN_HASH":
            self.consume("TOKEN_HASH")
            self.consume("TOKEN_IDENTIFIER")
        elif self.current_token.ttype == "TOKEN_DOT":
            self.consume("TOKEN_DOT")
            self.consume("TOKEN_IDENTIFIER")
        elif self.current_token.ttype == "TOKEN_COLON":
            self.consume("TOKEN_COLON")
            self.consume("TOKEN_IDENTIFIER")
        elif self.current_token.ttype == "TOKEN_STAR":
            self.consume("TOKEN_STAR")
        else:
            self.consume("TOKEN_IDENTIFIER")

    # <combinator> ::= "+" | ">" | " "
    def parse_combinator(self):
        print("-> parsing combinator")
        combinator = self.current_token.ttype
        if (
            combinator == "TOKEN_PLUS"
            or combinator == "TOKEN_GREATER"
            or combinator == "TOKEN_DESCENDANT"
        ):
            self.consume(combinator)
        else:
            raise SyntaxError(
                f"Expected '+' or '>' or ' ', but found {self.current_token_details()}"
            )

    # <declarations> ::= <declaration> | <declaration> ";" | <declaration> ";" <declarations>
    def parse_declarations(self):
        print("-> parsing declarations")
        while (
            self.current_token is not None
            and self.current_token.ttype == "TOKEN_PROPERTY_KEYWORD"
        ):
            self.parse_declaration()
            if (
                self.current_token is not None
                and self.current_token.ttype == "TOKEN_SEMICOLON"
            ):
                self.consume("TOKEN_SEMICOLON")
                self.parse_declarations()

    # <declaration> ::= <property_keyword> ":" <values>
    def parse_declaration(self):
        print("-> parsing declaration")
        self.consume("TOKEN_PROPERTY_KEYWORD")
        self.consume("TOKEN_COLON")
        self.parse_values()

    # <values> ::= <value> | <value> <values>
    def parse_values(self):
        print("-> parsing values")
        self.parse_value()
        if self.current_token is not None and self.current_token.ttype not in [
            "TOKEN_SEMICOLON",
            "TOKEN_DEDENT",
        ]:
            self.parse_values()

    # <value> ::= <COLOR> | <URL> | <LENGTH> | <STRING> |  <NUMBER> | <PERCENTAGE> | <IDENTIFIER> | <value_keyword>
    def parse_value(self):
        print("-> parsing value")
        if self.current_token.ttype in dict(VALUE_PATTERNS):
            self.consume(self.current_token.ttype)
        else:
            raise SyntaxError(f"Invalid token: {self.current_token_details()}")


if __name__ == "__main__":
    parser = Parser(SOURCE)
    parser.parse()
