Making a transaction processor and client for Hyperledger Sawtooth DLT. 

We will remove the IntegerKey transaction processor from the sawtooth-default network. Notice that the client and transaction processor need to have the same data model, thus we will also use the IntegerKey data model.

```
#  intkey-tp-python:
#    image: hyperledger/sawtooth-intkey-tp-python:1.0
#    container_name: sawtooth-intkey-tp-python-default
#    depends_on:
#      - validator
#    entrypoint: intkey-tp-python -vv -C tcp://validator:4004

```

and change the shell `definition` into:


```
shell:
    image: hyperledger/sawtooth-all:1.0
    container_name: sawtooth-shell-default
    depends_on:
      - rest-api
    entrypoint: "bash -c \"\
        sawtooth keygen && \
        tail -f /dev/null \
        \""
    volumes:
      - ./set:/set

```