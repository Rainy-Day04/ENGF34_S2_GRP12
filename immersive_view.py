import tkinter as tk
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageTk

class Rect:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

def run_vr(root):
    def create_rounded_rectangle(width, height, x1, y1, x2, y2, radius, fill):
        img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius, fill=fill)

        return img

    def create_overlay_widgets(window_width, window_height, widgetObj1, widgetObj2, widgetObj3):
        overlay_img = create_rounded_rectangle(window_width, window_height, widgetObj1.start_x, widgetObj1.start_y,
                                            widgetObj1.end_x, widgetObj1.end_y, radius=20,
                                            fill=(0, 0, 0, 180))
        overlay_img_2 = create_rounded_rectangle(window_width, window_height, widgetObj2.start_x, widgetObj2.start_y,
                                                widgetObj2.end_x, widgetObj2.end_y, radius=20,
                                                fill=(0, 0, 0, 180))

        overlay_img_3 = create_rounded_rectangle(window_width, window_height, widgetObj3.start_x, widgetObj3.start_y,
                                                widgetObj3.end_x, widgetObj3.end_y, radius=20,
                                                fill=(0, 0, 0, 180))
        return overlay_img, overlay_img_2, overlay_img_3

    def frame_by_frame():
        def video_player():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image=frame)
                canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                canvas.image = photo
            else:
                cap.release()
                root.destroy()
                return
            canvas.delete("overlay")

        def heart_rate_text(heart_rate_rect):
            text = "HEART RATE"
            canvas.create_text((heart_rate_rect.start_x + heart_rate_rect.end_x - len(text)) // 2,
                            (heart_rate_rect.start_y + heart_rate_rect.end_y - len(text)) // 2, text=text, fill="white",
                            font=('Helvetica 15 bold'))

        video_player()

        heart_rate_rect = Rect(590, 100, 770, 320)
        progress_rect = Rect(590, 30, 770, 90)
        time_rect = Rect(10, 10, 190, 50)

        overlay_img, overlay_img_2, overlay_img_3 = create_overlay_widgets(window_width, window_height, heart_rate_rect,
                                                                        progress_rect, time_rect)
        overlay_photo = ImageTk.PhotoImage(overlay_img)
        overlay_photo_2 = ImageTk.PhotoImage(overlay_img_2)
        overlay_photo_3 = ImageTk.PhotoImage(overlay_img_3)
        canvas.create_image(0, 0, anchor=tk.NW, image=overlay_photo, tags="overlay")
        canvas.create_image(0, 0, anchor=tk.NW, image=overlay_photo_2, tags="overlay")
        canvas.create_image(0, 0, anchor=tk.NW, image=overlay_photo_3, tags="overlay")

        canvas.overlay_photo = overlay_photo
        canvas.overlay_photo_2 = overlay_photo_2
        canvas.overlay_photo_3 = overlay_photo_3

        heart_rate_text(heart_rate_rect)
        root.after(int(1000 / video_fps), frame_by_frame)  # Adjust the delay according to the frame rate

    window_width = 800
    window_height = 480
    root.minsize(width=window_width, height=window_height)
    root.maxsize(width=window_width, height=window_height)
    root.geometry(f"{window_width}x{window_height}")
    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.pack()
    video_path = "pictures/vid.mp4"
    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_by_frame()
    root.mainloop()