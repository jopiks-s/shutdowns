import re

with open("unicode.txt", "w", encoding="utf-8") as file:
    ustr = "привет \u0df1"
    file.write(ustr)
    print(ustr)