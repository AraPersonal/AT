import sys
import re

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    content = f.read()

# 1. Remove duplicate ConsoleView
# The script inserted ConsoleView, so let's find the FIRST ConsoleView and delete it, or the second one.
console_view_pattern = r"@Composable\nfun ConsoleView\(viewModel: AgentViewModel\) \{.*?\}\n"
# Find all matches (dotall)
matches = list(re.finditer(r"@Composable\nfun ConsoleView\(viewModel: AgentViewModel\) \{.*?\n\}\n", content, re.DOTALL))
if len(matches) > 1:
    # Remove the second one
    match = matches[1]
    content = content[:match.start()] + content[match.end():]

# 2. Re-insert MessageBubble
message_bubble = """
@Composable
fun MessageBubble(message: com.example.data.ChatMessageEntity) {
    val isUser = message.role == "user"
    val isTool = message.role == "tool"
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
    ) {
        Surface(
            shape = RoundedCornerShape(16.dp),
            color = if (isUser) Color(0xFF3B3A40) else if (isTool) Color(0xFF1E1D22) else Color(0xFF2D2C31),
            border = if (isTool) androidx.compose.foundation.BorderStroke(1.dp, Color(0xFF333333)) else null,
            modifier = Modifier.widthIn(max = 320.dp)
        ) {
            androidx.compose.foundation.text.selection.SelectionContainer {
                Text(
                    text = message.content,
                    modifier = Modifier.padding(12.dp),
                    color = if (isTool) Color.Gray else Color.White,
                    style = if (isTool) MaterialTheme.typography.bodySmall.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace) else MaterialTheme.typography.bodyMedium
                )
            }
        }
    }
}
"""
if "fun MessageBubble" not in content:
    chat_view_pos = content.find("@Composable\nfun ChatView")
    content = content[:chat_view_pos] + message_bubble + content[chat_view_pos:]

# 3. Fix Send icon
content = content.replace("Icons.AutoMirrored.Filled.Send", "Icons.Default.Send")

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "w") as f:
    f.write(content)
print("Cleaned up HomeScreen.kt")
