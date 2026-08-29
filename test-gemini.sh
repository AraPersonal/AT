export API_KEY="$(grep 'API_KEY' app/.env | cut -d'=' -f2)"
curl -s -X POST https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=$API_KEY \
    -H 'Content-Type: application/json' \
    -d '{
      "contents": [
        {"role": "user", "parts": [{"text": "What is the weather?"}]},
        {"role": "model", "parts": [{"functionCall": {"name": "get_weather", "args": {}}}]},
        {"role": "user", "parts": [{"functionResponse": {"name": "get_weather", "response": {"weather": "sunny"}}}]}
      ],
      "tools": [{"function_declarations": [{"name": "get_weather", "description": "get weather"}]}]
    }'
