import sys

with open("app/src/main/java/com/example/data/AgentTools.kt", "r") as f:
    content = f.read()

# Add missing import
pkg_idx = content.find("package com.example.data\n") + len("package com.example.data\n")
content = content[:pkg_idx] + "\nimport org.json.JSONObject\n" + content[pkg_idx:]

with open("app/src/main/java/com/example/data/AgentTools.kt", "w") as f:
    f.write(content)
