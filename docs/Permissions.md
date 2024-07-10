# Permissions 

## Overview

Permissions are a way to control access to most parts of the application on a variety of levels. Permissions are 
assigned to roles or users (on a channel-by-channel basis), and roles are assigned to users. This allows for a flexible 
and granular way to control access to the application.

A permissions set is a collection of permissions represented as a bitmask. Each bit in the bitmask represents a
specific permission. The permissions are defined [here](#permission-definitions)

## Permission Definitions

There are three different permission types, each with their own set of bitmasks:

### Guild Permissions 


| Permission      | Bit Number | Bit Position                     | Description                                                                                 |
|-----------------|------------|----------------------------------|---------------------------------------------------------------------------------------------|
| Administrator   | 31         | 10000000000000000000000000000000 | Allows the user to bypass all permissions checks                                            |
| View Audit Logs | 30         | 01000000000000000000000000000000 | Allows the user to view the guild audit logs                                                |
| View Insights   | 29         | 00100000000000000000000000000000 | Allows the user to view the guild insights and statistics                                   |
| Manage Guild    | 28         | 00010000000000000000000000000000 | Allows the user to manage the guild settings such as name and icon                          |
| Delete Roles    | 27         | 00001000000000000000000000000000 | Allows the user to delete roles                                                             | 
| Create Roles    | 26         | 00000100000000000000000000000000 | Allows the user to create roles                                                             |
| Manage Roles    | 25         | 00000010000000000000000000000000 | Allows the user to manage role settings such as name and colour                             |
| Remove Roles    | 24         | 00000001000000000000000000000000 | Allows the user to remove roles from a user with lower permissions                          |
| Assign Roles    | 23         | 00000000100000000000000000000000 | Allows the user to assign roles with lower permissions to a user                            |
| Delete Channels | 22         | 00000000010000000000000000000000 | Allows the user to delete channels                                                          |
| Create Channels | 21         | 00000000001000000000000000000000 | Allows the user to create channels                                                          |
| Manage Channels | 20         | 00000000000100000000000000000000 | Allows the user to manage channel settings such as names                                    |
| Ban Members     | 19         | 00000000000010000000000000000000 | Allows the user to ban members                                                              |
| Kick Members    | 18         | 00000000000001000000000000000000 | Allows the user to kick members                                                             |
| Manage Members  | 17         | 00000000000000100000000000000000 | Allows the user to manage member settings such as nicknames or reset guild profile pictures |
| Manage Invites  | 16         | 00000000000000010000000000000000 | Allows the user to manage active guild invites                                              |
| Delete Emojis   | 15         | 00000000000000001000000000000000 | Allows the user to delete emojis                                                            |
| Create Emojis   | 14         | 00000000000000000100000000000000 | Allows the user to create emojis                                                            |
| Manage Emojis   | 13         | 00000000000000000010000000000000 | Allows the user to manage emoji names (not images)                                          |
| Delete Stickers | 12         | 00000000000000000001000000000000 | Allows the user to delete stickers                                                          |
| Create Stickers | 11         | 00000000000000000000100000000000 | Allows the user to create stickers                                                          |
| Manage Stickers | 10         | 00000000000000000000010000000000 | Allows the user to manage sticker names (not images)                                        |
| Delete Webhooks | 9          | 00000000000000000000001000000000 | Allows the user to delete webhooks                                                          |
| Create Webhooks | 8          | 00000000000000000000000100000000 | Allows the user to create webhooks                                                          |
| Manage Webhooks | 7          | 00000000000000000000000010000000 | Allows the user to manage webhook settings                                                  |
| Delete Events   | 6          | 00000000000000000000000001000000 | Allows the user to delete events                                                            |
| Create Events   | 5          | 00000000000000000000000000100000 | Allows the user to create events                                                            |
| Manage Events   | 4          | 00000000000000000000000000010000 | Allows the user to manage event settings                                                    |
| Send Invites    | 3          | 00000000000000000000000000001000 | Allows the user to send invites                                                             |
| Not Used        | 2          | 00000000000000000000000000000100 | Not used                                                                                    |
| Not Used        | 1          | 00000000000000000000000000000010 | Not used                                                                                    |
| Not Used        | 0          | 00000000000000000000000000000001 | Not used                                                                                    |

### Text Channel Permissions 

### Voice Channel Permissions