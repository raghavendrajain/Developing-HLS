import sys
import pkg_resources

from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_sdk.processor.log import init_console_logging
from handler import SetGetTransactionHandler


def main(args=None):
    processor = TransactionProcessor(url="tcp://validator:4004")
    handler = SetGetTransactionHandler()

    processor.add_handler(handler)
    processor.start()

if __name__ == '__main__':
    main()