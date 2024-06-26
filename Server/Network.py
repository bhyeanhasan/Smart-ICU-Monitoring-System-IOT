import socket

print("\n**** Make sure both Server and Pi connected to the same network ****\n")
# Server IP Address
server_host = socket.gethostname()
IP1 = socket.gethostbyname(socket.gethostname())
print(
    "** Server Side **\nHost Name\t:\t" + server_host + "\nIP Address\t:\t" + IP1 + "\nServer URL:\t:\t" + IP1 + ":8000")

# Raspberry PI
pi_host = "pstu"
try:
    IP2 = socket.gethostbyname(pi_host)
    print(
        "\n** Raspberry Side **\nHost Name\t:\tpstu" + "\nIP Address\t:\t" + IP2 + "\n\n** Establish Remote Connection **\nAddress\t\t:\t" + IP2 + "\nUsername\t:\tpi\nPassword\t:\tcse")
except:
    print("\n** Raspberry Side **\nPI is not connected\nCan't connect to WIFI? Hint : use Earthnet or set a WIFI")
    print("SSID\t\t:\t" + "DIR")
    print("PASS\t\t:\t" + "csecsecse1")
