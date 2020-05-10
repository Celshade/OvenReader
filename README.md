# OvenReader
[![GNU GPLv3 license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/Celshade/OvenReader/blob/master/LICENSE.txt)
[![built with Python3](https://img.shields.io/badge/built%20with-Python3-green.svg)](https://www.python.org/)

_Parse raw oven data and output details in a more useful format_

Welcome to OvenReader!

OvenReader is a program built to automate the process of parsing a specific
type of text file. This text file (or "report") contains a unique collection of
data points which are generated by industrial oven software -> i.e. cook data.
OvenRreader parses these reports, creates a Cook object which encapsulates
the unique data relevant to that specific cook, and finally outputs a formatted
visual of the critical data points for easy viewing.

**Disclaimer**

This project was built for parsing very specific data which is organized in
uniquely formatted text files. This format may not be universal, and the
program may need to be tuned accordingly for anyone using this code in their
own projects.

For the sake of privacy and compliance, all names and product information used
in the example data file **_\docs\404E_PL123456L.txt_** (report titles, program
names, employee names, product names, and lot numbers) are fictitious.
***

## Requirements
1. _**Python [3.8+]**_: Can be downloaded ->[here](https://www.python.org/)<-

_Some older versions of python may work, but this has not been tested._
***

## Instructions
This program is intended to be run in the CLI. Simply download the package, and
run **_ovenreader.py_** from the package directory to start the program.
***

Found a bug or care to drop some feedback? See the link below!
_Comments & bugs -> https://www.github.com/Celshade/OvenReader/issues_

Peace

**//Cel**
