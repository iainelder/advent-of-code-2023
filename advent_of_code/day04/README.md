# Day 4 Notes

## Part 2

The counter class is just what I need to count copies of cards and tell the total.

But it doesn't have an index that makes it easy to access the n+1'th card while iterating.

Try update method which updates counts instead of replacing items. I hope because I'm only updating keys that already exist that I won't break the iterator. Oh, that won't work because I can't index the next card.

The Counter indexes ah object by its hash. Change the `__hash__` method of the card to return its game ID. As long as the game IDs are inserted in sequental order (1, 2, 3, ...) then I can generate an index. A hashable object needs a `__hash__` method and a `__eq__` method.

No, that won't work because I still can't just use an int to index into the Counter.

Try copying the iterator and looking ahead.

That works! I implemented it first using itertools' `tee` function and its `take` recipe.

The more-itertools package has a peekable iterator. Try that to see if it makes the code simpler.

That works too. It's maybe slightly more readable, and may be more efficient although I don't test for that.
