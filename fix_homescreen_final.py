import sys

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    content = f.read()

# Add missing imports
imports = """import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.animation.core.FastOutSlowInEasing
"""
if "import androidx.compose.ui.text.font.FontWeight" not in content:
    content = content.replace("import androidx.compose.ui.Alignment", "import androidx.compose.ui.Alignment\n" + imports)

# Re-insert ConsoleView, ShimmeringGeneratingIndicator, ChatView
missing_views = """@Composable
fun ConsoleView(viewModel: AgentViewModel) {
    val logs by viewModel.terminalLogs.collectAsState()
    Column(modifier = Modifier.fillMaxSize().padding(start = 16.dp, top = 16.dp, end = 16.dp, bottom = 96.dp)) {
        Text("Console", style = MaterialTheme.typography.titleLarge, color = Color.White)
        Spacer(modifier = Modifier.height(16.dp))
        Box(modifier = Modifier.fillMaxSize().background(Color.Black, RoundedCornerShape(8.dp)).padding(8.dp)) {
            androidx.compose.foundation.text.selection.SelectionContainer {
                Text(logs, color = Color.Green, style = MaterialTheme.typography.bodySmall.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace))
            }
        }
    }
}

@Composable
fun ShimmeringGeneratingIndicator() {
    val infiniteTransition = rememberInfiniteTransition(label = "typing")
    val dotCount = 3
    val dotSize = 8.dp
    
    Row(
        modifier = Modifier
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .background(Color(0xFF2D2C31), RoundedCornerShape(16.dp))
            .padding(horizontal = 16.dp, vertical = 12.dp),
        horizontalArrangement = Arrangement.spacedBy(4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        for (i in 0 until dotCount) {
            val alpha by infiniteTransition.animateFloat(
                initialValue = 0.2f,
                targetValue = 1f,
                animationSpec = infiniteRepeatable(
                    animation = tween(durationMillis = 400, delayMillis = i * 150, easing = LinearEasing),
                    repeatMode = RepeatMode.Reverse
                ),
                label = "dot_alpha_$i"
            )
            val yOffset by infiniteTransition.animateFloat(
                initialValue = 0f,
                targetValue = -4f,
                animationSpec = infiniteRepeatable(
                    animation = tween(durationMillis = 400, delayMillis = i * 150, easing = FastOutSlowInEasing),
                    repeatMode = RepeatMode.Reverse
                ),
                label = "dot_y_$i"
            )
            Box(
                modifier = Modifier
                    .offset(y = yOffset.dp)
                    .size(dotSize)
                    .background(Color.White.copy(alpha = alpha), CircleShape)
            )
        }
    }
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

    val transition = rememberInfiniteTransition(label = "bg")
    val alphaAnim by transition.animateFloat(
        initialValue = 0.0f, targetValue = if (isGenerating) 0.05f else 0.0f,
        animationSpec = infiniteRepeatable(animation = tween(2000, easing = LinearEasing), repeatMode = RepeatMode.Reverse), label = "bg_anim"
    )

    Column(modifier = Modifier.fillMaxSize().background(Brush.verticalGradient(colors = listOf(Color.White.copy(alpha = alphaAnim), Color.Transparent)))) {
        LazyColumn(
            modifier = Modifier.weight(1f).padding(horizontal = 16.dp),
            contentPadding = PaddingValues(vertical = 16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(messages) { msg -> MessageBubble(msg) }
        }

        if (isToolRunning) {
            Box(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp), contentAlignment = Alignment.CenterStart) {
                Surface(shape = RoundedCornerShape(8.dp), color = Color(0xFF2D2C31), border = BorderStroke(1.dp, Color(0xFF4A4950))) {
                    Row(modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                        CircularProgressIndicator(modifier = Modifier.size(12.dp), color = Color.White, strokeWidth = 2.dp)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("CALLING: ${currentToolName ?: "tool"}", style = MaterialTheme.typography.labelSmall.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace, fontSize = 10.sp), color = Color.LightGray)
                    }
                }
            }
        } else if (isGenerating) {
            ShimmeringGeneratingIndicator()
        }

        Column(modifier = Modifier.fillMaxWidth().background(Color(0xFF252429)).padding(start = 12.dp, top = 12.dp, end = 12.dp, bottom = 92.dp)) {
            Row(modifier = Modifier.fillMaxWidth().background(Color(0xFF1C1B1F), RoundedCornerShape(24.dp)).padding(end = 6.dp), verticalAlignment = Alignment.CenterVertically) {
                OutlinedTextField(
                    value = inputText, onValueChange = { inputText = it }, modifier = Modifier.weight(1f),
                    placeholder = { Text("Command or prompt...", color = Color.Gray) },
                    shape = RoundedCornerShape(24.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Color.Transparent, unfocusedBorderColor = Color.Transparent,
                        focusedTextColor = Color.White, unfocusedTextColor = Color.White, cursorColor = Color.White
                    )
                )
                FloatingActionButton(
                    onClick = {
                        if (inputText.isNotBlank()) {
                            viewModel.sendMessage(inputText)
                            inputText = ""
                        }
                    },
                    modifier = Modifier.size(40.dp),
                    containerColor = Color.White, contentColor = Color.Black, shape = RoundedCornerShape(20.dp)
                ) {
                    Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send")
                }
            }
        }
    }
}

"""

insert_pos = content.find("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun SettingsView(")
if insert_pos != -1:
    content = content[:insert_pos] + missing_views + content[insert_pos:]
    print("Re-inserted missing views")
else:
    print("Could not find insert point")

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "w") as f:
    f.write(content)
