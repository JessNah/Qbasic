import Main
import TxnProcess
import ErrorHandler


class Utility:
    def __init__(self):
        self.variable = 0

    def process_account_file(self, fileName): #creating valid account list array
        with open(fileName) as file:
            for line in file:
                line = line.strip() #or some other preprocessing
                #TODO remove all trailing spaces and leading spaces from each line before converting to int
                line = int(line)
                TxnProcess.valid_acc_list.append(line) #storing everything in memory!

    #forms the transaction msg to be added into the transaction summary file
    def create_txn_msg(self, txnCode, toAcc, amount, fromAcc, accName):
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

    #create the transaction summary file
    def create_txn_summary_file(self, listTxnMsgs):
        myfile = open('txn_summary_file.txt', 'w')
        for line in listTxnMsgs:
                #var1, var2 = line.split(",");
                myfile.writelines(line + "\n")
        myfile.close()

    def is_account_valid(self, accNum):
        if(accNum in TxnProcess.valid_acc_list):
            return True
        else:
            return False
    
    def is_account_unique(self, accNum):
        if(accNum in TxnProcess.valid_acc_list or accNum in TxnProcess.new_acc_list):
            return False
        else:
            return True

    def is_amount_valid(self, amount):
        if((amount < 0 or amount > 100000) and not TxnProcess.login_user_agent):
            return False
        if((amount < 0 or amount >= 100000000) and TxnProcess.login_user_agent):
            return False
        return True

    def is_name_valid(self, accName):
        if(len(accName) < 3 or len(accName) > 30):
            return False
        if(accName[0] is " " or accName[len(accName)-1] is " "):
            return False
        if(not accName.replace(" ", "").isalnum()):
            return False
        return True
