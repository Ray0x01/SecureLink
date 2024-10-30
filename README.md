# SecureLink

**SecureLink** is a Python-based encrypted messaging and file transfer application with a graphical user interface (GUI) built using PyQt5. The app provides end-to-end encryption for secure communication, making it ideal for anyone who values privacy.

Developed by Rayyan Afridi.

## Features

- End-to-end encrypted messaging using AES encryption.
- Secure file transfer with automatic encryption.
- Status tracking for connection and encryption.
- Simple and user-friendly graphical interface.
- Logs to track connection status and encryption key exchange.
- Additional animations for smooth tab switching.

## Prerequisites

- Python 3.6 or higher
- `cryptography` library
- `PyQt5` library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/kaliafridi/SecureLink
    cd SecureLink
    ```

2. Install the required libraries:

    ```bash
    pip3 install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python3 securelink.py
    ```

## Usage

1. **Connect to a Server**: Enter the server IP and port in the "Status" tab, then click "Connect". Once connected, the AES encryption key will be exchanged.
   
2. **Send Encrypted Messages**: Type your message in the "Messages" tab and click "Send". Your message will be encrypted before being sent.
   
3. **Transfer Files**: Select a file from the "File Transfer" tab and click "Send File" to transfer it securely.

4. **Check Status**: The "Status" tab shows connection status and encryption information.

5. **Logs**: Use the logs to troubleshoot connection issues or encryption errors.

## How It Works

- **Encryption**: SecureLink uses AES encryption with the `cryptography` library. The encryption key is exchanged during the connection process, ensuring all messages and files are securely encrypted before transmission.
  
- **Messaging**: After the encryption key exchange, messages are encrypted and sent over a socket connection.
  
- **File Transfer**: Files are selected via the GUI, encrypted, and sent over the same secure connection as the messages.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue for any bugs or feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
