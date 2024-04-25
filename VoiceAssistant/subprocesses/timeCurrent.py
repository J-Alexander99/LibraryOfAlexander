import datetime

# Get the current date and time
current_time = datetime.datetime.now()

# Format and print the time
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
print("Current time:", formatted_time)
