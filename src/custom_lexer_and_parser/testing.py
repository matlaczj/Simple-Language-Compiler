from kompilatory.lexer import Lexer


def test_lexer(code, expected_tokens_types):
    lexer = Lexer(code)
    lexer.tokenize()
    tokens_types = lexer.tokens_types()
    assert tokens_types == expected_tokens_types
    print("OK")


def test_lexer_1():
    code = """
#abc
	background: url(watch?v=Ct6BUPvE2sM);
	color: #f00;
	box-shadow: none;
	text-shadow: none;
"""
    expected_tokens_types = [
        "TOKEN_HASH",
        "TOKEN_IDENTIFIER",
        "TOKEN_INDENT",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_URL",
        "TOKEN_SEMICOLON",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_COLOR",
        "TOKEN_SEMICOLON",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_SEMICOLON",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_SEMICOLON",
        "TOKEN_DEDENT",
        "TOKEN_EOF",
    ]
    test_lexer(code, expected_tokens_types)


def test_lexer_2():
    code = """
.def
	content: "see below";
"""
    expected_tokens_types = [
        "TOKEN_DOT",
        "TOKEN_IDENTIFIER",
        "TOKEN_INDENT",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_STRING",
        "TOKEN_SEMICOLON",
        "TOKEN_DEDENT",
        "TOKEN_EOF",
    ]
    test_lexer(code, expected_tokens_types)


def test_lexer_3():
    code = """
p > pre
	border: 1px solid #999;
	page-break-inside: avoid;
"""
    expected_tokens_types = [
        "TOKEN_IDENTIFIER",
        "TOKEN_GREATER",
        "TOKEN_IDENTIFIER",
        "TOKEN_INDENT",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_LENGTH",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_COLOR",
        "TOKEN_SEMICOLON",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_SEMICOLON",
        "TOKEN_DEDENT",
        "TOKEN_EOF",
    ]

    test_lexer(code, expected_tokens_types)


def test_lexer_4():
    code = """
div + p,
div > p
	font-weight: bolder
"""
    expected_tokens_types = [
        "TOKEN_IDENTIFIER",
        "TOKEN_PLUS",
        "TOKEN_IDENTIFIER",
        "TOKEN_COMMA",
        "TOKEN_IDENTIFIER",
        "TOKEN_GREATER",
        "TOKEN_IDENTIFIER",
        "TOKEN_INDENT",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_DEDENT",
        "TOKEN_EOF",
    ]

    test_lexer(code, expected_tokens_types)


def test_lexer_5():
    code = """
p img
	max-width: 100% !important;
"""
    expected_tokens_types = [
        "TOKEN_IDENTIFIER",
        "TOKEN_DESCENDANT",
        "TOKEN_IDENTIFIER",
        "TOKEN_INDENT",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_PERCENTAGE",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_SEMICOLON",
        "TOKEN_DEDENT",
        "TOKEN_EOF",
    ]

    test_lexer(code, expected_tokens_types)


def test_lexer_6():
    code = """
pine + apple,
* + * // * jest poprawnym selektorem
	orphans: 3;
	widows: 3rem;
"""
    expected_tokens_types = [
        "TOKEN_IDENTIFIER",
        "TOKEN_PLUS",
        "TOKEN_IDENTIFIER",
        "TOKEN_COMMA",
        "TOKEN_STAR",
        "TOKEN_PLUS",
        "TOKEN_STAR",
        "TOKEN_INDENT",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_NUMBER",
        "TOKEN_SEMICOLON",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_LENGTH",
        "TOKEN_SEMICOLON",
        "TOKEN_DEDENT",
        "TOKEN_EOF",
    ]

    test_lexer(code, expected_tokens_types)


def test_lexer_7():
    code = """
a:visited
	color: white;
"""
    expected_tokens_types = [
        "TOKEN_IDENTIFIER",
        "TOKEN_COLON",
        "TOKEN_SELECTOR_KEYWORD",
        "TOKEN_INDENT",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_SEMICOLON",
        "TOKEN_DEDENT",
        "TOKEN_EOF",
    ]

    test_lexer(code, expected_tokens_types)


def test_lexer_8():
    # NOTE: Presented syntax is incorrect, but it's not the lexer's job to check it.
    code = """
p + + q // kombinator (np. +, >) nie może pojawić się więcej niż raz między selektorami
	content: "see below";
	border: 1px solid #999;
	page-break-inside: avoid;
"""
    expected_tokens_types = [
        "TOKEN_IDENTIFIER",
        "TOKEN_PLUS",
        "TOKEN_PLUS",
        "TOKEN_IDENTIFIER",
        "TOKEN_INDENT",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_STRING",
        "TOKEN_SEMICOLON",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_LENGTH",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_COLOR",
        "TOKEN_SEMICOLON",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_SEMICOLON",
        "TOKEN_DEDENT",
        "TOKEN_EOF",
    ]

    test_lexer(code, expected_tokens_types)


def test_lexer_9():
    # NOTE: Indentation and space-tab were corrected because lexer does actually check it.
    code = """
div+p,
div>p
	font-size: smaller; // nie cztery spacje to niepoprawne wcięcie
	font-family: serif; // ale zbyt duże wcięcie to też problem
	font-weight: bolder; // powinna być tabulacja, jak tutaj
	font-style: normal; // ta linia jest dobrze wcięta
"""
    expected_tokens_types = [
        "TOKEN_IDENTIFIER",
        "TOKEN_PLUS",
        "TOKEN_IDENTIFIER",
        "TOKEN_COMMA",
        "TOKEN_IDENTIFIER",
        "TOKEN_GREATER",
        "TOKEN_IDENTIFIER",
        "TOKEN_INDENT",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_SEMICOLON",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_SEMICOLON",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_SEMICOLON",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_SEMICOLON",
        "TOKEN_DEDENT",
        "TOKEN_EOF",
    ]

    test_lexer(code, expected_tokens_types)


def test_lexer_10():
    code = """
pine + apple
	max-width: 100% !important;
"""
    expected_tokens_types = [
        "TOKEN_IDENTIFIER",
        "TOKEN_PLUS",
        "TOKEN_IDENTIFIER",
        "TOKEN_INDENT",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_PERCENTAGE",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_SEMICOLON",
        "TOKEN_DEDENT",
        "TOKEN_EOF",
    ]

    test_lexer(code, expected_tokens_types)


def test_lexer_11():
    code = """
foo _bar, // identyfikatory poprawne
baz,
:quax // ten też jest poprawny
	display: flex;
	margin: 1px // ale jest OK na końcu
"""
    expected_tokens_types = [
        "TOKEN_IDENTIFIER",
        "TOKEN_DESCENDANT",
        "TOKEN_IDENTIFIER",
        "TOKEN_COMMA",
        "TOKEN_IDENTIFIER",
        "TOKEN_COMMA",
        "TOKEN_COLON",
        "TOKEN_IDENTIFIER",
        "TOKEN_INDENT",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_VALUE_KEYWORD",
        "TOKEN_SEMICOLON",
        "TOKEN_PROPERTY_KEYWORD",
        "TOKEN_COLON",
        "TOKEN_LENGTH",
        "TOKEN_DEDENT",
        "TOKEN_EOF",
    ]

    test_lexer(code, expected_tokens_types)


test_lexer_1()
test_lexer_2()
test_lexer_3()
test_lexer_4()
test_lexer_5()
test_lexer_6()
test_lexer_7()
test_lexer_8()
test_lexer_9()
test_lexer_10()
test_lexer_11()
