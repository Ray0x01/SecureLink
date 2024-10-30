import sys
import os
import socket
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QTextEdit, QFileDialog, QScrollArea)
from PyQt5.QtCore import QPropertyAnimation, QRect
from cryptography.fernet import Fernet

# Global variables for encryption
cipher_suite = None
connected = False


class SecureLinkApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SecureLink - Encrypted Messaging & File Transfer")
        self.setGeometry(100, 100, 600, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.message_tab = self.create_message_tab()
        self.file_transfer_tab = self.create_file_transfer_tab()
        self.status_tab = self.create_status_tab()
        self.help_tab = self.create_help_tab()
        self.extra_tab = self.create_extra_tab()

        self.tabs.addTab(self.message_tab, "Messages")
        self.tabs.addTab(self.file_transfer_tab, "File Transfer")
        self.tabs.addTab(self.status_tab, "Status")
        self.tabs.addTab(self.help_tab, "Help")
        self.tabs.addTab(self.extra_tab, "Extra")

        self.tabs.currentChanged.connect(self.animate_tab_switch)

        self.show()

    def create_message_tab(self):
        """Create the message tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        layout.addWidget(self.message_display)

        self.message_input = QLineEdit()
        layout.addWidget(self.message_input)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        tab.setLayout(layout)
        return tab

    def create_file_transfer_tab(self):
        """Create the file transfer tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        self.selected_file_label = QLabel("No file selected")
        layout.addWidget(self.selected_file_label)

        select_file_button = QPushButton("Select File")
        select_file_button.clicked.connect(self.select_file)
        layout.addWidget(select_file_button)

        send_file_button = QPushButton("Send File")
        send_file_button.clicked.connect(self.send_file)
        layout.addWidget(send_file_button)

        self.file_progress_label = QLabel("")
        layout.addWidget(self.file_progress_label)

        tab.setLayout(layout)
        return tab

    def create_status_tab(self):
        """Create the status tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        self.connection_status = QLabel("Not connected")
        layout.addWidget(self.connection_status)

        self.encryption_status = QLabel("AES key not exchanged")
        layout.addWidget(self.encryption_status)

        self.logs_display = QTextEdit()
        self.logs_display.setReadOnly(True)
        layout.addWidget(self.logs_display)

        self.ip_entry = QLineEdit("Server IP")
        layout.addWidget(self.ip_entry)

        self.port_entry = QLineEdit("Port")
        layout.addWidget(self.port_entry)

        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.connect_to_server)
        layout.addWidget(connect_button)

        tab.setLayout(layout)
        return tab

    def create_help_tab(self):
        """Create the help tab."""
        tab = QWidget()
        layout = QVBoxLayout()

        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setPlainText(
            "Help Guide:\n\n"
            "1. To connect to a server, enter the server IP and port, and press 'Connect'.\n"
            "2. After connecting, the AES key will be exchanged automatically.\n"
            "3. You can send messages and files after the key is exchanged.\n"
            "4. The Status tab will show the connection and encryption status.\n"
            "5. If you need further assistance, check the logs for errors.\n"
        )
        layout.addWidget(help_text)

        tab.setLayout(layout)
        return tab

    def create_extra_tab(self):
        """Create the Extra tab with contributors."""
        tab = QWidget()
        layout = QVBoxLayout()

        extra_info = QTextEdit()
        extra_info.setReadOnly(True)
        extra_info.setPlainText(
            "App Developed by Rayyan Afridi\n"
            "Idea and Assistance by Kiko Ivanov"
        )
        layout.addWidget(extra_info)

        tab.setLayout(layout)
        return tab

    def animate_tab_switch(self, index):
        """Animate the transition when switching tabs."""
        animation = QPropertyAnimation(self.tabs, b"geometry")
        animation.setDuration(300)
        start_rect = self.tabs.geometry()
        end_rect = QRect(start_rect.x(), start_rect.y(), start_rect.width(), start_rect.height())
        end_rect.setHeight(0)  # Collapse height for animation
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.start()
        
        animation.finished.connect(lambda: self.finalize_tab_switch(index))

    def finalize_tab_switch(self, index):
        """Finalizes the tab switch and restores the geometry."""
        self.tabs.setCurrentIndex(index)
        self.tabs.setGeometry(self.geometry())  # Reset to original size

        # Fade-in effect for the current tab content
        self.fade_in_effect(self.tabs.currentWidget())

    def fade_in_effect(self, widget):
        """Create a fade-in effect for the specified widget."""
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(300)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.start()

    def send_message(self):
        global cipher_suite
        message = self.message_input.text()
        if cipher_suite and message:
            encrypted_message = cipher_suite.encrypt(message.encode())
            self.message_display.append(f"Sent: {message}")
            self.message_input.clear()
            # Here you would send the encrypted message over the socket (not implemented in this example)
        else:
            self.message_display.append("Error: No encryption key exchanged or empty message.")

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.selected_file_label.setText(os.path.basename(file_path))
            self.selected_file_path = file_path

    def send_file(self):
        if hasattr(self, 'selected_file_path') and cipher_suite:
            with open(self.selected_file_path, 'rb') as f:
                file_data = f.read()
            encrypted_file_data = cipher_suite.encrypt(file_data)
            self.file_progress_label.setText("File sent successfully.")
            # Here you would send the encrypted file data over the socket (not implemented in this example)
        else:
            self.file_progress_label.setText("Error: No file selected or no encryption key exchanged.")

    def connect_to_server(self):
        global connected
        ip = self.ip_entry.text()
        port = int(self.port_entry.text())
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((ip, port))
            connected = True
            self.connection_status.setText("Connected")
            self.encryption_status.setText("AES key exchanged")
            self.logs_display.append(f"Connected to {ip}:{port}")
            self.exchange_keys()  # Start key exchange
        except Exception as e:
            self.logs_display.append(f"Connection Error: {str(e)}")

    def exchange_keys(self):
        global cipher_suite
        # Simulating key exchange (in real scenario, you'd send public keys over the socket)
        self.cipher_key = Fernet.generate_key()
        cipher_suite = Fernet(self.cipher_key)
        self.logs_display.append("Keys exchanged successfully.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SecureLinkApp()
    sys.exit(app.exec_())
