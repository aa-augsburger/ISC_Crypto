import sys
from PySide6.QtWidgets import QApplication


from Client_CLI import Client_CLI
from Client_GUI import Client_GUI

ADDRESS = "vlbelintrocrypto.hevs.ch"
PORT = 6000

def start_cli():
    print("Welcome to ISC Crypto")
    client = Client_CLI(ADDRESS, PORT)
    while True:
        client.command_controller()

def start_gui():
    app = QApplication(sys.argv)
    window = Client_GUI()
    sys.exit(app.exec())


if __name__ == '__main__':
    mode = sys.argv[1]
    match mode:
        case "gui":
            start_gui()
        case "cli":
            start_cli()

    print(mode)
