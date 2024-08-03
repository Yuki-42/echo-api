# Security

The application handles authentication using JWT. Tokens are generated when a user logs in and are stored how the client 
sees fit. The token is then sent with each request to the server to authenticate the user. The token is signed with a
secret key that is stored in the server's environment variables. The token is set to expire after 1 week. 

The application also uses bcrypt to hash passwords before storing them in the database. This is to ensure that even if the
database is compromised, the passwords are not easily accessible.

## Tokens

The token is generated using the `PyJWT` library. The data encoded in the token is as follows:
```json
{
    "sub": user_id,
    "device": device_id,
    "exp": datetime.utcnow() + timedelta(days=7)
}
```

Upon initial user registration, they are granted a temporary token that is used to authenticate the user for adding a 
device to their account. This token is generated using the same method as the login token, but with a shorter expiry time
of 5 minutes. This token is used to authenticate the user when adding a device to their account.

If the user does not add a device to their account within the 5 minutes, they will need to log in again to get a new
token.

The user_id is the id of the user that is logged in and the device_id is the id of the device that the user is logged in
on. The token is set to expire after 1 week.

The device_id is stored inside the token as a way to make it slightly harder to steal a token. If a token is stolen, it
can only be used on the device that it was stolen from. This is to prevent a token from being used on multiple devices.

## End To End Encryption

The application uses HTTPS on all endpoints to secure traffic in transit between the client and the server. This is 
considered the absolute minimum for security. In addition to this, the application makes use of end-to-end encryption 
when sending messages directly between users. When a new DM is created between two users, each client generates a 
public key and private key. These clients then complete a diffie-hellman key exchange to generate a shared secret.

This shared secret is calculated on each client individually and is never sent unencrypted to the server. Each user then 
encrypts the shared secret using their password and sends it to the server. The server then stores the encrypted shared
secret in the database in the user_channels table. 

When a user logs in, they are sent all shared secrets for their DMs and decrypt them using their password. This shared
secret is then used to encrypt and decrypt messages between the two users. This ensures that even if the server is
compromised, the messages are still secure.

## Server Administrators

Server administrators have the ability to view all messages in guild channels, delete users, and delete messages. This
is to ensure that the server is kept clean and that users are not abusing the system.

The server administrator is authenticated using a signature that is stored in the server's environment variables, 
similar to how SSH works. A server administrator handshake is conducted when the someone tries to connect to the 
administrator websocket endpoint.

The handshake works as follows:
1. The server generates a random list of 32 bytes, encrypts it using the server's public key, and sends it to the client.
2. The client decrypts the message using the server's private key and calculates the MD5 hash of the message.
3. The client then encrypts the MD5 hash using the server's public key and sends it back to the server. (not encrypted)
4. The server then calculates the MD5 hash of the original message and compares it to the hash sent by the client. If
they match, the client is authenticated as a server administrator.