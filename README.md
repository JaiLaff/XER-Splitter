# XER-Parser
A tool to handle the parsing of Oracles Primavera P6 .XER output files.
Convert your .XER files into seperate CSVs for parsing and transforming in other tools (eg. PowerBI for reporting)

## Features include
- CSV output of .XER files
- GUI and CLI available
- Optionally ignore problematic RISKTYPE & POBS tables
- Basic metrics (Total tables & rows)

## Setup / Usage

I'm working on making this a complete package to be installed via pip and other package managers -> Something I've never done before

``` 
usage: XER Parser [-h] [-csv | -xlsx] [-i] [-o] [-cli] [-a]

A script to parse those pesky .xer files from Primavera P6

optional arguments:
  -h, --help           show this help message and exit
  -csv                 Comma seperated output
  -xlsx                Excel file output
  -i , --inputFile     The path to the input .xer file
  -o , --outputDir     The directory where the output files will be placed
  -cli, --suppressGui  Show the GUI
  -a, --allTables      Parse all tables - Turn on to stop skipping RISKTYPE & POBS tables
```
