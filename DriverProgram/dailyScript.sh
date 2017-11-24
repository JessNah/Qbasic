#!/bin/bash

# STDOUT Colour Definitions (NC stands for No Colour)
RED='\033[0;31m';
BLUE='\033[0;34m';
GREEN='\033[0;32m';
NC='\033[0m';

#TODO: Add check to ensure 3 input arguement is provided

mkdir Temp_Output_Files/

echo -e "${BLUE}Running Front End 3 times. View logs at \"Logs/frontEnd_run_<run_time>.txt\"  ${NC}";

for i in {1..3}
do
	time=$(date +"%FT%H%M%S%3N")
	../FrontEnd/QBasic.py "${1}" "Temp_Output_Files/transactionSummaryFile_${i}.txt" < "${3}/input_daily_transaction_${i}.txt" > "Logs/frontEnd_run_${time}.txt"
done

echo -e "Completed running Front End 3 times.";

echo -e "\n${BLUE}Creating merged transaction summary file.  ${NC}";
#Merge transaction files
FILES="Temp_Output_Files/*"
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

echo -e "${mergedTransactionString}" > "Daily_Transaction_File/mergedTransactionSummaryFile.txt";
echo -e "Successfully created merged transaction summary file.";

time=$(date +"%FT%H%M%S%3N")
echo -e "\n${BLUE}Running BackOffice with merged transaction summary file. View logs at \"Logs/backend_run_${time}.txt\"  ${NC}";

../BackOffice/BackOffice.py "${2}" "Daily_Transaction_File/mergedTransactionSummaryFile.txt" "${2}" "${1}" > "Logs/backend_run_${time}.txt"

echo -e "Completed running BackOffice. View output files in \"Output_Files\".";

rm -rf Temp_Output_Files