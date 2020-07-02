import csv
import sys
import os
import time

scriptName = "XERSplitter"
errors = []
baselineFile = False

def log(input):
    print(input)
    #Put gui stuff here

argsCount = len(sys.argv)
# Test if num of args met
if argsCount < 3:
    lineToLog = ["ERROR: Requires target .xer file and output directory as arguments","Usage: python xerSplitter.py path/to/xerFile.xer path/to/outputDirectory [BaselineFlag (1/0)]"]
    errors.append(lineToLog)
    log(lineToLog)
    
    exit()

# Get filename
xerFile = sys.argv[1]
outputFolder = sys.argv[2]

# Is baseline -> Only need task table
if len(sys.argv) == 4: baselineFile = sys.argv[3]

# check if filename exists before opening
if not os.path.exists(xerFile):
    lineToLog = f"ERROR: Could not find target file \"{xerFile}\""
    errors.append(lineToLog)
    log(lineToLog)
    
    exit()

if not os.path.exists(outputFolder):
    lineToLog = f"ERROR: Could not find target output directory \"{outputFolder}\""
    errors.append(lineToLog)
    log(lineToLog)
    
    exit()

#continue and run
try:
    with open(xerFile, "r", encoding="cp1252", errors="ignore") as file:

        # Timing length of runtime
        startTime = time.time()

        eof = False
        
        # metrics for final reporting
        rowCount = 0
        tableCount = 0

        while not eof:
            # Split the row and create a list of attributes per line
            # Allows easy writing to a csv
            line = file.readline().split('\t')
            line[len(line)-1] = line[len(line)-1][:-1]

            # Saving our place in the file should we need to jump back
            # Used for skipping the RiskType table
            # Reading the entire row crashes the program, we need to read the first 2 chars
            # If those chars match to a table flag we just back and grab the table's title
            savedLine = file.tell()

            if line[0] == "%T":
                title = line[1]

                print(f"Reading: {title}\n")

                # Is the XER the baseline file? - We only need Task from baseline
                if baselineFile:
                    if title != "TASK":
                        while file.readline(2) != "%T":
                            # save previous line position for when a table is found
                            savedLine = file.tell()

                        # new table found -> go back to the line and read the whole line
                        file.seek(savedLine)

                        #go back to start of main loop
                        continue
                else:
                    # Risktype data was encoded differently so we will skip it as it breaks everything
                    # Basically checking if the heading is risktype
                    if title == "RISKTYPE" || title == "POBS":
                        print("Skipping bad tables - Searching for next table")
                        print("This may take some time\n")

                        while file.readline(2) != "%T":
                            # save previous line position for when a table is found
                            savedLine = file.tell()

                        # new table found -> go back to the line and read the whole line
                        file.seek(savedLine)

                        #go back to start of main loop
                        continue
                
                if baselineFile: title += "-BASELINE"
                # Create new file with the title
                currentWritingFile = open(outputFolder + "/" + title + ".csv", "w+", newline="")

                tableCount += 1

                # Create csv writer - Allows us to write a list as a csv line
                writer = csv.writer(currentWritingFile, quoting=csv.QUOTE_MINIMAL)

                print ("Writing " + title)

                # While there exists a row
                # Exit conditions are either the end of the XER file or a new title
                while True:
                    # Read the new line and place in a list
                    line = file.readline().split('\t')

                    # If %E (end of xer file) flag -> exit
                    if line[0] == "%E\n":
                        eof = True
                        break

                    # Removes the new line character from the last entry in each line
                    line[len(line)-1] = line[len(line)-1][:-1]

                    # check if new title
                    # New title means we're done with this table
                    if line[0] == "%T": 
                        currentWritingFile.close()

                        #exit this inner loop
                        break

                    # ----- REMOVE IF STATEMENT IF snake_case IS ACCEPTABLE ----- #
                    # Convert snake_case to CamelCase
                    # There are oneliners out there but they didn't allow for statements mid convertion
                    if line[0] == "%F": 
                        newline = []
                        for item in line:
                            # snake_case -> ["snake", "case"]
                            splitString = item.split("_")
                            output = ""
                            for x in splitString:
                                if x == "id": 
                                    output += "ID" 
                                    continue
                                # snake -> Snake
                                # output = Snake
                                # case -> Case
                                # output = SnakeCase
                                output += x.capitalize()
                            # ["SnakeCase"...]
                            newline.append(output)
                        line = newline
                    
                    # Save position in case it's a title
                    savedLine = file.tell()

                    # Removing first element in list as it's the flag character
                    writeline = line
                    writeline.pop(0)

                    # Do the Writing
                    writer.writerow(writeline)
                    rowCount += 1

                if baselineFile: break

                # Title must have been found -> revert to title line position
                file.seek(savedLine)

            #back to start of the main loop
            #If we got to this point in the baseline we've already written the task table
            
    file.close()

except BaseException as e:
        # Report and log exceptions, File not moved and skipped
        lineToLog = [type(e).__name__ + " splitting XER " + file, str(e) + "\n"]
        errors.append(lineToLog)
        log(lineToLog)
else:
    # main loop completed
    completionTime = int((time.time() - startTime)* 1000)
    rows = str(rowCount)
    tables = str(tableCount)

    lineToLog = [f"XER Split of: {xerFile}",f"Completed successfully in: {str(completionTime)}ms",f"{rows} rows written across {tables} files",f"Rows written per ms: {rowCount/completionTime}"]
    errors.append(lineToLog)
    log(lineToLog)
    
    
