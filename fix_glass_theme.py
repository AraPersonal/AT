import re

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    content = f.read()

# Dashboard Workspaces Cards
old_elevated_card = """colors = CardDefaults.elevatedCardColors(containerColor = Color(0xFF2D2C31)),
                        modifier = Modifier.height(120.dp).fillMaxWidth()"""
new_elevated_card = """colors = CardDefaults.elevatedCardColors(containerColor = Color.Transparent),
                        modifier = Modifier.height(120.dp).fillMaxWidth().glassMorphism(16.dp)"""
content = content.replace(old_elevated_card, new_elevated_card)

# Dashboard History Cards
old_card_dash = """colors = CardDefaults.cardColors(containerColor = Color(0xFF2D2C31)),
                        modifier = Modifier.fillMaxWidth().height(64.dp)"""
new_card_dash = """colors = CardDefaults.cardColors(containerColor = Color.Transparent),
                        modifier = Modifier.fillMaxWidth().height(64.dp).glassMorphism(16.dp)"""
content = content.replace(old_card_dash, new_card_dash)

# Gallery Cards
old_card_gal = """Card(colors = CardDefaults.cardColors(containerColor = Color(0xFF2D2C31)), modifier = Modifier.fillMaxWidth())"""
new_card_gal = """Card(colors = CardDefaults.cardColors(containerColor = Color.Transparent), modifier = Modifier.fillMaxWidth().glassMorphism(12.dp))"""
content = content.replace(old_card_gal, new_card_gal)

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "w") as f:
    f.write(content)
print("Fixed cards")
