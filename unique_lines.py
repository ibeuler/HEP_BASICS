with open("python_scr,ipt_open_data_scource.py", "r") as file:
        file_contents = file.readlines()
        file_contents = ["".join(i for i in j if (i != " " or i != "\n"))  for j in file_contents ]

# Identify unique code snippets by filtering out the duplicate lines
unique_lines = []
seen_lines = set()

for j in file_contents[20:]:
    print(j)
for i, line in enumerate(file_contents):
    if line not in seen_lines:
        unique_lines.append((i + 1, line))
        seen_lines.add(line)
print(unique_lines[-1][0])
