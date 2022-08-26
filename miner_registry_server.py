import os
import socket

MINER_PORT = 5020
SERVER_HOST = "0.0.0.0"

def register_miner():
    while True:
        s = socket.socket()
        s.bind((SERVER_HOST, MINER_PORT))
        s.listen(5)
        print(f"[*] Listening as {SERVER_HOST}:{MINER_PORT}")

        client_socket, address = s.accept()
        client_socket.settimeout(120)

        if not os.path.exists("mining.json"):
            data_file = open("mining.json", "w")
            data_file.write("{}")

        data_file = open("mining.json", "r")
        data = data_file.read()
        dum = data

        json_values = dum.replace("{", "").replace("}", "").replace(" ", "").split("]")

        client_socket.sendall(hex(len(json_values)).encode('utf8'))
        print("Sent mining data")
        # close the
        data_file.close()

        fz = open("mining.json", "w")
        fz_text = data
        fz_text = fz_text[:len(fz_text) - 1]

        bytes_read = client_socket.recv(2048)
        print("Received key")

        client_socket.close()
        print("Closed connection")
        print("Writing this: " + str((fz_text + "[ miner_id: " + str(hex(len(json_values)))
                                      + ",\n" + "public_key: " + bytes_read.decode('utf8') + "]" + "}")))

        fz.write(fz_text + "[ miner_id: " + str(hex(len(json_values)))
                 + ",\n" + "public_key: " + bytes_read.decode('utf8') + "]" + "}")
        fz.close()
        print("Finished updating mining.json")

        # close the server socket
        s.close()
