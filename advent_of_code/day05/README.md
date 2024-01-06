# Day 5 Notes

2023-12-13.

Search Google for `1-dimensional rtree`.

* http://lin-ear-th-inking.blogspot.com/2007/06/packed-1-dimensional-r-tree.html
* https://stackoverflow.com/questions/23527175/data-structure-for-a-one-dimensional-spatial-index

Interval tree. https://en.wikipedia.org/wiki/Interval_tree

rtree is not the same as a range tree! https://en.wikipedia.org/wiki/Range_tree

Range searching. https://en.wikipedia.org/wiki/Range_searching

## Exploring in Python

2024-01-03.

The Wikipedia article on [Interval tree](https://en.wikipedia.org/wiki/Interval_tree) is a good enough starting point.

> In a simple case, the intervals do not overlap and they can be inserted into a simple binary search tree and queried in O ( log ⁡ n ) O(\log n) time.

Assume the intervals don't overlap so that I can use a binary search.

Ranges aren't naturally sortable.

```python
sorted([range(0, 69), range(69, 1)])
```

```text
TypeError: '<' not supported between instances of 'range' and 'range'
```

You can sort them with the start property.

```python
sorted([range(0, 69), range(69, 1)], key=lambda r: r.start)
```

```text
[range(0, 69), range(69, 1)]
```

Python's bisect module is a partial implementation of binary search. It looks awkward to use.

## Try to install intervaltree

Try the [intervaltree](https://github.com/chaimleib/intervaltree) module.

I get a weird error from Poetry.

```bash
poetry add intervaltree
```

```text
Using version ^3.1.0 for intervaltree

Updating dependencies
Resolving dependencies... (1.6s)

Package operations: 2 installs, 0 updates, 0 removals

  • Installing sortedcontainers (2.4.0)
  • Installing intervaltree (3.1.0): Failed

  ChefBuildError

  Backend 'setuptools.build_meta:__legacy__' is not available.

  at ~/.local/pipx/venvs/poetry/lib/python3.8/site-packages/poetry/installation/chef.py:147 in _prepare
      143│
      144│                 error = ChefBuildError("\n\n".join(message_parts))
      145│
      146│             if error is not None:
    → 147│                 raise error from None
      148│
      149│             return path
      150│
      151│     def _prepare_sdist(self, archive: Path, destination: Path | None = None) -> Path:

Note: This error originates from the build backend, and is likely not a problem with poetry but with intervaltree (3.1.0) not supporting PEP 517 builds. You can verify this by running 'pip wheel --use-pep517 "intervaltree (==3.1.0)"'.
```

Read [Poetry GitHub issue 7611](https://github.com/python-poetry/poetry/issues/7611). Randy Döring provided a fix for the issue in October 2023.

I was still using Poetry 1.6.1. I upgrade to Poetry 1.7.1.

```console
$ pipx upgrade poetry
upgraded package poetry from 1.6.1 to 1.7.1 (location: /home/isme/.local/pipx/venvs/poetry)
```

Another error now.

```console
$ poetry add intervaltree
Using version ^3.1.0 for intervaltree

Updating dependencies
Resolving dependencies... (1.1s)

Package operations: 1 install, 0 updates, 0 removals

  • Installing intervaltree (3.1.0): Failed

  ChefInstallError

  Failed to install wheel, setuptools >= 40.8.0.

  Output:
  Updating dependencies
  Resolving dependencies...

  Package operations: 2 installs, 0 updates, 0 removals

    • Installing setuptools (69.0.3)
    • Installing wheel (0.42.0)

    CalledProcessError

    Command '['/tmp/tmpxw72pzui/.venv/bin/python', '-I', '-W', 'ignore', '-c', '\nimport importlib.util\nimport json\nimport sys\n\nfrom pathlib import Path\n\nspec = importlib.util.spec_from_file_location(\n    "packaging", Path(r"/home/isme/.local/pipx/venvs/poetry/lib/python3.8/site-packages/packaging/__init__.py")\n)\npackaging = importlib.util.module_from_spec(spec)\nsys.modules[spec.name] = packaging\n\nspec = importlib.util.spec_from_file_location(\n    "packaging.tags", Path(r"/home/isme/.local/pipx/venvs/poetry/lib/python3.8/site-packages/packaging/tags.py")\n)\npackaging_tags = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(packaging_tags)\n\nprint(\n    json.dumps([(t.interpreter, t.abi, t.platform) for t in packaging_tags.sys_tags()])\n)\n']' returned non-zero exit status 1.

    at /usr/lib/python3.8/subprocess.py:516 in run
         512│             # We don't call process.wait() as .__exit__ does that for us.
         513│             raise
         514│         retcode = process.poll()
         515│         if check and retcode:
      →  516│             raise CalledProcessError(retcode, process.args,
         517│                                      output=stdout, stderr=stderr)
         518│     return CompletedProcess(process.args, retcode, stdout, stderr)
         519│
         520│

  The following error occurred when trying to handle this error:


    EnvCommandError

    Command ['/tmp/tmpxw72pzui/.venv/bin/python', '-I', '-W', 'ignore', '-c', '\nimport importlib.util\nimport json\nimport sys\n\nfrom pathlib import Path\n\nspec = importlib.util.spec_from_file_location(\n    "packaging", Path(r"/home/isme/.local/pipx/venvs/poetry/lib/python3.8/site-packages/packaging/__init__.py")\n)\npackaging = importlib.util.module_from_spec(spec)\nsys.modules[spec.name] = packaging\n\nspec = importlib.util.spec_from_file_location(\n    "packaging.tags", Path(r"/home/isme/.local/pipx/venvs/poetry/lib/python3.8/site-packages/packaging/tags.py")\n)\npackaging_tags = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(packaging_tags)\n\nprint(\n    json.dumps([(t.interpreter, t.abi, t.platform) for t in packaging_tags.sys_tags()])\n)\n'] errored with the following return code 1

    Error output:
    Traceback (most recent call last):
      File "<string>", line 18, in <module>
      File "<frozen importlib._bootstrap_external>", line 883, in exec_module
      File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
      File "/home/isme/.local/pipx/venvs/poetry/lib/python3.8/site-packages/packaging/tags.py", line 7, in <module>
        import distutils.util
    ModuleNotFoundError: No module named 'distutils.util'


    at ~/.local/pipx/venvs/poetry/lib/python3.8/site-packages/poetry/utils/env/base_env.py:354 in _run
        350│                 output = subprocess.check_output(
        351│                     cmd, stderr=stderr, env=env, text=True, **kwargs
        352│                 )
        353│         except CalledProcessError as e:
      → 354│             raise EnvCommandError(e)
        355│
        356│         return output
        357│
        358│     def execute(self, bin: str, *args: str, **kwargs: Any) -> int:

  Cannot install setuptools.


    CalledProcessError

    Command '['/tmp/tmpxw72pzui/.venv/bin/python', '-I', '-W', 'ignore', '-c', '\nimport importlib.util\nimport json\nimport sys\n\nfrom pathlib import Path\n\nspec = importlib.util.spec_from_file_location(\n    "packaging", Path(r"/home/isme/.local/pipx/venvs/poetry/lib/python3.8/site-packages/packaging/__init__.py")\n)\npackaging = importlib.util.module_from_spec(spec)\nsys.modules[spec.name] = packaging\n\nspec = importlib.util.spec_from_file_location(\n    "packaging.tags", Path(r"/home/isme/.local/pipx/venvs/poetry/lib/python3.8/site-packages/packaging/tags.py")\n)\npackaging_tags = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(packaging_tags)\n\nprint(\n    json.dumps([(t.interpreter, t.abi, t.platform) for t in packaging_tags.sys_tags()])\n)\n']' returned non-zero exit status 1.

    at /usr/lib/python3.8/subprocess.py:516 in run
         512│             # We don't call process.wait() as .__exit__ does that for us.
         513│             raise
         514│         retcode = process.poll()
         515│         if check and retcode:
      →  516│             raise CalledProcessError(retcode, process.args,
         517│                                      output=stdout, stderr=stderr)
         518│     return CompletedProcess(process.args, retcode, stdout, stderr)
         519│
         520│

  The following error occurred when trying to handle this error:


    EnvCommandError

    Command ['/tmp/tmpxw72pzui/.venv/bin/python', '-I', '-W', 'ignore', '-c', '\nimport importlib.util\nimport json\nimport sys\n\nfrom pathlib import Path\n\nspec = importlib.util.spec_from_file_location(\n    "packaging", Path(r"/home/isme/.local/pipx/venvs/poetry/lib/python3.8/site-packages/packaging/__init__.py")\n)\npackaging = importlib.util.module_from_spec(spec)\nsys.modules[spec.name] = packaging\n\nspec = importlib.util.spec_from_file_location(\n    "packaging.tags", Path(r"/home/isme/.local/pipx/venvs/poetry/lib/python3.8/site-packages/packaging/tags.py")\n)\npackaging_tags = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(packaging_tags)\n\nprint(\n    json.dumps([(t.interpreter, t.abi, t.platform) for t in packaging_tags.sys_tags()])\n)\n'] errored with the following return code 1

    Error output:
    Traceback (most recent call last):
      File "<string>", line 18, in <module>
      File "<frozen importlib._bootstrap_external>", line 883, in exec_module
      File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
      File "/home/isme/.local/pipx/venvs/poetry/lib/python3.8/site-packages/packaging/tags.py", line 7, in <module>
        import distutils.util
    ModuleNotFoundError: No module named 'distutils.util'


    at ~/.local/pipx/venvs/poetry/lib/python3.8/site-packages/poetry/utils/env/base_env.py:354 in _run
        350│                 output = subprocess.check_output(
        351│                     cmd, stderr=stderr, env=env, text=True, **kwargs
        352│                 )
        353│         except CalledProcessError as e:
      → 354│             raise EnvCommandError(e)
        355│
        356│         return output
        357│
        358│     def execute(self, bin: str, *args: str, **kwargs: Any) -> int:

  Cannot install wheel.



  Error:


  at ~/.local/pipx/venvs/poetry/lib/python3.8/site-packages/poetry/installation/chef.py:102 in install
       98│             InstalledRepository.load(self._env),
       99│         )
      100│         installer.update(True)
      101│         if installer.run() != 0:
    → 102│             raise ChefInstallError(requirements, io.fetch_output(), io.fetch_error())
      103│
      104│
      105│ class Chef:
      106│     def __init__(

Cannot install build-system.requires for intervaltree.


```

The errors metion Poetry 3.8, so the problem is in the virtual environment of Poetry itself.

Try using a later verion of Python for Poetry. I'm not sure why this would fix it, but let's try it.

```console
$ pipx uninstall poetry
uninstalled poetry! ✨ 🌟 ✨
$ pipx install --python python3.10 poetry
  installed package poetry 1.7.1, installed using Python 3.10.13
  These apps are now globally available
    - poetry
done! ✨ 🌟 ✨
```

Now I can install intervaltree without a problem.

```console
$ poetry add intervaltree
Using version ^3.1.0 for intervaltree

Updating dependencies
Resolving dependencies... (0.8s)

Package operations: 1 install, 0 updates, 0 removals

  • Installing intervaltree (3.1.0)

Writing lock file
```

## Explore intervaltree

It works as I expect, and I don't have to worry about how to implement the search.

```python
from intervaltree import IntervalTree, Interval
tree = IntervalTree([Interval(0, 69), Interval(69, 70)])
tree[1]
tree[70]
```

```python
{Interval(0, 69)}
set()
```

To get the interval that contains the point:

```python
next(iter(tree[0]))
```

I want to use syntax like this to solve the problem.

```python
almanac.seed(3)["location"].number
```

## Solve part 1

2024-01-04.

Thinking first about what the solution syntax looks like and then writing a lot of unit tests around the parts helped to develop a clean implementation.

## Spñve part 2

2024-01-04.

I should be able to solve this with only a small change to processing of the seed number input.

Upgrade to Python 3.12 to use the `batched` function of itertools. Check notes from day 2 for how to upgrade from Python 3.8 to Python 3.10.

```bash
sudo apt install python3.12 # From deadsnakes PPA
poetry env use python3.12
poetry install
poetry run pre-commit run --all-files
```

All the tests still pass, and there is one warning about a deprecated datetime method. I don't know where it comes from. I don't call the method in my own code.

```text
================================================== warnings summary ==================================================
../../../.cache/pypoetry/virtualenvs/advent-of-code-fP-JUSe0-py3.12/lib/python3.12/site-packages/dateutil/tz/tz.py:37
  /home/isme/.cache/pypoetry/virtualenvs/advent-of-code-fP-JUSe0-py3.12/lib/python3.12/site-packages/dateutil/tz/tz.py:37: DeprecationWarning: datetime.datetime.utcfromtimestamp() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.fromtimestamp(timestamp, datetime.UTC).
    EPOCH = datetime.datetime.utcfromtimestamp(0)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
```

The redifinition of the problem exploded the amount of work that my program has to do. This is the first puzzle that doesn't complete too quickly to time. It's churning away for several seconds, minutes, long enough for me to take a break and come back. This is the first puzzle where optimization may matter.

I cancel about 12 minutes into the run. It's doing a stupid amount of extra work because it's mapping each value in a range where most of the sources will have the same destination.

## Use range indexes to find unique ranges

2024-01-04.

Cases to consider:

1. Source interval is a subset of a range -> Translate to one destination interval
2. Search interval overlaps a range -> Split source and treat part like 1 and part like 4
3. Search interval contains a range -> Split source and treat part like 1 and part like 4
4. Search interval is disjoint from all ranges - No translation; destination interval is the same

I need to break down each source interval to a set of intervals in case 1 and case 4.

## Consider now to refactor the solution

2023-12-06.

I extracted a "seed locator" class. Now the almanac and its supporters are just data classes. Now I can more easily add a "range locator" class.

I removed any code to solve the day 2 part since it wasn't working properly anyway.
