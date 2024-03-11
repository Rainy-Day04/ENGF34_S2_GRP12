# from backend import User, Patientinfo, Heart_rate, Pedometer, front_end_calendar
# from datetime import datetime, timedelta
#
#
# class HealthAppController:
#     def __init__(self, user_id, view):
#         self.user = User(user_id)
#         self.view = view
#
#
#     def add_steps_and_update(self, user_id, date, steps):
#       self.user.pedometer.add_steps(date, steps)
#       self.update_step_count_view()
#
#     def update_step_count_view(self):
#       new_step_count = self.user.pedometer.get_step_count()
#       self.view.set_current_progress(new_step_count)
#
#
#     def display_heart_rate(self):
#       print(f"current heart rate: {self.user.heart_rate.get_heart_rate()}")
#
#     def init_day_for_user(self, date):
#       self.user.load_day_data(date)
#       print(f"Intialised day data for user with date: {date}")
#
#     def view_day_data(self, date):
#       data = self.user.get_step_count(date)
#       if data:
#         print(f"Day data for date {date}: ID={data[0]}, date={data[1]}, steps={data[2]}, target={data[3]}, Target Achieved={data[4]}")
#       else:
#         print(f"No data found for date {date}")
#
#     def reset_user_day_data(self, date):
#       self.user.reset_day_data_one_person(self.user.ID(), date)
#       print(f"Reset day data for {self.user.ID} on {date}.")
#
#     def compile_weekly_target_achievement(self, date_str):
#         """Compiles target achievement data into a weekly array for the week containing the given date."""
#         start_of_week, end_of_week = self.get_week_range(date_str)
#         target_achievement_array = [None] * 7
#
#         current_date = start_of_week
#         while current_date <= end_of_week:
#             date_formatted = current_date.strftime("%d-%m-%Y")
#             day_data = self.user.get_step_count(date_formatted)
#             day_index = current_date.weekday()  # Monday is 0 and Sunday is 6
#
#             if day_data:
#                 target_achievement_array[day_index] = day_data[4]
#
#
#             current_date += timedelta(days=1)
#
#         return target_achievement_array
#
#
#     def add_patient(self, ID, first, last):
#       self.patient_info_db.add_patient(ID, first, last)
#       print(f"Added patient with ID: {ID}, First Name: {first}, Last Name: {last}")
#
#     def view_patient(self, ID):
#       patient = self.patient_info_db.get_patient(ID)
#       if patient:
#         print(f"Patient with ID: {patient[0]}, First Name: {patient[1]}, Last Name: {patient[2]}")
#       else:
#         print(f"No patient found with ID: {ID}")
#
#
#
#
#
#
#
#
#