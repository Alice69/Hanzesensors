from tkinter import *
import serial, time

# FF seriele poortje openen
ser = serial.Serial('COM4', 19200, timeout=10)

# tk object maken + simpel Canvasje erin pleuren
tk = Tk()
canvas = Canvas(bg='#666', width=640, height=480)
canvas.pack()

# Maken nieuw text object voor canvas
label = canvas.create_text(100,100,text="Hier komt de data", fill='#FFF', font=("Helvetica", 12, "bold"))


# Dit is de update functie
def update():
    data = ser.readline().decode('ascii').strip()   # We lezen de seriële verbinding
    canvas.itemconfig(label, text=data)             # Aanpassen van het label
    tk.after(1000, update)                          # Om de seconde update() opnieuw roepen

# Roepen om te starten 1 keer update() aan
update()

# Mainloop zodat tkInter voor ons dat mooie schermpje tovert
tk.mainloop()