
file_name = "python_script_open_data_scource.py"

with open(file_name) as file:
    file_lines = file.readlines()

lines_to_append = []

for i in file_lines:
    if "\n" == i:
        continue
    lines_to_append.append(i)

with open(file_name, "w") as f:
    f.writelines(lines_to_append)