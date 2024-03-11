import random
import tkinter as tk
from tkinter import Canvas, Toplevel, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from immersive_view import run_vr
import time
import threading

from backend import Heart_rate, Pedometer, front_end_calendar,Database1
from datetime import datetime, timedelta


class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("480x800")
        self.root.configure(bg='#333333')
        self.root.minsize(480, 800)
        self.root.maxsize(480, 800)
        self.target = 100
        self.trend_length = 0
        self.progress = 50
        self.week_progress = [True, False, True, False, True, False, False]
        self.pulse_rate = [40,36,65,87,90,110,121,124,98,89] # queue, maintain its length

        # Grey column on the left of the screen
        self.settings_column = tk.Label(self.root, bg='#454545', width=17, height=800)
        self.settings_column.place(x=0, y=0, anchor='nw')

        # Today's Goal
        rounded_rect1 = self.create_rounded_rectangle(310, 99, 0, 0, 310, 99, 15, '#ff8c00')
        rounded_rect1 = ImageTk.PhotoImage(rounded_rect1)
        self.label = tk.Label(self.root, image=rounded_rect1, text="Today's Goal", fg='white', bg="#333333", font=('Helvetica', 20, 'bold'), compound='center')
        self.label.image = rounded_rect1
        self.label.place(x=460, y=20, anchor='ne')

        # Orange bar on the background
        rounded_rect2 = self.create_rounded_rectangle(275, 15, 0, 0, 275, 15, 10, '#fb8334')
        rounded_rect2 = ImageTk.PhotoImage(rounded_rect2)
        self.progress_bg = tk.Label(self.root, image=rounded_rect2, fg='white', bg='#333333')
        self.progress_bg.image = rounded_rect2
        self.progress_bg.place(x=160, y=125, anchor='nw')

        # Process bar on the foreground
        rounded_rect3 = self.create_rounded_rectangle(275, 15, 0, 0, 275, 15, 10, '#b8f7f2')
        rounded_rect3 = ImageTk.PhotoImage(rounded_rect3)
        self.progress_fg = tk.Label(self.root, image=rounded_rect3, bg='#333333', fg='white')
        self.progress_fg.image = rounded_rect3
        self.progress_fg.place(x=160, y=125, anchor='nw')

        # Progress and Percentage
        self.progress_label = tk.Label(self.root, text="", bg='#333333', fg='white', font=('European', 10, 'italic'))
        self.progress_label.place(x=460, y=150, anchor='ne')

        # logo
        rounded_logo_bg = self.create_rounded_rectangle(80, 80, 0, 0, 80, 80, 20, '#fb8334', alt=True)
        rounded_logo_bg = ImageTk.PhotoImage(rounded_logo_bg)
        self.logo_label = tk.Label(self.root, image=rounded_logo_bg, bg='#454545')
        self.logo_label.image = rounded_logo_bg
        self.logo_label.place(x=20, y=20, anchor='nw')

        # label on the background of the logo
        img = Image.open("pictures/logo.png")
        self.logo = ImageTk.PhotoImage(img)
        self.logo_label = tk.Label(self.root, image=self.logo, bg='#fb8334')
        self.logo_label.place(x=32, y=35, anchor='nw')

        # weekly progress and the schedule title
        rounded_rect5 = self.create_rounded_rectangle(310, 200, 0, 0, 310, 200, 10, '#454545')
        rounded_rect5 = ImageTk.PhotoImage(rounded_rect5)
        rounded_rect_schedule = self.create_rounded_rectangle(120, 30, 0, 0, 120, 30, 15, '#454545')
        rounded_rect_schedule = ImageTk.PhotoImage(rounded_rect_schedule)
        self.week_progress_bg = tk.Label(self.root, image=rounded_rect5, bg="#333333")
        self.week_progress_bg.image = rounded_rect5
        self.week_progress_bg.place(x=460, y=220, anchor='ne')
        self.schedule_label = tk.Label(self.root, image=rounded_rect_schedule, text="  Schedule  ", bg = "#333333", fg='white', font=('European', 16, 'bold'), compound='center')
        self.schedule_label.image = rounded_rect_schedule
        self.schedule_label.place(x=140, y=180)

        # circles for weekly progress
        for i, done in enumerate(self.week_progress):
            canvas = tk.Canvas(self.root, width=50, height=60, bg='#454545', highlightthickness=0)
            fill_color = '#b8f7f2' if done else '#ff9060'
            canvas.create_oval(10, 10, 40, 40, fill=fill_color, outline='#454545')
            canvas.create_text(25, 25, text=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i], fill='#454545')
            canvas.place(x=160 + i * 40, y=230)

        # label with text upcoming
        self.upcoming_label = tk.Label(self.root, text="Upcoming", bg='#454545', fg='white', font=('European', 12, 'italic', 'underline'))
        self.upcoming_label.place(x=160, y=290)

        # reminders
        reminder1_text = "19:30   30min   Today".ljust(50)
        reminder2_text = "19:00   30min   Tomorrow".ljust(50)

        self.reminder1_label = tk.Label(self.root, text=reminder1_text, bg='#454545', fg='white', font=('European', 10))
        self.reminder1_label.place(x=160, y=330)

        self.reminder2_label = tk.Label(self.root, text=reminder2_text, bg='#454545', fg='white', font=('European', 10))
        self.reminder2_label.place(x=160, y=360)

        # title of pulse rate detector
        rounded_rect_pulse = self.create_rounded_rectangle(140, 30, 0, 0, 140, 30, 15, '#454545')
        rounded_rect_pulse = ImageTk.PhotoImage(rounded_rect_pulse)
        self.pulse_rate_label = tk.Label(self.root, image=rounded_rect_pulse, text="Pulse Rate", bg="#333333", fg='white', font=('European', 16, 'bold'), compound='center')
        self.pulse_rate_label.image = rounded_rect_pulse
        self.pulse_rate_label.place(x=140, y=445)

        # pulse rate background
        rounded_rect6 = self.create_rounded_rectangle(310, 200, 0, 0, 310, 200, 10, '#454545')
        rounded_rect6 = ImageTk.PhotoImage(rounded_rect6)
        self.pulse_rate_bg = tk.Label(self.root, image=rounded_rect6, bg="#333333")
        self.pulse_rate_bg.image = rounded_rect6
        self.pulse_rate_bg.place(x=460, y=485, anchor='ne')

        # product title
        self.product_title = tk.Label(self.root, text="Shuffler App", bg='#454545', fg='#FFFFFF', font=('European', 8, 'bold', 'underline'))
        self.product_title.place(x=23, y=120, anchor='nw')

        # user information here (click on the button to show)
        self.user_info_label = tk.Label(self.root, text="", bg='#454545', fg='white', font=('European', 11), anchor='n')
        self.user_info_label.place(x=127, y=58)

        # user info button
        self.user_info_button = tk.Button(self.root, text="  User Info  ", bg='#333333', fg='white', command=self.show_user_info)
        self.user_info_button.place(x=28, y=160, anchor='nw')

        self.user_info_visible = False

        # goal button
        self.set_goal_button = tk.Button(self.root, text="   Set Goal  ", bg='#333333', fg='white', command=self.set_goal)
        self.set_goal_button.place(x=28, y=200, anchor='nw')

        # enter vr button
        self.enter_vr_button = tk.Button(self.root, text="   Enter VR  ", bg='#fb8334', fg='white', width=12, height=3, command=self.enter_vr)
        self.enter_vr_button.place(x=16, y=710, anchor='nw')

        # show up after clicking set goal
        self.goal_entry = tk.Entry(self.root, bg='#454545', fg='white', font=('European', 10))
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_goal, bg='#454545', fg='white')
        self.cancel_button = tk.Button(self.root, text="Cancel", command=self.cancel_goal, bg='#454545', fg='white')

        # show up after complete today's goal
        self.completion_label = tk.Label(self.root, text="", fg='#b8f7f2', bg='#333333', font=('European', 12, 'italic'))

        # pulse rate line chart
        self.fig, self.ax = plt.subplots(figsize=(3.1, 2))
        self.Database = Database1("data.sqlite")
        self.Database.reset_all_data()
        self.id = 1
        current_date = datetime.now()
        formatted_date = current_date.strftime("%d-%m-%Y")
        self.Database.init_day(self.id, formatted_date)
        self.Database.close()
        self.heartrate = Heart_rate()
        self.pedometer = Pedometer()
        print("UI initialized 1")
        threading.Thread(target=self.heartrate.dummy_heart_rate).start()
        threading.Thread(target=self.pedometer.dummy_walker).start()
        print("UI initialized")

    # pulse rate update
    def draw_pulse_rate_chart(self, fig, ax):
        if self.progress_fg.winfo_exists():
            for widget in self.pulse_rate_bg.winfo_children():
                widget.destroy()
            ax.set_facecolor('#454545')
            fig.patch.set_facecolor('#454545')
            ax.spines['left'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.xaxis.set_ticks([])
            ax.yaxis.tick_left()
            ax.tick_params(axis='y', colors='white')
            start, end = ax.get_ylim()
            ax.yaxis.set_ticks(np.arange(0, 160, 20))
            x_coords = list(range(len(self.pulse_rate)))
            colors = []
            for rate in self.pulse_rate:
                if 60 <= rate <= 110:
                    colors.append('#b8f7f2')
                elif 40 <= rate <= 130:
                    colors.append('yellow')
                else:
                    colors.append('red')
            ax.plot(x_coords, self.pulse_rate, c='#c23b0a')
            ax.scatter(x_coords, self.pulse_rate, 5, c=colors)
            ax.fill_between(x_coords, self.pulse_rate, color='#c23b0a', alpha=0.3)
            canvas = FigureCanvasTkAgg(fig, master=self.pulse_rate_bg)
            canvas.draw()
            canvas.get_tk_widget().pack(padx=5, pady=5)

    def clear_pulse_rate_chart(self):
        self.ax.clear()

    def set_goal(self):
        self.goal_entry.place(x=3, y=243, anchor='nw', width=120)
        self.submit_button.place(x=15, y=265, anchor='nw')
        self.cancel_button.place(x=65, y=265, anchor='nw')
        self.goal_entry.focus_set()

    def submit_goal(self):
        new_target = int(self.goal_entry.get())
        if new_target < self.progress:
            messagebox.showerror("Invalid goal", "Goal cannot be less than current progress.")
            return
        elif new_target > 50000:
            messagebox.showerror("Invalid goal", "Excessive exercise could be harful.")
            return
        self.target = new_target
        self.update_progress(self.progress, self.target)
        self.goal_entry.place_forget()
        self.cancel_button.place_forget()
        self.submit_button.place_forget()
        self.Database = Database1("data.sqlite")
        current_date = datetime.now()
        formatted_date = current_date.strftime("%d-%m-%Y")
        self.Database.update_day_data(self.id, formatted_date, self.progress, self.target)
        self.Database.close()

    def cancel_goal(self):
        self.goal_entry.place_forget() 
        self.submit_button.place_forget()
        self.cancel_button.place_forget()

    def show_user_info(self):
        if self.user_info_visible:
            self.user_info_label['text'] = ""
            self.user_info_title['text'] = ""
            self.user_info_label['width'] = 0
            self.user_info_title['width'] = 0
            self.user_info_visible = False
        else:
            name = "User Name" 
            id = "User ID"
            self.user_info_title = tk.Label(self.root, text="User Information", bg='#454545', fg='white', font=('European', 20, 'bold'), anchor='sw', width=23)
            self.user_info_title.place(x=127, y=20, anchor='nw')
            self.user_info_label['text'] = f"\nName: {name}\nID: {id}"
            self.user_info_label['width'] = 39
            self.user_info_label['height'] = 45
            self.user_info_label.lift()
            self.user_info_title['text'] = "User Information"
            self.user_info_visible = True

    def update_progress(self, current, target):
        if self.progress_fg.winfo_exists() and self.progress < self.target:
            progress_width = int((current / target) * 275)
            rounded_rect = self.create_rounded_rectangle(progress_width, 15, 0, 0, progress_width, 15, 10, '#b8f7f2')
            rounded_rect = ImageTk.PhotoImage(rounded_rect)
            self.progress_fg.configure(image=rounded_rect)
            self.progress_fg.image = rounded_rect
            self.progress_label['text'] = f"{current} / {target} ({(current/target)*100:.2f}%)"
            self.progress_label['fg'] = 'white'
            self.completion_label.destroy()

        elif self.progress_fg.winfo_exists() and self.progress == self.target:
            progress_width = 275
            rounded_rect = self.create_rounded_rectangle(progress_width, 15, 0, 0, progress_width, 15, 10, '#b8f7f2')
            rounded_rect = ImageTk.PhotoImage(rounded_rect)
            self.progress_fg.configure(image=rounded_rect)
            self.progress_fg.image = rounded_rect
            self.progress_label['text'] = f"{current} / {target} ({(current/target)*100:.2f}%)"
            self.progress_label['fg'] = 'green'
            self.completion_label = tk.Label(self.root, text="Well done!\nYou have completed today's goal!", fg='#b8f7f2', bg='#333333', font=('European', 12, 'italic'))
            self.completion_label.place(x=140, y=720)

    def create_rounded_rectangle(self, width, height, x1, y1, x2, y2, radius, fill, alt=False):
        if alt:
            img = Image.new("RGBA", (width + 2, height + 2), (69, 69, 69, 255))
        else:
            img = Image.new("RGBA", (width + 2, height + 2), (51, 51, 51, 255))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([(x1, y1), (x2 + 2, y2 + 2)], radius, fill=fill)
        return img

    def enter_vr(self, event=None):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.geometry("800x480")
        run_vr(self.root)

    def run(self):
        self.update_ui()
        self.root.mainloop()

    def update_pulse_rate(self, pulse_rate):
        self.pulse_rate.remove(self.pulse_rate[0])
        self.pulse_rate.append(pulse_rate)
        self.clear_pulse_rate_chart()
        self.draw_pulse_rate_chart(self.fig, self.ax)

    def update_ui(self):
        self.progress = self.pedometer.get_step_count()
        pulse_rate = self.heartrate.get_heart_rate()
        self.update_progress(self.progress, self.target)
        self.update_pulse_rate(pulse_rate)
        self.root.after(1000, self.update_ui)

if __name__ == "__main__":
    ui = UI()
    ui.run()