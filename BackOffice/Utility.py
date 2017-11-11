import TxnProcess
import ErrorHandler
import sys
import re
import Account

err = ErrorHandler.ErrorHandler()

class Utility:
    """Class used for utility functions for QBasic application.
    Utility functions are by TxnProcess for routine operations.
    """

    def process_masterAccount(self, fileName):
        with open(fileName) as file:
            for line in file:
                #remove leading and trailing spaces.
                line = line.strip()
                try:
                    items = line.split(" ")
                    accountObj = Account.Account(int(items[0]), int(items[1]), items[2])
                    TxnProcess.accounts_dic[accountObj.getAccountNum()] = accountObj
                except ValueError:
                    err.process_error("ERR_MASTERACCOUNT")
                    sys.exit()

    def create_master_valid_account_files(self, dic, masterAccountFile, validAccountFile):
        """Function to write all cached dictionary items to master account file and valid account file."""
        masterF = open(masterAccountFile, 'w')
        validF = open(validAccountFile, 'w')
        for item in dic:
            #TODO make sure the account balance is formated to 3 decimal places
            masterF.writelines(str(dic[item].getAccountNum()) + " " + str(dic[item].getAccountBalance()) + " " + dic[item].getAccountName() + "\n")
            validF.writelines(str(dic[item].getAccountNum()) + "\n")
        masterF.close()
        validF.close()
