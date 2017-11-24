#!/bin/bash

# STDOUT Colour Definitions (NC stands for No Colour)
RED='\033[0;31m';
BLUE='\033[0;34m';
GREEN='\033[0;32m';
NC='\033[0m';

rm -rf Logs/*

#Empty the masteraccounts.txt and validaccounts.txt file from the previous week
> Output_Files/masteraccounts.txt
> Output_Files/validaccounts.txt

for i in {1..5}
do
	echo -e "\n${RED}Running Daily Script for Day ${i}.";
	./dailyScript.sh "Output_Files/validaccounts.txt" "Output_Files/masteraccounts.txt" "Input_Files/Day${i}"
done