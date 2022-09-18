from tkinter import Tk, Canvas, PhotoImage, NW
import tkinter as tk


BG = '#555555'
BTN_COLOR = '#999999'
GREEN = "#00e702"
FONT_NAME = "Courier"
CHECK = '✓'
CIRCLE = '•'

pad = 70
running_state = 'PAUSED'
timer_state = 'WORK'
states = {'LONG PAUSE': 15, 'SHORT PAUSE': 5, 'WORK': 25}
remainig_seconds = states['WORK']

#---------------------------------------------------------------Buttons---------------------------------------------------------------

def start_button_command():
    global running_state
    if running_state == 'PAUSED':
        running_state = 'STARTED'
        timer(remainig_seconds)

def pause_button_command():
    global running_state
    if running_state == 'STARTED': running_state = 'PAUSED'

def reset_button_command():
    global running_state, remainig_seconds
    running_state = 'PAUSED'
    remainig_seconds = states[timer_state]
    _timer_text_updater(remainig_seconds)

#---------------------------------------------------------------TIMER---------------------------------------------------------------

def _timer_text_updater(seconds):
    mins = seconds//60
    secs = seconds%60
    canvas.itemconfig(timer_text, text=f'{mins:02d}:{secs:02d}')

def _set_mark():
    for index, mark in enumerate(marks_list):
        if mark['text'] == CIRCLE: return marks_list[index].config(text=CHECK, fg=GREEN, font=('Arial', 27))
            
def _timer_count_change(text, seconds):
    cur_msg.config(text=text)
    root.after(1, timer, seconds)



def _change_timer_state():
    global timer_state, states
    if marks_count() == 4: pause = 'LONG PAUSE'
    else: pause = 'SHORT PAUSE'

    if timer_state == 'WORK': 
        timer_state = pause

    else: 
        timer_state = 'WORK'
        _set_mark()

    _timer_count_change(timer_state, states[timer_state])


def timer(seconds):
    global running_state, remainig_seconds

    if running_state == 'PAUSED': return
    if seconds == 0: return _change_timer_state()

    remainig_seconds = seconds - 1
    root.after(1000, timer, remainig_seconds)



    _timer_text_updater(seconds)
    
#------------------------------------------------------------------------------------------------------------------------------------------
root = Tk()
root.geometry('650x600')
root.resizable(0, 0)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.config(bg=BG)

cur_msg = tk.Label(root, text=timer_state, font=(FONT_NAME, 30))
cur_msg.grid(row=0, column=1, columnspan=3, pady=(40, 0))

img = PhotoImage(file="tomato.png")
canvas = Canvas(root, width = 300, height = 300, highlightbackground=BG)
canvas.create_image(50, 20, anchor=NW, image=img)
canvas.grid(row=1, column=1, columnspan=3)

timer_text = canvas.create_text(150, 150, text="00:00", fill="white", font=(FONT_NAME, 50, "bold"))

marks_list = [tk.Label(root, text=CIRCLE, font=('Arial', 15)) for _ in range(8)]
marks_count = lambda: len(tuple(filter(lambda x: x['text'] == CHECK, marks_list)))

for index, mark in enumerate(marks_list):
    if index == 4: pad += 30
    mark.grid(row=2, column=1, columnspan=4, sticky='nsw', padx=(pad, 0))
    pad += 33


tk.Label(root, text='', height=4).grid(row=2, column=0) # Space placeholder

start_button = tk.Button(root, text='Start', command=start_button_command, bg=BTN_COLOR)
start_button.grid(row=4, column=0, padx=(15, 0), sticky='nsw')

pause_button = tk.Button(root, text='Pause', command=pause_button_command, bg=BTN_COLOR)
pause_button.grid(row=4, column=2)

reset_button = tk.Button(root, text='Reset', command=reset_button_command, bg=BTN_COLOR)
reset_button.grid(row=4, column=4, padx=(0, 15), sticky='nse')




for widget in root.winfo_children():
    if widget['bg'] == '#d9d9d9': widget['bg'] = BG



root.mainloop()