"""CASSIE.
A menstruation tracking system with simple gui, that store menstruation history, predict the next possible menstruation, and check for menstruarion regularity.
Thiss program uses customtkinter for much more modern gui approach, allowing a wide variation of features.

Author: Endrea Castillo
"""

#Initializing module needed by the program
import customtkinter as ctk
from tkinter import *
import tkinter.messagebox as msg
from tkcalendar import *
from datetime import datetime, timedelta
from CTkTable import *
import json


#Setting default apperance mode of the app.
ctk.set_appearance_mode("light")

#FILE HANDLING (With the use of JSON, read)
try:
    with open("users-information.json", "r") as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}


#To save users in json file (write)
def save_users():
    with open("users-information.json", "w") as f:
        json.dump(users, f, indent=4)

#To open the application window.
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cassie")
        self.geometry("1020x1080")
        self.minsize(1220, 1080)
        self.maxsize(1920, 1080)

        self.configure(fg_color="#fefae0")

        LoginWindow(self)

#First Window (Login window)
class LoginWindow(ctk.CTkFrame):
    #initialize the window
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill="both", expand=True)

        self.logo_font = ctk.CTkFont(family="Galins", size=35)
        self.logodes_font = ctk.CTkFont(family="Century Gothic", size=14)  
        self.content_font = ctk.CTkFont(family="Century Gothic", size=16)  
        self.header_font = ctk.CTkFont(family="Century Gothic", size=40, weight="bold")

        self.configure(fg_color="transparent")
        self.build_widgets()
        
    #Widgets inside login window
    def build_widgets(self):
        #OVERALL FRAME
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1) #LOGO/HEADER
        self.rowconfigure(1, weight=3) #WELCOME MESSAGE
        self.rowconfigure(2, weight=1) #FOOTER
  

#-------LOGO/HEADER FRAME--------------------
        logo_frame = ctk.CTkFrame(self,
                                  fg_color="transparent")
        logo_frame.grid(row = 0, column = 0)
        
        #logo name
        logo = ctk.CTkLabel(logo_frame, text="CASSIE",
                    font=self.logo_font)
        logo.grid(row = 0,column = 0, sticky ="n")

        #logo description
        logo_description = ctk.CTkLabel(logo_frame, text="Your Period Companion.",
                                        font=self.logodes_font, fg_color= "transparent")
        logo_description.grid(row = 1,column = 0, sticky ="nsew")

#-------WELCOME & LOGIN BOX--------------------
        welcome_login_frame = ctk.CTkFrame(self,
                                     fg_color="#f9e4c5",
                                     border_width=3,
                                     border_color="#1b4436")
        welcome_login_frame.grid(row = 1, column = 0,
                                 padx = 100,
                                 pady = 50)

        welcome_frame = ctk.CTkFrame(welcome_login_frame,
                                     fg_color="transparent")
        welcome_frame.grid(row = 1, column = 0,
                                    padx = 90,
                                    pady = (90, 60))      
        
        #Greetings
        welcome = ctk.CTkLabel(welcome_frame, text="Welcome! I'm Cassie.✦ ݁˖",
                               font=self.header_font, text_color="#283618")
        welcome.grid(row = 0, column = 0, sticky = "nsew", pady = 15)

        #Greetings text
        welcome_message = ctk.CTkLabel(welcome_frame, text="I will help you to go through your mestruation cycle!",
                               font=self.content_font)
        welcome_message.grid(row = 1, column = 0, sticky = "nsew", pady=(5, 25))


#-------LOGIN INFORMATION FRAME----------------
        login_frame = ctk.CTkFrame(welcome_frame,
                                     fg_color="transparent")
        login_frame.grid(row = 2, column = 0,
                                    padx = 25,
                                    pady = 25) 

        username_description = ctk.CTkLabel(login_frame, text="Username:",
                               font=(self.content_font), text_color="#283618")
        username_description.grid(row = 0, column = 0, sticky = "w")

        self.username_entry = ctk.CTkEntry(login_frame,
                                      placeholder_text="Please enter your username...",
                                      placeholder_text_color="grey",
                                      width=500,
                                      height=35,
                                      font=self.logodes_font,
                                      border_color="black",
                                      border_width=1)
        self.username_entry.grid(row = 1, column = 0, sticky = "ew")

        #login & register button
        button_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0)
        #Login Button
        ctk.CTkButton(button_frame, text="Login", command=self.login, font=ctk.CTkFont(weight="bold", size=18), text_color="#fefae0", fg_color="#1b4436").grid(row=0, column=0, padx=10, pady=5)
        #Register Button
        ctk.CTkButton(button_frame, text="Register", command=self.register, font=ctk.CTkFont(weight="bold", size=18), text_color="#fefae0", fg_color="#88a33b").grid(row=0, column=1, padx=10, pady=5)

#-------FOOTER FRAME-----------------------
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column= 0)

        footer_label = ctk.CTkLabel(footer, text="Cassie by Endrea | 2026", font=self.logodes_font)
        footer_label.grid(row =0, column = 0)

    

#FUNCTIONS FOR LoginWindow

    #Function for login | to verify if the user already exists
    def login(self):
        user_name = self.username_entry.get().capitalize() #username

        if user_name in users:
            self.destroy()
            DashboardWindow(self.parent, user_name)
        elif user_name == "":
            msg.showerror("Error", "Please enter your username.")
        else:
            msg.showerror("Error", "Profile does not Exist. Please Register First.")

    #Function for register | to add users
    def register(self):
        register_name = self.username_entry.get().capitalize()

        if register_name == "":
            msg.showerror("Error", "Please enter valid username.")
        elif register_name not in users:
            users[register_name] = {"history": []}
            save_users()
            msg.showinfo("Register", "Registered successfully, Please Login!")
        else:
            msg.showerror("Error", "Already registered. Please Login.")


#SECOND WINDOW (Dashboard)
class DashboardWindow(ctk.CTkFrame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.pack(fill="both", expand=True)
        self.configure(fg_color="#1b4436")

        self.build_widgets()
        self.load_history()

    def build_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1) #LOGO/HEADER
        self.rowconfigure(1, weight=5) #WELCOME MESSAGE
        self.rowconfigure(2, weight=1) #FOOTER

        self.tab_font = ctk.CTkFont(family="Century Gothic", size=18, weight="bold")

#-------HEADER FRAME----------------------
        header_frame = ctk.CTkFrame(self,
                                    fg_color="transparent")
        header_frame.pack_propagate(False)
        header_frame.grid(row=0, column=0, sticky="nsew", pady = (20, 0))
        header_frame.columnconfigure(0, weight=4)
        header_frame.columnconfigure(1, weight=1)


        #WELCOME MESSAGE AND LOGOUT BUTTON
        ctk.CTkLabel(header_frame, text=f"Hello, {self.username}! ── .✦",
          font=("Century Gothic", 50, "bold"), text_color="white").grid(row=0, column=0, padx=(30, 0), pady = 10, sticky="w")
        ctk.CTkButton(header_frame, text="Logout", command=self.logout, font=ctk.CTkFont(weight="bold", size=18), text_color="#fefae0", fg_color="#eb7d00").grid(row=0, column=1, pady=30, padx=(0, 30),  sticky="e")

#-------DASHBOARD (Using Tabview | notebook in ttk)
        dashboard_menu = ctk.CTkTabview(
            self,
            fg_color="#ffffff",          #notebook background
            segmented_button_fg_color="#fefae0",       #tab background
            segmented_button_selected_color="#88a33b", #selected tab color
            segmented_button_selected_hover_color="#ff69b4",
            segmented_button_unselected_color="#5b758c", #unselected tab
            text_color="#FFFFFF",
            anchor="nw",
            border_width= 2,
            border_color="black",
            height=700
        )
        dashboard_menu.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        dashboard_menu._segmented_button.configure(font=self.tab_font)
        dashboard_menu._segmented_button.grid_configure(padx=10, pady=(15, 0), sticky= "ew")
        dashboard_menu._segmented_button.columnconfigure(0, weight=1)

        # Add tabs
        dashboard_menu.add("Record menstruation.")
        dashboard_menu.add("Present menstruation history.")

        # Get the tab frames
        mens_record = dashboard_menu.tab("Record menstruation.")
        history_mens = dashboard_menu.tab("Present menstruation history.")

#-------TAB1 (RECORD, PREDICT, AND CHECK FOR MENSTRUATION)---------------------------------
        mens_record.rowconfigure(0, weight=1) #heading text
        mens_record.rowconfigure(1, weight=1) #info frame
        mens_record.rowconfigure(2, weight=1) #predict space
        mens_record.columnconfigure(0, weight=1)
        mens_record.configure(fg_color="#f9e4c5", border_color="#1b4436")

        heading_record =ctk.CTkFrame(mens_record, fg_color="transparent")
        heading_record.grid(row = 0, 
                        column = 0,
                        padx = 25,
                        pady = 45)
        
        heading =ctk.CTkLabel(heading_record, text="This will serve as your menstruation diary. (๑ᵔ⤙ᵔ๑)\n𓇼 ⋆.˚ 𓆉 𓆝 𓆡⋆.˚ 𓇼",
            font=("Century Gothic", 30, "bold"), text_color="#283618")
        heading.grid(row = 0, column = 0, padx= 40, pady = 25)

        info_frame = ctk.CTkFrame(mens_record,
                                     fg_color="transparent", border_color="#1b4436", border_width=2)
        info_frame.grid(row = 1, 
                        column = 0,
                        padx = 25) 
        
        #DATE
        date_description = ctk.CTkLabel(info_frame, text="Please input menstruation date:",
            font=("Century Gothic", 15, "bold"))
        date_description.grid(row=1, column=0, padx=60,  pady=55, sticky="w")

        self.date_entry = DateEntry(info_frame,
                                    width=50,
                                    font=("Century Gothic", 14))
        self.date_entry.grid(row=1, column=1, padx= 55, pady=30, sticky="w")

        #SYMPTOMS
        symptoms_description = ctk.CTkLabel(info_frame, text="Please enter your symptoms:",
            font=("Century Gothic", 15, "bold"))
        symptoms_description.grid(row=2, column=0, padx=60, pady=(0, 30), sticky="w")

        self.symptoms_entry = ctk.CTkEntry(info_frame,
                                      placeholder_text="Please enter your symptopms...",
                                      placeholder_text_color="grey",
                                      width=350,
                                      height=35,
                                      font=("Century Gothic", 14),
                                      border_color="black",
                                      border_width=1)
        self.symptoms_entry.grid(row=2, column=1, padx=55, pady=(0, 30), sticky="w")

        #BUTTON (SAVE ENTRY)
        ctk.CTkButton(info_frame, 
                      text="Submit Entry", 
                      command=self.submit_date, 
                      font=ctk.CTkFont(weight="bold", size=18), 
                      text_color="#fefae0", 
                      fg_color="#88a33b",
                      border_color="#1b4436",
                      border_width=1).grid(row=2, column=1, padx=60, pady=5, sticky = "ne")
        
        #PREDICT SECTION
        menstruation_check = ctk.CTkFrame(mens_record, fg_color= "transparent")
        menstruation_check.grid(row = 2, column = 0)
        menstruation_check.rowconfigure(0, weight=1)
        menstruation_check.rowconfigure(1, weight=1)
        menstruation_check.columnconfigure(0, weight=1)
        menstruation_check.columnconfigure(1, weight=1)

        
        ctk.CTkLabel(menstruation_check,text="Check your next menstruation here:",
            font=("Century Gothic", 15, "bold")).grid(row= 0, column = 0)

        self.predict_textbox = ctk.CTkTextbox( menstruation_check,
                                            width=500,
                                            height=100,
                                            font=("Century Gothic", 14),
                                            border_width=1,
                                            border_color="black",
                                            fg_color="#ffffff",
                                            text_color="#1b4436",
                                            state="disabled")
        self.predict_textbox.grid(row=1, column=0, padx=25, pady=(0, 25))

        ctk.CTkButton( menstruation_check,
                    text="Predict Next Period",
                    command=self.predict_menstruation,
                    font=ctk.CTkFont(weight="bold", size=18),
                    text_color="#fefae0",
                    fg_color="#88a33b",
                    border_color="#1b4436",
                    border_width=1).grid(row=1, column=0, pady=(30, 10), sticky = "s")
        
        #REGULARITY SECTION
        ctk.CTkLabel(menstruation_check,text="Check your menstruation state here:",
            font=("Century Gothic", 15, "bold")).grid(row= 0, column = 1)

        self.regularity_textbox = ctk.CTkTextbox( menstruation_check,
                                            width=500,
                                            height=100,
                                            font=("Century Gothic", 14),
                                            border_width=1,
                                            border_color="black",
                                            fg_color="#ffffff",
                                            text_color="#1b4436",
                                            state="disabled")
        self.regularity_textbox.grid(row=1, column=1, padx=25, pady=(0, 25), sticky = "n")

        ctk.CTkButton( menstruation_check,
                    text="Regularity Check",
                    command=self.regularity_check,
                    font=ctk.CTkFont(weight="bold", size=18),
                    text_color="#fefae0",
                    fg_color="#88a33b",
                    border_color="#1b4436",
                    border_width=2).grid(row=1, column=1, pady=(30, 10), sticky = "s")
      
        #TAB 2 (History)
        history_mens.rowconfigure(0, weight=1)
        history_mens.rowconfigure(1, weight=1)
        history_mens.columnconfigure(0, weight=1)
        history_mens.configure(fg_color="#f9e4c5", border_color="#1b4436")

        # Header label
        ctk.CTkLabel(history_mens, text="Menstruation History⸜(｡˃ ᵕ ˂)⸝♡\n❁✿❀❁✿❀",
                    font=("Century Gothic", 45, "bold"),
                    text_color="#1b4436").grid(row=0, column=0, pady=(10, 5))

        #Scrollable frame for multiple entries
        table_frame = ctk.CTkScrollableFrame(history_mens,
                                            fg_color="transparent")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 25))

        # Initial table with just headers
        self.history_table = CTkTable(table_frame,
                                    row=1,
                                    column=3,
                                    values=[["Date", "Symptoms", "Cycle Length (days)"]],
                                    header_color="#88a33b",
                                    text_color="#1b4436",
                                    font=("Century Gothic", 18, "bold"),
                                    border_width=1,
                                    border_color="black",
                                    width=250)
        self.history_table.pack(fill="both", expand=True)


#FUNCTION FOR DASHBOARD WINDOW

    #Logout button | upper right
    def logout(self):
        self.destroy()
        LoginWindow(self.parent)

    
    #First button in tab 1
    def submit_date(self): 
        date = self.date_entry.get_date().strftime("%Y-%m-%d")
        symptoms = self.symptoms_entry.get()
        history = users[self.username]["history"]

        current_date = datetime.strptime(date, "%Y-%m-%d")

        #Check for duplicate date
        if any(entry["Date"] == date for entry in history):
            msg.showerror("Error", "This date has already been recorded.")
            return  

        #Find the closest previous date
        past_dates = [datetime.strptime(e["Date"], "%Y-%m-%d") for e in history if datetime.strptime(e["Date"], "%Y-%m-%d") < current_date]
        
        if past_dates:
            nearest_past = max(past_dates)
            cycle_length = (current_date - nearest_past).days
        else:
            cycle_length = None  # No previous date found

        #Also update the cycle length of the next entry if it exists
        history.append({
            "Date": date,
            "Symptoms": symptoms,
            "Cycle Length": cycle_length
        })

        #Re-sort history and recalculate all cycle lengths, when user input unsorted dates
        history.sort(key=lambda e: e["Date"])
        for i, entry in enumerate(history):
            if i == 0:
                entry["Cycle Length"] = None
            else:
                prev_date = datetime.strptime(history[i - 1]["Date"], "%Y-%m-%d")
                curr_date = datetime.strptime(entry["Date"], "%Y-%m-%d")
                entry["Cycle Length"] = (curr_date - prev_date).days

        save_users()
        msg.showinfo("Successful", "Successfully Recorded")
        self.load_history()

    #Tab 1 | Button in left
    def predict_menstruation(self):
        history = users[self.username].get("history", [])

        #Need to have 2 dates to have computation
        if len(history) < 2:
            self.predict_textbox.configure(state="normal")
            self.predict_textbox.delete("1.0", "end")
            self.predict_textbox.insert("end", "Not enough data to predict. Record at least 2 periods.")
            self.predict_textbox.configure(state="disabled")
            return

        #Dates are sorted to avoid negative days
        dates = sorted([datetime.strptime(e["Date"], "%Y-%m-%d") for e in history])
        gaps = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
        avg_cycle = sum(gaps) / len(gaps)
        next_period = dates[-1] + timedelta(days=avg_cycle)

        #Saving prediction date
        users[self.username]["prediction"] = {
            "Next Expected Period": next_period.strftime("%B %d %Y")
        }
        save_users()
        self.load_history()

        self.predict_textbox.configure(state="normal")
        self.predict_textbox.delete("1.0", "end")
        self.predict_textbox.insert("end", f"Average cycle length : {avg_cycle:.1f} days\n")
        self.predict_textbox.insert("end", f"Next expected period : {next_period.strftime('%B %d, %Y')}")
        self.predict_textbox.configure(state="disabled")

    def regularity_check(self):
        history = users[self.username].get("history", [])

        #Need to have 2 dates to have computation
        if len(history) < 2:
            self.regularity_textbox.configure(state="normal")
            self.regularity_textbox.delete("1.0", "end")
            self.regularity_textbox.insert("end", "Not enough data to Check Regularity. Record at least 2 periods.")
            self.regularity_textbox.configure(state="disabled")
            return

        dates = sorted([datetime.strptime(e["Date"], "%Y-%m-%d") for e in history])
        gaps = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
        avg = sum(gaps) / len(gaps)
        regular = all(abs(g - avg) <= 7 for g in gaps)

        #To know the number of days in between periods
        for i, gap in enumerate(gaps):
            from_month = dates[i].strftime("%B %Y")      #example: January 2025
            to_month = dates[i+1].strftime("%B %Y")      #example: February 2025
            self.regularity_textbox.configure(state="normal")
            self.regularity_textbox.delete("1.0", "end")
            self.regularity_textbox.insert("end", f"{from_month} → {to_month} : {gap} days")
            self.regularity_textbox.configure(state="disabled")

        self.regularity_textbox.configure(state="normal")
        self.regularity_textbox.delete("1.0", "end")
        self.regularity_textbox.insert("end", f"Average : {avg:.1f} days\n")
        self.regularity_textbox.insert("end", "Status  : Regular ✓" if regular else "Status  : Irregular ✗")
        self.regularity_textbox.configure(state="disabled")

    #Tab 2 (Showing the history)
    def load_history(self):
        history = users[self.username].get("history", [])
        sorted_history = sorted(history, key=lambda e: e["Date"])

        #table
        values = [["Date", "Symptoms", "Cycle Length (days)"]] #Header
        for entry in sorted_history:
            cycle = entry["Cycle Length"] if entry["Cycle Length"] is not None else "N/A" #N/A for earliest input
            values.append([entry["Date"], entry["Symptoms"], cycle])

        self.history_table.destroy()
        self.history_table = CTkTable(self.history_table.master,
                                    row=len(values),
                                    column=3,
                                    values=values,
                                    header_color="#88a33b",
                                    text_color="#1b4436",
                                    font=("Century Gothic", 13, "bold"),
                                    border_width=1,
                                    border_color="black",
                                    width=250)
        self.history_table.pack(fill="both", expand=True)
        
        
#To run the app
if __name__ == "__main__":
    app = App()
    app.mainloop()