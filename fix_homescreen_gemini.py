import re

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    content = f.read()

# Add imports
imports_to_add = """
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.draw.clip
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.animation.animateColorAsState
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.rounded.Edit
import androidx.compose.material.icons.rounded.MoreHoriz
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.Mic
"""
if "import androidx.compose.ui.draw.drawBehind" not in content:
    content = content.replace("import androidx.compose.ui.Alignment", "import androidx.compose.ui.Alignment\n" + imports_to_add)

# Replace MessageBubble
old_message_bubble_pattern = r"@Composable\nfun MessageBubble\(message: com\.example\.data\.ChatMessageEntity\) \{.*?\}\n"
new_message_bubble = """@Composable
fun MessageBubble(message: com.example.data.ChatMessageEntity) {
    val isUser = message.role == "user"
    val isTool = message.role == "tool"
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
    ) {
        if (isTool) {
            Surface(
                shape = RoundedCornerShape(16.dp),
                color = Color(0xFF1E1D22),
                border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFF333333)),
                modifier = Modifier.widthIn(max = 320.dp)
            ) {
                androidx.compose.foundation.text.selection.SelectionContainer {
                    Text(
                        text = message.content,
                        modifier = Modifier.padding(12.dp),
                        color = Color.Gray,
                        style = MaterialTheme.typography.bodySmall.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace)
                    )
                }
            }
        } else {
            Box(
                modifier = Modifier
                    .background(if (isUser) Color(0xFF262626) else Color(0x40000000), RoundedCornerShape(24.dp))
                    .padding(horizontal = 20.dp, vertical = 12.dp)
            ) {
                androidx.compose.foundation.text.selection.SelectionContainer {
                    Text(
                        text = message.content,
                        color = Color.White,
                        fontSize = 16.sp
                    )
                }
            }
        }
    }
}
"""

content = re.sub(r"@Composable\nfun MessageBubble\(message: com\.example\.data\.ChatMessageEntity\) \{.*?\n\}\n", new_message_bubble, content, flags=re.DOTALL)

# Replace ChatView
old_chat_view_pattern = r"@Composable\nfun ChatView\(viewModel: AgentViewModel\) \{.*?\n\}\n"

new_chat_view = """fun androidx.compose.ui.Modifier.glassMorphism(
    cornerRadius: androidx.compose.ui.unit.Dp = 32.dp,
    borderWidth: androidx.compose.ui.unit.Dp = 1.dp
): androidx.compose.ui.Modifier = this
    .clip(RoundedCornerShape(cornerRadius))
    .background(Color(0x40000000))
    .border(
        width = borderWidth,
        brush = Brush.linearGradient(
            colors = listOf(Color(0x4DFFFFFF), Color(0x00FFFFFF), Color(0x1AFFFFFF)),
            start = Offset(0f, 0f),
            end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
        ),
        shape = RoundedCornerShape(cornerRadius)
    )

@Composable
fun GlowingBackground(glowColor: Color) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .drawBehind {
                drawRect(
                    brush = Brush.radialGradient(
                        colors = listOf(glowColor.copy(alpha = 0.5f), Color.Transparent),
                        center = Offset(size.width / 2, size.height * 0.2f),
                        radius = size.width * 1.2f
                    )
                )
            }
    )
}

@Composable
fun ChatView(viewModel: AgentViewModel) {
    val messages by viewModel.messages.collectAsState()
    val isToolRunning by viewModel.isToolRunning.collectAsState()
    val currentToolName by viewModel.currentToolName.collectAsState()
    val isGenerating by viewModel.isGenerating.collectAsState()
    var inputText by remember { mutableStateOf("") }
    val haptic = LocalHapticFeedback.current

    LaunchedEffect(isToolRunning) { if (isToolRunning) haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove) }
    LaunchedEffect(isGenerating) { if (!isGenerating) haptic.performHapticFeedback(HapticFeedbackType.LongPress) }

    val animatedGlowColor by animateColorAsState(
        targetValue = if (isGenerating) Color(0xFF1B5E20) else Color(0xFF0D47A1),
        animationSpec = tween(durationMillis = 1000),
        label = "GlowColorAnimation"
    )

    Box(modifier = Modifier.fillMaxSize().background(Color.Black)) {
        GlowingBackground(glowColor = animatedGlowColor)
        
        Column(modifier = Modifier.fillMaxSize()) {
            // Top Bar Replica
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = { }, modifier = Modifier.size(48.dp).background(Color(0xFF1A1A1A), CircleShape)) {
                    Icon(imageVector = Icons.Default.Menu, contentDescription = "Menu", tint = Color.White)
                }
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(horizontal = 12.dp)) {
                    Text(text = "Pro Extended", color = Color.LightGray, fontSize = 16.sp, fontWeight = FontWeight.Medium)
                    Spacer(modifier = Modifier.width(4.dp))
                    Icon(imageVector = Icons.Default.KeyboardArrowDown, contentDescription = "Expand", tint = Color.LightGray, modifier = Modifier.size(20.dp))
                }
                Row(
                    modifier = Modifier.height(48.dp).glassMorphism(cornerRadius = 24.dp).padding(horizontal = 4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(onClick = { }) {
                        Icon(imageVector = Icons.Rounded.Edit, contentDescription = "New Chat", tint = Color.White, modifier = Modifier.size(20.dp))
                    }
                    IconButton(onClick = { viewModel.clearHistory() }) {
                        Icon(imageVector = Icons.Rounded.MoreHoriz, contentDescription = "More options", tint = Color.White, modifier = Modifier.size(20.dp))
                    }
                }
            }

            LazyColumn(
                modifier = Modifier.weight(1f).padding(horizontal = 16.dp),
                contentPadding = PaddingValues(vertical = 16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(messages) { msg -> MessageBubble(msg) }
                
                if (isToolRunning) {
                    item {
                        Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.CenterStart) {
                            Surface(shape = RoundedCornerShape(8.dp), color = Color(0xFF2D2C31), border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFF4A4950))) {
                                Row(modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                                    CircularProgressIndicator(modifier = Modifier.size(12.dp), color = Color.White, strokeWidth = 2.dp)
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text("CALLING: ${currentToolName ?: "tool"}", style = MaterialTheme.typography.labelSmall.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace, fontSize = 10.sp), color = Color.LightGray)
                                }
                            }
                        }
                    }
                } else if (isGenerating) {
                    item { ShimmeringGeneratingIndicator() }
                }
            }

            // Bottom Input Bar Replica
            Box(modifier = Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, bottom = 92.dp)) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(72.dp)
                        .glassMorphism(cornerRadius = 36.dp)
                        .padding(horizontal = 8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(onClick = { }) {
                        Icon(imageVector = Icons.Rounded.Add, contentDescription = "Add", tint = Color.LightGray, modifier = Modifier.size(28.dp))
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    BasicTextField(
                        value = inputText,
                        onValueChange = { inputText = it },
                        modifier = Modifier.weight(1f),
                        textStyle = MaterialTheme.typography.bodyLarge.copy(color = Color.White),
                        cursorBrush = SolidColor(Color.White),
                        decorationBox = { innerTextField ->
                            if (inputText.isEmpty()) {
                                Text("Ask Gemini", color = Color.LightGray, fontSize = 18.sp)
                            }
                            innerTextField()
                        }
                    )
                    
                    if (inputText.isNotBlank()) {
                        IconButton(onClick = { viewModel.sendMessage(inputText); inputText = "" }) {
                            Icon(imageVector = Icons.Default.Send, contentDescription = "Send", tint = Color.White, modifier = Modifier.size(24.dp))
                        }
                    } else {
                        IconButton(onClick = { }) {
                            Icon(imageVector = Icons.Rounded.Mic, contentDescription = "Voice input", tint = Color.LightGray, modifier = Modifier.size(24.dp))
                        }
                    }
                }
            }
        }
    }
}
"""

content = re.sub(r"@Composable\nfun ChatView\(viewModel: AgentViewModel\) \{.*?\n\}\n", new_chat_view, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "w") as f:
    f.write(content)

print("Updated HomeScreen.kt")
