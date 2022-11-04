import json
import mongoengine as  me
import random
import time

from flask import Flask, request, jsonify, render_template
from flask_mongoengine import MongoEngine
from walkingpad import walkingpad

db = None

#Create Init
def create_app(test_config=None):
    app = Flask(__name__)
    app.register_blueprint(walkingpad, url_prefix='/api/')

    #Mongodb Setting
    app.config['MONGODB_SETTINGS'] = {
        "db": "healingpod",
        "host": "127.0.0.1",
        "port": 27017
    }

    db = MongoEngine(app)

    return app

APP = create_app()


# @app.route('/')
# def index():
#     return render_template('index.html', title='Welcome', username="Kotemon")


# @app.route('/admin')
# def admin_home():
#     patients = Patient.objects()
#     return render_template('/admin/index.html', patients=patients)

# @app.route('/admin/monitoring')
# def admin_monitoring():
#     args = request.args
#     patient_id = args.get('id')

#     return render_template('/admin/monitoring.html', patient=patient_id)

# @app.route('/admin/mtest')
# def admin_monitoring_test():
#     args = request.args
#     patient_id = args.get('id')

#     return render_template('/admin/monitoring-test.html', patient=patient_id)

# @app.route('/patient/register', methods=['GET'])
# def patient_register():
#     return render_template('register.html')

# @app.route('/api/heartrate/_rand', methods=['GET'])
# def api_rand_heartrate():
#     return jsonify(result=random.randint(80, 140))

# @app.route('/api/patient/register', methods=['POST'])
# def api_patient_register():
#     fname = request.form.get("name")
#     fphone = request.form.get("phone")
#     fage = request.form.get("age")

    
#     patient = Patient(
#         name=fname, 
#         phone=fphone,
#         age=fage
#         )

#     patient.save()
#     return jsonify(patient.to_json())



# @app.route('/api/patient/list', methods=['GET'])
# def api_patient_list():
#     # record = json.loads(request.data)
    
#     # patient = Patient(name=record['name'], email=record['email'])
#     # patient.save()
#     patients = Patient.objects()
#     return jsonify(patients)


# class Patient(me.Document):
#     name = me.StringField(required=True)
#     phone = me.StringField()
#     age = me.IntField()
#     address = me.StringField()
#     disability = me.StringField()

#     def to_json(self):
#         return {
#             "name" : self.name,
#             "phone" : self.phone,
#             "age" : self.age
#         }


#main 
if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=8081, processes=1, threaded=False)
    APP.run(debug=True)


