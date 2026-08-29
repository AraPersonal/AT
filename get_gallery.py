import sys
with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    c = f.read()
start = c.find("fun GalleryView")
end = c.find("fun ConsoleView")
print(c[start:end])
