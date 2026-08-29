import sys

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    content = f.read()

# Replace ShimmeringGeneratingIndicator
old_indicator = """@Composable
fun ShimmeringGeneratingIndicator() {
    val transition = rememberInfiniteTransition(label = "shimmer")
    val translateAnim by transition.animateFloat(
        initialValue = 0f, targetValue = 1000f,
        animationSpec = infiniteRepeatable(animation = tween(durationMillis = 1500, easing = LinearEasing), repeatMode = RepeatMode.Restart), label = "shimmer_anim"
    )
    val brush = Brush.linearGradient(
        colors = listOf(Color(0xFF333333), Color(0xFF666666), Color(0xFF333333)),
        start = Offset(translateAnim - 200f, translateAnim - 200f),
        end = Offset(translateAnim, translateAnim)
    )
    Box(modifier = Modifier.fillMaxWidth().padding(16.dp), contentAlignment = Alignment.CenterStart) {
        Box(modifier = Modifier.size(width = 120.dp, height = 24.dp).clip(RoundedCornerShape(12.dp)).background(brush))
    }
}"""

new_indicator = """@Composable
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
}"""

if old_indicator in content:
    content = content.replace(old_indicator, new_indicator)
    print("Patched indicator")
else:
    print("Could not find old indicator")

# SettingsView patching
start_settings = content.find("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun SettingsView(")
end_settings = content.find("@Composable\nfun TelegramBottomBar", start_settings)

if start_settings != -1 and end_settings != -1:
    new_settings = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsView(viewModel: AgentViewModel) {
    val context = LocalContext.current as android.app.Activity
    val currentModel by viewModel.currentModelName.collectAsState()
    val currentTemp by viewModel.temperature.collectAsState()
    val currentPat by viewModel.githubPat.collectAsState()
    val currentWorkspace by viewModel.workspaceDir.collectAsState()
    val apiKey by viewModel.apiKey.collectAsState()
    
    var keyInput by remember { mutableStateOf(apiKey ?: "") }
    var tempInput by remember { mutableStateOf(currentTemp) }
    var patInput by remember { mutableStateOf(currentPat) }
    var workspaceInput by remember { mutableStateOf(currentWorkspace) }
    var modelInput by remember { mutableStateOf(currentModel) }
    var expanded by remember { mutableStateOf(false) }
    val availableModels = listOf("gemini-3.6-flash", "models/gemini-3.1-pro-preview", "gemini-1.5-pro", "gemini-1.5-flash")

    val scrollState = rememberScrollState()

    Column(modifier = Modifier
        .fillMaxSize()
        .padding(top = 16.dp, start = 16.dp, end = 16.dp, bottom = 96.dp)
    ) {
        Text("Settings", style = MaterialTheme.typography.headlineMedium, color = Color.White, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(24.dp))
        
        Column(modifier = Modifier
            .weight(1f)
            .verticalScroll(scrollState), 
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            // Authentication Section
            SettingsSection(title = "Authentication") {
                OutlinedTextField(
                    value = keyInput, onValueChange = { keyInput = it },
                    label = { Text("Gemini API Key", color = Color.Gray) },
                    modifier = Modifier.fillMaxWidth(), singleLine = true,
                    colors = OutlinedTextFieldDefaults.colors(focusedTextColor = Color.White, unfocusedTextColor = Color.White),
                    visualTransformation = androidx.compose.ui.text.input.PasswordVisualTransformation(),
                    supportingText = { Text("Required for LLM generation", color = Color.Gray) }
                )
                Spacer(modifier = Modifier.height(16.dp))
                OutlinedTextField(
                    value = patInput, onValueChange = { patInput = it },
                    label = { Text("GitHub PAT (Optional)", color = Color.Gray) },
                    modifier = Modifier.fillMaxWidth(), singleLine = true,
                    colors = OutlinedTextFieldDefaults.colors(focusedTextColor = Color.White, unfocusedTextColor = Color.White),
                    visualTransformation = androidx.compose.ui.text.input.PasswordVisualTransformation(),
                    supportingText = { Text("Used for git clone and repo operations", color = Color.Gray) }
                )
            }
            
            // Model Configuration
            SettingsSection(title = "Model Configuration") {
                ExposedDropdownMenuBox(
                    expanded = expanded,
                    onExpandedChange = { expanded = it }
                ) {
                    OutlinedTextField(
                        value = modelInput, onValueChange = {}, readOnly = true,
                        label = { Text("AI Model", color = Color.Gray) },
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                        colors = OutlinedTextFieldDefaults.colors(focusedTextColor = Color.White, unfocusedTextColor = Color.White),
                        modifier = Modifier.menuAnchor().fillMaxWidth()
                    )
                    ExposedDropdownMenu(
                        expanded = expanded,
                        onDismissRequest = { expanded = false },
                        modifier = Modifier.background(Color(0xFF2D2C31))
                    ) {
                        availableModels.forEach { selectionOption ->
                            DropdownMenuItem(
                                text = { Text(selectionOption, color = Color.White) },
                                onClick = { modelInput = selectionOption; expanded = false }
                            )
                        }
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
                Text("Temperature: ${String.format(java.util.Locale.US, "%.1f", tempInput)}", color = Color.White, style = MaterialTheme.typography.bodyMedium)
                Slider(
                    value = tempInput, onValueChange = { tempInput = it }, valueRange = 0f..2f,
                    colors = SliderDefaults.colors(thumbColor = Color.White, activeTrackColor = Color.White)
                )
                Text("Higher values make output more random.", color = Color.Gray, style = MaterialTheme.typography.bodySmall)
            }

            // Environment
            SettingsSection(title = "Environment") {
                OutlinedTextField(
                    value = workspaceInput, onValueChange = { workspaceInput = it },
                    label = { Text("Workspace Directory", color = Color.Gray) },
                    modifier = Modifier.fillMaxWidth(), singleLine = true,
                    colors = OutlinedTextFieldDefaults.colors(focusedTextColor = Color.White, unfocusedTextColor = Color.White),
                    supportingText = { Text("Base path for all agent shell executions", color = Color.Gray) }
                )
            }
        }

        Spacer(modifier = Modifier.height(16.dp))
        Button(
            onClick = { viewModel.saveSettings(context, keyInput, modelInput, tempInput, patInput, workspaceInput) },
            modifier = Modifier.fillMaxWidth().height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color.White, contentColor = Color.Black),
            shape = RoundedCornerShape(16.dp)
        ) {
            Icon(Icons.Default.Check, contentDescription = "Save")
            Spacer(modifier = Modifier.width(8.dp))
            Text("Save Configuration", fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun SettingsSection(title: String, content: @Composable () -> Unit) {
    Column(modifier = Modifier.fillMaxWidth()) {
        Text(title, style = MaterialTheme.typography.titleMedium, color = Color(0xFFAAAAAA), fontWeight = FontWeight.SemiBold)
        Spacer(modifier = Modifier.height(12.dp))
        Surface(
            shape = RoundedCornerShape(16.dp),
            color = Color(0xFF1E1D22),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                content()
            }
        }
    }
}

"""
    content = content[:start_settings] + new_settings + content[end_settings:]
    print("Patched SettingsView")
else:
    print("Could not find SettingsView boundaries")

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "w") as f:
    f.write(content)
