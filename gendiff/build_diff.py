handlers = [
    {
        'check': lambda key, dict1, _: key not in dict1,
        'handle': lambda key, _, dict2, func: {
            'type': 'added', 'key': key, 'value': dict2.get(key)
        }
    },
    {
        'check': lambda key, _, dict2: key not in dict2,
        'handle': lambda key, dict1, *_: {
            'type': 'deleted', 'key': key, 'value': dict1.get(key)
        }
    },
    {
        'check': lambda key, dict1, dict2:
            type(dict1.get(key)) == dict and type(dict2.get(key)) == dict,
        'handle': lambda key, dict1, dict2, func: {
            'type': 'nested',
            'key': key,
            'children': func(dict1.get(key), dict2.get(key))}
    },
    {
        'check': lambda key, dict1, dict2: dict1.get(key) == dict2.get(key),
        'handle': lambda key, dict1, *_: {
            'type': 'unchanged', 'key': key, 'value': dict1.get(key)
        }
    },
    {
        'check': lambda key, dict1, dict2: dict1.get(key) != dict2.get(key),
        'handle': lambda key, dict1, dict2, _: {
            'type': 'updated',
            'key': key,
            'value': dict2.get(key),
            'prev_value': dict1.get(key)
        }
    },
]


def build_diff(data1, data2):
    keys = sorted(set(data1.keys()) | set(data2.keys()))

    results = [
        next(handler['handle'](key, data1, data2, build_diff)
             for handler in handlers
             if handler['check'](key, data1, data2))
        for key in keys
    ]

    return results
