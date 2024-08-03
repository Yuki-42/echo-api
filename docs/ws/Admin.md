# Administrator Websockets API

The Admin API is entirely self-contained inside a single websockets connection and is used to securely provide 
administrative functions to the server owner. This API is not intended for use by any users but the server owner. 

## Handshake

The handshake for the Admin API is conducted as follows:
1. The server generates a random list of 32 bytes, encrypts it using the server's public key, and sends it to the client.
2. The client decrypts the message using the server's private key and calculates the MD5 hash of the message.
3. The client then encrypts the MD5 hash using the server's public key and sends it back to the server. (not encrypted)
4. The server then calculates the MD5 hash of the original message and compares it to the hash sent by the client. If
they match, the client is authenticated as a server administrator.

This concludes the authentication handshake for the Admin API. 

A 2nd handshake is conducted after the initial handshake to establish a shared secret between the client and the server.
This shared secret is used to encrypt and decrypt messages between the client and the server. This handshake is 
extremely simple:
1. The server generates a 2048-bit symmetric key and encrypts it using the client's public key.
2. The client decrypts the message using their private key and the shared secret is established.

## Actions

The Admin API provides various actions that can be used by the server owner to manage their server.

### `get_users`

This action is used to retrieve a list of all users on the server. This list includes all data in the users table.

### `delete_user`

This action is used to delete a user from the server. This action requires the user_id of the user to be deleted.