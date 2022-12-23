import codecs

# with open("resp_0_text.txt", "r", encoding="utf-8") as file:
#     for line in file:
#         line = line.strip('\n')
#         line = line.encode().decode()
#         print(line)

with open("resp_0_text.txt", "r", encoding="utf-8") as file_base, open("resp_short.txt", "w", encoding="utf-8") as file_copy:
    lines = file_base.readlines()
    start = lines.index('      <div class="modal__footer">\n')
    lines = lines[start:-1]
    file_copy.writelines(lines)
