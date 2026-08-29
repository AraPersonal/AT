import sys

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    content = f.read()

# Fix ChatView bottom padding
old_chat = "Column(modifier = Modifier.fillMaxWidth().background(Color(0xFF252429)).padding(12.dp)) {"
new_chat = "Column(modifier = Modifier.fillMaxWidth().background(Color(0xFF252429)).padding(start = 12.dp, top = 12.dp, end = 12.dp, bottom = 92.dp)) {"
content = content.replace(old_chat, new_chat)

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "w") as f:
    f.write(content)
