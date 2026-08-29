import sys
with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    c = f.read()
start = c.find("fun DashboardView")
end = c.find("fun GalleryView")
print(c[start:end])
