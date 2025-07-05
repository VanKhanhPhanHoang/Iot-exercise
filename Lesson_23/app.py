from flask import Flask
import time

app = Flask(__name__)

# Timer variable
timer_running = False
timer_end_time = None

@app.route('/start_timer/<int:seconds>', methods=['POST'])
def start_timer(seconds):
    global timer_running, timer_end_time
    timer_running = True
    timer_end_time = time.time() + seconds
    return "Timer started for {} seconds".format(seconds)

@app.route('/cancel_timer', methods=['POST'])
def cancel_timer():
    global timer_running, timer_end_time
    if timer_running:
        timer_running = False
        timer_end_time = None
        return "Timer has been cancelled."
    else:
        return "No timer running to cancel."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
