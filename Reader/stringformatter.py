replacements = {'\u2018': "",
                '\u2019': "",
                '\u201A': "",
                '\uFFFD': "",
                '\u201c': "",
                '\u201d': "",
                '\xe9': "e",
                '\xfa': "u",
                '\xe4': "a",
                # '\xa2': "C",
                ';': ""}


def convert(s_input):
    string = str(s_input)
    string = replace(string)
    return string


def replace(string):
    for target, replacement in replacements.iteritems():
        string = string.replace(target, replacement)
    return string