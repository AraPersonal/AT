import com.google.ai.client.generativeai.type.*

fun main() {
    val f = FunctionDeclaration("test", "desc", listOf(Schema(name="param", description="desc", type=FunctionType.STRING, format="string")), listOf("param"))
    println(f.name)
    println(f.description)
    println(f.parameters?.size)
    println(f.parameters?.get(0)?.name)
    println(f.parameters?.get(0)?.type?.name)
}
