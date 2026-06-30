with open('app.py', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'category = request.form.get' in line:
        print(f"Line {i+1}: {repr(line)}")
