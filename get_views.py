import sys

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    content = f.read()

def print_block(func_name):
    start = content.find(f"fun {func_name}(")
    if start == -1:
        print(f"{func_name} not found")
        return
    # find the matching closing brace
    brace_count = 0
    in_block = False
    for i in range(start, len(content)):
        if content[i] == '{':
            brace_count += 1
            in_block = True
        elif content[i] == '}':
            brace_count -= 1
        if in_block and brace_count == 0:
            print(content[start:i+1])
            print("---")
            return

print_block("MessageBubble")
print_block("ChatView")
