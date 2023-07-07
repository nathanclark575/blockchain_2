import fastapi
import blockchain

"""
ReadMe:
This script uses FastAPI and my blockchain script to make an API acsessable blockchain

Room for update:
To make an API that acsesses a stored blockchain on a json file so that the blockchain is stored and mainted when the
connection to the API is terminated.
"""

# to open API
"""
1. Go to this directory
2. enter the following into the terminal:
    source venv/bin/activate
    uvicorn main:app --reload
3. type in to the browser:
    localhoast:8000/docs
"""

bc = blockchain.Blockchain()
app = fastapi.FastAPI()

# endpoint to mine (add) a block
@app.post("/mine_block/")
def mine_block(data):
    if not bc.is_chain_valid():
        return fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    block = bc.mine_block(data)
    return block

# endpoint to return entire blockchain
@app.get("/blockchain/")
def get_blockchain():
    if not bc.is_chain_valid():
        return fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    chain = bc.chain
    return chain

# endpoint to see if blockchain is valid
@app.get("/validate/")
def is_blockchain_valid():
    return bc.is_chain_valid()