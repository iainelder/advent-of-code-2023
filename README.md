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
