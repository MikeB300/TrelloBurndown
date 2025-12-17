import csv
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import simpledialog, messagebox

# Læs CSV
filename = "trelloexport.csv"
cards = []

with open(filename, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row["Card Name"]
        points = int(row["Points"])
        done_date = datetime.fromisoformat(row["Done Date"].replace("Z",""))
        cards.append({"name": name, "points": points, "done_date": done_date})

# Start- og slutdato
root_temp = tk.Tk()
root_temp.withdraw()
start_input = simpledialog.askstring("Dato range", "Indtast startdato (YYYY-MM-DD):", initialvalue=min(c["done_date"] for c in cards).strftime("%Y-%m-%d"))
end_input = simpledialog.askstring("Dato range", "Indtast slutdato (YYYY-MM-DD):", initialvalue=max(c["done_date"] for c in cards).strftime("%Y-%m-%d"))
root_temp.destroy()

start_date = datetime.strptime(start_input, "%Y-%m-%d")
end_date = datetime.strptime(end_input, "%Y-%m-%d")
days = (end_date - start_date).days + 1

# Resterende arbejde per dag
total_points = sum(c["points"] for c in cards)
daily_remaining = []
for i in range(days):
    day = start_date + timedelta(days=i)
    done_today = sum(c["points"] for c in cards if c["done_date"].date() <= day.date())
    daily_remaining.append(total_points - done_today)

# Ideallinje
ideal_line = [total_points - total_points*i/(days-1) for i in range(days)]

# Tkinter graf
WIDTH, HEIGHT = 1000, 600
MARGIN = 80

root = tk.Tk()
root.title("Interactive Burndown Chart")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# Skaleringsfunktioner
def scale_x(i):
    return MARGIN + i*(WIDTH-2*MARGIN)/(days-1)
def scale_y(val):
    return HEIGHT - MARGIN - val*(HEIGHT-2*MARGIN)/total_points

# Grid
for i in range(days):
    x = scale_x(i)
    canvas.create_line(x, MARGIN, x, HEIGHT-MARGIN, fill="#ddd")
for i in range(0, total_points+1, max(1,total_points//10)):
    y = scale_y(i)
    canvas.create_line(MARGIN, y, WIDTH-MARGIN, y, fill="#ddd")
    canvas.create_text(MARGIN-10, y, text=str(i), anchor="e")

# Plot ideallinje
for i in range(days-1):
    x1, y1 = scale_x(i), scale_y(ideal_line[i])
    x2, y2 = scale_x(i+1), scale_y(ideal_line[i+1])
    canvas.create_line(x1, y1, x2, y2, fill="green", dash=(4,2), width=2)
canvas.create_text(WIDTH-100, scale_y(ideal_line[-1])+15, text="Ideallinje", fill="green", font=("Arial",10,"bold"))

# Plot burndown linje med punkter
for i in range(days-1):
    x1, y1 = scale_x(i), scale_y(daily_remaining[i])
    x2, y2 = scale_x(i+1), scale_y(daily_remaining[i+1])
    canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
for i in range(days):
    x, y = scale_x(i), scale_y(daily_remaining[i])
    canvas.create_oval(x-4, y-4, x+4, y+4, fill="blue")
canvas.create_text(WIDTH-100, scale_y(daily_remaining[-1])-15, text="Resterende", fill="blue", font=("Arial",10,"bold"))

# X-akse labels
for i in range(days):
    x = scale_x(i)
    canvas.create_text(x, HEIGHT-MARGIN+15, text=(start_date+timedelta(days=i)).strftime("%d-%m"), angle=90)

canvas.create_text(WIDTH//2, 30, text=f"Burndown Chart - {total_points} point, {days} dage, 3 teammedlemmer", font=("Arial", 14, "bold"))

# Milepæle med drag & drop
milepæle = []
colors = ["orange", "red", "purple", "green", "brown"]

def make_draggable(item):
    def on_drag(event):
        canvas.coords(item, event.x, event.y)
    canvas.tag_bind(item, "<B1-Motion>", on_drag)

def draw_milestone(ms):
    i = (ms["date"] - start_date).days
    if 0 <= i < days:
        x = scale_x(i)
        y = MARGIN - 15
        line = canvas.create_line(x, MARGIN, x, HEIGHT-MARGIN, fill=ms["color"], dash=(2,2))
        text = canvas.create_text(x, y, text=ms["label"], fill=ms["color"], font=("Arial",10,"bold"))
        make_draggable(text)
        ms["canvas"] = (line, text)

def add_milestone():
    date_str = simpledialog.askstring("Milepæl", "Indtast dato (YYYY-MM-DD):")
    label = simpledialog.askstring("Milepæl", "Indtast milepæl label:")
    color = simpledialog.askstring("Milepæl", f"Vælg farve blandt: {', '.join(colors)}", initialvalue=colors[0])
    if date_str and label and color in colors:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            ms = {"date": date, "label": label, "color": color}
            milepæle.append(ms)
            draw_milestone(ms)
        except:
            messagebox.showerror("Fejl", "Ugyldig datoformat")
    elif color not in colors:
        messagebox.showerror("Fejl", "Farven skal vælges blandt de 5 muligheder")

def remove_milestone():
    if not milepæle:
        messagebox.showinfo("Info", "Ingen milepæle at slette")
        return
    labels = [ms["label"] for ms in milepæle]
    selected = simpledialog.askstring("Slet milepæl", f"Vælg milepæl at slette:\n{', '.join(labels)}")
    for ms in milepæle:
        if ms["label"] == selected:
            line, text = ms.get("canvas", (None, None))
            if line: canvas.delete(line)
            if text: canvas.delete(text)
            milepæle.remove(ms)
            break

btn_add = tk.Button(root, text="Tilføj milepæl", command=add_milestone)
btn_add.pack(pady=5)
btn_remove = tk.Button(root, text="Slet milepæl", command=remove_milestone)
btn_remove.pack(pady=5)

root.mainloop()
