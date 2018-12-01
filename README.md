# Air Ticket Information Search Project

This is a semester project for Autogroup1 of IEORE4501 Fall 2018 at Columbia University.

# What is it?

The project aims to build a web crawler that searches available flight tickets with preferences. 
Output will be flight tickets that satisfies the input requirements listed from the cheapest to the most expensive one.
This project will print the available information to your terminal screen.
The source of the output is the internet.

# Main Features

Given required air ticket information, the program will return flight information to the console. And the return value will be oriented dictionaries.

## required input
The program requires a string input of all travel information, including...

## output style
The output will be an oriented dictionary with information of all trips that satisfies the requests. The output is printed to the console.

# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

Here are a list of required preperations to install the programm successfully.

Python 3.6+ is required to run the program.

* Windows Installation -- [Windows](https://www.python.org/downloads/windows/)
* Mac OS X Installation -- [Mac OS X](https://www.python.org/downloads/mac-osx/)
* Other platforms -- [Other](https://www.python.org/download/other/)

In order to get useful information from the webpage, some HTMl parsing modules are also required.
* requests
* html
* json
* re

These modules will be imported when executing the program. And such importation is included at the beginning of the program, such as:
```
import(requests)
```
 
## Installing

Clone the AirTicketProject to your terminal.

## How to use?

First, execute the Airticket.py with a helper function [-h] in command line, you will be able to see the required input and the style.
```
Airticket.py -h
```
Following the style of input, type in your inputs and then execute the program.
For example, a serach about one-way ticket for one adult passanger on date 12/25/2018 
```
python3 Airticket.py 
```
The information matching your inputs will be printed to the console for you to check.
```

```

# Authors

* **Aijing** -- [Aijing](https://github.com/muliamuli)
* **Chen Wang** -- [Chen Want](https://github.com/az2525)
* **Siyuan Liu** -- [Siyuan Liu](https://github.com/intoxiah2014)

# Acknowledgments

Our project was inspired by scrapehero's project -- [scrapehero](https://gist.github.com/scrapehero/bc34513e2ea72dc0890ad47fbd8a1a4f)
