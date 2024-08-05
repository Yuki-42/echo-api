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

| Permission      | Bit Number | Bit Position (HEX) | Description                                                                                 | OAuth Scope           |
|-----------------|------------|--------------------|---------------------------------------------------------------------------------------------|-----------------------|
| Administrator   | 31         | 8000 0000          | Allows the user to bypass all permissions checks                                            | guild:admin           |
| View Audit Logs | 30         | 4000 0000          | Allows the user to view the guild audit logs                                                | guild:audit           |
| View Insights   | 29         | 2000 0000          | Allows the user to view the guild insights and statistics                                   | guild:insights        |
| Manage Guild    | 28         | 1000 0000          | Allows the user to manage the guild settings such as name and icon                          | guild:manage          |
| Delete Roles    | 27         | 0800 0000          | Allows the user to delete roles                                                             | guild:roles:delete    |
| Create Roles    | 26         | 0400 0000          | Allows the user to create roles                                                             | guild:roles:create    |
| Manage Roles    | 25         | 0200 0000          | Allows the user to manage role settings such as name and colour                             | guild:roles:manage    |
| Remove Roles    | 24         | 0100 0000          | Allows the user to remove roles from a user with lower permissions                          | guild:roles:remove    |
| Assign Roles    | 23         | 0080 0000          | Allows the user to assign roles with lower permissions to a user                            | guild:roles:assign    |
| Delete Channels | 22         | 0040 0000          | Allows the user to delete channels                                                          | guild:channels:delete |
| Create Channels | 21         | 0020 0000          | Allows the user to create channels                                                          | guild:channels:create |
| Manage Channels | 20         | 0010 0000          | Allows the user to manage channel settings such as names                                    | guild:channels:manage |
| Unban Members   | 19         | 0008 0000          | Allows the user to unban members                                                            | guild:members:unban   |
| Ban Members     | 18         | 0004 0000          | Allows the user to ban members                                                              | guild:members:ban     |
| Kick Members    | 17         | 0002 0000          | Allows the user to kick members                                                             | guild:members:kick    |
| Manage Members  | 16         | 0001 0000          | Allows the user to manage member settings such as nicknames or reset guild profile pictures | guild:members:manage  |
| Manage Invites  | 15         | 0000 8000          | Allows the user to manage active guild invites                                              | guild:invites:manage  |
| Delete Emojis   | 14         | 0000 4000          | Allows the user to delete emojis                                                            | guild:emojis:delete   |
| Create Emojis   | 13         | 0000 2000          | Allows the user to create emojis                                                            | guild:emojis:create   |
| Manage Emojis   | 12         | 0000 1000          | Allows the user to manage emoji names (not images)                                          | guild:emojis:manage   |
| Delete Stickers | 11         | 0000 0800          | Allows the user to delete stickers                                                          | guild:stickers:delete | 
| Create Stickers | 10         | 0000 0400          | Allows the user to create stickers                                                          | guild:stickers:create |
| Manage Stickers | 9          | 0000 0200          | Allows the user to manage sticker names (not images)                                        | guild:stickers:manage |
| Delete Webhooks | 8          | 0000 0100          | Allows the user to delete webhooks                                                          | guild:webhooks:delete |
| Create Webhooks | 7          | 0000 0080          | Allows the user to create webhooks                                                          | guild:webhooks:create |
| Manage Webhooks | 6          | 0000 0040          | Allows the user to manage webhook settings                                                  | guild:webhooks:manage |
| Delete Events   | 5          | 0000 0020          | Allows the user to delete events                                                            | guild:events:delete   |
| Create Events   | 4          | 0000 0010          | Allows the user to create events                                                            | guild:events:create   |
| Manage Events   | 3          | 0000 0008          | Allows the user to manage event settings                                                    | guild:events:manage   |
| Send Invites    | 2          | 0000 0004          | Allows the user to send invites                                                             | guild:invites:send    |
| Not Used        | 1          | 0000 0002          | Not used                                                                                    | Not used              |
| Not Used        | 0          | 0000 0001          | Not used                                                                                    | Not used              |

### Text Channel Permissions

| Permission                     | Bit Number | Bit Position | Description                                                      | OAuth Scope                     |
|--------------------------------|------------|--------------|------------------------------------------------------------------|---------------------------------|
| Moderate Private Threads       | 31         | 8000 0000    | Allows the user to moderate private threads in the channel       | text:private_threads:moderate   |
| Moderate Public Threads        | 30         | 4000 0000    | Allows the user to moderate public threads in the channel        | text:public_threads:moderate    |
| Moderate Messages              | 29         | 2000 0000    | Allows the user to moderate messages in the channel              | text:messages:moderate          |
| Moderate Embeds                | 28         | 1000 0000    | Allows the user to moderate embeds in the channel                | text:embeds:moderate            |
| Moderate Attachments           | 27         | 0800 0000    | Allows the user to moderate attachments in the channel           | text:attachments:moderate       |
| Moderate Pins                  | 26         | 0400 0000    | Allows the user to moderate pins in the channel                  | text:pins:moderate              |
| Moderate Reactions             | 25         | 0200 0000    | Allows the user to moderate reactions in the channel             | text:reactions:moderate         |
| Not Used                       | 24         | 0100 0000    | Not used                                                         | Not used                        |
| Not Used                       | 23         | 0080 0000    | Not used                                                         | Not used                        |
| Not Used                       | 22         | 0040 0000    | Not used                                                         | Not used                        |
| Not Used                       | 21         | 0020 0000    | Not used                                                         | Not used                        |
| Not Used                       | 20         | 0010 0000    | Not used                                                         | Not used                        |
| Not Used                       | 19         | 0008 0000    | Not used                                                         | Not used                        |
| Not Used                       | 18         | 0004 0000    | Not used                                                         | Not used                        |
| Embed Links                    | 17         | 0002 0000    | Allows the user to embed links in the channel                    | text:links:embed                |
| Attach Files                   | 16         | 0001 0000    | Allows the user to attach files in the channel                   | text:files:attach               |
| Add Reactions                  | 15         | 0000 8000    | Allows the user to add reactions in the channel                  | text:reactions:add              |
| Delete Private Threads         | 14         | 0000 4000    | Allows the user to delete private threads they created           | text:private_threads:delete     |
| Create Private Threads         | 13         | 0000 2000    | Allows the user to create private threads in the channel         | text:private_threads:create     |
| Send TTS Messages              | 12         | 0000 1000    | Allows the user to send TTS messages in the channel              | text:tts:send                   |
| Delete Public Threads          | 11         | 0000 0800    | Allows the user to delete public threads they created            | text:public_threads:delete      |
| Create Public Threads          | 10         | 0000 0400    | Allows the user to create public threads in the channel          | text:public_threads:create      |
| Use External Animated Stickers | 9          | 0000 0200    | Allows the user to use external animated stickers in the channel | text:stickers:external_animated |
| Use External Stickers          | 8          | 0000 0100    | Allows the user to use external stickers in the channel          | text:stickers:external          |
| Use Animated External Emojis   | 7          | 0000 0080    | Allows the user to use animated external emojis in the channel   | text:emojis:external_animated   |
| Use External Emojis            | 6          | 0000 0040    | Allows the user to use external emojis in the channel            | text:emojis:external            |
| Use Animated Stickers          | 5          | 0000 0020    | Allows the user to use animated stickers in the channel          | text:stickers:animated          |
| Use Stickers                   | 4          | 0000 0010    | Allows the user to use stickers in the channel                   | text:stickers:default           |
| Use Animated Emojis            | 3          | 0000 0008    | Allows the user to use animated emojis in the channel            | text:emojis:animated            |
| Use Emojis                     | 2          | 0000 0004    | Allows the user to use emojis in the channel                     | text:emojis:default             |
| Delete Messages                | 1          | 0000 0002    | Allows the user to delete their own messages in the channel      | text:messages:delete            |
| Send Messages                  | 0          | 0000 0001    | Allows the user to send messages in the channel                  | text:messages:send              |

### Voice Channel Permissions

| Permission            | Bit Number | Bit Position | Description                                             | OAuth Scope          |
|-----------------------|------------|--------------|---------------------------------------------------------|----------------------|
| Server Deafen Members | 31         | 8000 0000    | Allows the user to server deafen members in the channel | voice:global_deafen  |
| Server Mute Members   | 30         | 4000 0000    | Allows the user to server mute members in the channel   | voice:global_mute    |
| Move Members          | 29         | 2000 0000    | Allows the user to move members in the channel          | voice:move           |
| Not Used              | 28-7       | 1FFF FF00    | Not used                                                | Not used             |
| Stream Screens        | 7          | 0000 0040    | Allows the user to stream their screen in the channel   | voice:stream         |
| View Screen Streams   | 6          | 0000 0020    | Allows the user to view screen streams in the channel   | voice:view_streams   |
| Stream Camera         | 6          | 0000 0010    | Allows the user to stream their camera in the channel   | voice:camera         |
| View Cameras          | 3          | 0000 0008    | Allows the user to view cameras in the channel          | voice:view_cameras   |
| Use Voice Activity    | 2          | 0000 0004    | Allows the user to use voice activity in the channel    | voice:voice_activity |
| Speak                 | 1          | 0000 0002    | Allows the user to speak in the channel                 | voice:speak          |
| Listen                | 0          | 0000 0001    | Allows the user to listen in the channel                | voice:listen         |
