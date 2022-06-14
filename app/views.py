import threading, time
from app import app
from flask import render_template, request, send_file
import os
from appointment.work import FacilityBooking

app.config['UPLOAD_FOLDER'] = 'app/static/csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        csvfile = request.files['csvfile']
        print(csvfile)
        if csvfile.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], csvfile.filename)
            print("file path: ", filepath)
            csvfile.save(filepath)
    return render_template("index.html")

@app.route('/run', methods = ['GET'])
def run():
    print("run view")
    bot = FacilityBooking()
    bot.run()
    # while True:
    #     active_thread = threading.active_count()
    #     print("active thread: ", active_thread)
    #
    #     if active_thread < 4:
    #         bot.run()
    #         # You are tired, now sleep for 30 seconds.
    #         time.sleep(30)
    #     else:
    #         print("Some process is running, so wait 1 minute and try again...")
    #         time.sleep(60)

    return "bot is running"

