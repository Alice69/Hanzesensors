from tkinter import *
import serial, time

# FF seriele poortje openen
ser = serial.Serial('COM4', 19200, timeout=10)

# tk object maken + simpel Canvasje erin pleuren
tk = Tk()
canvas = Canvas(bg='#333', width=640, height=480)
canvas.pack()

# Maken nieuw text object voor canvas
label = canvas.create_text(100,100,text="Hier komt de data", fill='#FFF', font=("Helvetica", 12, "bold"))


# List voor het opslaan van de waardes
waardes = []
for i in range(20):
    waardes.append(0)
lines = {}
graphPos = (80, 60)
graphSize = (640-(80*2), 480-(60*2))


# Dit is de update functie
def update():
    # Uitlezen data
    data = ser.readline().decode('ascii').strip()   # We lezen de seriële verbinding
    temperature = int(str.split(data, ':')[1])      # Halen alleen waarde uit string
    waardes.pop(0)
    waardes.append(temperature)

    # Change canvas items
    canvas.itemconfig(label, text=data)             # Aanpassen van het label

    for i in range(len(waardes) - 1):
        x1 = graphPos[0] + (i * (graphSize[0] / len(waardes)))
        x2 = graphPos[0] + ((i + 1) * (graphSize[0] / len(waardes)))
        y1 = graphSize[1] - (waardes[i] * ((graphSize[1]- graphPos[1]) / max(waardes)))
        y2 = graphSize[1] - (waardes[i + 1] * ((graphSize[1]- graphPos[1]) / max(waardes)))
        if i not in lines.keys():
            lines[i] = canvas.create_line(x1, y1, x2, y2, fill='#FA0', width=1)
        else:
            canvas.coords(lines[i], x1, y1, x2, y2)
    tk.after(100, update)                          # Om de seconde update() opnieuw roepen

# Roepen om te starten 1 keer update() aan
update()

# Mainloop zodat tkInter voor ons dat mooie schermpje tovert
tk.mainloop()