#System-specific parameters and functions

import sys 

# The pkg_resources module distributed with setuptools 
# provides an API for Python libraries to access their 
# resource files, and for extensible applications and 
# frameworks to automatically discover plugins
import pkg_resources 

# TransactionProcessor is a generic class for communicating with 
# a validator and routing transaction processing requests to a 
# registered handler. It uses ZMQ and channels to handle requests concurrently.
from sawtooth_sdk.processor.core import TransactionProcessor

# Set up the console logging for a transaction processor. :param verbose_level: 
# The log level that the console should print out :type verbose_level: int
from sawtooth_sdk.processor.log import init_console_logging


from handler import SetGetTransactionHandler


def main(args=None):
    processor = TransactionProcessor(url="tcp://validator:4004")
    handler = SetGetTransactionHandler()
    # Adds a transaction family handler :param handler: the handler to 
    # be added :type handler: TransactionHandler
    processor.add_handler(handler)
    #Connects the transaction processor to a validator and starts listening
    #for requests and routing them to an appropriate transaction handler.
    processor.start()

if __name__ == '__main__':
    main()