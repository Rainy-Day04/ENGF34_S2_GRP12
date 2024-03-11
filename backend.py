import time
import random
from datetime import datetime
import sqlite3
from sqlite3 import Error
# this is to demo the behavior of a pedometer, should use another thread to run it
class Pedometer:
    def __init__(self):
        self.step_count = 0
    # for testing ONLY!!!
    def add_steps(self, steps):
        self.step_count+=steps

    def reset_steps(self):
        self.step_count=0

    def get_step_count(self):
        return self.step_count
    
    def dummy_walker(self): # dummy walker, add 1 step every ? second
        while True:
            self.add_steps(1)
            sleep_time=0
            if random.random()<0.5:
                sleep_time = random.random()*1
            time.sleep(1+sleep_time) 
# this is to demo the behavior of a heart rate sensor, should use another thread to run it    
class Heart_rate:
    def  __init__(self):
        self.heart_rate=0
    
    def get_heart_rate(self):
        return self.heart_rate   
    def dummy_heart_rate  (self):
        while True:
            self.heart_rate = random.randint(60, 100) # random heart rate between 60 and 100
            time.sleep(1)

# the database uses id as the primary key, and date as the secondary key to do operations on the current steps and target steps    
class Database1:
    def __init__(self, db):
        self.con = None   
        try:
            self.con = sqlite3.connect(db)
            self.cur = self.con.cursor()
            self.cur.execute("CREATE TABLE IF NOT EXISTS data (ID, date, steps, target, target_achieved)")
        except Error as error_msg:
            print(error_msg)
    
    #used to init when a day starts
    def init_day(self, ID, date):
        self.cur.execute("INSERT INTO data(ID, date, steps, target, target_achieved) VALUES (?, ?, ?, ?,?)",  (ID,date, 0, 0, False))
        self.con.commit()
    
    # get data from the database use indexing
    def get_day_data(self, ID, date):
        self.cur.execute("SELECT * FROM data WHERE ID=? AND date=?", (ID, date,))
        return self.cur.fetchone()
    
    # reset all data of the day back to 0, use of development only
    def reset_day_data(self, date):
        self.cur.execute("UPDATE data SET steps=0 , target=0, target_achieved=False WHERE  date=?",  (date,))
        self.con.commit()
        if self.cur.rowcount == 0:
            return False
        else:
            return True
    # reset all data of one patient, one day back to 0
    def reset_day_data_one_person(self, ID, date):
        self.cur.execute("UPDATE data SET steps=0 , target=0, target_achieved=False WHERE  ID=? AND date=?",  (ID, date))
        self.con.commit()
        if self.cur.rowcount == 0:
            return False
        else:
            return True
    # if False ,error in code
    def update_day_data(self,  ID, date, steps, target):
        index=True
        try:
            self.cur.execute("UPDATE data SET steps=?, target=?, target_achieved=? WHERE  ID=? AND date=?", (steps, target, steps>=target, ID, date))
            self.con.commit()
        except Error as error_msg:
            print(error_msg)
            return False
        
    # used for clear the dattabase table
    def reset_all_data(self):
        self.cur.execute("DELETE FROM data")
        self.con.commit()
    
    # please close the database after use!
    def close(self):
        self.con.close()

    def drop_table(self): # used for debugging only, DO NOT USE IT!
        self.cur.execute("DROP TABLE IF EXISTS data")
        self.con.commit()  

# THIS IS TO STORE DATA FROM THE PATIENT, WHICH ADDS FUTUIRE ABILITY TO CONNECT TO FHIR DATABSE
class Patientinfo:

    def __init__(self, db):
        self.con = None   
        try:
            self.con = sqlite3.connect(db)
            self.cur = self.con.cursor()
            self.cur.execute("CREATE TABLE IF NOT EXISTS PATIENTINFO (ID, first, last)")
        except Error as error_msg:
            print(error_msg)

    def add_patient(self, ID, first, last):
        self.cur.execute("INSERT INTO PATIENTINFO(ID, first, last)  VALUES  (?, ?, ?)", (ID, first, last))
        self.con.commit()

    # get all the patient info USING ID AS INDEX
    def get_patient(self, ID):
        self.cur.execute("SELECT * FROM PATIENTINFO WHERE  ID=?", (ID,))
        return self.cur.fetchone()
    
    #DELETE THE PATIENT USING ID AS INDEX
    def delete_patient(self, ID):
        self.cur.execute("DELETE FROM PATIENTINFO WHERE  ID=?", (ID,))
        self.con.commit()
    # PLEASE CLOSE THE DATABASE AFTER USE!!!!!!
    def close(self):    
        self.con.close()
    # used for clear the dattabase table
    def reset_all_data(self):
        self.cur.execute("DELETE FROM PATIENTINFO")
        self.con.commit()
    # used for debugging only, DO NOT USE IT!！！！！！
    def drop_table(self):
        self.cur.execute("DROP TABLE IF EXISTS PATIENTINFO")
        self.con.commit()

#This is used to transfer the date into which day it is in a week
class front_end_calendar:
    def __init__(self,date):
        self.date = date
        self.week=self.datetime.strptime(date, "%d-%m-%Y")

    def get_week(self,date):
        self.week=self.datetime.strptime(date, "%d-%m-%Y")
        self.day=self.week.weekday()
        return self.day
