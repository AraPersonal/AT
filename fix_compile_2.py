import sys

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    content = f.read()

# Fix duplicates (only keep one import)
def remove_duplicate_imports(text, import_statement):
    # Find all occurrences of the import statement
    parts = text.split(import_statement + "\n")
    if len(parts) > 2:
        # Rejoin with only one import
        return parts[0] + import_statement + "\n" + "".join(parts[1:])
    return text

content = remove_duplicate_imports(content, "import androidx.compose.ui.geometry.Offset")
content = remove_duplicate_imports(content, "import androidx.compose.ui.graphics.Brush")

# Fix clearHistory() error
content = content.replace("viewModel.clearHistory()", "")

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "w") as f:
    f.write(content)
print("Fixed compile issues")
