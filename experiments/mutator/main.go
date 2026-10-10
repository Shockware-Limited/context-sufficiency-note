// Command mutator injects exactly one body-only, signature-preserving mutant into a Go
// source file and prints a JSON record describing it. It never touches declarations,
// signatures, exported names, or imports, so the package's interface is unchanged.
//
// Usage: mutator -file path/to/file.go -seed N
// Exit code 3 means "no mutation site found" (caller should pick another file/seed).
package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"go/ast"
	"go/format"
	"go/parser"
	"go/token"
	"math/rand"
	"os"
	"strconv"
)

type site struct {
	apply func() string // applies the mutation, returns operator name
	fn    string
	line  int
}

func main() {
	file := flag.String("file", "", "Go source file to mutate (in place)")
	seed := flag.Int64("seed", 1, "random seed")
	flag.Parse()
	if *file == "" {
		fmt.Fprintln(os.Stderr, "need -file")
		os.Exit(2)
	}
	src, err := os.ReadFile(*file)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
	fset := token.NewFileSet()
	f, err := parser.ParseFile(fset, *file, src, parser.ParseComments)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}

	var sites []site
	for _, d := range f.Decls {
		fd, ok := d.(*ast.FuncDecl)
		if !ok || fd.Body == nil {
			continue
		}
		fname := fd.Name.Name
		ast.Inspect(fd.Body, func(n ast.Node) bool {
			switch x := n.(type) {
			case *ast.BinaryExpr:
				if alt, ok := swapOp(x.Op); ok {
					line := fset.Position(x.OpPos).Line
					sites = append(sites, site{fn: fname, line: line, apply: func() string {
						from := x.Op.String()
						x.Op = alt
						return "binop:" + from + "->" + alt.String()
					}})
				}
			case *ast.IfStmt:
				if x.Cond != nil {
					line := fset.Position(x.If).Line
					sites = append(sites, site{fn: fname, line: line, apply: func() string {
						x.Cond = &ast.UnaryExpr{Op: token.NOT, X: &ast.ParenExpr{X: x.Cond}}
						return "negate-if"
					}})
				}
			case *ast.BasicLit:
				if x.Kind == token.INT {
					if v, err := strconv.Atoi(x.Value); err == nil {
						line := fset.Position(x.ValuePos).Line
						sites = append(sites, site{fn: fname, line: line, apply: func() string {
							x.Value = strconv.Itoa(v + 1)
							return "int+1"
						}})
					}
				}
				if x.Kind == token.STRING && len(x.Value) >= 2 && x.Value[0] == '"' {
					line := fset.Position(x.ValuePos).Line
					sites = append(sites, site{fn: fname, line: line, apply: func() string {
						x.Value = x.Value[:len(x.Value)-1] + `x"`
						return "str+x"
					}})
				}
			}
			return true
		})
	}
	if len(sites) == 0 {
		os.Exit(3)
	}
	r := rand.New(rand.NewSource(*seed))
	s := sites[r.Intn(len(sites))]
	op := s.apply()

	var buf bytes.Buffer
	if err := format.Node(&buf, fset, f); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
	if bytes.Equal(buf.Bytes(), src) {
		os.Exit(3)
	}
	if err := os.WriteFile(*file, buf.Bytes(), 0o644); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
	_ = json.NewEncoder(os.Stdout).Encode(map[string]any{
		"file": *file, "func": s.fn, "line": s.line, "operator": op, "sites": len(sites),
	})
}

func swapOp(op token.Token) (token.Token, bool) {
	switch op {
	case token.EQL:
		return token.NEQ, true
	case token.NEQ:
		return token.EQL, true
	case token.LSS:
		return token.GEQ, true
	case token.GTR:
		return token.LEQ, true
	case token.LEQ:
		return token.GTR, true
	case token.GEQ:
		return token.LSS, true
	case token.ADD:
		return token.SUB, true
	case token.SUB:
		return token.ADD, true
	case token.LAND:
		return token.LOR, true
	case token.LOR:
		return token.LAND, true
	}
	return 0, false
}
