from datetime import datetime, timedelta
import json

try:
    with open("users-info.json", "r") as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}

def save_users():
    with open("users-info.json", "w") as f:
        json.dump(users, f, indent=4)

def record(user_name):
    print("=" *50)
    date = input("\nEnter date (YYYY-MM-DD): ")
    symptoms = input("Enter symptoms: ")

    history = users[user_name]["history"]

    # Calculate cycle length from last record
    if history:
        last_date = datetime.strptime(history[-1]["Date"], "%Y-%m-%d")
        current_date = datetime.strptime(date, "%Y-%m-%d")
        cycle_length = (current_date - last_date).days
    else:
        cycle_length = None  # First record, no previous date

    history.append({
        "Date": date,
        "Symptoms": symptoms,
        "Cycle Length": cycle_length  # ← saved here
    })

    save_users()
    print("Record saved successfully.")
    print("-" *50)

def view_history(user_name):
    history = users[user_name]["history"]
    print("=" *50)
    print("Menstruation History")
    print("-" *50)
    if not history:
        print("No records yet.")

    sorted_history = sorted(history, key=lambda e: e["Date"])

    for entry in sorted_history:
        print(f"Date: {entry['Date']}")
        print(f"Symptoms: {entry['Symptoms']}")
        print()
    
    print("-" *50)
    prediction = users[user_name].get("prediction")
    if prediction:
         print(f"Next Expected Period : {prediction['Next Expected Period']}")
         print("Date may not be updated. To update go to (2) in Menu Options")
    print()
    print("-" *50)

    print("Returning to menu...")
    
def predict_next_period(user_name):
    history = users[user_name]["history"]
    if len(history) < 2:
        print("Not enough data to predict. Record at least 2 periods.")
        return
    dates = sorted([datetime.strptime(e["Date"], "%Y-%m-%d") for e in history])
    gaps = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
    avg_cycle = sum(gaps) / len(gaps)
    next_period = dates[-1] + timedelta(days=avg_cycle)
    print(f"Average cycle length : {avg_cycle:.1f} days")
    print(f"Next expected period : {next_period.strftime('%Y-%m-%d')}")

    users[user_name]["prediction"] = {
        "Next Expected Period": next_period.strftime("%B %d %Y")  # ← convert to string
    }
    save_users()

def check_regularity(user_name):
    history = users[user_name]["history"]
    if len(history) < 2:
        print("Not enough data to check regularity.")
        return
    dates = sorted([datetime.strptime(e["Date"], "%Y-%m-%d") for e in history])
    gaps = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
    avg = sum(gaps) / len(gaps)
    regular = all(abs(g - avg) <= 7 for g in gaps)

    print("=" * 50)
    print("Cycle Regularity Check")
    print("-" * 50)
    for i, gap in enumerate(gaps):
        from_month = dates[i].strftime("%B %Y")      # e.g. January 2025
        to_month = dates[i+1].strftime("%B %Y")      # e.g. February 2025
        print(f"{from_month} → {to_month} : {gap} days")

    print("-" * 50)
    print(f"Average : {avg:.1f} days")
    print("Status  : Regular ✓" if regular else "Status  : Irregular ✗")
    print("=" * 50)

def menu_options():
    print()
    print("=" *50)
    print("Select Menu Options")
    print("-" *50)
    print("(1) Record a menstruation.")
    print("(2) Predict for next menstruation.")
    print("(3) Check for menstruation regularity.")
    print("(4) Present menstruation history.")
    print("(5) Exit.")
    menu_choice = input("\nMenu Choice: ")
    print()
    return menu_choice
    
while True:
    print("=" *50)
    print("MENSTRUAL CYCLE TRACKING AND PREDICTION SYSTEM")
    print("=" *50)
    print("(1) Login.")
    print("(2) Register.")
    print("(3) Exit.")
    main_choice = input("\nSelect Action: ")
    print()
    
    if main_choice == "1":
        print("=" *50)
        print("Welcome!")
        user_name = input("Enter username: ").capitalize()
        if user_name in users:
            print("Login sucessfully.")
            while True:
                menu_choice = menu_options()
                if menu_choice == "1":
                    record(user_name)
                elif menu_choice == "2":
                    predict_next_period(user_name)
                elif menu_choice == "3":
                    check_regularity(user_name)
                elif menu_choice == "4":
                   view_history(user_name)
                elif menu_choice =="5":
                    print("Returning to menu...")
                    break
                else:
                    print("Invalid choice")
        else:
            print("\nProfile does not Exist. Please Register First.\n")

    elif main_choice == "2":
        print("=" *50)
        print("Welcome! Please enter your name.")
        register_name = input("Enter username: ").capitalize()

        if register_name not in users:
            users[register_name] = {"history": []}
            print(f"\n{register_name} is successfully registered. Please Login.")
            save_users()
        else:
            print("\nAlready registered. Please Login.")
    elif main_choice == "3":
        print("Thank you for using the system!")
        break
    else:
        print("Invalid Choice.")
    print("-" *50)




    





