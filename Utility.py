import Main
import TxnProcess
import ErrorHandler


class Utility:
    """Class used for utility functions for QBasic application.
    Utility functions are by TxnProcess for routine operations.
    """

    def process_account_file(self, fileName):
        """Function to process valid accounts file.
        Valid account numbers are stored in TxnProcess.valid_acc_list.
        """ 
        with open(fileName) as file:
            for line in file:
                line = line.strip() #or some other preprocessing
                #TODO remove all trailing spaces and leading spaces from each line before converting to int
                line = int(line)
                TxnProcess.valid_acc_list.append(line) #storing everything in memory!
        #TODO ensure file ends in 0000000
    
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
                #var1, var2 = line.split(",");
                myfile.writelines(line + "\n")
        myfile.close()

    def is_account_valid(self, accNum):
        """Function to check if passed in account number is valid."""
        if(accNum in TxnProcess.valid_acc_list):
            return True
        else:
            return False
    
    def is_account_unique(self, accNum):
        """Function to check if passed in account number is unique(or new)."""
        if(accNum in TxnProcess.valid_acc_list or accNum in TxnProcess.new_acc_list):
            return False
        else:
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