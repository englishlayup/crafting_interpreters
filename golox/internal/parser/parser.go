package parser

import (
	"fmt"
	"log"

	"github.com/englishlayup/crafting_interpreters/golox/internal/expr"
	"github.com/englishlayup/crafting_interpreters/golox/internal/stmt"
	"github.com/englishlayup/crafting_interpreters/golox/internal/token"
)

type ParseError struct {
}

func (p *ParseError) Error() string {
	return ""
}

type Parser struct {
	tokens      []token.Token
	current     int
	reportError func(token.Token, string)
}

func NewParser(tokens []token.Token, reportError func(token.Token, string)) Parser {
	return Parser{
		tokens:      tokens,
		reportError: reportError,
	}
}

func (p *Parser) Parse() []stmt.Stmt[any] {
	statements := make([]stmt.Stmt[any], 0)

	for p.isAtEnd() {
		statements = append(statements, p.declaration())
	}
	return statements
}

func (p *Parser) handleParseError(err error) {
    if _, ok := err.(*ParseError); ok {
        p.synchronize()
    }
    log.Fatal(err)
}

func (p *Parser) declaration() stmt.Stmt[any] {
	if p.match(token.CLASS) {
		decl, err := p.classDeclaration()
		if err != nil {
            p.handleParseError(err)
            return nil
		}
		return decl
	}
	if p.match(token.FUN) {
		decl, err := p.function("function")
		if err != nil {
            p.handleParseError(err)
            return nil
		}
		return decl
	}
	if p.match(token.VAR) {
		decl, err := p.varDelaration()
		if err != nil {
            p.handleParseError(err)
            return nil
		}
		return decl
	}
	return nil
}

func (p Parser) varDelaration() (stmt.Var[any], error) {
	name, err := p.consume(token.IDENTIFIER, "Expect variable name.")
	if err != nil {
		return stmt.Var[any]{}, err
	}
	var initializer expr.Expr[any]
	if p.match(token.EQUAL) {
		initializer, err = p.expression()
		if err != nil {
			return stmt.Var[any]{}, err
		}
	}
	if _, err := p.consume(
		token.SEMICOLON,
		"Expect ';' after variable declaration.",
	); err != nil {
		return stmt.Var[any]{}, err
	}
	return stmt.Var[any]{
		Name:        name,
		Initializer: initializer,
	}, nil
}

func (p *Parser) expression() (expr.Expr[any], error) {
	expression, err := p.assignment()
	if err != nil {
		return nil, err
	}
	return expression, nil
}

func (p *Parser) assignment() (expr.Expr[any], error) {
	expression, err := p.or()
	if err != nil {
		return nil, err
	}

	if p.match(token.EQUAL) {
		equals := p.previous()
		value, err := p.assignment()
		if err != nil {
			return nil, err
		}
		switch e := expression.(type) {
		case expr.Variable[any]:
			return expr.Assign[any]{
				Name:  e.Name,
				Value: value,
			}, nil
		case expr.Get[any]:
			return expr.Set[any]{
				Object: e.Object,
				Name:   e.Name,
				Value:  value,
			}, nil
		default:
			return expression, p.error(equals, "Invalid assignment target.")
		}
	}
	return expression, nil
}

func (p *Parser) or() (expr.Expr[any], error) {
	expression, err := p.and()
	if err != nil {
		return nil, err
	}

	for p.match(token.OR) {
		operator := p.previous()
		right, err := p.and()
		if err != nil {
			return nil, err
		}
		expression = expr.Logical[any]{
			Left:     expression,
			Operator: operator,
			Right:    right,
		}
	}
	return expression, nil
}

func (p *Parser) and() (expr.Expr[any], error) {
	expression, err := p.equality()
	if err != nil {
		return nil, err
	}

	for p.match(token.AND) {
		operator := p.previous()
		right, err := p.equality()
		if err != nil {
			return nil, err
		}
		expression = expr.Logical[any]{
			Left:     expression,
			Operator: operator,
			Right:    right,
		}
	}
	return expression, nil
}

func (p *Parser) equality() (expr.Expr[any], error) {
	expression, err := p.comparison()
	if err != nil {
		return nil, err
	}

	for p.match(token.EQUAL_EQUAL, token.BANG_EQUAL) {
		operator := p.previous()
		right, err := p.comparison()
		if err != nil {
			return nil, err
		}
		expression = expr.Binary[any]{
			Left:     expression,
			Operator: operator,
			Right:    right,
		}
	}
	return expression, nil
}

func (p *Parser) comparison() (expr.Expr[any], error) {
	expression, err := p.term()
	if err != nil {
		return nil, err
	}

	for p.match(
		token.GREATER,
		token.GREATER_EQUAL,
		token.LESS,
		token.LESS_EQUAL,
	) {
		operator := p.previous()
		right, err := p.term()
		if err != nil {
			return nil, err
		}
		expression = expr.Binary[any]{
			Left:     expression,
			Operator: operator,
			Right:    right,
		}
	}
	return expression, nil
}

func (p *Parser) term() (expr.Expr[any], error) {
	expression, err := p.factor()
	if err != nil {
		return nil, err
	}

	for p.match(
		token.MINUS,
		token.PLUS,
	) {
		operator := p.previous()
		right, err := p.factor()
		if err != nil {
			return nil, err
		}
		expression = expr.Binary[any]{
			Left:     expression,
			Operator: operator,
			Right:    right,
		}
	}
	return expression, nil
}

func (p *Parser) factor() (expr.Expr[any], error) {
	expression, err := p.unary()
	if err != nil {
		return nil, err
	}

	for p.match(
		token.SLASH,
		token.STAR,
	) {
		operator := p.previous()
		right, err := p.unary()
		if err != nil {
			return nil, err
		}
		expression = expr.Binary[any]{
			Left:     expression,
			Operator: operator,
			Right:    right,
		}
	}
	return expression, nil
}

func (p *Parser) unary() (expr.Expr[any], error) {
	if p.match(
		token.BANG,
		token.MINUS,
	) {
		operator := p.previous()
		right, err := p.unary()
		if err != nil {
			return nil, err
		}
		return expr.Unary[any]{
			Operator: operator,
			Right:    right,
		}, nil
	}
	return p.call()
}

func (p *Parser) call() (expr.Expr[any], error) {
	expression, err := p.primary()
	if err != nil {
		return nil, err
	}

	for {
		if p.match(token.LEFT_PAREN) {
			expression, err = p.finishCall(expression)
		} else if p.match(token.DOT) {
			name, err := p.consume(
				token.IDENTIFIER,
				"Expect property name after '.'.",
			)
			if err != nil {
				return nil, err
			}
			expression = expr.Get[any]{
				Object: expression,
				Name:   name,
			}
		} else {
			break
		}
	}
	return expression, nil
}

func (p *Parser) finishCall(expression expr.Expr[any]) (expr.Expr[any], error) {
	arguments := make([]expr.Expr[any], 0)

	if p.check(token.RIGHT_PAREN) {
		argument, err := p.expression()
		if err != nil {
			return nil, err
		}
		arguments = append(arguments, argument)
		for p.match(token.COMMA) {
			if len(arguments) >= 255 {
				return nil, p.error(
					p.peek(),
					"Can't have more than 255 arguments.",
				)
			}
			argument, err := p.expression()
			if err != nil {
				return nil, err
			}
			arguments = append(arguments, argument)
		}
	}

	paren, err := p.consume(token.RIGHT_PAREN, "Expect ')' after arguments.")
	if err != nil {
		return nil, err
	}

	return expr.Call[any]{
		Callee:    expression,
		Paren:     paren,
		Arguments: arguments,
	}, nil
}

func (p *Parser) primary() (expr.Expr[any], error) {
	if p.match(token.TRUE) {
		return expr.Literal[any]{Value: true}, nil
	}
	if p.match(token.FALSE) {
		return expr.Literal[any]{Value: false}, nil
	}
	if p.match(token.NIL) {
		return expr.Literal[any]{Value: nil}, nil
	}
	if p.match(token.IDENTIFIER) {
		return expr.Variable[any]{Name: p.previous()}, nil
	}
	if p.match(token.NUMBER, token.STRING) {
		return expr.Literal[any]{Value: p.previous().Literal}, nil
	}
	if p.match(token.THIS) {
		return expr.This[any]{Keyword: p.previous()}, nil
	}
	if p.match(token.LEFT_PAREN) {
		expression, err := p.expression()
		if err != nil {
			return nil, err
		}
		if _, err := p.consume(
			token.RIGHT_PAREN,
			"Expect ')' after expression.",
		); err != nil {
			return nil, err
		}
		return expr.Grouping[any]{Expression: expression}, nil
	}
	if p.match(token.SUPER) {
		keyword := p.previous()
		if _, err := p.consume(
			token.DOT,
			"Expect '.' after 'super'.",
		); err != nil {
			return nil, err
		}
		method, err := p.consume(token.IDENTIFIER, "Expect superclass method name.")
		if err != nil {
			return nil, err
		}
		return expr.Super[any]{
			Keyword: keyword,
			Method:  method,
		}, nil
	}
	return nil, p.error(p.peek(), "Expect expression.")
}

func (p *Parser) classDeclaration() (stmt.Class[any], error) {
	name, err := p.consume(token.IDENTIFIER, "Expect class name.")
	if err != nil {
		return stmt.Class[any]{}, err
	}
	var superclass expr.Variable[any]
	if p.match(token.LESS) {
		if _, err := p.consume(
			token.IDENTIFIER,
			"Expect superclass name.",
		); err != nil {
			return stmt.Class[any]{}, err
		}
		superclass = expr.Variable[any]{
			Name: p.previous(),
		}
	}
	if _, err := p.consume(
		token.LEFT_BRACE,
		"Expect '{' before class body.",
	); err != nil {
		return stmt.Class[any]{}, err
	}
	methods := make([]stmt.Function[any], 0)
	for p.check(token.RIGHT_BRACE) && !p.isAtEnd() {
		function, err := p.function("method")
		if err != nil {
			return stmt.Class[any]{}, nil
		}
		methods = append(methods, function)
	}
	if _, err := p.consume(
		token.RIGHT_BRACE,
		"Expect '}' after class body.",
	); err != nil {
		return stmt.Class[any]{}, err
	}
	return stmt.Class[any]{
		Name:       name,
		Superclass: superclass,
		Methods:    methods,
	}, nil
}

func (p *Parser) function(kind string) (stmt.Function[any], error) {
	name, err := p.consume(token.IDENTIFIER, fmt.Sprintf("Expect %s name.", kind))
	if err != nil {
		return stmt.Function[any]{}, err
	}
	if _, err := p.consume(
		token.LEFT_PAREN,
		fmt.Sprintf("Expect '(' after %s name.", kind),
	); err != nil {
		return stmt.Function[any]{}, err
	}
	arguments := make([]token.Token, 0)
	if !p.check(token.RIGHT_PAREN) {
		identifer, err := p.consume(token.IDENTIFIER, "Expect parameter name.")
		if err != nil {
			return stmt.Function[any]{}, err
		}
		arguments = append(arguments, identifer)
		for p.match(token.COMMA) {
			if len(arguments) >= 255 {
				p.reportError(p.peek(), "Can't have more than 255 parameters.")
			}
			identifer, err := p.consume(token.IDENTIFIER, "Expect parameter name.")
			if err != nil {
				return stmt.Function[any]{}, err
			}
			arguments = append(arguments, identifer)
		}
	}
	if _, err := p.consume(
		token.RIGHT_PAREN,
		"Expect ')' after parameters.",
	); err != nil {
		return stmt.Function[any]{}, err
	}
	if _, err := p.consume(
		token.LEFT_BRACE,
		fmt.Sprintf("Expect '{' before %s body.", kind),
	); err != nil {
		return stmt.Function[any]{}, err
	}
	body, err := p.block()
	if err != nil {
		return stmt.Function[any]{}, err
	}
	return stmt.Function[any]{
		Name:   name,
		Params: arguments,
		Body:   body,
	}, nil
}

func (p *Parser) block() ([]stmt.Stmt[any], error) {
	statements := make([]stmt.Stmt[any], 0)

	for !p.check(token.RIGHT_BRACE) && !p.isAtEnd() {
		statements = append(statements, p.declaration())
	}
	if _, err := p.consume(
		token.RIGHT_BRACE,
		"Expect '}' after block.",
	); err != nil {
		return nil, err
	}
	return statements, nil
}

func (p *Parser) isAtEnd() bool {
	return p.tokens[p.current].TokenType == token.EOF
}

func (p *Parser) match(types ...token.TokenType) bool {
	for _, t := range types {
		if p.check(t) {
			p.advance()
			return true
		}
	}
	return false
}

func (p *Parser) check(expected token.TokenType) bool {
	if p.isAtEnd() {
		return false
	}
	return p.peek().TokenType == expected
}

func (p *Parser) advance() token.Token {
	if !p.isAtEnd() {
		p.current += 1
	}
	return p.previous()
}

func (p *Parser) previous() token.Token {
	return p.tokens[p.current-1]
}

func (p *Parser) consume(expected token.TokenType, message string) (token.Token, error) {
	if p.check(expected) {
		return p.advance(), nil
	}
	return token.Token{}, p.error(p.peek(), message)
}

func (p *Parser) error(token token.Token, message string) error {
	p.reportError(token, message)
	return &ParseError{}
}

func (p *Parser) peek() token.Token {
	return p.tokens[p.current]
}

func (p *Parser) synchronize() {
	for p.isAtEnd() {
		if p.previous().TokenType == token.SEMICOLON {
			return
		}
		switch p.peek().TokenType {
		case token.CLASS,
			token.FUN,
			token.VAR,
			token.FOR,
			token.IF,
			token.WHILE,
			token.PRINT,
			token.RETURN:
			return
		default:
			p.advance()
		}
	}
}
