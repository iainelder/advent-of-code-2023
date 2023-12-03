# Day 3 Notes

I want read every character in the text no more than once. I need a tokenizer that stores the horizontal and vertical position of each token in the text. Python's tokenizer module does it but is specialized for Python source code and doesn't appear to be configurable for other languages.

## Reading about parsers, lexes, and scanners

I read [pythonmembers.club's "building a lexer in python - a tutorial"](https://medium.com/@pythonmembers.club/building-a-lexer-in-python-a-tutorial-3b6de161fe84) to understand that maybe what I need is a lexer.

Google `python configurable lexer`.

* https://stackoverflow.com/questions/9100704/implementing-a-customizable-lexer-class-in-python - not helpful
* https://pygments.org/docs/lexerdevelopment/ - for highlighting in Pygments. Probably not what I need.
* https://github.com/aubreyrjones/lemon-py - well documented, but just 12 stars and no updates in 2 years
* https://github.com/lark-parser/lark - this is a proper library for parsing. See below.
* https://www.reddit.com/r/Python/comments/e0g512/best_python_parser_lexer_generators/ - recommends lark. The Python reddit has an Advent of Code 2023 banner right now!
* https://ipython.readthedocs.io/en/stable/api/generated/IPython.lib.lexers.html - for hightlighting in IPython. Probably not what I need.
* https://pypi.org/project/pylexer/ - I need something like this
* https://www.quora.com/I-need-to-write-a-parser-in-Python-What-are-some-good-resources-that-can-help-me-with-this. Taine Zhao: "Pyparsing and PLY are both not that good, and pyparsing still has its case, while PLY is totally out of date. There’re many alternatives in current day. Search PyPI using following keywords ...:"
* http://python-history.blogspot.com/2018/05/the-origins-of-pgen.html
* https://www.dabeaz.com/ply/ply.html - this looks good. See below

Google `python string scanner`.

* https://stackoverflow.com/questions/1751949/python-equivalent-of-rubys-stringscanner - many answers over 10 years old. Nothing current.

undocumented Scanner class in re module

Google `python re scanner`.

* [Armin Ronacher's "Python's Hidden Regular Expression Gems"](https://github.com/mitsuhiko/python-regex-scanner/tree/master) shows how to use the undocumented Scanner class and provides an experimental solution on GitHub to enhance it. He is also the author of the Flask framework. This is great for learning, but surely there must be a properly maintained Scanner package.

---

## Regular expression?

I haven't read any of the above yet. I just got an idea of what's out there.

An even simpler way to do it would be to scan and remember two lines ahead and two lines back.

If we assume that every line is the same length, that the file describes a grid, then I can use a constant-size buffer to do that.

Can I use a multiline regular expression to detect matching cases? (I discard this line of thought because the expression isn't regular but it varies according to how far from a newline the part symbol is.)

## Test harness

First write a test harness to test simple cases, even more simple than the the sample input.

I want to make a dedented file writer to make the tests easy to read inline. How do I override a method with typing? I want to override `write_text` or add a new method with the same signature that calls it.

Google `python override method`.

Or do I just want to add a method to the Path class? Because the test framework gives me Path object.

Google `python add method to class`.

Reading:

* [Sean Osier's "How to Add a Methof to an Existing Class in Python](https://www.seanosier.com/2021/03/20/python-add-method-existing-class/) shows that it's as simple as adding a new property to the class name that is a function with a self argument.

But that doesn't make sense to the type checker.

Can I convert or coerce a Path object to a subclass instance?

Google `python coerce object to subclass`.

I don't need the full set of Path functions. I just need a function to write the file contents. So instead of inheritance use composition.

If I do this, then I can just use the function that I would have attached directly, without attaching it. Pass the object in explcitly instead of hiding that with self.

## PLY (Python Lex-Yacc)

Read [David M Beazley's documentation for PLY](https://www.dabeaz.com/ply/ply.html).

Things I like and will look for in other implementations:

[Index](http://www.dabeaz.com/ply/index.html):

* "Because of its use in an instructional setting, a lot of work went into providing extensive error checking."
* "[PLY compared with pyparsing and ANTLR](http://www.dalkescientific.com/writings/diary/archive/2007/11/03/antlr_java.html) by Andrew Dalke."
* Cites real projects using it. Some are popular and even current.

Documentation:

* "You will probably want to consult an introductory text such as "Compilers: Principles, Techniques, and Tools", by Aho, Sethi, and Ullman. O'Reilly's "Lex and Yacc" by John Levine may also be handy. In fact, the O'Reilly book can be used as a reference for PLY as the concepts are virtually identical."
* "The `lex.py` module is used to break input text into a collection of tokens specified by a collection of regular expression rules"
* "Unlike traditional lex/yacc which require a special input file that is converted into a separate source file, the specifications given to PLY are valid Python programs."
* "The tokens returned by `lexer.token()` are instances of `LexToken`. This object has attributes `tok.type`, `tok.value`, `tok.lineno`, and `tok.lexpos`."

```console
$ python example.py
LexToken(NUMBER,3,2,1)
LexToken(PLUS,'+',2,3)
LexToken(NUMBER,4,2,5)
LexToken(TIMES,'*',2,7)
LexToken(NUMBER,10,2,10)
LexToken(PLUS,'+',3,14)
LexToken(MINUS,'-',3,16)
LexToken(NUMBER,20,3,18)
LexToken(TIMES,'*',3,20)
LexToken(NUMBER,2,3,21)
```

I don't think I need the `yacc` part for the context-free grammar.

Things I don't like:

* You have to compute the line number and the column number yourself (See "Line numbers and positional information"), but it does show you how to do that.
* [PLY. A different tool for implementing LALR(1) parsers in Python. Instead of abusing metaprogramming \[like SLY\], it abuses doc-strings.](https://www.dabeaz.com/software.html) If it works, then not a deal breaker, but sounds like it's doing something weird to enable cute syntax.
* ["Important Notice - October 27, 2022: The PLY project will make no further package-installable releases. If you want the latest version, you'll need to download it here or clone the repo."](https://github.com/dabeaz/ply) Not installable by pip? That's a deal breaker.

Notes:

* [LALR parser](https://en.wikipedia.org/wiki/LALR_parser) - look-ahead, left-to-right, rightmost derivation parser.
* ["What is a Context-Sensitive Grammar/Language?"](https://www.youtube.com/watch?v=PjXA2cvfHF0&t=2s) - rabit hole!

## Lark Parser

This looks like a good place to start. It's widely used, frequently updated, and has a lot of contributors.

It's used by a lot of projects, including Poetry.

Compares to other options with benchmarks:

* [PLY](http://www.dabeaz.com/ply/)
* [PyParsing](https://github.com/pyparsing/pyparsing)
* [Parsley](https://pypi.python.org/pypi/Parsley)
* [Parsimonious](https://github.com/erikrose/parsimonious)
* [ANTLR](https://github.com/antlr/antlr4)

[Repositories that depend on Lark](https://github.com/lark-parser/lark/network/dependents?package_id=UGFja2FnZS01MjI1OTE0NQ%3D%3D):

* https://github.com/bodnarbm/advent-of-code-2023
* https://github.com/dbfarrow/adventofcode-2023

At least two people have tried this already! I won't read their code, but It¡s good enough to know that they have tried this.

But I don't want to define a grammar. I just want a lexer. Can I do that?

> Lark implements both Earley(SPPF) and LALR(1), and several different lexers

Sounds like it's possible.

Jump into the [documentation](https://lark-parser.readthedocs.io/en/stable/) to see.

I like:

* "Fast unicode lexer with regexp support, and automatic line-counting"
* "Automatically keep track of line & column numbers"
* "Automatic line & column tracking (for both tokens and matched rules)"
* "Warns on regex collisions using the optional `interegular` library. (read more)"
* "Standard library of terminals (strings, numbers, names, etc.)"
* "Unicode fully supported"
* "Extensive test suite"
* "Type annotations (MyPy support)"
* "Pure-Python implementation"

A "terminal" in grammar-speak is something that doesn't need to be broken down into something more basic. So it would be a symbol or a number.

I don't see how to control the lexer explicitly. It all seems automatic via the grammar. Maybe I can write a simple grammar to detect just symbols and numbers and get the line and column info.

See [source code `common.lark`](https://github.com/lark-parser/lark/blob/master/lark/grammars/common.lark) for the list of common terminals. I can't find this listing in the documentation.

```python
from lark import Lark

parser = Lark(
    r"""
    value: NUMBER

    %import common.NUMBER
    %import common.WS
    %ignore WS
    """,
    start="value"
)
```

It appears to track the line and column automatically, which I need to find the numbers adjacent to symbols.

```pycon
>>> tree = parser.parse("1")
>>> tree
Tree(Token('RULE', 'value'), [Token('NUMBER', '1')])
>>> token = tree.children[0]
>>> token
Token('NUMBER', '1')
>>> token.start_pos
0
>>> token.column
1
>>> token.line
1
>>> token.end_pos
1
>>> token.end_line
1
>>> token.end_column
2
```

```python
parser = Lark(
    r"""
    value: NUMBER*

    %import common.NUMBER
    %import common.WS
    %ignore WS
    """,
    start="value"
)
```

```pycon
>>> tree = parser.parse("1 22 333")
>>> tree
Tree(Token('RULE', 'value'), [Token('NUMBER', '1'), Token('NUMBER', '22'), Token('NUMBER', '333')])
>>> for token in tree.children:
...     token.column
...
1
3
6
```

Can it parse incrementally or as a stream? And can I implement behavior for certain symbols?

Search for `stream` in the docs gives one result for ["Custom lexer"](https://lark-parser.readthedocs.io/en/stable/examples/advanced/custom_lexer.html) in Advanced Examples.

The example shows how to extend the `Lexer` class to parse arbitrary objects. I don't need to do that, but I have learned that there is a public `Lexer` class.

```python
from lark.lexer import Lexer
```

The `help` shows no documentation, so maybe I'm not supposed to use that.

The main `Lark` class has a `lex` method that returns `Iterator[Token]`.

`Lark` has a `lex_callbacks` property. It's a dictionary of callbacks for the lexer that may alter tokens during lexing.

The `lex` and `parse` methods both take `str` arguments. Can they stream from a file?

Google `lark stream from file`.

https://github.com/lark-parser/lark/issues/488#issuecomment-691723113

> What I think you're asking for, which is to parse a large file without having to load all of it into memory, is something that Lark already does.
>
> 1. Python automatically buffers files as they are being read
> 2. Lark supports the `transformer=...` option, which applies a transformer as the text is being parsed, rule by rule, instead of building a whole tree first. You don't have to create a tree, or store the parsed data, if you choose to.
>
> All you have to do is something like this:
>
> ```python
> parser = Lark.open("my_grammar.lark", parser="lalr", transformer=MyTransformer())
> with open("my_input.json") as f:
>     result = parser.parse(f)
> ```

So I think what I really need is a [transformer](https://lark-parser.readthedocs.io/en/stable/visitors.html) to filter out the parsed elements that I don't need.

```python
from lark import Lark, Transformer

grammar = r"""
value: NUMBER*
%import common.NUMBER
%import common.WS
%ignore WS
"""

parser = Lark(grammar)

tree = parser.parse("1 22 333")
```
