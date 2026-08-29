package com.example.data

import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import android.util.Log

class GeminiService(
    private val apiKey: String, 
    private val modelName: String = "gemini-3.6-flash",
    private val temperature: Float = 1.0f,
    private val githubPat: String = "",
    private val workspaceDir: String = "/sdcard/NexusWorkspace",
    private val sessionType: String = "NORMAL"
) {
    private val history = JSONArray()
    private val systemInstructionText: String
    
    init {
        val baseInstruction = """You are an autonomous on-device terminal engineer. Use the tools provided instead of just answering with markdown. If a command fails, try to diagnose and fix it. You have full access to a rooted Android environment via libsu.
WORKSPACE INSTRUCTIONS:
Your designated workspace is: $workspaceDir
All operations, unless specified otherwise, should be inside this workspace.
GIT AUTHENTICATION:
Use the provided GitHub PAT for remote operations. Example: `git clone https://${githubPat}@github.com/user/repo.git`. Execute these using the `run_shell` tool."""
        val typeInstruction = when (sessionType) {
            "SYSTEM_TWEAK" -> "You are managing system tweaks. ALWAYS call `backup_file` before modifying any file in /system, /vendor, or /data so the user can rollback. Then modify using `modify_prop` or writing the file."
            "APK_BUILDER" -> "You are an APK builder. You can compile Android projects using `run_gradlew assembleDebug`. Ensure the build environment is set up first using `setup_build_environment`."
            "MODULE_BUILDER" -> "You are a Magisk/KernelSU module builder. Use `scaffold_magisk_module` to create a new module, edit its contents, and then use `zip_module`."
            "TERMINAL" -> "You are a raw shell interface assistant. You can execute raw commands."
            else -> "You are a general AI assistant. You don't have access to dangerous tools."
        }
        systemInstructionText = baseInstruction + "\n\n" + typeInstruction
    }

    suspend fun sendMessage(
        message: String,
        onToolExecute: suspend (String, JSONObject) -> JSONObject
    ): String = withContext(Dispatchers.IO) {
        val userPart = JSONObject().put("text", message)
        val userContent = JSONObject().put("role", "user").put("parts", JSONArray().put(userPart))
        history.put(userContent)

        var finalResponse = ""
        var currentLoop = 0

        while (currentLoop < 5) {
            currentLoop++
            val requestBody = JSONObject()
            requestBody.put("contents", history)

            if (sessionType != "NORMAL") {
                val toolsObj = JSONObject()
                toolsObj.put("function_declarations", AgentTools.getToolsAsJsonArray(sessionType))
                requestBody.put("tools", JSONArray().put(toolsObj))
            }
            
            requestBody.put("system_instruction", JSONObject().put("parts", JSONArray().put(JSONObject().put("text", systemInstructionText))))
            
            val config = JSONObject()
            config.put("temperature", temperature)
            requestBody.put("generationConfig", config)

            val cleanModelName = if (modelName.contains("/")) modelName.split("/")[1] else modelName
            val url = URL("https://generativelanguage.googleapis.com/v1beta/models/$cleanModelName:generateContent?key=$apiKey")
            val connection = url.openConnection() as HttpURLConnection
            connection.requestMethod = "POST"
            connection.setRequestProperty("Content-Type", "application/json")
            connection.doOutput = true
            
            try {
                connection.outputStream.write(requestBody.toString().toByteArray())
            } catch (e: Exception) {
                return@withContext "Network error: ${e.message}"
            }

            if (connection.responseCode != 200) {
                val err = try { connection.errorStream.bufferedReader().readText() } catch (e: Exception) { "Unknown error" }
                return@withContext "Error: ${connection.responseCode} $err\n"
            }

            val responseStr = connection.inputStream.bufferedReader().readText()
            val responseJson = JSONObject(responseStr)

            val candidates = responseJson.optJSONArray("candidates")
            if (candidates == null || candidates.length() == 0) return@withContext "No response."

            val firstCandidate = candidates.getJSONObject(0)
            val contentObj = firstCandidate.optJSONObject("content")
            if (contentObj == null) return@withContext "No content in response."
            
            // Add model response to history as-is (this preserves thought_signature inside parts!)
            history.put(contentObj) 

            val parts = contentObj.optJSONArray("parts") ?: JSONArray()
            val functionCalls = mutableListOf<JSONObject>()
            for (i in 0 until parts.length()) {
                val part = parts.getJSONObject(i)
                if (part.has("text")) {
                    finalResponse += part.getString("text") + "\n"
                }
                if (part.has("functionCall")) {
                    functionCalls.add(part.getJSONObject("functionCall"))
                }
            }

            if (functionCalls.isEmpty()) {
                break
            }

            val toolResponseParts = JSONArray()
            for (fc in functionCalls) {
                val name = fc.getString("name")
                val args = fc.optJSONObject("args") ?: JSONObject()
                val result = try { onToolExecute(name, args) } catch (e: Exception) { JSONObject().put("error", e.message) }
                val functionResponse = JSONObject()
                functionResponse.put("name", name)
                functionResponse.put("response", result)
                if (fc.has("id")) {
                    functionResponse.put("id", fc.getString("id"))
                }
                
                val toolResponse = JSONObject()
                toolResponse.put("functionResponse", functionResponse)
                toolResponseParts.put(toolResponse)
            }

            val toolResponseContent = JSONObject()
            toolResponseContent.put("role", "user")
            toolResponseContent.put("parts", toolResponseParts)
            history.put(toolResponseContent)
        }

        return@withContext finalResponse.trim().ifEmpty { "No text response." }
    }
}
