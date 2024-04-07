from main import main_run
from datetime import datetime
from input import values
import time

# Run main.py
results, total_running_trains = main_run()


# Get current time
current_time = time.time()
current_time_dt = datetime.fromtimestamp(current_time)

i = 0
j = 0

print(f"Date = {current_time_dt.date()}" )
print(f"Time = {current_time_dt.hour}:{current_time_dt.minute} hs " )
print("---" * 6)
print(f"Line = {values['line']}" )
print("---" * 6)


for res in results:

    if j == total_running_trains+1:
        print("")
        print("More Scheduled Services: ")
        print("")
    j+=1
    
    res = list(res) 
    time_from = res[0]
    time_to = res[1]

    if time_from > current_time_dt:
        if i == 0:

            print('Next Service: ')
            print('')
            
            print(f"From: {values['stop_from']} at {time_from.hour}:{time_from.minute}:{time_from.second}")
            print(f"To: {values['stop_to']} at {time_to.hour}:{time_to.minute}:{time_to.second}")
            i+=1

        elif i == 1:
            
            print("")
            print("More Services: ")
            print("")
            print(f"From: {values['stop_from']} at {time_from.hour}:{time_from.minute}:{time_from.second}")
            print(f"To: {values['stop_to']} at {time_to.hour}:{time_to.minute}:{time_to.second}")
            print("")
            i+=1

        else:
            
            print(f"From: {values['stop_from']} at {time_from.hour}:{time_from.minute}:{time_from.second}")
            print(f"To: {values['stop_to']} at {time_to.hour}:{time_to.minute}:{time_to.second}")
            print("")
                    



