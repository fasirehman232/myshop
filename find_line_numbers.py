with open('app.py', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    line_num = i + 1
    if 100 <= line_num <= 200:
        print(f"Line {line_num}: {repr(line)}")
