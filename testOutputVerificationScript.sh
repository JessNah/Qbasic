#!/bin/bash

RED='\033[0;31m';
BLUE='\033[0;34m';
GREEN='\033[0;32m';
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
  
  ActualTransactionFile="Testing/${pathArray[0]}/Output Files/${pathArray[2]}.txt"
  ExpectedTransactionFile="Testing/${pathArray[0]}/Expected Output Files/${pathArray[2]}.txt"
  ActualOutputFile="Testing/${pathArray[0]}/Output Files/output_${pathArray[1]}.txt"
  ExpectedOutputFile="Testing/${pathArray[0]}/Expected Output Files/output_${pathArray[1]}.txt"
  
  echo -e "${BLUE}Verifying ${pathArray[0]}/${pathArray[1]} test:${NC}";
  echo "diff \"${ActualTransactionFile}\" \"${ExpectedTransactionFile}\"";
  OUTPUT1="$(diff ${ActualTransactionFile} ${ExpectedTransactionFile})"''
  echo "${OUTPUT1}";
  
  echo "diff \"${ActualOutputFile}\" \"${ExpectedOutputFile}\"";
  OUTPUT2="$(diff ${ActualOutputFile} ${ExpectedOutputFile})"''
  echo "${OUTPUT2}";
  
  # PRINT PASS OR FAIL
  if [ -z "${OUTPUT1}" ] && [ -z "${OUTPUT2}" ]; then
	  echo -e "${GREEN}${pathArray[0]}/${pathArray[1]} TEST PASSED!${NC}";
  else
	  echo -e "${RED}${pathArray[0]}/${pathArray[1]} TEST FAILED!${NC}";
  fi
  
  # New line
  echo "";
  
done <testsToRun.txt