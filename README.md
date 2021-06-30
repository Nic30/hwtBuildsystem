# hwtBuildsystem
[![CircleCI](https://circleci.com/gh/Nic30/hwtBuildsystem.svg?style=svg)](https://circleci.com/gh/Nic30/hwtBuildsystem)
[![PyPI version](https://badge.fury.io/py/hwtBuildsystem.svg)](http://badge.fury.io/py/hwtBuildsystem)
[![Coverage Status](https://coveralls.io/repos/github/Nic30/hwtBuildsystem/badge.svg?branch=master)](https://coveralls.io/github/Nic30/hwtBuildsystem?branch=master)
[![Documentation Status](https://readthedocs.org/projects/hwtbuildsystem/badge/?version=latest)](http://hwtbuildsystem.readthedocs.io/en/latest/?badge=latest)
[![Python version](https://img.shields.io/pypi/pyversions/hwtBuildsystem.svg)](https://img.shields.io/pypi/pyversions/hwtBuildsystem.svg)
[![Join the chat at https://gitter.im/hwt-community/community](https://badges.gitter.im/hwt-community/community.svg)](https://gitter.im/hwt-community/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Note that the coverage does treat the vendor tool dependent tests as not covered because we can not install vendor tools in the CI.

----------------------------------------------------------------------------------------------------------------------------------------

This python package is a library of utils for interaction with the vendor tools. It also contains a predefined compilation scripts which can be used to build and analyze the HWT based designs.

The library does contain an executors and log parsers which are working with specific tool and the abstract project which allows you to write universal "compile" scripts.

Currently supports Xilinx Vivado, Modelsim, Intel Quartus, Yosys.


# Similar software

* [edalize](https://github.com/olofk/edalize)
* [hdl-make](https://www.ohwr.org/projects/hdl-make)
* [IPBB](https://github.com/ipbus/ipbb)
* [midas](https://github.com/ucb-bar/midas)
* [ruckus](https://github.com/slaclab/ruckus)
* [mflowgen](https://github.com/cornell-brg/mflowgen) - ASIC/FPGA Flow Generator
* [Vivado-CI](https://github.com/Viq111/Vivado-CI)
* [VivadoScripting](https://github.com/paulscherrerinstitute/VivadoScripting)
* [python-quartus](https://github.com/CatherineH/python-quartus)
* [quartustcl](https://github.com/agrif/quartustcl)
* [pySerdes](https://github.com/jeepx5/pySerdes)
