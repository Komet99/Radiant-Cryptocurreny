Welcome! To get started with radiant, follow these simple steps!

1. Start miner_registry.py
2. Start miner.py

ClientInstructions:

1. Start clientSetUp.py and follow instructions.
2. Start transaction_client.py to commission transactions.
3. After that, you can change the server address in clientdata/blockchain-address.txt, which is the first of the two values. Usually these values are "localhost" and 5010. The second value is the server port in that matter.

This is it!
Now you should be able to use the fairly self-explaining client, which has just two basic options:

1. Create a new transaction
or
2. Upload all existing transactions to the server

As you can see, it could not be any easier!


Server Instrcutions:

Start localhost_server.py to receive transactions locally without further setup.
Additionally, start:
- server_key_distributor.py 	(Generates and shares the public key of the server)
- block_distributor.py		    (Shares the "raw" blocks with miners)
- block_processor.py		    (Processes received blocks and adds them to the blockchain)
- transaction_processor.py	    (Processes received transactions to blocks)