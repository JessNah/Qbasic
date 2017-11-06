import TxnProcess
import ErrorHandler
import sys
import re

err = ErrorHandler.ErrorHandler()

class Utility:
    """Class used for utility functions for QBasic application.
    Utility functions are by TxnProcess for routine operations.
    """

    def process_account_file(self, fileName):
        """Function to process valid accounts file.
        Valid account numbers are stored in TxnProcess.valid_acc_list
        """
        with open(fileName) as file:
            for line in file:
                #remove leading and trailing spaces.
                line = line.strip()
                try:
                    if(not self.is_string_amount_valid(line) and line != "0000000"):
                        err.process_error("ERR_INVALIDACCFILE")
                        sys.exit()
                    line = int(line)
                except ValueError:
                    err.process_error("ERR_INVALIDACCFILE")
                    sys.exit()
                #storing everything in memory!
                TxnProcess.valid_acc_list.append(line)

    def intiliaze_withdraw_totals(self):
        """Function to initiliaze withdrawal amounts for each valid account."""
        TxnProcess.withdraw_limits.clear()
        for accNum in TxnProcess.valid_acc_list:
            TxnProcess.withdraw_limits[accNum] = 0

    def create_txn_msg(self, txnCode, toAcc, amount, fromAcc, accName):
        """Function to form the transaction msg to be added into the transaction summary file."""
        msg = ""

        if(txnCode == None):
            return None

        msg += txnCode

        if(toAcc == None):
            msg += " 0000000"
        else:
            msg += " " + str(toAcc)

        if(amount == None):
            msg += " 000"
        else:
            msg += " " + str(amount)

        if(fromAcc == None):
            msg += " 0000000"
        else:
            msg += " " + str(fromAcc)

        if(accName == None):
            msg += " ***"
        else:
            msg += " " + accName

        return msg

    def create_txn_summary_file(self, transactionSummaryFile, listTxnMsgs):
        """Function to write all cached transaction messages to transaction summary file."""
        myfile = open(transactionSummaryFile, 'w')
        for line in listTxnMsgs:
                myfile.writelines(line + "\n")
        myfile.close()

    def is_account_valid(self, accNum):
        """Function to check if passed in account number is valid."""
        if(str(accNum)[0] == "0"):
            #Account number can not start with zero.
            return False
        elif(accNum in TxnProcess.valid_acc_list):
            return True
        else:
            return False

    def is_account_unique(self, accNum):
        """Function to check if passed in account number is unique(or new)."""
        if(accNum in TxnProcess.valid_acc_list or accNum in TxnProcess.new_acc_list):
            return False
        else:
            return True

    def is_string_amount_valid(self, amount):
        if(amount.startswith("0")):
            return False
        return True

    def is_amount_valid(self, amount):
        """Function to check if passed in amount is within limits for machine and agent users.
        Used by deposit, withdraw, and transfer transaction commands.
        """
        # Machine amount limit
        if((amount < 0 or amount > 100000) and not TxnProcess.login_user_agent):
            return False
        # Agent amount limit
        if((amount < 0 or amount >= 100000000) and TxnProcess.login_user_agent):
            return False
        return True

    def is_name_valid(self, accName):
        """Function to check if passed in account name is valid."""
        if(len(accName) < 3 or len(accName) > 30):
            return False
        if(accName[0] is " " or accName[len(accName)-1] is " "):
            return False
        if(not accName.replace(" ", "").isalnum()):
            return False
        return True

    def is_within_withdraw_limit(self, accNum, amount):
        """Function to check if passed in account will surpass daily withdraw limit by completing pending withdrawal.
        Returns False if limit will be reached with pending withdrawal, true if withdrawal is valid.
        """
        newAmount = TxnProcess.withdraw_limits[accNum] + amount
        # Machine user can only withdraw max $1000 from a single acount in a single session
        if(newAmount > 100000 and not TxnProcess.login_user_agent):
            return False
        return True

    def get_input(self, prompt):
        """Function to get input from the user by first presenting the given prompt to them.
        """

        # Python 2.x requires use of raw_input() if reading from std input file.
        # While Python 3.x has merged raw_input() functionality into the standard input() function.
        if sys.version_info[0] < 3:
            inputValue = raw_input(prompt).upper()
        else:
            inputValue = input(prompt).upper()

        if (inputValue == "Q" or inputValue == "QUIT"):
            sys.exit()

        print("\nUser Entered:" + inputValue)

        return inputValue

    def validTxnList(self, txn_message_list):
        """Function to check if the list of transactionsummary messages is of valid format.
        Returns False if incorrect format
        """

        for string in txn_message_list:
            # check max 61 characters
            count = 0
            for char in string:
                count = count + 1
                if(count > 61):
                    return False
            # test first 3 characters is a valid txn code
            txnCode = string[:3]
            if(txnCode != "DEP" and txnCode != "WDR" and txnCode != "XFR" and txnCode != "NEW" and txnCode != "DEL" and txnCode != "EOS"):
                return False
            #test that all the individual elements are seperated by exactly one space
            count = 0
            for char in string:
                if(char == " "):
                    count = count + 1
                    if(count > 4):
                        return False
            #test 7 digit account number TO
            substring = string[4:]
            #check first character is no zero
            firstChar = substring[0:0]
            if(firstChar == "0"):
                return False
            count = 0
            for char in substring:
                if(char != " "):
                    count+=1
                else:
                    break
                if(count > 7):
                    return False
            #test 7 digit account number FROM
            #find index for from account number
            spaceCount = 0
            count = 0
            for char in string:
                count += 1
                if(char == " "):
                    spaceCount += 1
                    if(spaceCount >= 3):
                        break
            substring = string[count:]
            #check first character is no zero
            firstChar = substring[0:0]
            if(firstChar == "0"):
                return False
            count = 0
            for char in substring:
                if(char != " "):
                    count+=1
                else:
                    break
                if(count > 7):
                    return False

            #check monetary amount is between 3 8 decimmal digits
            spaceCount = 0
            count = 0
            for char in string:
                count += 1
                if(char == " "):
                    spaceCount += 1
                    if(spaceCount >= 2):
                        break
            substring = string[count:]
            count = 0
            for char in substring:
                if(char != " "):
                    count+=1
                else:
                    break

            if(count < 3 or count > 8):
                return False

            #test that the new account name is between 3 - 30 characters
            txnCode = string[:3]
            if(txnCode == "NEW"):
                wordList = string.split()
                if(len(wordList[-1]) < 3 or len(wordList[-1]) > 30):
                    return False

            #test that only alphanumeric and space characters'
            #if(re.match('^[\w\s\w\s\w\s\w\s[\w\*]*]+',string) is not None):
            #    return False

            #test that there is no beginning or ending trailing space
            if string.startswith(" ") or string.endswith(" "):
                return False

        return True
