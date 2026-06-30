with open('app.py', 'r') as f:
    lines = f.readlines()

# Line 141 is index 140
lines[140] = '            category = request.form.get("category", "other")\n'

# Line 171 is index 170
lines[170] = '        category = request.form.get("category", "other")\n'

with open('app.py', 'w') as f:
    f.writelines(lines)

print("Fixed lines 141 and 171!")
