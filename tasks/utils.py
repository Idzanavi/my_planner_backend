def fix_line(line):
    line = line.strip()
    if line:
        return ' ' + line
    else:
        return line

def fix_line_capitalize(line):
    line = line.strip()
    if line:
        return ' ' + line[0].upper() + line[1:]
    else:
        return line

def fix_for_separator(text, separator, capitalize):
    if capitalize:
        func = fix_line_capitalize
    else:
        func = fix_line
    return ((separator).join(map(func, text.split(separator)))).strip()


def fix_dup_wspaces(text):
    wspaces = (' ', '\t')
    if text:
        res = text[0]
        for c in text[1:]:
            if c not in wspaces or res[-1] not in wspaces:
                res += c
        return res
    else:
        return ''


def fix_text(text):
    separators = (('.', True), ('!', True), ('?', True), (',', False), )
    for separator, capitalize in separators:
        text = fix_for_separator(text, separator, capitalize)
    text = fix_dup_wspaces(text)
    return text

