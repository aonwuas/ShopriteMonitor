import datetime

replacements = {u'\u2018': "",
                r'\u2018': "",
                u'\u2019': "",
                r'\u2019': "",
                u'\u201A': "",
                u'\uFFFD': "",
                u'\u201c': "",
                u'\u201d': "",
                u'\xe9': "e",
                u'\xfa': "u",
                u'\xe4': "a",
                u'\xa2': "C",
                u'\xae': "",
                r'\u201A': "",
                r'\uFFFD': "",
                r'\u201c': "",
                r'\u201d': "",
                r'\xe9': "e",
                r'\xfa': "u",
                r'\xe4': "a",
                r'\xa2': "C",
                r'\xae': "",
                r';': "",
                r"[u'": '',
                r"']": '',
                }


def convert(s_input):
    if type(s_input) == type(u'unicode'):
        string = replace(s_input)
        return string
    else:
        string = str(s_input)
        string = replace(str(string))
        return ''.join(string)


def replace(string):
    for target, replacement in replacements.iteritems():
        string = string.replace(target, replacement)
    return string

def convert_date(string):
    return datetime.datetime.strptime(string, "%d/%m/%y").strftime("%Y-%m-%d")