# Status

Echo represents statuses as a JSON object internally. This object has two fields: `type` and `text`.

The `type` field can be one of the values in this enum:

```python
class StatusType(int, Enum):
    offline = 0
    online = 1
    away = 2
    dnd = 3
    playing = 4
    watching = 5
    listening = 6
```

When constructing the status object, the `type` field must be one of the values in the enum. The `text` field is a
string that can be set to any value.

Example for default status

```json
{
  "type": 0,
  "text": ""
}
```

Example for default online status

```json
{
  "type": 1,
  "text": ""
}
```

Example for playing Skyrim. The `text` field is set to " Skyrim" (note the leading space) as the client will display the
status as "Playing Skyrim".

```json
{
  "type": 4,
  "text": " Skyrim"
}
```
