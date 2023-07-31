from gendiff.format_diff.transform_value import transform_value


def format_plain(diff, ancestry=[]):
    nodes = filter(lambda node: node.get('type') != 'eq', diff)
    result = map(
        lambda node:
            node_formatters.get(node.get('type'))(node, ancestry, format_plain),
        nodes
    )

    final_symbol = '\n' if len(ancestry) == 0 else ''

    return '\n'.join(result) + final_symbol


node_formatters = {
    'add': lambda node, ancestry, _:
        "Property '{key}' was added with value: {value}".format(
            key=fmt_key(node.get('key'), ancestry),
            value=fmt_value(node.get('value'))),
    'del': lambda node, ancestry, _:
        "Property '{key}' was removed".format(
            key=fmt_key(node.get('key'), ancestry)),
    'upd': lambda node, ancestry, _:
        "Property '{key}' was updated. From {prev_value} to {value}".format(
            key=fmt_key(node.get('key'), ancestry),
            prev_value=fmt_value(node.get('prev_value')),
            value=fmt_value(node.get('value'))),
    'nested': lambda node, ancestry, fmt_nested:
        fmt_nested(node.get('children'), [*ancestry, node.get('key')]),
}


def fmt_key(key, ancestry):
    return '.'.join([*ancestry, key])


def fmt_value(value):
    if type(value) == dict:
        return '[complex value]'

    if type(value) == str:
        return f"'{value}'"

    return transform_value(value)
