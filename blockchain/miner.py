import hashlib
import requests
import json
import sys
import os

from uuid import uuid4

# from timeit import default_timer as timer
from time import time

import random

def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...999123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    """
    proof = 0


    last_hash = hashlib.sha256(json.dumps(last_proof).encode()).hexdigest()

    start = time()
    print("Searching for next proof")
    while not valid_proof(last_hash, proof):
        proof += 1
        
    end = time()
    print("Proof found: " + str(proof) + " in " + str(end - start))

    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the last hash match the first six characters of the proof?

    IE:  last_hash: ...999123456, new hash 123456888...
    """
    current_hash = hashlib.sha256(json.dumps(proof).encode()).hexdigest()
    if last_hash[-6:] == current_hash[:6]:
        return True
    else:
        return False

# print(proof_of_work(99))


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    if len(id) == 0:
        f = open("my_id.txt", "w")
        # Generate a globally unique ID
        id = str(uuid4()).replace('-', '')
        print("Created new ID: " + id)
        f.write(id)
        f.close()
    # Run forever until interrupted
    while coins_mined < 3:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        print(data,"data")
        print("current proof",data.get('proof'))
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
