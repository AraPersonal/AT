import re
with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    content = f.read()

# 1. Update HomeScreen
homescreen_start = content.find("@Composable\nfun HomeScreen(viewModel: AgentViewModel")
homescreen_end = content.find("NavHost(", homescreen_start)

old_homescreen = content[homescreen_start:homescreen_end]
new_homescreen = old_homescreen.replace(
    "fun HomeScreen(viewModel: AgentViewModel = viewModel(factory = AgentViewModel.Factory)) {",
    "fun HomeScreen(viewModel: AgentViewModel = viewModel(factory = AgentViewModel.Factory)) {\n    val isGenerating by viewModel.isGenerating.collectAsState()\n    val currentToolName by viewModel.currentToolName.collectAsState()\n\n    Box(modifier = Modifier.fillMaxSize().background(Color.Black)) {\n        DynamicGlowingBackground(isGenerating, currentToolName)\n"
)
new_homescreen = new_homescreen.replace("containerColor = Color(0xFF1C1B1F)", "containerColor = Color.Transparent")
new_homescreen = new_homescreen.replace("containerColor = Color(0xFF151419)", "containerColor = Color.Transparent")

content = content.replace(old_homescreen, new_homescreen)

# Close the Box at the end of HomeScreen
homescreen_close_pos = content.find("}\n\n@Composable\nfun DashboardView")
if homescreen_close_pos != -1:
    content = content[:homescreen_close_pos] + "    }\n}\n" + content[homescreen_close_pos+2:]

# 2. Add DynamicGlowingBackground
dynamic_bg = """
@Composable
fun DynamicGlowingBackground(isGenerating: Boolean, currentToolName: String?) {
    var stepCount by remember { mutableIntStateOf(0) }
    
    LaunchedEffect(currentToolName) {
        if (currentToolName != null) {
            stepCount++
        }
    }

    val idleColor = Color(0xFF0D47A1)
    
    val thinkingColors = listOf(
        Color(0xFF1B5E20), // Green
        Color(0xFFB71C1C), // Red
        Color(0xFF4A148C), // Purple
        Color(0xFFE65100), // Orange
        Color(0xFF006064)  // Teal
    )
    
    val targetColor = if (isGenerating) {
        if (currentToolName != null) {
            thinkingColors[stepCount % thinkingColors.size]
        } else {
            Color(0xFF1565C0)
        }
    } else {
        idleColor
    }
    
    val animatedColor by animateColorAsState(
        targetValue = targetColor,
        animationSpec = tween(durationMillis = 1500, easing = LinearEasing),
        label = "BgColor"
    )

    val infiniteTransition = rememberInfiniteTransition(label = "pulse")
    val radiusMultiplier by infiniteTransition.animateFloat(
        initialValue = 1.0f,
        targetValue = 1.4f,
        animationSpec = infiniteRepeatable(
            animation = tween(4000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "radius"
    )
    
    val xOffset by infiniteTransition.animateFloat(
        initialValue = 0.2f,
        targetValue = 0.8f,
        animationSpec = infiniteRepeatable(
            animation = tween(6000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "xOffset"
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            .drawBehind {
                drawRect(
                    brush = Brush.radialGradient(
                        colors = listOf(animatedColor.copy(alpha = 0.6f), Color.Transparent),
                        center = Offset(size.width * xOffset, size.height * 0.3f),
                        radius = size.width * radiusMultiplier
                    )
                )
            }
    )
}
"""

content = content.replace("@Composable\nfun GlowingBackground", dynamic_bg + "\n@Composable\nfun GlowingBackground")

# 3. Remove old GlowingBackground from ChatView
chatview_pattern = r"val animatedGlowColor by animateColorAsState.*?\)\n\n\s*Box\(modifier = Modifier\.fillMaxSize\(\)\.background\(Color\.Black\)\) \{\n\s*GlowingBackground\(glowColor = animatedGlowColor\)"

new_chatview_start = """Box(modifier = Modifier.fillMaxSize()) {"""
content = re.sub(r"val animatedGlowColor by animateColorAsState.*?\)\n\n\s*Box\(modifier = Modifier\.fillMaxSize\(\)\.background\(Color\.Black\)\) \{\n\s*GlowingBackground\(glowColor = animatedGlowColor\)", new_chatview_start, content, flags=re.DOTALL)


# 4. SettingsSection
old_settings_surface = """Surface(
            shape = RoundedCornerShape(16.dp),
            color = Color(0xFF1E1D22),
            modifier = Modifier.fillMaxWidth()
        )"""
new_settings_surface = """Box(
            modifier = Modifier.fillMaxWidth().glassMorphism(16.dp)
        )"""
content = content.replace(old_settings_surface, new_settings_surface)


# 5. ConsoleView
old_console_box = """Box(modifier = Modifier.fillMaxSize().background(Color.Black, RoundedCornerShape(8.dp)).padding(8.dp))"""
new_console_box = """Box(modifier = Modifier.fillMaxSize().glassMorphism(8.dp).padding(8.dp))"""
content = content.replace(old_console_box, new_console_box)

# 6. MessageBubble
old_tool_bubble = """Surface(
                shape = RoundedCornerShape(16.dp),
                color = Color(0xFF1E1D22),
                border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFF333333)),
                modifier = Modifier.widthIn(max = 320.dp)
            )"""
new_tool_bubble = """Box(
                modifier = Modifier.widthIn(max = 320.dp).glassMorphism(16.dp)
            )"""
content = content.replace(old_tool_bubble, new_tool_bubble)

old_user_bubble = """Box(
                modifier = Modifier
                    .background(if (isUser) Color(0xFF262626) else Color(0x40000000), RoundedCornerShape(24.dp))
                    .padding(horizontal = 20.dp, vertical = 12.dp)
            )"""
new_user_bubble = """Box(
                modifier = Modifier
                    .glassMorphism(24.dp)
                    .padding(horizontal = 20.dp, vertical = 12.dp)
            )"""
content = content.replace(old_user_bubble, new_user_bubble)

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "w") as f:
    f.write(content)
print("Updated theme elements")
