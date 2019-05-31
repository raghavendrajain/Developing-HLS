

#This module implements a common interface to many different
#secure hash and message digest algorithms.
import hashlib

# A binary data serialization format 
import cbor


# TransactionHandler is the Abstract Base Class that defines 
# the business logic for a new transaction family. The family_name, 
# family_versions, and namespaces properties are used by the processor 
# to route processing requests to the handler.
from sawtooth_sdk.processor.handler import TransactionHandler

# Raised for an Invalid Transaction.
from sawtooth_sdk.processor.exceptions import InvalidTransaction

# Raised when an internal error occurs during transaction processing.
from sawtooth_sdk.processor.exceptions import InternalError

ADDRESS_PREFIX = hashlib.sha512("set".encode('utf-8')).hexdigest()[0:6]

def make_address(name):
    return ADDRESS_PREFIX + hashlib.sha512(
        name.encode('utf-8')).hexdigest()[-64:]

class SetGetTransactionHandler(TransactionHandler):

    #family_name should return the name of the transaction family
    #that this handler can process, e.g. “intkey”
    @property
    def family_name(self):
        return "set"

    #family_versions should return a list of versions this transaction family 
    #handler can process, e.g. [“1.0”]
    @property
    def family_versions(self):
        return ['1.0']

    #namespaces should return a list containing all 
    #the handler’s namespaces, e.g. [“abcdef”]

    @property
    def namespaces(self):
        return [ADDRESS_PREFIX]

    # Apply is the single method where all the business logic 
    # for a transaction family is defined. The method will be called 
    # by the transaction processor upon receiving a TpProcessRequest
    # that the handler understands and will pass in the TpProcessRequest
    # and an initialized instance of the Context type.

    def apply(self, transaction, context):

        content = cbor.loads(transaction.payload) 

        name  = content["Name"]
        value = content["Value"]

        address   = make_address(name)
        encoded   = cbor.dumps({name:value})

        #set_state requests that each address in the 
        #provided dictionary be set in validator state 
        #to its corresponding value. A list is returned 
        #containing the successfully set addresses.
        addresses = context.set_state({address: encoded}) #SET


