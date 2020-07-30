import csv
import sys
import os
import time
import PySimpleGUI as sg
import argparse
import _thread

def InitParser():
    global parser 
    parser = argparse.ArgumentParser(description="A script to parse those pesky .xer files from Primavera P6", prog="XER Parser")

    fileTypeGroup = parser.add_mutually_exclusive_group()
    fileTypeGroup.add_argument("-csv", help="Comma seperated output", action="store_const", dest="type", const="csv")
    fileTypeGroup.add_argument("-xlsx", help="Excel file output", action="store_const",dest="type", const="xlsx")

    parser.add_argument("-i","--inputFile", help="The path to the input .xer file",type=str,default="", metavar="")
    parser.add_argument("-o","--outputDir", help="The directory where the output files will be placed", type=str,default="",metavar="")
    parser.add_argument("-cli", "--suppressGui", help="Show the GUI" ,action="store_true")
    parser.add_argument("-a", "--allTables", help="Parse all tables - Turn on to stop skipping RISKTYPE & POMS tables", action="store_true")

    parser.set_defaults(type="csv")
    
    args = parser.parse_args()

    return args

def ConstructGUI(args):
    sg.theme("Default1")

    OptionsLayout = [      
            [sg.Checkbox('Ignore Problematic Tables',key='-IGNORETABLES-', default=(not args.allTables), tooltip="Ignores RISKTYPE & POMS Tables:\nThey are auto-generated by P6 and cause problems")],
            [sg.Frame(title='Output File Type',layout=[     
                [sg.Radio('.csv', 'type', key='-TYPECSV-', default=(args.type=='csv')), sg.Radio('.xlsx', "type",key='-TYPEXLSX-', default=(args.type=="xlsx"), disabled=False, tooltip="Not Currently Supported")]])
            ]
    ]

    mainLayout = [
        [sg.Text('XER Splitter', justification='center', font=("",15))],
        [sg.Text('XER File', size=(20,1))],      
        [sg.InputText(size=(35,1), key='-INPUTFILE-', default_text=(args.inputFile)), sg.FileBrowse(file_types=(('P6 XER File', '*.xer'),))],
        [sg.Text('Output Folder', size=(20,1))],
        [sg.InputText(size=(35,1), key='-OUTPUTFOLDER-', default_text=(args.outputDir)), sg.FolderBrowse()],
        [sg.Frame(title='Options',layout=OptionsLayout)],
        [sg.Text('_' * 50)],
        [sg.Text('Press \'Split\' to begin', key="-WORKINGTEXT-"), sg.Text("", size=(35,1), justification="right", visible=False, key="-STATSTEXT-")],
        [sg.Output(size=(50,15), key='-OUTPUT-')],
        # Maybe someday
        # [sg.Text('Select Tables')],
        [sg.Button(button_text='Split', key="-SPLIT-"), sg.Button(button_text="Clear"), sg.CloseButton("Close", key="-STOPBUTTON-")]
    ]


    global window
    window = sg.Window("XER Splitter", mainLayout, finalize=True)

    introText = "Welcome to the XER Splitter\n\n"
    window["-OUTPUT-"].update(introText)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit', "Close"):
            break

        if event == "Clear":
            window['-OUTPUT-'].update("")

        if event == "-SPLIT-":
            window['-WORKINGTEXT-'].update(value="Working...")
            window['-SPLIT-'].update(disabled=True)
            if values["-TYPECSV-"]: args.type='csv'
            if values["-TYPEXLSX-"]: args.type='xlsx'
            args.inputFile = values["-INPUTFILE-"]
            args.outputDir = values["-OUTPUTFOLDER-"]
            args.allTables = not values["-IGNORETABLES-"]

            StartThread(args)

        

def UpdateGui(success=None, tables=-1, rows=-1, writtenTables=-1, writtenRows=-1):
    if args.suppressGui: return

    global window
    if success == True:
        window['-WORKINGTEXT-'].update(value="Error Found")
        window['-SPLIT-'].update(disabled=False)
    
    if success == False:
        #window['-WORKINGTEXT-'].update(value="Complete!")
        window['-SPLIT-'].update(disabled=False)

    if tables != -1 or rows != -1:

        window["-STATSTEXT-"].update(visible=True)
        valueString = f"{str(writtenRows)}/{str(rows)} rows, {str(writtenTables)}/{str(tables)} tables"
        window["-STATSTEXT-"].update(value=valueString)


########### THE SCRIPT #############

def CheckDirectories(args):


    if not os.path.exists(args.inputFile):
        print(f"ERROR: Could not find target xer file \"{args.inputFile}\"")
        return False

    if not os.path.exists(args.outputDir):
        print(f"INFO: Could not find target output directory \"{args.outputDir}\"")
        print(f"Attempting to create target output directory...")
        
        try:
            os.makedirs(args.outputDir)
        except BaseException as e:
            print(f"ERROR: Failed to create target output directory \"{args.outputDir}\"")
            print(f"{type(e).__name__} was caught")
            print(str(e))
            return False
        else: print(f"Target output directory \"{args.outputDir}\" created successfully.")
    
    return True

def PreCheck(file):
    print("INFO: Beginning PreCheck of the XER File")
    
    eof = False

    totalTables = 0
    totalRows = 0
    try:
        with open(file, "r", encoding="cp1252", errors="ignore") as xer:
            

            while not eof:
                rowType = xer.readline(2)
                if rowType == "%T": totalTables += 1
                elif rowType == "%R": totalRows += 1
                elif rowType == "%E": eof = True
                
            UpdateGui(tables=totalTables, rows=totalRows, writtenTables=0, writtenRows=0)
            
    except BaseException as e:
        print("Critical error during Pre Check of XER File")
        print(f"{type(e).__name__} was caught")
        print(str(e))
        return False

    print("INFO: Pre Check completed successfully")
    print(f"{totalRows} rows and {totalTables} found")
    return True
    

def Split(args):
    try:
        pass
    except BaseException as e:
        print(f"Critical error splitting XER")
        print(f"{type(e).__name__} was caught")
        print(str(e))
    else:
        pass
    

def SplitXer(args):
    print("INFO: Settings Confirmed")
    print(args)

    if not CheckDirectories(args): 
        UpdateGui(success=False)
        return
    
    if not PreCheck(args.inputFile):
        UpdateGui(success=False)
        return
    
    UpdateGui(success=True)
    

def StartThread(args):
    print("INFO: Starting Compute Thread...")
    _thread.start_new_thread(SplitXer, (args,))



if __name__ == "__main__":
    args = InitParser()
    
    if not args.suppressGui: ConstructGUI(args)
    else: SplitXer(args)