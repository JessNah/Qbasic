# QBasic Project

Software Quality Assurance Project for CISC/CMPE 327.
Basic banking system that uses a FrontEnd and a BackOffice application to do daily processing. 

The basic work flow of the system is as follows:
1. FrontEnd Application uses valid accounts file to determine valid accounts. Each FrontEnd execution allows the user to interactively perform transactions such as deposit, createacct, deleteacct etc. Each session produces a transaction summary file detailing what transactions took place.
2. At the end of a day (after multiple FrontEnd application's have been run), the BackOffice uses a master accounts file, the current valid accounts file, and the merged transaction summary files (from the FrontEnd) to produce a new version of the master accounts file and the valid accounts file.
3. Repeat steps 1 and 2 the next processing day using the NEW valid accounts file and the NEW master accounts file.

## Front End Application Usage
The following provides a brief overview of how to use the QBasic python front end application.
The Front End takes two arguments: the name of a Valid Accounts List file, and the name of a Transaction Summary file.
Additionally, the Front End reads input from standard input, which can either be typed in by the user or redirected from a file (when testing). 

**For the first case (production mode):**
./QBasic.py validaccounts.txt transactionsummary.txt

**When testing, use redirection to feed in the "user" input, say testinput.txt:**
./QBasic.py validaccounts.txt transactionsummary.txt < testinput.txt

**You can also save the terminal output created by the test:**
./QBasic.py validaccounts.txt transactionsummary.txt < testinput.txt > testoutput.txt

## BackOffice Application Usage:
The following provides a brief overview of how to use the QBasic Back-Office python application.
The Back-Office takes four arguments: the previous day Master Accounts File, the Merged Transaction Summary File, and file to use for the new Master Accounts File created, and the file to use for the new Valid Accounts File created.

The previous day Master Accounts File is created by the last run of the back-office application. The Merged Transaction Summary File will be provided by an intermediate script that concatenates the Front End’s Transaction Summary Files. Lastly the new Master Accounts File created by the Back-Office application will be used by the next day’s Back-Office, and the new Valid Accounts File will be used by the next day’s Front-End sessions.

**How to run the Back-Office application:**
./BackOffice.py masteraccount.txt transactionsummary.txt newmasteraccount.txt newvalidaccount.txt

## Daily and Weekly Banking Simulation Scripts:
To simulate daily and weekly banking transactions two scripts were created to allow automated transactions to take place without user input at the FrontEnd application. Each script is detailed below along with their respective usage.

### Daily Script
The daily script (dailyScript.sh) is used to run the FrontEnd application and BackOffice application to simulate a day’s worth of transaction. Currently the script is set to run the FrontEnd (ATM type) application 3 times before running the BackOffice application once at the end of the day. The 3 FrontEnd’s transaction summary files are merged by the script before being provided to the BackOffice. The script itself has 3 inputs and creates 4 types of outputs as seen below. Example usage for the script can be found below along with the error message provided if the user does not provide the correct number of input parameters. 

**Daily Script Inputs:**
•	Valid Accounts File: Path to the valid accounts file to be used for all the FrontEnd sessions during the day. This file is provided by the previous day’s BackOffice application. This path is also used to output the new valid accounts file at the end of the day. 
•	Master Accounts File: Path to the master accounts file to be updated by the BackOffice at the end of the day.
•	Directory of transaction session inputs: Specify the directory where the transaction session inputs for the day can be found. This directory must contain as many files as necessary for the amount of FrontEnd calls (in this case 3). Each filename must be in the format of “input_daily_transaction_<run #>.txt”.

**Daily Script Outputs:**
•	Valid Accounts File: The new valid accounts file created by the BackOffice at the end of the day will be saved in the path provided using the script parameters (see inputs above).
•	Master Accounts File: The new master accounts file created by the BackOffice at the end of the day will be saved in the path provided using the script parameters (see inputs above).
•	Merged Transaction Summary File: The merged transaction summary file created by concatenating all the FrontEnd’s transaction summary files can be found in "Daily_Transaction_File/mergedTransactionSummaryFile.txt". For simplicity and space consumption, this file will be overwritten on subsequent daily script calls.
•	Logs: Logs are created for each FrontEnd and BackOffice session’s std output. Each log is saved in Logs/ in the format of "Logs/frontEnd_run_${time}.txt" and "Logs/backend_run_${time}.txt".

**Example Usage:**
./dailyScript.sh validaccounts.txt masteraccounts.txt Input_Files/Day3

**Error message displayed if invalid number of parameters passed to daily script:**
Johans-MacBook-Pro:DriverProgram johancornelissen$ ./dailyScript.sh validaccounts.txt masteraccounts.txt
Error, 3 input arguements must be supplied to dailyScript.sh 
Example usage: ./dailyScript.sh validaccounts.txt masteraccounts.txt Input_Files/Day1 
Where: 
 validaccounts.txt is the valid accounts file used for the day 
 masteraccounts.txt is the master accounts file to use for backend processing at the end of the day 
 Input_Files/Day1 is the path to the directory containing the input transaction files

### Weekly Script
The weekly script (weeklyScript.sh) is used to run the daily script a total of 5 times. This corresponds to the number of business days in a week as it is assumed that the banking system is not in use during the weekend. This action simulates the banking system being used for a total of 5 days, where each day consists of 3 FrontEnd runs and one BackOffice run. The weekly script does not directly take any input parameters but does use multiple pre-defined inputs as described below. The inputs used by the script are assumed to be of proper format and in the pre-defined locations (example, the transaction session inputs must be found in “Input_Files/Day[X]”).

**Weekly Script Inputs:**
The weekly script does not directly accept any inputs; however, the daily script is called for each processing day using a set of inputs. See the description of dailyScript.sh inputs above. The weekly script itself uses “Output_Files/masteraccounts.txt” and “Output_Files/validaccounts.txt” as the starting of the week account files (which are cleared at the start of the week) as well as the location for saving the final master and valid accounts files created for the week’s transactions. The transaction session inputs used for each day should be located in “Input_Files/Day[X]” before starting the weekly script.

**Weekly Script Outputs:**
•	Valid Accounts File: The new valid accounts file created by the BackOffice at the end of the last day in the week will be saved at “Output_Files/validaccounts.txt”.
•	Master Accounts File: The new master accounts file created by the BackOffice at the end of the last day in the week will be saved at “Output_Files/masteraccounts.txt”.
•	Logs: The daily script which is invoked through the weekly script creates logs for each FrontEnd and BackOffice session’s std output. Each log is saved in Logs/ in the format of "Logs/frontEnd_run_${time}.txt" and "Logs/backend_run_${time}.txt". The /Logs directory is cleared at the beginning of each week.

**Example Usage:**
./weeklyScript.sh

## Authors
* Muhammad Usman Majeed
* Jessica Nahulan
* Johan Cornelissen
