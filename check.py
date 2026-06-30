with open('app.py', 'r') as f:
    lines = f.readlines()

print("Line 131:", repr(lines[130]))  # indexes start at 0!
print("Line 160:", repr(lines[159]))
