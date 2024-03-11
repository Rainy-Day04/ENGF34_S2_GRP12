# import tkinter as tk
# import cv2
# from PIL import Image, ImageDraw, ImageFont, ImageTk
#
# class VideoOverlayApp(tk.Tk):
#     class Rect:
#         def __init__(self, start_x, start_y, end_x, end_y):
#             self.start_x = start_x
#             self.start_y = start_y
#             self.end_x = end_x
#             self.end_y = end_y
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.title("Overlay Widgets on Video")
#
#         # Set the window size
#         self.window_width = 800
#         self.window_height = 480
#         self.geometry(f"{self.window_width}x{self.window_height}")
#
#         # Create a canvas for displaying video
#         self.canvas = tk.Canvas(self, width=self.window_width, height=self.window_height)
#         self.canvas.pack()
#
#         # Load the video
#         self.video_path = "pictures/vid.mp4"  # Replace with your video path
#         self.cap = cv2.VideoCapture(self.video_path)
#
#         # Get the frame rate of the video
#         self.video_fps = self.cap.get(cv2.CAP_PROP_FPS)
#
#         # Create a button
#         self.button = tk.Button(self, text="Portrait Mode", command=self.button_clicked)
#         self.button.place(x=self.window_width - 15 - self.button.winfo_reqwidth(), y=self.window_height - 15 - self.button.winfo_reqheight())
#
#     def create_rounded_rectangle(self, width, height, x1, y1, x2, y2, radius, fill):
#         img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
#         draw = ImageDraw.Draw(img)
#         draw.rounded_rectangle([(x1, y1), (x2, y2)], radius, fill=fill)
#         return img
#
#     def create_overlay_widgets(self, widgetObj1, widgetObj2, widgetObj3):
#         overlay_img = self.create_rounded_rectangle(self.window_width, self.window_height, widgetObj1.start_x, widgetObj1.start_y, widgetObj1.end_x, widgetObj1.end_y, radius=20, fill=(0, 0, 0, 180))
#         overlay_img_2 = self.create_rounded_rectangle(self.window_width, self.window_height, widgetObj2.start_x, widgetObj2.start_y, widgetObj2.end_x, widgetObj2.end_y, radius=20, fill=(0, 0, 0, 180))
#         overlay_img_3 = self.create_rounded_rectangle(self.window_width, self.window_height, widgetObj3.start_x, widgetObj3.start_y, widgetObj3.end_x, widgetObj3.end_y, radius=20, fill=(0, 0, 0, 180))
#         return ImageTk.PhotoImage(overlay_img), ImageTk.PhotoImage(overlay_img_2), ImageTk.PhotoImage(overlay_img_3)
#
#     def frame_by_frame(self):
#         def video_player():
#             ret, frame = self.cap.read()
#             if ret:
#                 frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 frame = Image.fromarray(frame)
#                 photo = ImageTk.PhotoImage(image=frame)
#                 self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
#                 self.canvas.image = photo
#             else:
#                 self.cap.release()
#                 self.destroy()
#                 return
#             self.canvas.delete("overlay")
#
#         def heart_rate_text(heart_rate_rect):
#             text = "HEART RATE"
#             self.canvas.create_text((heart_rate_rect.start_x + heart_rate_rect.end_x - len(text)) // 2,
#                                      (heart_rate_rect.start_y + heart_rate_rect.end_y - len(text)) // 2, text=text, fill="white",
#                                      font=('Helvetica 15 bold'))
#
#         video_player()
#
#         heart_rate_rect = self.Rect(590, 100, 770, 320)
#         progress_rect = self.Rect(590, 30, 770, 90)
#         time_rect = self.Rect(10, 10, 190, 50)
#
#         overlay_photo, overlay_photo_2, overlay_photo_3 = self.create_overlay_widgets(heart_rate_rect, progress_rect, time_rect)
#         self.canvas.create_image(0, 0, anchor=tk.NW, image=overlay_photo, tags="overlay")
#         self.canvas.create_image(0, 0, anchor=tk.NW, image=overlay_photo_2, tags="overlay")
#         self.canvas.create_image(0, 0, anchor=tk.NW, image=overlay_photo_3, tags="overlay")
#
#         self.canvas.overlay_photo = overlay_photo
#         self.canvas.overlay_photo_2 = overlay_photo_2
#         self.canvas.overlay_photo_3 = overlay_photo_3
#
#         heart_rate_text(heart_rate_rect)
#         self.after(int(1000 / self.video_fps), self.frame_by_frame)  # Adjust the delay according to the frame rate
#
#     def button_clicked(self):
#         print("Button clicked!")  # Change this to perform your desired action
#
#     def run_vr(self):
#         app = VideoOverlayApp()
#         app.frame_by_frame()
#         app.mainloop()
