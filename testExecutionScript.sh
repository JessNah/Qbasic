#!/bin/bash

RED='\033[0;31m';
NC='\033[0m';

while read p; do
  #echo $p
  IFS=',' ;
  index=0;
  
  # Skip blank lines
  if [ -z "$p" ]; then
	  continue
  fi
  
  for path in $p; do 
  	pathArray[index]=$path;
	#echo $path; 
	index=$index+1;
  done
  
  ValidAccountsFile="Testing/${pathArray[0]}/Input Files/valid_accounts_file_${pathArray[1]}.txt"
  TransactionFile="Testing/${pathArray[0]}/Output Files/${pathArray[2]}.txt"
  InputFile="Testing/${pathArray[0]}/Input Files/input_${pathArray[1]}.txt"
  OutputFile="Testing/${pathArray[0]}/Output Files/output_${pathArray[1]}.txt"
  
  
  echo -e "${RED}Executing ${pathArray[0]}/${pathArray[1]} test:${NC}";
  echo "./QBasic.py \"${ValidAccountsFile}\" \"${TransactionFile}\" < \"${InputFile}\" > \"${OutputFile}\"";
  ./QBasic.py ${ValidAccountsFile} ${TransactionFile} < ${InputFile} > ${OutputFile};
  echo "${pathArray[0]}/${pathArray[1]} test output saved to ${OutputFile}";
  
  # New line
  echo "";
  
done <testsToRun.txt