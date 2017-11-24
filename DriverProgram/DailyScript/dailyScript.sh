#!/bin/bash

# STDOUT Colour Definitions (NC stands for No Colour)
RED='\033[0;31m';
BLUE='\033[0;34m';
GREEN='\033[0;32m';
NC='\033[0m';

rm -rf Output_Files/*
rm -rf Logs/*
mkdir temp_output_files

echo -e "${BLUE}Running Front End 3 times. View logs at \"Logs/frontEnd_run_<run_number>.txt\"  ${NC}";

# Iterate over all the lines in the testsToRun.txt file.
for i in {1..3}
do
	../../FrontEnd/QBasic.py "Input_Files/validaccounts.txt" "temp_output_files/transactionSummaryFile_${i}.txt" < "Input_Files/input_daily_transaction_${i}.txt" > "Logs/frontEnd_run_${i}.txt"
done

echo -e "Completed running Front End 3 times.";

echo -e "\n${BLUE}Creating merged transaction summary file.  ${NC}";
#Merge transaction files
FILES="temp_output_files/*"
firstFile=true
for file in $FILES
do
	if [ "$firstFile" = true ] ; then
		mergedTransactionString="$(cat ${file})"''
		firstFile=false	
	else
		mergedTransactionString="${mergedTransactionString}\n$(cat ${file})"''	
	fi
done

echo -e "${mergedTransactionString}" >> "temp_output_files/mergedTransactionSummaryFile.txt";
echo -e "Successfully created merged transaction summary file.";

echo -e "\n${BLUE}Running BackOffice with merged transaction summary file. View logs at \"Logs/backen_run.txt\"  ${NC}";

../../BackOffice/BackOffice.py "Input_Files/masteraccounts.txt" "temp_output_files/mergedTransactionSummaryFile.txt" "Output_Files/masteraccounts.txt" "Output_Files/validaccounts.txt" > "Logs/backen_run.txt"

echo -e "Completed running BackOffice. View output files in \"Output_Files\".";

rm -rf temp_output_files/