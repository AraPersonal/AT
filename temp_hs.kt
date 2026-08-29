package com.example.ui

import android.content.Context
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.Chat
import androidx.compose.material.icons.automirrored.filled.List
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment

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

import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.animation.core.FastOutSlowInEasing

import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.compose.ui.draw.blur
import androidx.compose.ui.draw.scale
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.animation.animateColorAsState
import java.io.File
import com.example.data.ChatMessageEntity

object Routes {
    const val DASHBOARD = "dashboard"
    const val GALLERY = "gallery"
    const val CHAT = "chat"
    const val CONSOLE = "console"
    const val SETTINGS = "settings"
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(viewModel: AgentViewModel = viewModel(factory = AgentViewModel.Factory)) {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route ?: Routes.DASHBOARD

    Scaffold(
        containerColor = Color(0xFF1C1B1F),
        bottomBar = {
            TelegramBottomBar(
                currentRoute = currentRoute,
                onNavigate = { route -> navController.navigate(route) { launchSingleTop = true } }
            )
        },
        topBar = {
            TopAppBar(
                title = { Text("Nexus Agent AI", style = MaterialTheme.typography.titleMedium, color = Color.White) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color(0xFF151419))
            )
        }
    ) { paddingValues ->
        NavHost(
            navController = navController,
            startDestination = Routes.DASHBOARD,
            modifier = Modifier
                .fillMaxSize()
                .padding(top = paddingValues.calculateTopPadding()) // Only top padding so content draws under the blurred bottom bar
        ) {
            composable(Routes.DASHBOARD) { DashboardView(viewModel, navController) }
            composable(Routes.GALLERY) { GalleryView(viewModel) }
            composable(Routes.CHAT) { ChatView(viewModel) }
            composable(Routes.CONSOLE) { ConsoleView(viewModel) }
            composable(Routes.SETTINGS) { SettingsView(viewModel) }
        }
    }
}

@Composable
fun DashboardView(viewModel: AgentViewModel, navController: NavHostController) {
    val workspaces = listOf(
        Pair("Chat", "NORMAL"),
        Pair("Terminal", "TERMINAL"),
        Pair("Tweaks", "SYSTEM_TWEAK"),
        Pair("Apps", "APK_BUILDER"),
        Pair("Modules", "MODULE_BUILDER")
    )
    
    var selectedWorkspace by remember { mutableStateOf<String?>(null) }
    val allSessions by viewModel.allSessions.collectAsState()
    
    if (selectedWorkspace == null) {
        Column(modifier = Modifier.fillMaxSize().padding(start = 16.dp, top = 16.dp, end = 16.dp, bottom = 96.dp)) {
            Text("Workspaces", style = MaterialTheme.typography.titleLarge, color = Color.White)
            Spacer(modifier = Modifier.height(16.dp))
            LazyVerticalGrid(
                columns = GridCells.Fixed(2),
                horizontalArrangement = Arrangement.spacedBy(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(workspaces) { workspace ->
                    ElevatedCard(
                        onClick = { selectedWorkspace = workspace.second },
                        colors = CardDefaults.elevatedCardColors(containerColor = Color(0xFF2D2C31)),
                        modifier = Modifier.height(120.dp).fillMaxWidth()
                    ) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Text(workspace.first, color = Color.White, style = MaterialTheme.typography.titleMedium)
                        }
                    }
                }
            }
        }
    } else {
        Column(modifier = Modifier.fillMaxSize().padding(start = 16.dp, top = 16.dp, end = 16.dp, bottom = 96.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = { selectedWorkspace = null }) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                }
                Text("Session History", style = MaterialTheme.typography.titleMedium, color = Color.White)
            }
            Spacer(modifier = Modifier.height(16.dp))
            
            Button(
                onClick = { 
                    viewModel.createNewSession(selectedWorkspace!!)
                    navController.navigate(Routes.CHAT) { launchSingleTop = true }
                },
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(containerColor = Color.White, contentColor = Color.Black)
            ) {
                Text("New Session")
            }
            Spacer(modifier = Modifier.height(16.dp))
            
            val filteredSessions = allSessions.filter { it.sessionType == selectedWorkspace }
            LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                items(filteredSessions) { session ->
                    Card(
                        onClick = { 
                            viewModel.loadSession(session.id, session.sessionType)
                            navController.navigate(Routes.CHAT) { launchSingleTop = true }
                        },
                        colors = CardDefaults.cardColors(containerColor = Color(0xFF2D2C31)),
                        modifier = Modifier.fillMaxWidth().height(64.dp)
                    ) {
                        Box(modifier = Modifier.padding(16.dp), contentAlignment = Alignment.CenterStart) {
                            Text(session.title, color = Color.White)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun GalleryView(viewModel: AgentViewModel) {
    val sessionType by viewModel.currentSessionType.collectAsState()
    
    val targetAssetType = when (sessionType) {
        "SYSTEM_TWEAK" -> "BACKUP"
        "APK_BUILDER" -> "APK"
        "MODULE_BUILDER" -> "MODULE"
        else -> null
    }

    if (targetAssetType == null) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text("No gallery available for $sessionType workspace.", color = Color.Gray)
        }
        return
    }

    LaunchedEffect(targetAssetType) { viewModel.loadAssetVersions(targetAssetType) }
    val versions by viewModel.assetVersions.collectAsState()

    Column(modifier = Modifier.fillMaxSize().padding(start = 16.dp, top = 16.dp, end = 16.dp, bottom = 96.dp)) {
        Text("Gallery ($targetAssetType)", style = MaterialTheme.typography.titleLarge, color = Color.White)
        Spacer(modifier = Modifier.height(16.dp))
        
        if (versions.isEmpty()) {
            Text("No assets found.", color = Color.Gray)
        } else {
            LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                items(versions) { version ->
                    Card(colors = CardDefaults.cardColors(containerColor = Color(0xFF2D2C31)), modifier = Modifier.fillMaxWidth()) {
                        Row(modifier = Modifier.padding(12.dp).fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text(File(version.filePath).name, color = Color.LightGray, fontSize = 14.sp, modifier = Modifier.weight(1f))
                            when (targetAssetType) {
                                "BACKUP" -> {
                                    Button(onClick = { viewModel.restoreBackup(version) }, contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp)) {
                                        Text("Restore", fontSize = 12.sp)
                                    }
                                }
                                "APK" -> {
                                    Button(onClick = { viewModel.installApk(version.filePath) }, contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp)) {
                                        Text("Install", fontSize = 12.sp)
                                    }
                                }
                                "MODULE" -> {
                                    Button(onClick = { viewModel.sendMessage("Please flash the module at ${version.filePath} using `su -c magisk --install-module ${version.filePath}`") }, contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp)) {
                                        Text("Flash", fontSize = 12.sp)
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ConsoleView(viewModel: AgentViewModel) {
    val logs by viewModel.terminalLogs.collectAsState()
    Column(modifier = Modifier.fillMaxSize().padding(start = 16.dp, top = 16.dp, end = 16.dp, bottom = 96.dp)) {
        Text("Console", style = MaterialTheme.typography.titleLarge, color = Color.White)
        Spacer(modifier = Modifier.height(16.dp))
        Box(modifier = Modifier.fillMaxSize().background(Color.Black, RoundedCornerShape(8.dp)).padding(8.dp)) {
            SelectionContainer {
                Text(logs, color = Color.Green, style = MaterialTheme.typography.bodySmall.copy(fontFamily = FontFamily.Monospace))
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
fun androidx.compose.ui.Modifier.glassMorphism(
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
                    IconButton(onClick = {  }) {
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

@OptIn(ExperimentalMaterial3Api::class)
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

@Composable
fun TelegramBottomBar(
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
}
