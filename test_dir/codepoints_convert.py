import re
from codecs import decode


def unicode_escape(s) -> str:
    # https://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python#24519338
    escape_pattern = re.compile(r'''
            ( \\U........      # 8-digit hex escapes
            | \\u....          # 4-digit hex escapes
            | \\x..            # 2-digit hex escapes
            | \\[0-7]{1,3}     # Octal escapes
            | \\N\{[^}]+\}     # Unicode characters by name
            | \\[\\'"abfnrtv]  # Single-character escapes
            )''', re.UNICODE | re.VERBOSE)
    return escape_pattern.sub(lambda m: decode(m.group(), 'unicode-escape'), s)


with open("resp.txt", "r", encoding="utf-8") as raw_file, open("resp_decoded.txt", "w", encoding="utf-8") as u_file:
    for line in raw_file.readlines():
        u_file.write(unicode_escape(line))
