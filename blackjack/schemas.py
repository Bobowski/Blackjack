
schemas = {
    "register": {
        "type": "object",
        "properties": {
            "cash": {
                "type": "number"
            }
        },
        "required": ["cash"]
    },
    "begin_game": {
        "type": "object",
        "properties": {
            "table_id": {
                "type": "number",
            },
            "bid": {
                "type": "number"
            }
        },
        "required": ["table_id", "bid"]
    },
    "action_in_game": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["split", "insure", "double", "hit", "pass", "quit"]
            }
        },
        "required": ["action"]
    }
}
