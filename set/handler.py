import hashlib

import cbor


from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError

ADDRESS_PREFIX = hashlib.sha512(
    "intkey".encode('utf-8')).hexdigest()[0:6]


def make_address(name):
    return ADDRESS_PREFIX + hashlib.sha512(
        name.encode('utf-8')).hexdigest()[-64:]


class SetGetTransactionHandler(TransactionHandler):

    @property
    def family_name(self):
        return "intkey"

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [ADDRESS_PREFIX]

    def apply(self, transaction, context):

        content = cbor.loads(transaction.payload)

        name = content['Name']
        value = content['Value']

        address = make_address(name)

        address = make_address(name)
        encoded = cbor.dumps({name:value})
        addresses = context.set_state({address: encoded}) # SET