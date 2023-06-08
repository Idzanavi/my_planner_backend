def remove_prefix(line, prefix):
    prefix_len = len(prefix)
    if len(line) >= prefix_len and line[:prefix_len] == prefix:
        return line[prefix_len:]
    else:
        return line

def prefix_remover(prefix):
    def func(line):
        return remove_prefix(line, prefix)
    return func

