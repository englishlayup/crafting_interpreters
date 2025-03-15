package main

type TokenType int

const (
    LEFT_PAREN TokenType = iota
    RIGHT_PAREN
    LEFT_BRACE
    RIGHT_BRACE
    COMMA
    DOT
    MINUS
    PLUS
    SEMICOLON
    SLASH
    STAR

    // One or two character tokens.
    BANG
    BANG_EQUAL
    EQUAL
    EQUAL_EQUAL
    GREATER
    GREATER_EQUAL
    LESS
    LESS_EQUAL

    // Literals.
    IDENTIFIER
    STRING
    NUMBER

    // Keywords.
    AND
    CLASS
    ELSE
    FALSE
    FUN
    FOR
    IF
    NIL
    OR
    PRINT
    RETURN
    SUPER
    THIS
    TRUE
    VAR
    WHILE

    EOF
)

var tokenTypeName = map[TokenType]string{
    LEFT_PAREN:     "LEFT_PAREN",
    RIGHT_PAREN:    "RIGHT_PAREN",
    LEFT_BRACE:     "LEFT_BRACE",
    RIGHT_BRACE:    "RIGHT_BRACE",
    COMMA:          "COMMA",
    DOT:            "DOT",
    MINUS:          "MINUS",
    PLUS:           "PLUS",
    SEMICOLON:      "SEMICOLON",
    SLASH:          "SLASH",
    STAR:           "STAR",

    // One or two character tokens.
    BANG:           "BANG",
    BANG_EQUAL:     "BANG_EQUAL",
    EQUAL:          "EQUAL",
    EQUAL_EQUAL:    "EQUAL_EQUAL",
    GREATER:        "GREATER",
    GREATER_EQUAL:  "GREATER_EQUAL",
    LESS:           "LESS",
    LESS_EQUAL:     "LESS_EQUAL",

    // Literals.
    IDENTIFIER:     "IDENTIFIER",
    STRING:         "STRING",
    NUMBER:         "NUMBER",

    // Keywords.
    AND:            "AND",
    CLASS:          "CLASS",
    ELSE:           "ELSE",
    FALSE:          "FALSE",
    FUN:            "FUN",
    FOR:            "FOR",
    IF:             "IF",
    NIL:            "NIL",
    OR:             "OR",
    PRINT:          "PRINT",
    RETURN:         "RETURN",
    SUPER:          "SUPER",
    THIS:           "THIS",
    TRUE:           "TRUE",
    VAR:            "VAR",
    WHILE:          "WHILE",

    EOF:            "EOF",
}

func (tokenType TokenType) String() string {
    return tokenTypeName[tokenType]
}
