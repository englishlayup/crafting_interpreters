package parser

import "github.com/englishlayup/crafting_interpreters/golox/internal/token"

type Parser struct {
	tokens           []token.Token
	current          int
	reportParseError func(token.Token, string)
}

func NewParser(tokens []token.Token, reportParseError func(token.Token, string)) *Parser {
	return &Parser{
		tokens:           tokens,
		reportParseError: reportParseError,
	}
}
