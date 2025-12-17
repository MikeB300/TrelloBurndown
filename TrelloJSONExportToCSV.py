import json
import csv

# Filnavne
json_file = "EXPORT FILE HERE FROM WEB.json"
csv_file = "trelloexport.csv"

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

cards = data.get("cards", [])

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Card Name", "Points", "Done Date"])

    for card in cards:
        if card.get("dueComplete") == True:
            name = card.get("name")
            points = 1  # Ændr hvis du bruger story points
            done_date = card.get("dateCompleted", card.get("dateLastActivity", ""))
            writer.writerow([name, points, done_date])

print(f"CSV-fil klar: {csv_file}")
