# budgetParser

Python Budget Parser

This application parses credit card statements from American Express, Scotiabank, and Simplii Financial, extracts transaction data, and generates a simple budget report.Project Structurebudget-parser/
├── parsers/
│   ├── __init__.py
│   ├── amex_parser.py
│   ├── scotia_parser.py
│   └── simplii_parser.py
├── data/
│   └── (parsed_transactions.csv will be saved here)
├── statements/
│   └── (place your statement files here)
├── main.py
├── data_handler.py
├── reporting.py
└── requirements.txt
SetupClone the repository or download the files. 
Create a virtual environment:python -m venv venv
After creating it, you need to activate it:On macOS/Linux:source venv/bin/activate
On Windows (Command Prompt or PowerShell):venv\Scripts\activate
PowerShell Note: If you get an error message saying ...running scripts is disabled on this system..., your system's execution policy is blocking the script. To fix this for your current session only, run the following command first, and then try activating the environment again:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
Install the required packages:Make sure your virtual environment is activated before running this command. You should see (venv) at the start of your command prompt line.pip install -r requirements.txt
Create necessary directories:mkdir statements
mkdir data
Place your bank statements into the statements/ directory.How to RunRun the main application from your terminal:python main.py
The script will:Look for statement files in the statements/ directory.Parse the files using the appropriate parser based on the filename.Save the consolidated transactions to data/parsed_transactions.csv.Print a summary report to the console.TroubleshootingModuleNotFoundError: No module named 'pandas'This is the most common error and it means the required Python libraries were not installed in the virtual environment you are using. To fix it:Check if your virtual environment is active. Look for (venv) at the beginning of your terminal prompt.If you don't see it, activate the environment using the appropriate command for your system from Step 2 of the setup instructions.Once the environment is active, run the installation command again:pip install -r requirements.txt
This ensures that the packages are installed in the isolated venv environment where your script will look for them.