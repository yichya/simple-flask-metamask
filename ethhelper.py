# coding=utf8

import os
import sys
from web3 import Web3, HTTPProvider

w3 = Web3(HTTPProvider(os.environ.get('web3', "https://ganache.yichya.dev")))
erc20abi = '''[
    {
        "inputs": [],
        "stateMutability": "payable",
        "type": "constructor"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "oldOwner",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnerSet",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "_from",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "Sent",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "changeOwner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "charge",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getOwner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address payable[]",
                "name": "addrs",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amnts",
                "type": "uint256[]"
            }
        ],
        "name": "withdrawls",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]'''
gstAddress = '0x1e6717694D17535A05Eaf693595dF0d42ff0511F'
gstToken = w3.eth.contract(address=gstAddress, abi=erc20abi)


def multi_send(address_list, amount_list, value, from_address):
    return gstToken.functions.withdrawls(address_list, amount_list).buildTransaction({
        "value": value,
        'maxFeePerGas': w3.toWei(250, 'gwei'),
        'maxPriorityFeePerGas': w3.toWei(2, 'gwei'),
    })

def get_receipt(txhash, data):
    receipt = w3.eth.wait_for_transaction_receipt(txhash)
    logs = gstToken.events.Sent().processReceipt(receipt)
    return logs

if __name__ == "__main__":
    import pdb 
    pdb.set_trace()
