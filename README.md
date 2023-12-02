# Advent of Code 2023

My solutions to the Advent of Code competition.

The primary goal is of course to solve each puzzle.

The secondary goal is to learn more about the Python programming language, its standard library, its ecosystem of packages, and its support community.

## What I learned

* The input and the solutions are unique for each user, so I don't fee bad about sharing those (day 1).
* The `regex` package provides a simple flag to search backwards (day 1).
* [The standard `re` package can search backwards by prepending `(?s:.*)`](https://stackoverflow.com/a/33233868/111424) (day 1).
* The Counter class checks multiset containment as of Python 3.10 (day 2).
* Poetry can declare a different dependency version for each Python version (day 2).

## Day 2 notes

2023-12-02.

I need a "bag" or a "multiset" data structure with a `contains` operation.

The `contains` operation takes another instance as its sole argument. It returns `True` if the count of each element in arg is lesser than or equal to the count of the corresponding element in self. It returns `False` if there is any element in arg that doesn't exist in self.

Reading:

* [Leodanis Pazo Ramos from Real Python](https://realpython.com/python-counter/) shows how to use [Python's `Counter` class](https://docs.python.org/3/library/collections.html#collections.Counter) as a multiset.
* [Dan Bader from Real Python's list of data structures in the standard library](https://realpython.com/python-data-structures/)
* [Farley Knight's Three Implementations of Bag in Python](https://dev.to/farleyknight/three-implementations-of-a-bag-in-python-585p)

Start reading Real Python's Counter article from "Using Counter Instances as Multisets".

See "Subtracting the Elements' Multiplicity" from Real Python's Counter article. If `subtract` gives a negative count for any element, then `contains` would return `False`. You can check for negative counts using the unary minus (`-`).

See "Doing Arithmetric With Elements' Multiplicity". The union operator (`|`) returns the maximum of counts.

From Counter's documentation:

> Several mathematical operations are provided for combining Counter objects to produce multisets (counters that have counts greater than zero). Addition and subtraction combine counters by adding or subtracting the counts of corresponding elements. Intersection and union return the minimum and maximum of corresponding counts. Equality and inclusion compare corresponding counts. Each operation can accept inputs with signed counts, but the output will exclude results with counts of zero or less.

"Equality and inclusion compare corresponding counts." This sounds like a way to implement `contains`.

"Intersection and union return the minimum and maximum of corresponding counts." This sounds like a way to aggregate a game's handfuls into a single object to compare with the bag.

The inclusion operator is `<=`.

I rename the variables in the example to match my use case. It all goes well until the inclusion operator.

```pycon
>>> from collections import Counter
>>> bag = Counter(red=3, blue=1)
>>> hand = Counter(red=1, blue=2)
>>> bag + hand
Counter({'red': 4, 'blue': 3})
>>> bag - hand
Counter({'red': 2})
>>> bag & hand
Counter({'red': 1, 'blue': 1})
>>> bag | hand
Counter({'red': 3, 'blue': 2})
>>> bag == hand
False
>>> bag <= hand
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: '<=' not supported between instances of 'Counter' and 'Counter'
```

Python 3.8 doesn't implement inclusion. The 3.8 documentation omits it.

Equality and inclusion first appear in the 3.10 documentation.

> Counters support rich comparison operators for equality, subset, and superset relationships: `==`, `!=`, `<`, `<=`, `>`, `>=`. All of those tests treat missing elements as having zero counts so that `Counter(a=1) == Counter(a=1, b=0)` returns true.
>
> _New in version 3.10:_ Rich comparison operations were added.

The system Python is 3.8, so that's what Poetrry uses by default. I installed Python 3.10 using PyEnv. How do I configure Poetry to use Python 3.10?

```console
$ poetry env use python3.10
Creating virtualenv advent-of-code-fP-JUSe0-py3.10 in /home/isme/.cache/pypoetry/virtualenvs
Using virtualenv: /home/isme/.cache/pypoetry/virtualenvs/advent-of-code-fP-JUSe0-py3.10

$ poetry env list
advent-of-code-fP-JUSe0-py3.10 (Activated)
advent-of-code-fP-JUSe0-py3.8
```

I just realised that Poetry also needs a way to declare a different dependency version for each Python version.

[Thanks to someone asking the same question on Stack Overflow](https://stackoverflow.com/questions/65945929/poetry-how-to-publish-project-packages-targeting-multiple-python-versions), I find that [Poetry has concise syntax for "multiple constraints dependencies"](https://python-poetry.org/docs/dependency-specification/#multiple-constraints-dependencies).

```toml
[tool.poetry.dependencies]
foo = [
    {version = "<=1.9", python = ">=3.6,<3.8"},
    {version = "^2.0", python = ">=3.8"}
]
```

I don't think I need to use it here, because I'll just start using Python 3.10. But it may help in a project such as Sceptre which targets different Python versions.

The tests for day 1 pass in Python 3.10. So I update `pyproject.toml` to make that the minimum verison and delete the Python 3.8 environment.

```console
$ poetry env remove python3.8
Deleted virtualenv: /home/isme/.cache/pypoetry/virtualenvs/advent-of-code-fP-JUSe0-py3.8
```

And the inclusion operator works in Python 3.10. It seems to meet my requirements.

```pycon
>>> bag = Counter(red=3, blue=1)
>>> hand = Counter(red=1, blue=2)
>>> bag <= hand
False
>>> hand = Counter(red=1, blue=1, green=1)
>>> bag <= hand
False
```
