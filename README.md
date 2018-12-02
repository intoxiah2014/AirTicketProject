# Air Ticket Information Search Project

This is a project for Autogroup1 of IEORE4501 Fall 2018 at Columbia University.

# What is it?

The project aims to build a web crawler that searches available flight tickets with preferences. 
Output will be flight tickets that satisfies the input requirements listed from the cheapest to the most expensive one.
This project will print the available information to your terminal screen.
Currently, we are able to gather information from 2 websites, Expedia.com and Orbitz.com

# Main Features

Given required air ticket information, the program will return flight information to the console. And the return value will be oriented dictionaries.

## required input
The program requires the user input of:
* Trip type, one-way or roundtrip
* Start Date and Return Date
* Departing and Destination Airport (or city) Code
* Number of Adults
* Maximum number of stops acceptable
* Price Range of the ticket (Minimum and Maximum Price)
* Website Name

## output style
The output will be an oriented dictionary with information of all trips that satisfies the requests. 
The output consists:
* Ticket Price Per Persion
* Flight Duration
* Stops
* Departing Airport Code
* Arriving Airport Code
* Airline
* Plane Type
* Detailed Timeline of the Trip


# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

Here are a list of required preperations to install the programm successfully.

Python 3.6+ is required to run the program.

* Windows Installation -- [Windows](https://www.python.org/downloads/windows/)
* Mac OS X Installation -- [Mac OS X](https://www.python.org/downloads/mac-osx/)
* Other platforms -- [Other](https://www.python.org/download/other/)

Or use the Jupyter Notebook to run the program.
You can get the Jupyter Notebook with Python from [Anaconda](https://www.anaconda.com/download/).

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

### Method 1: Execute in Command Line
Execute the program by typing in this command in your conmmand line or terminal
```
python3 Airticket.py
```
Detailed Instruction regarding the input style will be provided step by step.
The information matching your inputs will be printed to the console for you to check.


### Method 2: Execute in Jupyter Notebook
Another way to execute the program will be using Jupyter Notebook
Open a notebook file in Jupyter Notebook and make a new line.
```
%run Airticket.py
```
Detailed Instruction regarding the input style will be provided step by step.
The information matching your inputs will be printed to the console for you to check.

# Authors

* **Aijing** -- [Aijing](https://github.com/muliamuli)
* **Chen Wang** -- [Chen Want](https://github.com/az2525)
* **Siyuan Liu** -- [Siyuan Liu](https://github.com/intoxiah2014)

# Acknowledgments

Our project was inspired by scrapehero's project -- [scrapehero](https://gist.github.com/scrapehero/bc34513e2ea72dc0890ad47fbd8a1a4f)
