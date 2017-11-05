#!/bin/bash

# STDOUT Colour Definitions (NC stands for No Colour)
RED='\033[0;31m';
BLUE='\033[0;34m';
GREEN='\033[0;32m';
NC='\033[0m';

# Statistic counters for number of passed/failed test cases
passed=0;
failed=0;

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
  
  # Create the path to actual/expected versions of the transaction summary file and standard output files.
  ActualTransactionFile="Testing/${pathArray[0]}/Output Files/${pathArray[2]}.txt"
  ExpectedTransactionFile="Testing/${pathArray[0]}/Expected Output Files/${pathArray[2]}.txt"
  ActualOutputFile="Testing/${pathArray[0]}/Output Files/output_${pathArray[1]}.txt"
  ExpectedOutputFile="Testing/${pathArray[0]}/Expected Output Files/output_${pathArray[1]}.txt"
  
  # Display in blue text what test is currently being verified.
  echo -e "${BLUE}Verifying ${pathArray[0]}/${pathArray[1]} test:${NC}";
  
  # If no transaction file should be created, verify no transaction got created.
  # These situations use special keyword NO_TRANSACTION_FILE.
  if [ ${pathArray[2]} = "NO_TRANSACTION_FILE" ]; then
	echo "Verifying no transaction file was created by this test."
	if [ ! -f ${ActualTransactionFile} ]; then
	    echo -e "Verified no transaction file was created.\n";
	else
		OUTPUT1="Error, a transaction file WAS created by the test. See file, ${ActualTransactionFile}";
		echo -e "${OUTPUT1}\n";
	fi  
  else
	# Otherwise if a transaction file IS expected, test if transaction file matches the expected one.
	
	if [ ! -f ${ActualTransactionFile} ]; then
	    OUTPUT1="${ActualTransactionFile} file not found!"
		echo "${OUTPUT1}";
	else
  		echo "diff \"${ActualTransactionFile}\" \"${ExpectedTransactionFile}\"";
  		OUTPUT1="$(diff ${ActualTransactionFile} ${ExpectedTransactionFile})"''
  		echo "${OUTPUT1}";
	fi
  fi
  
  # Test if the stdout file matches the expected one.
  if [ ! -f ${ActualOutputFile} ]; then
      OUTPUT1="\"${ActualOutputFile}\" file not found!"
  else
  	  echo "diff \"${ActualOutputFile}\" \"${ExpectedOutputFile}\"";
  	  OUTPUT2="$(diff ${ActualOutputFile} ${ExpectedOutputFile})"''
  	  echo "${OUTPUT2}";
  fi
  
  # PRINT PASS OR FAIL for the test cases (using green or red text appropriately)
  if [ -z "${OUTPUT1}" ] && [ -z "${OUTPUT2}" ]; then
	  echo -e "${GREEN}${pathArray[0]}/${pathArray[1]} TEST PASSED!${NC}";
	  passed=$((passed+1));
  else
	  echo -e "${RED}${pathArray[0]}/${pathArray[1]} TEST FAILED!${NC}";
	  failed=$((failed+1));
  fi
  
  # Print new line to seperate the test case output and results
  echo "";
  
done <testsToRun.txt

# Print to the user at the end of the verification phase the statistics of tests passed versus failed.
echo "#####################TESTING STATISTICS#####################";
echo -e "${GREEN}Tests Passed: $passed ${NC}";
echo -e "${RED}Tests Failed: $failed ${NC}";
testsRun=$((passed+failed));
echo -e "${BLUE}Tests Run : $testsRun ${NC}";
echo "############################################################";