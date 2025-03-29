package parser

import (
	"github.com/englishlayup/crafting_interpreters/golox/internal/stmt"
	"github.com/englishlayup/crafting_interpreters/golox/internal/token"
)

type Parser struct {
	tokens      []token.Token
	current     int
	reportError func(token.Token, string)
}

func NewParser(tokens []token.Token, reportError func(token.Token, string)) *Parser {
	return &Parser{
		tokens:      tokens,
		reportError: reportError,
	}
}

func (p *Parser) Parse() []stmt.Stmt[any] {
    statements := make([]stmt.Stmt[any], 0)

    for p.isAtEnd(){
        // statements = append(statements, parser.declaration())
    }
    return statements
}

func (p *Parser) isAtEnd() bool {
    return p.tokens[p.current].TokenType == token.EOF
}
