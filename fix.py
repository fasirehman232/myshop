with open('app.py', 'r') as f:
    content = f.read()

# Replace "category = request.form.get(\"category\", other)" with "category = request.form.get(\"category\", \"other\")"
fixed_content = content.replace(
    'category = request.form.get("category", other)',
    'category = request.form.get("category", "other")'
)

with open('app.py', 'w') as f:
    f.write(fixed_content)

print("Fixed!")
