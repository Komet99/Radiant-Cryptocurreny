-- UNFERTIG -- Nichts anfassen, bis ich da bin!!

Guten Tag!
Um Radiant erstmal lokal zum Laufen zu bekommen, befolgen Sie diese Schritte:

1. Starten Sie miner_registry_server
2. Starten Sie miner.py

Client-Anweisungen:

1. Starten Sie clientSetUp.py und folgen Sie den Anweisungen.
2. Starten Sie transaction_client.py, um Transaktionen aufzugeben.
3. Sollte dies erfolgt sein, können Sie die Serveraddresse in clientdata/blockchain-address.txt ändern, dabei handelt es sich um den ersten der beiden Werte. Standardmäßig sollten diese "localhost" und 5010 sein. Dabei ist der zweite Wert der port des servers.

Das war's!
Nun sollten Sie selbsständig den sich soweit selbsterklärenden Client verwenden können.



Server-Anweisungen:

Starten Sie localhost_server.py, um Transaktionen ohne weitere Einstellungen lokal entgegennehmen zu können.
Starten Sie außerdem:
- server_key_distributor.py 	(Generiert und teilt den public key des Servers)
- block_distributor.py		(Teilt die "rohen" Blöcke mit dem Miner")
- block_processor.py		(Verarbeitet eingereichte Blöcke und fügt diese ggf. in die Blockchain ein)
- transaction_processor.py	(Verarbeitet eingereichte Transaktionen zu Blöcken)