package main

import "fmt"

type Token struct{
    tipe TokenType
    lexeme string
    literal interface{}
    line int
}

func NewToken(tipe TokenType, lexeme string, literal interface{}, line int) *Token{
    return &Token{
        tipe: tipe,
        lexeme: lexeme,
        literal: literal,
        line: line,
    }
}

func (token Token) String() string {
    return fmt.Sprintf("%v %v %v", token.tipe, token.lexeme, token.literal)
}
