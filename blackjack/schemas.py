
schemas = {
    "register": {
        "type": "object",
        "properties": {
            "cash": {
                "type": "number"
            },
            "seed": {
                "type": "number"
            }
        },
        "required": ["cash"]
    },
    "begin_game": {
        "type": "object",
        "properties": {
            "bid": {
                "type": "number"
            }
        },
        "required": ["bid"]
    },
    "action_in_game": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["split", "double_down", "hit", "stand"]
            }
        },
        "required": ["action"]
    }
}
