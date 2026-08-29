import sys

with open("app/src/main/java/com/example/data/AgentTools.kt", "r") as f:
    content = f.read()

old_block = """            fd.put("parameters", params)
            
            val toolObj = JSONObject()
            toolObj.put("functionDeclaration", fd)
            arr.put(toolObj)
        }
        return arr"""

new_block = """            fd.put("parameters", params)
            
            arr.put(fd)
        }
        return arr"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/data/AgentTools.kt", "w") as f:
        f.write(content)
    print("Patched AgentTools.kt")
else:
    print("Could not find block")
