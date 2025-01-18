import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime, timedelta

# File path for saving and loading user data
DATA_FILE = "user_data.json"

# Default user data
default_data = {
    "xp": 0,
    "level": 1,
    "last_reset": None,
    "tasks": {
        "Daily": [{"name": "Morning Exercise", "progress": 0, "repetitions": 1, "xp": 10},
                  {"name": "Read a Chapter", "progress": 0, "repetitions": 1, "xp": 10},
                  {"name": "Drink 8 Glasses of Water", "progress": 3, "repetitions": 8, "xp": 20}],
        "Weekly": [{"name": "Clean the House", "progress": 0, "repetitions": 1, "xp": 50},
                   {"name": "Grocery Shopping", "progress": 0, "repetitions": 1, "xp": 40}],
        "Monthly": [{"name": "Pay Bills", "progress": 1, "repetitions": 1, "xp": 100},
                    {"name": "Organize Closet", "progress": 0, "repetitions": 1, "xp": 80}],
        "Yearly": [{"name": "File Taxes", "progress": 0, "repetitions": 1, "xp": 500},
                   {"name": "Plan Vacation", "progress": 0, "repetitions": 1, "xp": 300}]
    },
    "rewards": [
        {"name": "Coffee Treat", "level": 2, "redeemed": False},
        {"name": "Movie Night", "level": 5, "redeemed": False},
        {"name": "New Game", "level": 10, "redeemed": False}
    ]
}

# Load saved data or use default if file doesn't exist
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
        return data
    else:
        return default_data

# Save user data to a file
def save_data():
    user_data["xp"] = current_xp
    user_data["level"] = current_level
    with open(DATA_FILE, "w") as file:
        json.dump(user_data, file, indent=4)

#reset tasks 
def reset_tasks():
    global user_data, current_xp, current_level
    
    #get data
    now = datetime.now()
    last_reset = datetime.strptime(user_data["last_reset"],"%d/%m/%Y, %H:%M:%S") if user_data["last_reset"] else None
    
    #Daily
    if not last_reset or now.date() > last_reset.date():
        for task in user_data ["tasks"]["Daily"]:
            task["progress"] = 0
    #Weekly
    if not last_reset or now.isocalendar()[1] > last_reset.isocalendar()[1]:
        for task in user_data ["tasks"]["Weekly"]:
            task["progress"] = 0
    #Monthly
    if not last_reset or now.month > last_reset.month or now.year > last_reset.year:
        for task in user_data ["tasks"]["Monthly"]:
            task["progress"] = 0
        #reset xp 
        current_level = 1
        current_xp = 0
        #reset rewards
        for reward in user_data["rewards"]:
            reward["redeemed"] = False
            
    #anchor time/date
    user_data["last_reset"] = now.strftime("%d/%m/%Y, %H:%M:%S")
    save_data()
    
    #update UI
    display_tasks(selected_category)
    update_progress_bar()
    update_rewards()

#check for resets automatically
def check_for_resets():
    reset_tasks()
    root.after(1000, check_for_resets) #loop de loop and pull



# Switch between Tasks and Rewards tabs
def switch_tab(tab):
    if tab == "tasks":
        task_frame.tkraise()
        sidebar.pack(side="left", fill="y")  # Show sidebar
    elif tab == "rewards":
        reward_frame.tkraise()
        sidebar.pack_forget()  # Hide sidebar

# Display tasks for a specific category
def display_tasks(category):
    for widget in task_list_frame.winfo_children():
        widget.destroy()
    for task in task_data[category]:
        if task["progress"] < task["repetitions"]:
            status = f"{task['progress']}/{task['repetitions']}"
        else:
            status = "Complete"
        task_button = tk.Button(
            task_list_frame,
            text=f"{task['name']} | {status}",
            command=lambda t=task: update_task(t),
            anchor="w",
            padx=10,
            pady=5,
            bg="#FFC107" if task["progress"] < task["repetitions"] else "#8BC34A",
            fg="black",
            font=("Arial", 12),
            relief="flat"
        )
        task_button.pack(fill="x", pady=2)

# Update task progress
def update_task(task):
    if task["progress"] < task["repetitions"]:
        task["progress"] += 1
        if task["progress"] == task["repetitions"]:
            award_xp(task["xp"])
    save_data() #save after each task update
    display_tasks(selected_category)

# Award XP and handle level-up logic
def award_xp(xp):
    global current_xp, current_level
    current_xp += xp
    while current_xp >= xp_needed_for_level(current_level):
        current_xp -= xp_needed_for_level(current_level)
        current_level += 1
    update_progress_bar()
    update_rewards()

# Update the progress bar for XP
def update_progress_bar():
    level_label.config(text=f"Level {current_level}")
    xp_progress['value'] = current_xp
    xp_progress['maximum'] = xp_needed_for_level(current_level)

# XP required for next level
def xp_needed_for_level(level):
    return 100 + (level - 1) * 150

# Update rewards display
def update_rewards():
    for widget in reward_list_frame.winfo_children():
        widget.destroy()
    for reward in reward_data:
        if current_level < reward['level']:
            reward_status = "Locked"
            button_bg = "#9E9E9E"
        elif reward['redeemed']:
            reward_status = "Redeemed"
            button_bg = "#9E9E9E"
        else:
            reward_status = "Available"
            button_bg = "#FF9800"
        reward_button = tk.Button(
            reward_list_frame,
            text=f"{reward['name']} | Level {reward['level']} | {reward_status}",
            command=lambda r=reward: redeem_reward(r),
            anchor="w",
            padx=10,
            pady=5,
            bg=button_bg,
            fg="white",
            font=("Arial", 12),
            relief="flat"
        )
        reward_button.pack(fill="x", pady=2)

# Redeem a reward
def redeem_reward(reward):
    if current_level >= reward['level'] and not reward['redeemed']:
        reward['redeemed'] = True
        update_rewards()
        save_data()

# Initialize variables
user_data = load_data()
current_xp = user_data["xp"]
current_level = user_data["level"]
task_data = user_data["tasks"]
reward_data = user_data["rewards"]
selected_category = "Daily"

# Main window
root = tk.Tk()
root.title("Task Tracker")
root.geometry("600x450")

# Tabs at the top
tabs = ttk.Frame(root)
tabs.pack(side="top", fill="x")
ttk.Button(tabs, text="Tasks", command=lambda: switch_tab("tasks")).pack(side="left")
ttk.Button(tabs, text="Rewards", command=lambda: switch_tab("rewards")).pack(side="left")

# Sidebar for task categories
sidebar = tk.Frame(root, width=120, bg="lightgray")
for cat in ["Daily", "Weekly", "Monthly", "Yearly"]:
    tk.Button(
        sidebar,
        text=cat,
        command=lambda c=cat: [set_category(c), display_tasks(c)]
    ).pack(fill="x", padx=10, pady=5)

def set_category(category):
    global selected_category
    selected_category = category
    display_tasks(category)
    update_timer()

# Main content area
main_content = tk.Frame(root)
main_content.pack(side="right", expand=True, fill="both")

# Task tab content
task_frame = tk.Frame(main_content)
task_frame.grid(row=0, column=0, sticky="nsew")

task_list_frame = tk.Frame(task_frame)
task_list_frame.pack(fill="both", expand=True)

# Reward tab content
reward_frame = tk.Frame(main_content)
reward_frame.grid(row=0, column=0, sticky="nsew")
reward_list_frame = tk.Frame(reward_frame)
reward_list_frame.pack(fill="both", expand=True)

# Progress bar for XP
level_label = tk.Label(root, text=f"Level {current_level}", font=("Arial", 14))
level_label.pack(pady=10)
xp_progress = ttk.Progressbar(root, maximum=xp_needed_for_level(current_level), value=current_xp)
xp_progress.pack(fill="x", padx=10, pady=10)

#Countdown timer for each tab
def get_period_end(category):
    now = datetime.now()
    if category == "Daily":
        #Day
        return datetime(now.year, now.month, now.day, 23, 59, 59)
    elif category == "Weekly":
        #Week
        days_until_sunday = (6 - now.weekday()) % 7
        return now + timedelta(days=days_until_sunday, hours=23 - now.hour, minutes= 59 - now.minute, seconds= 59 - now.second)
    elif category == "Monthly":
        #Month
        next_month = now.month % 12 + 1
        year = now.year + (now.month // 12)
        return datetime(year, next_month, 1) - timedelta(seconds = 1)
    elif category == "Yearly":
        #Year
        return datetime(now.year, 12, 31, 23, 59, 59)
    return now

def update_timer():
    now = datetime.now()
    end_time = get_period_end(selected_category)
    remaining_time = end_time - now
    
    countdown_label.config(text=f"Time Remaining: {str(remaining_time).split('.')[0]}")
    root.after(1000, update_timer)


countdown_label = tk.Label(root, text="", font=("Arial", 12))
countdown_label.pack (pady = 5)

# Initialize
switch_tab("rewards")  # Default tab
update_rewards()
check_for_resets()
display_tasks("Daily")

# Save progress regularly
root.after(1000, save_data)
        
root.mainloop()
