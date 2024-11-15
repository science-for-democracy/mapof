[![PyPI Status](https://img.shields.io/pypi/v/mapof.svg)](https://pypi.python.org/pypi/mapof)
[![MainTests](https://github.com/science-for-democracy/mapof/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/science-for-democracy/mapof/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/github/science-for-democracy/mapof/branch/main/graph/badge.svg?token=XQ2W6SBI0V)](https://codecov.io/github/science-for-democracy/mapof)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Mapof

This open-source, MIT-licensed package is a core part of the Mapof ecosystem.
This framework allow for representing various features of (computational)
problem instances in the context of the instance structure in a visually
appealing way. Mapof is a direct successor of
[mapel](https://mapel.simple.ink/), which will be deprecated in the
(unforeseen) future.

## Mapel is abandoned, long live Mapof!!!
We've successively substituted mapel packages present when we decided
to start Mapof and have abandoned active development of mapel.
Here is a map of the old and new projects:
1. [~~mapel-core~~](https://pypi.org/project/mapel-core/) ==> [Mapof](https://pypi.org/project/mapof) 
2. [~~mapel-elections~~](https://pypi.org/project/mapel-elections/) ==> [Mapof-elections](https://pypi.org/project/mapof-elections) 
3. [~~mapel-roommates~~](https://pypi.org/project/mapel-rommmates/) ==> [Mapof-roommates](https://pypi.org/project/mapof-roommates) 
4. [~~mapel-marriagess~~](https://pypi.org/project/mapel-marriages/) ==> [Mapof-marriages](https://pypi.org/project/mapof-marriages) 

Hence, this package, Mapof, is a direct successor of mapel-core.

# Installation of Mapof
There are in principle three (standard to python packages) ways to install
Mapof. We *strongly* recommend installing the package from PyPi but you can
also: use the code as a local package or install the package from the local
code using some package manager.

## Installation from PyPi 
We recommend installing Mapof in a separate virtual environment (we use `venv`
but any reasonable environment manager should do). Installation from Pypi with
one of Python's package managers allows a seamless usage of Mapof with its
remaining modules, *that are to come soon*, which all declare Mapof as
dependency. A drawback is here that one cannot edit the Mapof code easily. If
you use `pip` type `pip install mapof` to get the newest version and your are
ready to go. If you use other package managers, do whatever it usually takes to
install packages from PyPi.
> [!TIP]
> You can still patch Mapof using the fact that functions are First-Class
> Citizens in Python. By separating changes from the actual Mapof code, the
> changes can later be easily changed to pull requests. And we would be very
> happy if you contribute to Mapof. For details, see the
> [section below](#patching-installation-from-pypi).

### Patching installation from PyPi
To patch function `mapof.bar.foo` you can define your own function `my_foo` and
then assign it using `mapof.bar.foo = mapof.bar.my_foo`. If you do this before
calling `mapof.bar.foo`, then each call to `mapof.bar.foo` will actually run
your `my_foo` function.

## Using code locally without package managers 
Using the code as a local package is another option. Doing so, by downloading
the package and importing different modules directly, comes with an easy way to
edit Mapof files. However, it enforces usage of all other Mapof packages in the
very same way. Trying installing other packages via some package manger will
most likely result in that you will be using the manager-downloaded PyPi
version of the Mapof module instead of your handcrafted one (there are
workarounds, but you probably know these tricks very well if you ever want to
take this path).

## Using code locally with package manager
A somewhat compromise solution is to fork the repo and install the package into
the package management system using your locally stored (perhaps edited) code.
This might have a drawback that you need to update your installation after
*every* change you make in the Mapof code.

However `pip` offers a handy solution here, the editable mode. Overall, using
`pip` you can pass to `pip install` the path to the project (where
`pyproject.toml` resides) and the `-e` switch. By this you get the best of two
worlds Mapof is managed by pip *and* your modifications of the package are
reflected immediately in the code that uses Mapof. This approach also have its
limitations but in most cases it should just work well. In case you experience
troubles, you should see what the `pip` documentation has to say about the
editable mode.

# Documentation

The complete documentation is available
[here](https://science-for-democracy.github.io/mapof/).

# Contribution

Feel free to contribute to Mapof using pull requests. We use
[black](https://pypi.org/project/black/) to enforce a coherent code style.

# Acknowledgments

This project is part of the [PRAGMA project](https://home.agh.edu.pl/~pragma/)
which has received funding from the [European Research Council
(ERC)](https://home.agh.edu.pl/~pragma/) under the European Union’s Horizon 2020
research and innovation programme ([grant agreement No
101002854](https://erc.easme-web.eu/?p=101002854)).



