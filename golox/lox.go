package main

import (
	"bufio"
	"fmt"
	"log"
	"os"

    "github.com/englishlayup/crafting_interpreters/golox/internal/scanner"
    "github.com/englishlayup/crafting_interpreters/golox/internal/token"
    "github.com/englishlayup/crafting_interpreters/golox/internal/interpreter"
)

type Interpreter = interpreter.Interpreter

type Lox struct {
    interpreter     Interpreter
	hadError        bool
	hadRuntimeError bool
}

func (lox *Lox) runFile(path string)  {
    fileData, err := os.ReadFile(path)
    if err != nil {
        log.Fatal(err)
    }

    lox.run(string(fileData))

    if lox.hadError {
        os.Exit(65)
    }
    if lox.hadRuntimeError {
        os.Exit(70)
    }
}

func (lox *Lox) runPrompt()  {
    reader := bufio.NewReader(os.Stdin)
    for {
        fmt.Print(">")
        input, err := reader.ReadString('\n')
        if err != nil {
            log.Fatal(err)
        }
        lox.run(input)
        lox.hadError = false
    }
}

func (lox *Lox) run(source string) error {
    scanner := scanner.NewScanner(source, lox.reportScannerError)
    tokens := scanner.ScanTokens()
    for _, t := range tokens {
        fmt.Print(t.Lexeme)
    }
    return nil
}

func (lox *Lox) reportScannerError(line int, message string)  {
    lox.report(line, "", message)
}

func (lox *Lox) reportError(t token.Token, message string)  {
    if t.TokenType == token.EOF {
        lox.report(t.Line, " at end", message)
    } else {
        lox.report(t.Line, fmt.Sprintf(" at '%v'", t.Lexeme), message)
    }
}

func (lox *Lox) report(line int, where string, message string)  {
    fmt.Fprintf(os.Stderr, "[line %v] Error%v: %v", line, where, message)
    lox.hadError = true
}
