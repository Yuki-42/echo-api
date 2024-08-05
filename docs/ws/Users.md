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
    * [Me (`me`)](#me-me)
    * [New (`new`)](#new-new)
    * [Details (`details`)](#details-details)
<!-- TOC -->

## Actions

### Me (`me`)

Gets all information about the current authenticated user. Shorthand for [details](#details-details) using current
`user_id`.

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

### Details (`details`)

Gets the details of a user (public information).