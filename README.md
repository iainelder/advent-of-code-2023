# Advent of Code 2023

My solutions to the Advent of Code competition.

The primary goal is of course to solve each puzzle.

The secondary goal is to learn more about the Python programming language, its standard library, its ecosystem of packages, and its support community.

## What I learned

### Day 1

* The input and the solutions are unique for each user, so I don't feel bad about sharing those
* The `regex` package provides a simple flag to search backwards
* [The standard `re` package can search backwards by prepending `(?s:.*)`](https://stackoverflow.com/a/33233868/111424)
* A class-based solution is easier to test

### Day 2

[See full notes for day 2](advent_of_code/day02/README.md).

* The Counter class checks multiset containment as of Python 3.10.
* Poetry can declare a different dependency version for each Python version.
* It's easy to switch between Python versions in Poetry
* Moving tests is easy with PyTest because it discovers based on name
* It's easier to group the test day with each day's solution
* Use table-driven tests to avoid test code repitition
* Part 2 was easy because I already found a good abstraction in part 1 (`max_hand` is what they call the "minimum set of cubes")

## Day 3

[See full notes for day 3](advent_of_code/day03/README.md)

* Researching the tools takes longer than coding the solution
* [Lark](https://github.com/lark-parser/lark) provides a tokenizer for strings confugirable using a declarative language to describe a grammar.
* Lark counts token row and column positions in the string
* [GeoPandas](https://geopandas.org/en/stable/) is a geopspatial extension to Pandas
* GeoPandas supports spatial joins
* GeoPandas probably uses an [R-tree](https://en.wikipedia.org/wiki/R-tree) implementation from its [Shapely](https://shapely.readthedocs.io/en/stable/strtree.html) or [rtree](https://rtree.readthedocs.io/en/latest/index.html) dependencies

## Day 4

* Exponent is not the same as iterated multiplication! `2 ** 0 = 1` and `2 ** -1 = 0.5`.

## Day 5

* Poetry's own virtualenv can cause problems when installing packages that need things like distutils to install them.
* Use Pipx's `--python` option to choose a later Python runtime to avoid those problems
