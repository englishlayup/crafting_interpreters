package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

type Lox struct {
	interpreter     Interpreter
	hadError        bool
	hadRuntimeError bool
}

func (lox Lox) runFile(path string)  {
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

func (lox Lox) runPrompt()  {
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

func (lox Lox) run(source string)  {
}

func (lox Lox) report(line int, where string, message string)  {
    fmt.Fprintf(os.Stderr, "[line %v] Error%v: %v", line, where, message)
    lox.hadError = true
}
