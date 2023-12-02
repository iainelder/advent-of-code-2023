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

A Game then is a list of Counters with a numeric ID. I model it as a class.

I need to parse a game object from a line of text. A factory function on the Game class seems like a neat way to do it.

Google `python class method factory`.

Reading:

* [Isaac Rodriguez from Real Python's "The Factory Method Pattern and Its Implementation in Python](https://realpython.com/factory-method-python/). Not my use case.
* [Danyson's How classmethod in Python helps in implementing Factory methods?](https://dev.to/danyson/how-classmethod-in-python-helps-in-implementing-factory-methods-23gl). Explains difference between `staticmethod` (no self) and `classmethod` (first argument is the class object). The example looks wrong. A factory class shouldn't subclass what it makes. Perhaps it's just poorly named and confusing matters with an abstract base class.
* [Henry Schreiner's "Factory classmethods in Python"](https://iscinumpy.gitlab.io/post/factory-classmethods-in-python/). A good example of using a `classmethod` factory to convert different representations of vectors. Goes into more advanced topics such as bypassing `__init__` with `__new__`. I don't need to do that here. The examples are untyped.

Google `python mypy classmethod factory`.

* https://stackoverflow.com/questions/46007544/python-3-type-hint-for-a-factory-method-on-a-base-class-returning-a-child-class
* https://github.com/python/typing/issues/58

Results are talking about generics and I don't care about that.

But I can just omit the type of `cls` in the same way that I omit the type of `self`. And the method returns a `Game` instance, so use a [mypy forward reference](https://mypy.readthedocs.io/en/stable/runtime_troubles.html#forward-references).

Is there elegant syntax to infix an operator in a list of values? Like this but without using `eval`.

```pycon
>>> hands = [Counter(red=3, blue=1, green=1), Counter(red=1, blue=4, green=1), Counter(red=1, blue=1, green=5)]
>>> "|".join([str(h) for h in hands])
"Counter({'red': 3, 'blue': 1, 'green': 1})|Counter({'blue': 4, 'red': 1, 'green': 1})|Counter({'green': 5, 'red': 1, 'blue': 1})"
>>> eval("|".join([str(h) for h in hands]))
Counter({'green': 5, 'blue': 4, 'red': 3})
```

Google `python infix a list`.

* [das-g's answer on Stack Overflow to "python infix operator on a list of objects"](https://stackoverflow.com/questions/41686624/python-infix-operator-on-a-list-of-objects)

Looks like a use for `reduce`.

```pycon
>>> from functools import reduce
>>> from operator import or_
>>> reduce(or_, hands)
Counter({'green': 5, 'blue': 4, 'red': 3})
```

The correct way to write the inclusion test is:

```python
hand <= bag
```

And you can read it as "Can you draw the hand from the bag?"

Replace List with Iterable. Do less to go faster. [See Mike Haertel's "why GNU grep is fast"](https://lists.freebsd.org/pipermail/freebsd-current/2010-August/019310.html). Here I don't need to index into the list of games. I just need to compute the max hand.

I had thought about using a complex regular expression to parse out the game from the line, but since I'm using a series of iterators that's not possible. Even if I did parse it all out at once I think it would be easier to read using string operations such as split and strip. I leard that once from a web scraping book with examples in PHP I read in 2010 (can't remember the author).
