import sys

#Returns an algorithm instance by name.
from sawtooth_signing import create_context 

#Factory for generating Signers.
from sawtooth_signing import CryptoFactory


# A binary data serialization format 
import cbor

#This module implements a common interface to many different
#secure hash and message digest algorithms.
import hashlib

#using the sha512 algorithms
from hashlib import sha512


from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch
from sawtooth_sdk.protobuf.batch_pb2 import BatchList

import urllib.request
from urllib.error import HTTPError

if len(sys.argv) != 3:
    sys.exit("This client needs a name and a value")

context = create_context('secp256k1') #Returns an algorithm instance by name.
private_key = context.new_random_private_key() #Generates a new random PrivateKey using this context.
signer = CryptoFactory(context).new_signer(private_key) #Create a new signer for the given private key.


FAMILY_NAME = 'set'

# define the payload, similar to the intkey
payload = {
    'Name': sys.argv[1],
    'Value':sys.argv[2]}

payload_bytes = cbor.dumps(payload)

ADDRESS_PREFIX = hashlib.sha512(
    FAMILY_NAME.encode('utf-8')).hexdigest()[0:6]


def make_address(name):
    return ADDRESS_PREFIX + hashlib.sha512(
        name.encode('utf-8')).hexdigest()[-64:]


txn_header_bytes = TransactionHeader(
    family_name=FAMILY_NAME,
    family_version='1.0',
    inputs=[make_address(payload["Name"])],
    outputs=[make_address(payload["Name"])],
    signer_public_key=signer.get_public_key().as_hex(),
    batcher_public_key=signer.get_public_key().as_hex(),
    dependencies=[],
    payload_sha512=sha512(payload_bytes).hexdigest()
).SerializeToString()

signature = signer.sign(txn_header_bytes)

txn = Transaction(
    header=txn_header_bytes,
    header_signature=signature,
    payload=payload_bytes
)

txns = [txn]

batch_header_bytes = BatchHeader(
    signer_public_key=signer.get_public_key().as_hex(),
    transaction_ids=[txn.header_signature for txn in txns],
).SerializeToString()

signature = signer.sign(batch_header_bytes)

batch = Batch(
    header=batch_header_bytes,
    header_signature=signature,
    transactions=txns
)

batch_list_bytes = BatchList(batches=[batch]).SerializeToString()

try:
    request = urllib.request.Request(
        'http://rest-api:8008/batches',
        batch_list_bytes,
        method='POST',
        headers={'Content-Type': 'application/octet-stream'})
    response = urllib.request.urlopen(request)

except HTTPError as e:
    response = e.file