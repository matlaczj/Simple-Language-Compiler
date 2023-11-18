# type: ignore
from re import match, sub

# NOTE: This code is correct and parser should be able to parse it.
SOURCE = """
#abc
	background: url(watch?v=Ct6BUPvE2sM);
	color: #f00;
	box-shadow: none;
	text-shadow: none;

.def
	content: "see below";

p > pre
	border: 1px solid #999;
	page-break-inside: avoid;

div + p,
div > p
	font-weight: bolder

p img
	max-width: 100% !important;

pine + apple,
* + * // * jest poprawnym selektorem
	orphans: 3;
	widows: 3rem;

a:visited
	color: white;
"""

# NOTE: Test parser by running, checking error, fixing and running again to proove
# that parser is working and useful. Below code is incorrect. After correcting please
# make it incorrect again for future use.
INCORRECT_SOURCE = """
p + + q // kombinator (np. +, >) nie może pojawić się więcej niż raz między selektorami
	content: "see below";
	border: 1px solid #999;
	page-break-inside: avoid;

div+p,
div>p
    font-size: smaller; // nie cztery spacje to niepoprawne wcięcie
		font-family: serif; // ale zbyt duże wcięcie to też problem
	font-weight: bolder; // powinna być tabulacja, jak tutaj
	font-style: normal; // ta linia jest dobrze wcięta

pine + apple
	max-width: 100% !oops; // !important jest jedynym słowem kluczowym z !

foo _bar, // identyfikatory poprawne
&baz, // identyfikator niepoprawny
:quax // ten też jest poprawny
	display: flex // brak średnika jest niedopuszczalny między deklaracjami
	margin: 1px // ale jest OK na końcu
"""

VALUE_PATTERNS = [
    (
        "TOKEN_VALUE_KEYWORD",
        r"none|solid|avoid|smaller|bolder|normal|serif|!important|white|flex",
    ),
    ("TOKEN_COLOR", r"#([0-9a-fA-F]{3,6})"),
    ("TOKEN_URL", r"url\((.*?)\)"),
    ("TOKEN_LENGTH", r"\d+(\.\d+)?(px|rem)"),
    ("TOKEN_PERCENTAGE", r"\d+(\.\d+)?%"),
    ("TOKEN_STRING", r'"([^"]+)"'),
    ("TOKEN_NUMBER", r"\d+(\.\d+)?"),
    ("TOKEN_IDENTIFIER", r"[A-Za-z\-\_]+"),
]

COMBINATOR_PATTERNS = [
    ("TOKEN_PLUS", r"\+"),
    ("TOKEN_GREATER", r">"),
    ("TOKEN_DESCENDANT", r" "),
]

TOKEN_PATTERNS = (
    [
        ("TOKEN_COMMA", r","),
        ("TOKEN_DOT", r"\."),
        ("TOKEN_COLON", r":"),
        ("TOKEN_SEMICOLON", r";"),
        ("TOKEN_HASH", r"#"),
        ("TOKEN_STAR", r"\*"),
        (
            "TOKEN_PROPERTY_KEYWORD",
            r"background|color|box-shadow|text-shadow|content|border|page-break-inside|font-weight|max-width|orphans|widows|font-size|font-family|font-style|display|margin",
        ),
        ("TOKEN_SELECTOR_KEYWORD", r"visited"),
    ]
    + VALUE_PATTERNS
    + COMBINATOR_PATTERNS
)


class Token:
    def __init__(self, ttype, value, line, column):
        self.ttype = ttype
        self.value = value
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, text):
        self.text = text
        self.remove_comments()
        self.tokens = []
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        self.line = 0
        self.column = 0

    def tokens_types(self):
        return [t.ttype for t in self.tokens]

    def tokens_values(self):
        return [t.value for t in self.tokens]

    def advance(self, step=1):
        self.pos += step
        self.column += step
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def peak_into_future(self, step=1):
        if (self.pos + step) < len(self.text):
            return self.text[self.pos + step]
        else:
            return None

    def remove_comments(self):
        self.text = sub(r"//.*", "", self.text)

    def print_tokens(self):
        for t in self.tokens:
            print(f"Token({t.ttype}, {t.value}, {t.line}, {t.column})")

    def tokenize(self):
        if_expected_value = False
        indent_stack = [0]
        while self.current_char is not None:
            # Check if we still expect value.
            if_expected_value = (
                False
                if (
                    self.peak_into_future() in ["\n", ";"]
                    or self.current_char in ["\n", ";"]
                )
                else if_expected_value
            )

            # Distinguish between space and descendant combinator.
            if (
                len(self.tokens) >= 1
                and self.tokens[-1].ttype == "TOKEN_IDENTIFIER"
                and self.current_char == " "
                and (
                    self.peak_into_future().isalpha() or self.peak_into_future() == "_"
                )
            ):
                self.tokens.append(
                    Token("TOKEN_DESCENDANT", " ", self.line, self.column)
                )
                self.advance()
                continue

            # Skip whitespace that are not after newline.
            if self.current_char in [" ", "\t"]:
                self.advance()
                continue

            # After newline we expect indent using tabs (not spaces).
            if self.current_char == "\n":
                self.line += 1
                self.column = 0
                self.advance()

                indent_level = 0
                while self.current_char in [" ", "\t"]:
                    if self.current_char == " ":
                        raise ValueError(
                            f"Invalid indentation: {self.line}:{self.column}. Remove non-tab whitespace."
                        )
                    indent_level += 1
                    self.advance()
                if indent_level != indent_stack[-1]:
                    if indent_level > indent_stack[-1]:
                        for _ in range(indent_level - indent_stack[-1]):
                            self.tokens.append(
                                Token(
                                    "TOKEN_INDENT",
                                    "",
                                    self.line,
                                    self.column - indent_level - 1,
                                )
                            )
                    if indent_level < indent_stack[-1]:
                        for _ in range(indent_stack[-1] - indent_level):
                            self.tokens.append(
                                Token(
                                    "TOKEN_DEDENT",
                                    "",
                                    self.line,
                                    self.column - indent_level - 1,
                                )
                            )
                    indent_stack.append(indent_level)
                continue

            # We expect value after property keyword and colon.
            if_expected_value = (
                True
                if len(self.tokens) >= 2
                and self.tokens[-2].ttype == "TOKEN_PROPERTY_KEYWORD"
                and self.tokens[-1].ttype == "TOKEN_COLON"
                else if_expected_value
            )

            # Match tokens.
            if_matched = False
            token_patterns = VALUE_PATTERNS if if_expected_value else TOKEN_PATTERNS
            for token_type, pattern in token_patterns:
                fit = match(pattern, self.text[self.pos :])
                if_matched = True if fit is not None else False
                if if_matched:
                    group = fit.group()
                    self.tokens.append(Token(token_type, group, self.line, self.column))
                    self.advance(step=len(group))
                    break
            if not if_matched:
                raise ValueError(
                    f"Invalid character: {self.current_char} at {self.line}:{self.column}"
                )

        # Add EOF token after the last token.
        self.tokens.append(Token("TOKEN_EOF", "", self.line, self.column))


if __name__ == "__main__":
    lexer = Lexer(SOURCE)
    lexer.tokenize()
    lexer.print_tokens()
