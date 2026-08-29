import sys

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "fun HomeScreen" in line or "Scaffold(" in line or "NavHost" in line:
        print(f"{i}: {line.strip()}")
