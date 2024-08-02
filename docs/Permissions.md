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


| Permission      | Bit Number | Bit Position | Description                                                                                 |
|-----------------|------------|--------------|---------------------------------------------------------------------------------------------|
| Administrator   | 31         | 8000 0000    | Allows the user to bypass all permissions checks                                            |
| View Audit Logs | 30         | 4000 0000    | Allows the user to view the guild audit logs                                                |
| View Insights   | 29         | 2000 0000    | Allows the user to view the guild insights and statistics                                   |
| Manage Guild    | 28         | 1000 0000    | Allows the user to manage the guild settings such as name and icon                          |
| Delete Roles    | 27         | 0800 0000    | Allows the user to delete roles                                                             | 
| Create Roles    | 26         | 0400 0000    | Allows the user to create roles                                                             |
| Manage Roles    | 25         | 0200 0000    | Allows the user to manage role settings such as name and colour                             |
| Remove Roles    | 24         | 0100 0000    | Allows the user to remove roles from a user with lower permissions                          |
| Assign Roles    | 23         | 0080 0000    | Allows the user to assign roles with lower permissions to a user                            |
| Delete Channels | 22         | 0040 0000    | Allows the user to delete channels                                                          |
| Create Channels | 21         | 0020 0000    | Allows the user to create channels                                                          |
| Manage Channels | 20         | 0010 0000    | Allows the user to manage channel settings such as names                                    |
| Unban Members   | 19         | 0008 0000    | Allows the user to unban members                                                            |
| Ban Members     | 18         | 0004 0000    | Allows the user to ban members                                                              |
| Kick Members    | 17         | 0002 0000    | Allows the user to kick members                                                             |
| Manage Members  | 16         | 0001 0000    | Allows the user to manage member settings such as nicknames or reset guild profile pictures |
| Manage Invites  | 15         | 0000 8000    | Allows the user to manage active guild invites                                              |
| Delete Emojis   | 14         | 0000 4000    | Allows the user to delete emojis                                                            |
| Create Emojis   | 13         | 0000 2000    | Allows the user to create emojis                                                            |
| Manage Emojis   | 12         | 0000 1000    | Allows the user to manage emoji names (not images)                                          |
| Delete Stickers | 11         | 0000 0800    | Allows the user to delete stickers                                                          |
| Create Stickers | 10         | 0000 0400    | Allows the user to create stickers                                                          |
| Manage Stickers | 9          | 0000 0200    | Allows the user to manage sticker names (not images)                                        |
| Delete Webhooks | 8          | 0000 0100    | Allows the user to delete webhooks                                                          |
| Create Webhooks | 7          | 0000 0080    | Allows the user to create webhooks                                                          |
| Manage Webhooks | 6          | 0000 0040    | Allows the user to manage webhook settings                                                  |
| Delete Events   | 5          | 0000 0020    | Allows the user to delete events                                                            |
| Create Events   | 4          | 0000 0010    | Allows the user to create events                                                            |
| Manage Events   | 3          | 0000 0008    | Allows the user to manage event settings                                                    |
| Send Invites    | 2          | 0000 0004    | Allows the user to send invites                                                             |
| Not Used        | 1          | 0000 0002    | Not used                                                                                    |
| Not Used        | 0          | 0000 0001    | Not used                                                                                    |

### Text Channel Permissions 

| Permission                     | Bit Number | Bit Position | Description                                                      |
|--------------------------------|------------|--------------|------------------------------------------------------------------|
| Moderate Private Threads       | 31         | 8000 0000    | Allows the user to moderate private threads in the channel       |
| Moderate Public Threads        | 30         | 4000 0000    | Allows the user to moderate public threads in the channel        |
| Moderate Messages              | 29         | 2000 0000    | Allows the user to moderate messages in the channel              |
| Moderate Embeds                | 28         | 1000 0000    | Allows the user to moderate embeds in the channel                |
| Moderate Attachments           | 27         | 0800 0000    | Allows the user to moderate attachments in the channel           |
| Moderate Pins                  | 26         | 0400 0000    | Allows the user to moderate pins in the channel                  |
| Moderate Reactions             | 25         | 0200 0000    | Allows the user to moderate reactions in the channel             |
| Not Used                       | 24         | 0100 0000    | Not used                                                         |
| Not Used                       | 23         | 0080 0000    | Not used                                                         |
| Not Used                       | 22         | 0040 0000    | Not used                                                         |
| Not Used                       | 21         | 0020 0000    | Not used                                                         |
| Not Used                       | 20         | 0010 0000    | Not used                                                         |
| Not Used                       | 19         | 0008 0000    | Not used                                                         |
| Not Used                       | 18         | 0004 0000    | Not used                                                         |
| Embed Links                    | 17         | 0002 0000    | Allows the user to embed links in the channel                    |
| Attach Files                   | 16         | 0001 0000    | Allows the user to attach files in the channel                   |
| Add Reactions                  | 15         | 0000 8000    | Allows the user to add reactions in the channel                  |
| Delete Private Threads         | 14         | 0000 4000    | Allows the user to delete private threads they created           |
| Create Private Threads         | 13         | 0000 2000    | Allows the user to create private threads in the channel         |
| Send TTS Messages              | 12         | 0000 1000    | Allows the user to send TTS messages in the channel              |
| Delete Public Threads          | 11         | 0000 0800    | Allows the user to delete public threads they created            |
| Create Public Threads          | 10         | 0000 0400    | Allows the user to create public threads in the channel          |
| Use External Animated Stickers | 9          | 0000 0200    | Allows the user to use external animated stickers in the channel |
| Use External Stickers          | 8          | 0000 0100    | Allows the user to use external stickers in the channel          |
| Use Animated External Emojis   | 7          | 0000 0080    | Allows the user to use animated external emojis in the channel   |
| Use External Emojis            | 6          | 0000 0040    | Allows the user to use external emojis in the channel            |
| Use Animated Stickers          | 5          | 0000 0020    | Allows the user to use animated stickers in the channel          |
| Use Stickers                   | 4          | 0000 0010    | Allows the user to use stickers in the channel                   |
| Use Animated Emojis            | 3          | 0000 0008    | Allows the user to use animated emojis in the channel            |
| Use Emojis                     | 2          | 0000 0004    | Allows the user to use emojis in the channel                     |
| Delete Messages                | 1          | 0000 0002    | Allows the user to delete their own messages in the channel      |
| Send Messages                  | 0          | 0000 0001    | Allows the user to send messages in the channel                  |

### Voice Channel Permissions

| Permission            | Bit Number | Bit Position | Description                                             |
|-----------------------|------------|--------------|---------------------------------------------------------|
| Server Deafen Members | 31         | 8000 0000    | Allows the user to server deafen members in the channel |
| Server Mute Members   | 30         | 4000 0000    | Allows the user to server mute members in the channel   |
| Move Members          | 29         | 2000 0000    | Allows the user to move members in the channel          |
| Not Used              | 28-7       | 1FFF FF00    | Not used                                                |
| Stream Screens        | 6          | 0000 0040    | Allows the user to stream their screen in the channel   |
| View Screen Streams   | 5          | 0000 0020    | Allows the user to view screen streams in the channel   |
| Stream Camera         | 4          | 0000 0010    | Allows the user to stream their camera in the channel   |
| View Cameras          | 3          | 0000 0008    | Allows the user to view cameras in the channel          |
| Use Voice Activity    | 2          | 0000 0004    | Allows the user to use voice activity in the channel    |
| Speak                 | 1          | 0000 0002    | Allows the user to speak in the channel                 |
| Listen                | 0          | 0000 0001    | Allows the user to listen in the channel                | 