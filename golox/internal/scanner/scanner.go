package scanner

import (
	"fmt"
	"log"
	"strconv"
	"unicode"

	"github.com/englishlayup/crafting_interpreters/golox/internal/token"
)


type Scanner struct {
	source  string
	tokens  []token.Token
	current int
	start   int
	line    int
	report  func(int, string)
}

func NewScanner(source string, report func(int, string)) *Scanner {
	return &Scanner{
		source:  source,
		tokens:  make([]token.Token, 0),
		current: 0,
		start:   0,
		line:    1,
		report:  report,
	}
}

func (s *Scanner) ScanTokens() []token.Token {
	for !s.isAtEnd() {
		s.start = s.current
		s.scanToken()
	}

	s.tokens = append(s.tokens, *token.NewToken(token.EOF, "", nil, s.line))
    return s.tokens
}

func (s *Scanner) scanToken() {
	c := s.advance()

	switch c {
	case '(':
		s.addToken(token.LEFT_PAREN, nil)
	case ')':
		s.addToken(token.RIGHT_PAREN, nil)
	case '{':
		s.addToken(token.LEFT_BRACE, nil)
	case '}':
		s.addToken(token.RIGHT_BRACE, nil)
	case ',':
		s.addToken(token.COMMA, nil)
	case '.':
		s.addToken(token.DOT, nil)
	case '-':
		s.addToken(token.MINUS, nil)
	case '+':
		s.addToken(token.PLUS, nil)
	case ';':
		s.addToken(token.SEMICOLON, nil)
	case '*':
		s.addToken(token.STAR, nil)
	case '!':
		if s.match('=') {
			s.addToken(token.BANG_EQUAL, nil)
		} else {
			s.addToken(token.BANG, nil)
		}
	case '>':
		if s.match('=') {
			s.addToken(token.GREATER_EQUAL, nil)
		} else {
			s.addToken(token.GREATER, nil)
		}
	case '<':
		if s.match('=') {
			s.addToken(token.LESS_EQUAL, nil)
		} else {
			s.addToken(token.LESS, nil)
		}
	case '=':
		if s.match('=') {
			s.addToken(token.EQUAL_EQUAL, nil)
		} else {
			s.addToken(token.EQUAL, nil)
		}
	case '/':
		if s.match('/') {
			for s.peek() != '\n' && !s.isAtEnd() {
				s.advance()
			}
		} else {
			s.addToken(token.SLASH, nil)
		}
	case ' ', '\r', '\t':
	case '\n':
		s.line += 1
	case '"':
		s.scanString()
	default:
        if s.isDigit(c) {
            s.scanNumber()
        } else if s.isAlpha(c) {
            s.identifier()
        } else {
            s.report(s.line, "Unexpected character.")
        }
	}
}

func (s *Scanner) isAlphaNumeric(c byte) bool {
    return s.isAlpha(c) || s.isDigit(c)
}

func (s *Scanner) isAlpha(c byte) bool {
    return unicode.IsLetter(rune(c)) || c == '_'
}

func (s *Scanner) isDigit(c byte) bool {
    return unicode.IsDigit(rune(c))
}

func (s *Scanner) identifier() {
    var keywords = map[string]token.TokenType{
        "and":    token.AND,
        "class":  token.CLASS,
        "else":   token.ELSE,
        "false":  token.FALSE,
        "for":    token.FOR,
        "fun":    token.FUN,
        "if":     token.IF,
        "nil":    token.NIL,
        "or":     token.OR,
        "print":  token.PRINT,
        "return": token.RETURN,
        "super":  token.SUPER,
        "this":   token.THIS,
        "true":   token.TRUE,
        "var":    token.VAR,
        "while":  token.WHILE,
    }

    for s.isAlphaNumeric(s.peek()){
        s.advance()
    }

    text := s.source[s.start:s.current]
    tokenType, exist := keywords[text]

    if !exist {
        tokenType = token.IDENTIFIER
    }

    s.addToken(tokenType, nil)
}

func (s *Scanner) scanNumber() {
    for s.isDigit(s.peek()){
        s.advance()
    }

    if s.peek() == '.' && s.isDigit(s.peekNext()) {
        s.advance()
        for s.isDigit(s.peek()){
            s.advance()
        }
    }

    value, err := strconv.ParseFloat(s.source[s.start:s.current], 64)
    if err != nil {
        log.Fatal(err)
    }
    s.addToken(token.NUMBER, value)
}

func (s *Scanner) scanString() {
	for s.peek() != '"' && !s.isAtEnd() {
		if s.peek() == '\n' {
			s.line += 1
		}
		s.advance()
	}

	if s.isAtEnd() {
		s.report(s.line, "Unterminated string.")
		return
	}

	s.advance()
	value := s.source[s.start+1 : s.current-1]
	s.addToken(token.STRING, value)
}

func (s *Scanner) peek() byte {
    if s.isAtEnd() {
        return 0
    }
	return s.source[s.current]
}

func (s *Scanner) peekNext() byte {
    if s.current + 1 >= len(s.source) {
        return 0
    }
	return s.source[s.current+1]
}

func (s *Scanner) match(expected byte) bool {
	if s.isAtEnd() {
		return false
	}
	if expected != s.source[s.current] {
		return false
	}

	s.current += 1
	return true
}

func (s *Scanner) addToken(tokenType token.TokenType, literal interface{}) {
	lexeme := s.source[s.start:s.current]
	s.tokens = append(s.tokens, *token.NewToken(tokenType, lexeme, literal, s.line))
}

func (s *Scanner) advance() byte {
	c := s.source[s.current]
	s.current += 1
	return c
}

func (s *Scanner) isAtEnd() bool {
	return s.current == len(s.source)-1
}
