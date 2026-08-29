package com.example.data

import com.google.ai.client.generativeai.type.*
import org.json.*

fun test() {
    val decl = FunctionDeclaration("test", "desc", listOf(Schema(name="param", description="desc", type=FunctionType.STRING, format="string")), listOf("param"))
    val p = decl.parameters
    if (p != null) {
        for (s in p) {
            val typeName = s.type.name
        }
    }
}
