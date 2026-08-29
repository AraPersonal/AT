import sys

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    content = f.read()

# Fix ConsoleView bottom padding
old_console = "Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {"
new_console = "Column(modifier = Modifier.fillMaxSize().padding(start = 16.dp, top = 16.dp, end = 16.dp, bottom = 96.dp)) {"
content = content.replace(old_console, new_console)

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "w") as f:
    f.write(content)
