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

The user_id is the id of the user that is logged in and the device_id is the id of the device that the user is logged in
on. The token is set to expire after 1 week.

The device_id is stored inside the token as a way to make it slightly harder to steal a token. If a token is stolen, it
can only be used on the device that it was stolen from. This is to prevent a token from being used on multiple devices.

## End To End Encryption

The application uses HTTPS on all endpoints to secure traffic in transit between the client and the server. This is 
considered the absolute minimum for security. In addition to this, the application makes use of end-to-end encryption 
when sending messages directly between users. Each user has a public and private key pair. The public key is stored in
the database completely unencrypted. The private key is stored in the database encrypted using the user's hashed and 
salted password. 
This may seem insecure, but the private key is only ever decrypted in memory on the server when the user logs in.

