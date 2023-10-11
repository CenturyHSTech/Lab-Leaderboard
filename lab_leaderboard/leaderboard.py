"""This is the script that will perform all the checks on day and time
and determine how much time is left in a class based on our schedule.

It will also change the background color based on whether students can
use a hall pass or not"""

# imports
import time

# define functions
def get_time():
    time.sleep(0.5)
    currentTime = time.gmtime()
    print(currentTime)

while True:
    get_time()

if __name__ == "__main__":
    print("Here's where we'll test our code.")
