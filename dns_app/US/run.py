from flask import Flask
from datetime import datetime
from pytz import timezone

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'

#webtime potral
@app.route('/time')
def Check_time():
    time = datetime.now(timezone("US/Eastern"))
    
    formatted_time = time.strftime("%Y:%m:%d:%H:%M:%S")
    
    return formatted_time

app.run(host='0.0.0.0',port=8080,debug=True)
