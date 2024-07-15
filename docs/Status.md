# Status

Disbroad represents statuses as a JSON object internally. This object has two fields: `type` and `text`. 

The `type` field can be one of the values in this enum:
```python
class StatusType(int, Enum):
    online = 0
    offline = 1
    away = 2
    dnd = 3
    playing = 4
    watching = 5
    listening = 6
```

When constructing the status object, the `type` field must be one of the values in the enum. The `text` field is a string that can be set to any value.