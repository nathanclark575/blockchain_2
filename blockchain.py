import hashlib
import json
import datetime as dt

"""
Creates a blockchain that can:
    be added to (mined)
    have its validity checked
"""

class Blockchain:

    def __init__(self):
        self.chain = list()
        # Need an initial block to start the chain
        initial_block = self.make_block(data="I am the initial block", proof=1, previous_hash=0, index=0)
        self.chain.append(initial_block)

    # This genrates blocks
    """
        Each block has a set of data that is used to create a hash code. This is used with the previous hashcode to
        check that the blockchain is valid using proof
    """
    def make_block(self, data, proof, previous_hash, index):
        block = {
            "index": index,
            "timestamp": str(dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous hash": previous_hash
        }
        return block

    # This adds blocks to the blockchain and returns the block to the miner
    def mine_block(self, data):
        previous_block = self.prev_block()
        previous_proof = previous_block["proof"]
        index = len(self.chain)

        # work out the new proof
        proof = self.proof_of_work(previous_proof, index, data)

        previous_hash = self.hash_block(previous_block)
        block = self.make_block(data, proof, previous_hash, index)

        self.chain.append(block)
        return block

    # hash the block and genrate a cryptographic hash value of that block
    def hash_block(self, block):
        # stores the encoded block in block as a json object
        encoded_block = json.dumps(block, sort_keys=True).encode()
        # return its hash
        return hashlib.sha256(encoded_block).hexdigest()

    # returns the previous block
    def prev_block(self):
        return self.chain[-1]

    # work out the new proof
    def proof_of_work(self, previous_proof, index, data):
        """
        increment the new proof until a hashcode with two starting values is genrated when placed in
        the "to_digest" function.

        When this occours, return the new_proof.

        This is the time constraining part of genrating a new block
        as meeting this condition can become very time consuming when the to_digest is complecated and when
        a large number of zeros are required

        The to_digest function is hidden so that people can not guess a hash
        """
        new_proof = 1
        check_proof = False
        while not check_proof:
            to_digest = self.to_digest(new_proof, previous_proof, index, data)
            hash_val = hashlib.sha256(to_digest).hexdigest()
            # number of zeros makes it exponentaly harder
            if hash_val[:2] == "00":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def to_digest(self, new_proof, previous_proof, index, data):
        # keep this secret to system, more complex the better (use previous points)
        to_digest = str(new_proof ** 2 - previous_proof ** 2 + index) + data
        # udf version
        return to_digest.encode()

    # check to see if chain is valid
    def is_chain_valid(self):
        current_block = self.chain[0]
        current_index = 0

        while current_index < len(self.chain) - 1:
            next_block = self.chain[current_index + 1]
            # easy check
            if next_block["previous hash"] != self.hash_block(current_block):
                return False

            # check the proof_of_work that makes the blockchain secure to manipulation
            current_proof = current_block["proof"]
            next_index, next_data, next_proof = next_block["index"], next_block["data"], next_block["proof"]

            hash_value = hashlib.sha256(
                self.to_digest(new_proof=next_proof, previous_proof=current_proof, index=next_index,
                               data=next_data)).hexdigest()

            # more zeros would make this harder to circumvent and the blockchain more secure
            if hash_value[:2] != "00":
                return False

            current_block = next_block
            current_index += 1

        return True


if __name__ == "__main__":

    print("This output is used to show the functionality of the blockchain data structure")

    # initilize
    bc = Blockchain()
    # add block_1 to the chain
    print("block_1 added to the chain = " + str(bc.mine_block("Hello World")))

    print("The chain = " + str(bc.chain))

    print("block_2 added to the chain = " + str(bc.mine_block("This is a block")))

    print("The chain = " + str(bc.chain))

    print("Is chain valid? " + str(bc.is_chain_valid()))

    print("Editing the chain")
    bc.chain[1]["data"] = "This is broken"
    #bc.chain[1]["data"]

    print("Is chain valid? " + str(bc.is_chain_valid()))

    print("The chain = " + str(bc.chain))