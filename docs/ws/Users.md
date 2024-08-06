# Users Websocket API

The users API is entirely self-contained inside a single websocket connection and is used to interact with the users
system of the app. This route is open to all users and is used to create users, view user details, and edit profiles.

Note that these functions are different from the [Admin](./Admin.md) api in that they can only be used by users with
appropriate permissions.

## Table of Contents

<!-- TOC -->
* [Users Websocket API](#users-websocket-api)
  * [Table of Contents](#table-of-contents)
  * [Actions](#actions)
    * [New (`new`)](#new-new)
    * [Login (`login`)](#login-login)
    * [Me (`me`)](#me-me)
    * [Details (`details`)](#details-details)
<!-- TOC -->

## Actions

### New (`new`)

Creates a new user.

Action Pathway:

1. Client sends a `new` action with the following payload:
    ```json
    {
        "action": "new",
        "data": {
            "username": "username",
            "email": "email",
            "password": "password"
        }
   }
   ```

2. Server responds with the following payload:
    ```json
    {
        "action": "new",
        "data": {
            "user_id": "user_id",
            "username": "username",
            "email": "email"
        }
    }
    ```
    Where `user_id` is the ID of the new user, `username` is the username of the new user, and `email` is the email of 
    the new user.

### Login (`login`)

Logs in a user.

Action Pathway:
1. Client sends a `login` action with the following payload:
    ```json
    {
        "action": "login",
        "data": {
            "username": "username",
            "password": "password"
        }
    }
    ```
   
2. Server responds with the following payload if login is successful:
    ```json
    {
        "action": "login",
        "data": {
            "token": "jwt_token"
        }
    }
    ```
    Where `user_id` is the ID of the user, `username` is the username of the user, and `email` is the email of the user.

    Server responds with the following payload if login is unsuccessful:
    ```json
    {
        "action": "login",
        "error": "error_message"
    }
    ```
   
### Logout (`logout`)

Remove a specified token from the database. This is used to log out a user on any device.

Action Pathway:

1. Client sends a `logout` action with the following payload:
    ```json
    {
        "action": "logout",
        "data": {
            "token": "jwt_token"
        }
    }
    ```
   
2. Server responds with the following payload if the token is found and belongs to the user:
    ```json
    {
        "action": "logout",
        "data": {
            "success": true
        }
    }
    ```
   
    Server responds with the following payload if the token is not found or does not belong to the user:
    ```json
    {
        "action": "logout",
        "error": "error_message"
    }
    ```

### Me (`me`)

Gets all information about the current authenticated user. Shorthand for [details](#details-details) using current
`user_id`.

### Details (`details`)

Gets the details of a user (public information).