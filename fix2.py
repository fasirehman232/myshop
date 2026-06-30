with open('app.py', 'r') as f:
    content = f.read()

# First occurrence (admin route)
content = content.replace(
    '            category = request.form.get("category", other)',
    '            category = request.form.get("category", "other")'
)

# Second occurrence (edit route)
content = content.replace(
    '        category = request.form.get("category", other)',
    '        category = request.form.get("category", "other")'
)

with open('app.py', 'w') as f:
    f.write(content)

print("Fixed both lines!")
