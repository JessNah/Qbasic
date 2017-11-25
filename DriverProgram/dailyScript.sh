#!/bin/bash

# STDOUT Colour Definitions (NC stands for No Colour)
RED='\033[0;31m';
BLUE='\033[0;34m';
GREEN='\033[0;32m';
NC='\033[0m';

#Check number of input arguements
if [ $# -ne 3 ]
  then
	errorMessage="
	${RED}Error, 3 input arguements must be supplied to dailyScript.sh
	\nExample usage: ./dailyScript.sh validaccounts.txt masteraccounts.txt Input_Files/Day1${NC}
	\nWhere:
	\n	validaccounts.txt is the valid accounts file used for the day
	\n	masteraccounts.txt is the master accounts file to use for backend processing at the end of the day
	\n	Input_Files/Day1 is the path to the directory containing the input transaction files
	"
	echo -e $errorMessage
	exit
fi

#Ensure directory path for transaction inputs has trailing slash.
case "$3" in
*/)
	#Has trailing slash in directory path
	inputTxnDir="${3}"
    ;;
*)
    #Does not have trailing slash in directory path so add one
	inputTxnDir="${3}/"
    ;;
esac

#Create a temporary directory to store transaction summary files for each front end session
mkdir Temp_Output_Files/

numFrontEndRuns=3

#Run front end application X number of times. Where stdout is stored in Logs/, and transaction summary file in stored in Temp_Output_Files
echo -e "${BLUE}Running Front End $numFrontEndRuns times. View logs at \"Logs/frontEnd_run_<run_time>.txt\"  ${NC}";

for i in $(seq 1 $numFrontEndRuns)
do
	time=$(date +"%FT%H%M%S%3N")
	../FrontEnd/QBasic.py "${1}" "Temp_Output_Files/transactionSummaryFile_${i}.txt" < "${inputTxnDir}input_daily_transaction_${i}.txt" > "Logs/frontEnd_run_${time}.txt"
done

echo -e "Completed running Front End $numFrontEndRuns times.";


#Create the merged transaction summary file from all transaction summary files created in Temp_Output_Files directory.
#Save the merged transaction file in Daily_Transactio_File/mergedTransactionSummaryFile.txt (overwrite if necessary)
echo -e "\n${BLUE}Creating merged transaction summary file.  ${NC}";

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


#Run the BackOffice application using the merged transaction summary file found in Daily_Transaction_File/mergedTransactionSummaryFile.txt
time=$(date +"%FT%H%M%S%3N")
echo -e "\n${BLUE}Running BackOffice with merged transaction summary file. View logs at \"Logs/backend_run_${time}.txt\"  ${NC}";

../BackOffice/BackOffice.py "${2}" "Daily_Transaction_File/mergedTransactionSummaryFile.txt" "${2}" "${1}" > "Logs/backend_run_${time}.txt"

echo -e "Completed running BackOffice.";


#Delete temporary directory used to store transaction summary files for each front end session
rm -rf Temp_Output_Files