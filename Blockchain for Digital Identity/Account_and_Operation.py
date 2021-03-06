from Signature import *
import hashlib

'''
Account class
- stores and exchanges data 
- signs and verifies data
'''
class Account:

    # Constructor
    def __init__(self, name: str, type: str):
        # Key Pair (wallet)
        self.key_pair = KeyPair()
        # Name
        self.name = name
        # Identity / Organization
        self.type = type
        # Identifier = SHA256 - hash
        self.ID = hashlib.sha256(str(self).encode('utf-8')).hexdigest()
        # Dictionary with personal data
        self.personal_data = {}
        # Dictionary with received data
        self.received_data = {}

    def createOperation(self, recipient, field: str):
        sig = self.signData(str(field) + str(self.personal_data[field]))
        operation = Operation(self, recipient, field, self.personal_data[field], sig)
        recipient.received_data[field] = self.personal_data[field]
        return operation

    def signData(self, message):
        sign = Signature()
        return sign.signData(self.key_pair.privateKey, message)

    def __str__(self):
        return str(self.name) + self.type + str(self.key_pair.pubKStr)

    def printInfo(self):
        print("Account Name: " + str(self.name) + '\n' + \
               "ID: " + str(self.ID) + '\n' + \
               "Account Type:" + str(self.type) + '\n' + \
               str(self.key_pair.pubKStr) + '\n')

    def printData(self):
        print("Personal Data :")
        if len(self.personal_data.items()):
            for key, value in self.personal_data.items():
                print('\t' + str(key) + " : " + str(value))
        else:
            print("\tNone")

        print("Received Data :")
        if len(self.received_data.items()):
            for key, value in self.received_data.items():
                print('\t' + str(key) + " : " + str(value))
        else:
            print("\tNone")

    # Prints the Key Pair
    def printKeyPair(self):
        self.key_pair.printKeyPair()


class Identity(Account):

    def __init__(self, name):
        super(Identity, self).__init__(name, "Identity")


class Organization(Account):

    def __init__(self, name):
        super(Organization, self).__init__(name, "Organization")


'''
Operation Class

Constructor :
    initiates a data exchange

boolean verifyOperation :
    returns if the operation is valid

'''


class Operation:
    def __init__(self, sender, receiver, field: str, value: str, signature: Signature):
        self.sender = sender        # Account
        self.receiver = receiver    # Account
        self.item = (field, value)  # Item (key_in_dictionary, value)
        self.signature = signature  # Signature

    def verifyOperation(self):
        if self.item[0] == '' or self.item[1] == '':
            return false
        return Signature.verifySignature(self.signature, self.signature, str(self.item[0]) + str(self.item[1]), self.sender.key_pair.publicKey)

    def __str__(self):
        return "\t\t" + str(self.sender.ID) + "\n\t\t -> \n\t\t" + str(self.receiver.ID) + "\n\t\t" + str(self.item[0]) + " : " + str(self.item[1]) + '\n'

    def print(self):
        print(str(self)) + "\n"
