[![MainTests](https://github.com/science-for-democracy/mapof/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/science-for-democracy/mapof/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/github/science-for-democracy/mapof/branch/main/graph/badge.svg?token=XQ2W6SBI0V)](https://codecov.io/github/science-for-democracy/mapof)

# Mapof

This package is a core part of the mapof ecosystem. This framework allow for
representing various features of (computational) problem instances in the
context of the instance structure in a visually appealing way. Mapof is a
direct successor of [mapel](https://mapel.simple.ink/), which will become
deprecated in some the (unforeseen) future.

## Current status of mapof vs mapel
When decided to start mapof and abandon active development of mapel, the latter
consisted of the following packages:
1. [mapel-core](https://pypi.org/project/mapel-core/)
1. [mapel-elections](https://pypi.org/project/mapel-elections/)
1. [mapel-roommates](https://pypi.org/project/mapel-rommmates/)
1. [mapel-marriages](https://pypi.org/project/mapel-marriages/)

This package is direct successor of mapel-core. Currently, *no* other packages
are provided in mapof. The development is ongoing.

# Installation of mapof
There are in principle three (standard to python packages) ways to install
mapof. We *strongly* recommend installing the package from PyPi but the other
two are using the code as a local package and installing package from local
code using some package manager.

## Installation from PyPi 
We recommend installing mapof in a separate virtual environment (we use `venv`
but any reasonable environment manager should do). Installation from Pypi with
one of Python's package managers allows a seamless usage of mapof with its
remaining modules, *that are to come soon*, which all declare mapof as
dependency. A drawback is here that one cannot edit the mapof code easily. If
you use `pip` type `pip install mapof` to get the newest version and your are
ready to go. If you use other package manager, do whatever it usually needs to
instal packages from PyPi.

## Using code locally without package managers 
Using the code as a local package is another option. Doing so, by downloading
the package and importing different modules directly, comes with an easy way to
edit mapof files. However, it enforces usage of all other mapof packages in the
very same way. Trying installing other packages via some package manger will
most likely result in that you will be using the manager-downloaded PyPi
version of the mapof module instead of your handcrafted one (there are
workarounds, but you probably know these tricks very well if you ever want to
take this path).

## Using code locally with package manager
A somewhat compromise solution is to fork the repo and install the package into
the package management system using your locally stored (perhaps edited) code.
This might have a drawback that you need to update your installation after
*every* change you make in the mapof code.

However `pip` has a handy solution here, the editable mode. Overall, using
`pip` you can pass to `pip install` the path to the project (where
`pyproject.toml` resides) and the `-e` switch. By this you get the best of two
world mapof is managed by pip *and* your modifications of the package are
reflected immediately in the code that uses mapof. This approach also have its
limitations but in most cases it should just work well. In case you experience
troubles, you should see what the `pip` documentation has to say about the
editable mode.

# Acknowledgments

This project is part of the [PRAGMA project](https://home.agh.edu.pl/~pragma/)
which has received funding from the [European Research Council
(ERC)](https://home.agh.edu.pl/~pragma/) under the European Union’s Horizon 2020
research and innovation programme ([grant agreement No
101002854](https://erc.easme-web.eu/?p=101002854)).



