import sys

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    content = f.read()

start_idx = content.find("fun TelegramBottomBar(")
end_idx = content.find("\n}", start_idx) + 2

new_bottom_bar = """fun TelegramBottomBar(
    currentRoute: String,
    onNavigate: (String) -> Unit
) {
    val tabs = listOf(
        Routes.DASHBOARD to Icons.Default.Home,
        Routes.GALLERY to Icons.AutoMirrored.Filled.List,
        Routes.CHAT to Icons.AutoMirrored.Filled.Chat,
        Routes.CONSOLE to Icons.Default.Terminal,
        Routes.SETTINGS to Icons.Default.Settings
    )
    val selectedIndex = tabs.indexOfFirst { it.first == currentRoute }.takeIf { it >= 0 } ?: 0

    BoxWithConstraints(
        modifier = Modifier
            .fillMaxWidth()
            .height(80.dp)
    ) {
        // Blur the entire bar for the glassy background
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color(0x22FFFFFF)) 
                .blur(radius = 32.dp, edgeTreatment = androidx.compose.ui.draw.BlurredEdgeTreatment.Unbounded)
        )
        
        // Inner translucent background to ground the glass
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color(0x33000000))
        )

        val tabWidth = maxWidth / tabs.size
        val pillWidth = 64.dp
        val pillHeight = 40.dp
        
        // Smooth liquid gliding pill indicator
        val indicatorOffset by animateDpAsState(
            targetValue = tabWidth * selectedIndex + (tabWidth / 2) - (pillWidth / 2),
            animationSpec = spring(
                dampingRatio = 0.6f, // bouncy/liquid feel
                stiffness = Spring.StiffnessLow
            ),
            label = "indicatorOffset"
        )

        // The glassy liquid pill behind the icon
        Box(
            modifier = Modifier
                .offset(x = indicatorOffset)
                .align(Alignment.CenterStart)
                .size(width = pillWidth, height = pillHeight)
                .background(Color(0x40FFFFFF), CircleShape)
                .border(1.dp, Color(0x33FFFFFF), CircleShape)
        )

        Row(
            modifier = Modifier.fillMaxSize(),
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.CenterVertically
        ) {
            tabs.forEachIndexed { index, (route, icon) ->
                val selected = index == selectedIndex

                // Scale animation
                val scale by animateFloatAsState(
                    targetValue = if (selected) 1.2f else 1.0f,
                    animationSpec = spring(
                        dampingRatio = Spring.DampingRatioMediumBouncy,
                        stiffness = Spring.StiffnessLow
                    ),
                    label = "scale"
                )

                val color by animateColorAsState(
                    targetValue = if (selected) Color.White else Color(0xFFAAAAAA),
                    label = "color"
                )

                Box(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxHeight()
                        .clickable(
                            interactionSource = remember { MutableInteractionSource() },
                            indication = null, // No ripple for native iOS feel
                            onClick = { onNavigate(route) }
                        ),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = icon,
                        contentDescription = route,
                        tint = color,
                        modifier = Modifier.scale(scale)
                    )
                }
            }
        }
    }
}"""

content = content[:start_idx] + new_bottom_bar + content[end_idx:]

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "w") as f:
    f.write(content)
