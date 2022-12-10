from flask import Flask, request, json, Response, Blueprint
from pymongo import MongoClient
import logging as log
import datetime;

hr = Blueprint('heartrate', __name__)


# @hr.route("/walkingpad")
# def index():
#     return "Walkingpad route"

# app = Flask(__name__)


class FlaskMongo:
    def __init__(self, data):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        self.client = MongoClient("mongodb://127.0.0.1:27017/") 
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        log.info('Reading All Data')
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data):
        log.info('Writing Data')
        response = self.collection.insert_one(data)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def findSessionActive(self):
        log.info('Reading All Data')
        documents = self.collection.find_one({"is_active": True})
        output = {item: documents[item] for item in documents if item != '_id'}
        return output

    def readLatest(self):
        documents = self.collection.find().sort("created_on",-1)
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return {
            "result": int(output[0].get("heart_rate_value"))
        }


@hr.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')


@hr.route('/mongodb', methods=['GET'])
def mongo_read():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = FlaskMongo(data)
    response = obj1.read()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@hr.route('/mongodb', methods=['POST'])
def mongo_write():
    data = request.json
    if data is None or data == {} or 'Document' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = FlaskMongo(data)
    response = obj1.write(data['Document'])
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@hr.route('/heart-rate', methods=['GET'])
def mongo_update_heart_rate():
    dataCollSession = json.loads('{"database":"vr", "collection":"session"}')   
    
    if dataCollSession is None or dataCollSession == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    collectionSession = FlaskMongo(dataCollSession)
    response = collectionSession.findSessionActive()
    
    heartRate = request.args.get('value')
    dataCollHeartRate = json.loads('{"database":"vr", "collection":"heart-rate"}')
    collectionHeartRate = FlaskMongo(dataCollHeartRate)

    dataInsert = json.loads('{"session_id":"", "heart_rate_value":"", "created_on":""}')
    dataInsert["session_id"] = response['session_id']
    dataInsert["heart_rate_value"] = heartRate
    dataInsert["created_on"] = datetime.datetime.now()
    
    response = collectionHeartRate.write(dataInsert)
    
    dataHeartRate = json.loads('{"database":"vr", "collection":"heart-rate"}')
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')



@hr.route('/latest', methods=['GET'])
def mongo_latest():
    dataCollHeartRate = json.loads('{"database":"vr", "collection":"heart-rate"}')
    collectionHeartRate = FlaskMongo(dataCollHeartRate)

    response = collectionHeartRate.readLatest()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')




if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')