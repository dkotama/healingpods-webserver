import time
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

ac_default = 28
ac_current = ac_default

def reset_state():
    print("RESETTING STATE THANK YOU")


def remote_ac(is_fan_on, degree):
    global ac_current

    if (is_fan_on):
        print("AC FAN ON ... ")
    else:
        print("AC FAN OFF ... ")

    if (degree is not ac_current):
        ac_current = degree 
        print("Turning AC to " + str(degree))
    

def remote_treadmill(treadmill_status): 
    if (treadmill_status == "" or treadmill_status == "stop") :
        print("Treadmill turn OFF ... ")
    elif (treadmill_status == "start") :
        print("Treadmill turn ON ... ")
    else :
        print("Unrecognized Trigger , Treadmill turn OFF ... ")

def countdown(t, title=None):
    if (title):
        print(title)
    
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
      
    if (title):
        print(title + " Finish")
    else :
        print('Finish')

@app.route('/api/phase', methods=['GET'])
def api_phase():
    args = request.args
    phase_num = args.get("num", default=0, type=int)
    treadmill = args.get("tm", default="", type=str)
    turn = args.get("turn", default="", type=str)

    if phase_num < 1:
        print("Undefined phase " + str(phase_num))
        return "Undefined phase. Must be higher than 1"

    print("... Initiating Phase " + str(phase_num))

    # Gather Apples
    if phase_num == 1:
        if (treadmill == "start"):
            countdown(5, "Starting Treadmill..")
            remote_treadmill(treadmill) 
            print("Waiting walking stop ..")
        elif(treadmill == "stop"):
            countdown(5, "Stopping Treadmill..")
            remote_treadmill(treadmill)
        elif(treadmill != ""):
            print("Unrecognized Treadmill Commands..")

        if (turn == "left"):
            print("Turning Left")
        elif(turn == "right"):
            print("Turning Right")


        return jsonify(
            success=True,
            phase=1,
            next_phase=2,
            session_code="00001"
            )

    # Apple Falls
    elif phase_num == 2:
        remote_ac(True, 20) 
        return jsonify(
            success=True,
            phase=2,
            next_phase=3,
            session_code="00001"
        )

    # Walk to gather branches
    elif phase_num == 3:
        if (treadmill == "start"):
            countdown(5, "Starting Treadmill..")
            remote_treadmill(treadmill) 
            print("Waiting walking stop ..")
        elif(treadmill == "stop"):
            countdown(5, "Stopping Treadmill..")
            remote_treadmill(treadmill)
        elif(treadmill != ""):
            print("Unrecognized Treadmill Commands..")

        return jsonify(
            success=True,
            phase=1,
            next_phase=2,
            session_code="00001"
        )


    # Cutscene Ujung Stage 2
    elif phase_num == 4:
        remote_ac(False, 20) 
        return jsonify(
            success=True,
            phase=4,
            next_phase=5,
            session_code="00001"
        )

    # Jalan ke Api unggun
    elif phase_num == 5:
        if (treadmill == "start"):
            countdown(5, "Starting Treadmill..")
            remote_treadmill(treadmill) 
            print("Waiting walking stop ..")
        elif(treadmill == "stop"):
            countdown(5, "Stopping Treadmill..")
            remote_treadmill(treadmill)
        elif(treadmill != ""):
            print("Unrecognized Treadmill Commands..")
            
        return jsonify(
            success=True,
            phase=5,
            next_phase=6,
            session_code="00001"
        )


    # Jalan ke Api unggun 2
    elif phase_num == 6:
        remote_ac(False, 28) 
        return jsonify(
            success=True,
            phase=6,
            next_phase=7,
            session_code="00001"
        )

    # Reset state
    elif phase_num == 7:
        reset_state()
        return jsonify(
            success=True,
            phase=7,
            next_phase=None,
            session_code="00001"
        )
    else:
        return jsonify(
            success=False,
            phase=None,
            next_phase=None,
            session_code=None
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)