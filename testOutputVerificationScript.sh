#!/bin/bash

# STDOUT Colour Definitions (NC stands for No Colour)
RED='\033[0;31m';
BLUE='\033[0;34m';
GREEN='\033[0;32m';
NC='\033[0m';

passed=0;
failed=0;

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
  
  # If no transaction file should be created, verify no transaction got created.
  # These situations use special keyword NO_TRANSACTION_FILE
  if [ ${pathArray[2]} = "NO_TRANSACTION_FILE" ]; then
	echo "Verifying no transaction file was created by this test."
	if [ ! -f ${ActualTransactionFile} ]; then
	    echo -e "Verified no transaction file was created.\n";
	else
		OUTPUT1="Error, a transaction file WAS created by the test. See file, ${ActualTransactionFile}";
		echo -e "${OUTPUT1}\n";
	fi  
  else
	# Test if transaction file matches the expected one.
  	echo "diff \"${ActualTransactionFile}\" \"${ExpectedTransactionFile}\"";
  	OUTPUT1="$(diff ${ActualTransactionFile} ${ExpectedTransactionFile})"''
  	echo "${OUTPUT1}";
  fi
  
  # Test if the stdout file matches the expected one.
  echo "diff \"${ActualOutputFile}\" \"${ExpectedOutputFile}\"";
  OUTPUT2="$(diff ${ActualOutputFile} ${ExpectedOutputFile})"''
  echo "${OUTPUT2}";
  
  # PRINT PASS OR FAIL
  if [ -z "${OUTPUT1}" ] && [ -z "${OUTPUT2}" ]; then
	  echo -e "${GREEN}${pathArray[0]}/${pathArray[1]} TEST PASSED!${NC}";
	  passed=$((passed+1));
  else
	  echo -e "${RED}${pathArray[0]}/${pathArray[1]} TEST FAILED!${NC}";
	  failed=$((failed+1));
  fi
  
  # New line
  echo "";
  
done <testsToRun.txt

echo "#####################TESTING STATISTICS#####################";
echo -e "${GREEN}Tests Passed: $passed ${NC}";
echo -e "${RED}Tests Failed: $failed ${NC}";
testsRun=$((passed+failed));
echo -e "${BLUE}Tests Run : $testsRun ${NC}";
echo "############################################################";