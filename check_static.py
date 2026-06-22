
import os

print("Checking static folder:")
static_path = os.path.join(os.path.dirname(__file__), 'static')
images_path = os.path.join(static_path, 'images')

print(f"Static path exists: {os.path.exists(static_path)}")
print(f"Images path exists: {os.path.exists(images_path)}")
print("Files in static/images:")
if os.path.exists(images_path):
    for file in os.listdir(images_path):
        print(f"  - {file}")
else:
    print("  No files found!")
