# Websockets API

The Echo-API makes extremely extensive use of websockets to provide most services. This document serves as an index page
for all websocket endpoints and their respective documentation.

## Global Actions

All ws endpoints implement the following actions:

| Name               | Code   |
|--------------------|--------|
| [Ping](#ping-ping) | `ping` |

### Ping (`ping`)

Basic debug action used to test the link.

Always responds with `{"action": "pong"}`.

## Table of Contents

<!-- TOC -->
* [Websockets API](#websockets-api)
  * [Global Actions](#global-actions)
    * [Ping (`ping`)](#ping-ping)
  * [Table of Contents](#table-of-contents)
<!-- TOC -->