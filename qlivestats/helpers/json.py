import re

def clean_json(string):
    """
    MK LiveStatus seems to have a buggy JSON output,
    so we are in need of some cleanup before proccessing it.
    """
    string = re.sub(",[ \t\r\n]+}", "}", string)
    string = re.sub(",[ \t\r\n]+\]", "]", string)
    return string
