import sys
with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    c = f.read()
start = c.find("fun SettingsSection")
print(c[start:start+400])
