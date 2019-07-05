import json
data = open("cache.json")

print(json.load(data))
data["name"].append("azfar")
with open('data.json', 'a+', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)