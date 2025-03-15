package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) > 2 {
		fmt.Fprintf(os.Stderr, "Usage: golox [script]")
		os.Exit(64)
	} else if len(os.Args) == 2 {
		lox := Lox{}
		lox.runFile(os.Args[1])
	} else {
		lox := Lox{}
		lox.runPrompt()
	}
}
