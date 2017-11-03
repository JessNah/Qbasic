#!/bin/bash

# STDOUT Colour Definitions (NC stands for No Colour)
RED='\033[0;31m';
NC='\033[0m';

# Iterate over all the lines in the testsToRun.txt file.
while read p; do

  # Skip blank lines (used purely for readability of testsToRun.txt file)
  if [ -z "$p" ]; then
	  continue
  fi
  
  # Create an array of the comma seperated values found for each test case.
  # Where 
  # 	pathArray[0] = test area name, ex: LOGIN, LOGOUT, etc.
  #		pathArray[1] = test case name
  #		pathArray[2] = transaction summary file name
  IFS=',' ;
  index=0;
  for path in $p; do 
  	pathArray[index]=$path;
	#echo $path; 
	index=$index+1;
  done
  
  # Create the path to valid accounts file, transaction summary file, standard input file, and the standard output file path
  ValidAccountsFile="Testing/${pathArray[0]}/Input Files/valid_accounts_file_${pathArray[1]}.txt"
  TransactionFile="Testing/${pathArray[0]}/Output Files/${pathArray[2]}.txt"
  InputFile="Testing/${pathArray[0]}/Input Files/input_${pathArray[1]}.txt"
  OutputFile="Testing/${pathArray[0]}/Output Files/output_${pathArray[1]}.txt"
  
  # Display in red text what test is currently being verified.
  echo -e "${RED}Executing ${pathArray[0]}/${pathArray[1]} test:${NC}";
  
  # Display what execution line is being executed in the rare case where manual intervention is necessary.
  echo "./QBasic.py \"${ValidAccountsFile}\" \"${TransactionFile}\" < \"${InputFile}\" > \"${OutputFile}\"";
  ./QBasic.py ${ValidAccountsFile} ${TransactionFile} < ${InputFile} > ${OutputFile};
  
  # Display where test output can be found for ease of debugging test failures.
  echo "${pathArray[0]}/${pathArray[1]} test output saved to ${OutputFile}";
  
  # Print new line to seperate the test case output and results
  echo "";
  
done <testsToRun.txt