import sys

with open("app/src/main/java/com/example/data/GeminiService.kt", "r") as f:
    content = f.read()

target = """                val functionResponse = JSONObject()
                functionResponse.put("name", name)
                functionResponse.put("response", result)"""

replacement = """                val functionResponse = JSONObject()
                functionResponse.put("name", name)
                functionResponse.put("response", result)
                if (fc.has("id")) {
                    functionResponse.put("id", fc.getString("id"))
                }"""

if target in content:
    content = content.replace(target, replacement)
else:
    print("WARNING: target not found")

with open("app/src/main/java/com/example/data/GeminiService.kt", "w") as f:
    f.write(content)
