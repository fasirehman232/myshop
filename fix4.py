with open('app.py', 'r') as f:
    content = f.read()

# Replace line 141's exact string (unquoted other → quoted "other")
content = content.replace(
    '''            category = request.form.get("category", other)''',
    '''            category = request.form.get("category", "other")'''
)

# Replace line 171's exact string (unquoted other → quoted "other")
content = content.replace(
    '''        category = request.form.get("category", other)''',
    '''        category = request.form.get("category", "other")'''
)

with open('app.py', 'w') as f:
    f.write(content)

print("Fixed both lines correctly!")
