import sys
with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    c = f.read()
start = c.find("fun DynamicGlowingBackground")
end = c.find("fun GlowingBackground")
print(c[start:end])
