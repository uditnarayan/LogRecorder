from flask import Flask, render_template, Response, request
from flask_restful import reqparse, abort, Api, Resource
import os, datetime

import psutil, json, logging, time
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)
api = Api(app)

datadir = "data"
counter = 0
window = [0,0,0,0,0]

class Message(Resource):
    def post(self):
        try:
            global counter, datadir

            parser = reqparse.RequestParser()
            parser.add_argument('namespace', type=str, required=True)
            parser.add_argument('text', type=str, required=True)
            parser.add_argument('task')
            args = parser.parse_args()

            # logger = logging.getLogger("LogRecorder_App")
            ns = args['namespace']
            text = args['text']
            clientip = unicode(request.remote_addr)
            dtime = datetime.datetime.now()
            dtstring =  dtime.strftime("%Y-%m-%d")

            # nsdir = datadir + "/" + ns
            # if not os.path.exists(nsdir):
            #     os.makedirs(nsdir)

            # nsdir = nsdir + "/" + "messages-" + dtstring + ".txt" 
            file = datadir + "/" + "messages-" + dtstring + ".log" 
            entry = unicode(dtime) + '  ' + clientip + '  "' + ns + '"  "' + text + '"'
            f = open(file,'a')
            f.write(entry + '\n')
            f.close()

            # logger.info(entry)
            counter = counter + 1
            return entry, 201
        except TypeError:
            return "Internal Server Error", 500
        except NameError:
            return "Internal Server Error", 500

class Messages(Resource):
    def get(self):

        file_list = os.listdir(datadir)

        if len(file_list) > 0:
            full_list = [os.path.join(datadir,i) for i in file_list]
            # time_sorted_list = sorted(file_list, key=os.path.getmtime)

            flist = []
            for file in full_list:
                mtime = os.path.getmtime(file)
                rec = {}
                rec["file"] = file
                rec["date"] = unicode(datetime.datetime.fromtimestamp(mtime))
                flist.append(rec)

            return json.dumps(flist), 200
        else:
            return json.dumps([]), 200

def event_stream():
    while True:
        message = cal_stats()
        yield 'data: %s\n\n' % json.dumps(message)
        time.sleep(1)

def cal_stats():
    global window, counter

    stats = {}
    # CPU
    stats["cpu"] = psutil.cpu_percent(interval=1)

    # Memory
    mem = psutil.virtual_memory()
    stats["mem"] = mem.percent

    # Request per second calculated over last 10 seconds
    window.pop()
    window.insert(0, counter)
    counter = 0
    rps = 0
    for num in window:
        rps = rps + num
    stats['rps'] = rps / 5
    return stats    

@app.route('/', methods=['GET'])
def show_homepage():
    return render_template("index.html")

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return Response(event_stream(), mimetype="text/event-stream")

api.add_resource(Message, '/message')
api.add_resource(Messages, '/messages')

# def create_timed_rotating_log(path):
#     logger = logging.getLogger("LogRecorder_App")
#     logger.setLevel(logging.INFO)
#     handler = TimedRotatingFileHandler(path,
#                                        when="M",
#                                        interval=1,
#                                        backupCount=1, 
#                                        utc=False)
#     logger.addHandler(handler)


if __name__ == '__main__':
    if not os.path.exists(datadir):
        os.makedirs(datadir)

    #logFile = datadir + "/" +  "messages.log"
    #create_timed_rotating_log(logFile)
    app.run(threaded=True, host='0.0.0.0', debug=True)