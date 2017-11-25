#!/bin/bash

# STDOUT Colour Definitions (NC stands for No Colour)
RED='\033[0;31m';
BLUE='\033[0;34m';
GREEN='\033[0;32m';
NC='\033[0m';

#Clear out the log file directory at the start of each week (logs created by frontEnd and backOffice applications)
rm -rf Logs/*

#Empty the masteraccounts.txt and validaccounts.txt file from the previous week.
#As stated in Assignment 6 description, each week should start with empty masteraccounts.txt and validaccounts.txt files.
> Output_Files/masteraccounts.txt
> Output_Files/validaccounts.txt

#Set the number of days in a week
numDays=5

#Run the daily script for every day in the week
for i in $(seq 1 $numDays)
do
	echo -e "\n${RED}Running Daily Script for Day ${i}.";
	./dailyScript.sh "Output_Files/validaccounts.txt" "Output_Files/masteraccounts.txt" "Input_Files/Day${i}"
done

echo -e "\n\n${GREEN}Weekly QBasic run completed successfully. Daily script (dailyScript.sh) was executed total of $numDays times.${NC}"