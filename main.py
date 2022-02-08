import  scotiaParser 
import americianExpressParser
import os
 
parsers =[]
statement_dir_lists =[]
# Get the list of all files and directories
# in the root directory
AMERICIAN_EXPRESS_PATH = os.getcwd() +"/americainExpressStatments"
statement_dir_lists.append(AMERICIAN_EXPRESS_PATH)
parsers.append(americianExpressParser)

SCOTIA_BANK_PATH = os.getcwd()+"/scotiaBankStatments"
statement_dir_lists.append(SCOTIA_BANK_PATH)
parsers.append(scotiaParser)
def automateParse(full_path, parser):
    statement_dir_list = os.listdir(full_path)
    for  path  in (statement_dir_list):
        file_path = full_path +"/"+ path
        parser.main(file_path)

for job in range(0,len(parsers)) : 
    automateParse(statement_dir_lists[job],parsers[job])