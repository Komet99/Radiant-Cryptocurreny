-- UNFERTIG -- Nichts anfassen, bis ich da bin!!

Guten Tag!
Um Radiant erstmal lokal zum Laufen zu bekommen, befolgen Sie diese Schritte:

1. Starten Sie miner_registry_server
2. Starten Sie miner.py

Client-Anweisungen:

1. Starten Sie clientSetUp.py und folgen Sie den Anweisungen.
2. Starten Sie transaction_client.py, um Transaktionen aufzugeben.
3. Sollte dies erfolgt sein, können Sie die Serveraddresse in clientdata/blockchain-address.txt ändern, dabei handelt es sich um den ersten der beiden Werte. Standardmäßig sollten diese "localhost" und 5010 sein. Dabei ist der zweite Wert der port des servers.


Server-Anweisungen synchron zu den Client-Anweisungen (als Schritt + C vor einem Doppelpunkt angegeben):

2C: Starten Sie localhost_server.py, um Transaktionen ohne weitere Einstellungen lokal entgegennehmen zu können.
