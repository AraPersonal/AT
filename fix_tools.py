import sys

with open("app/src/main/java/com/example/data/AgentTools.kt", "r") as f:
    lines = f.readlines()

new_lines = []
in_bad_import = False
for line in lines:
    if line.strip() == "import org.json.JSONArray":
        continue
    if line.strip() == "import org.json.JSONObject":
        continue
    new_lines.append(line)

content = "".join(new_lines)

# Now add import org.json.JSONArray at the top after package
pkg_idx = content.find("package com.example.data\n") + len("package com.example.data\n")
content = content[:pkg_idx] + "\nimport org.json.JSONArray\n" + content[pkg_idx:]

with open("app/src/main/java/com/example/data/AgentTools.kt", "w") as f:
    f.write(content)
