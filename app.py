from flask import Flask, render_template, Response, request
from flask_restful import reqparse, abort, Api, Resource
import os, datetime

import psutil, json, logging, time
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)
api = Api(app)

datadir = "data"

class Message(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('namespace', type=str, required=True)
            parser.add_argument('text', type=str, required=True)
            parser.add_argument('task')
            args = parser.parse_args()

            logger = logging.getLogger("Time Rotating Log")
            ns = args['namespace']
            text = args['text']
            clientip = unicode(request.remote_addr)

            #dtstring =  datetime.datetime.now().strftime("%Y_%m_%d")
            # nsdir = datadir + "/" + ns
            # if not os.path.exists(nsdir):
            #     os.makedirs(nsdir)

            # nsdir = nsdir + "/" + "messages-" + dtstring + ".txt" 
            entry = unicode(datetime.datetime.now()) + '  ' + clientip + '  "' + ns + '"  "' + text + '"'
            # f = open(nsdir,'a')
            # f.write(entry + '\n')
            # f.close()

            logger.info(entry)
            return entry, 201
        except TypeError:
            return "Internal Server Error", 500

def event_stream():
    while True:
        message = cal_stats()
        yield 'data: %s\n\n' % json.dumps(message)
        time.sleep(0.01)

def cal_stats():
    stats = {}
    stats["cpu"] = psutil.cpu_percent(interval=1)

    mem = psutil.virtual_memory()
    stats["mem"] = mem.percent

    return stats    

@app.route('/', methods=['GET'])
def show_homepage():
    return render_template("index.html")

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return Response(event_stream(), mimetype="text/event-stream")

api.add_resource(Message, '/message')

def create_timed_rotating_log(path):
    logger = logging.getLogger("Time Rotating Log")
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(path,
                                       when="H",
                                       interval=1,
                                       backupCount=2, 
                                       utc=False)

    #logFormatter = logging.Formatter("%(asctime)  %(message)s")
    #handler.setFormatter( logFormatter )
    logger.addHandler(handler)


if __name__ == '__main__':
    if not os.path.exists(datadir):
        os.makedirs(datadir)

    logFile = datadir + "/" +  "messages.log"
    create_timed_rotating_log(logFile)
    app.run(threaded=True, host='0.0.0.0', debug=True)