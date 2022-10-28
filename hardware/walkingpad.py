import time import logging from flask import Flask, request, jsonify
from ph4_walkingpad import pad
from ph4_walkingpad.pad import WalkingPad, Controller
from ph4_walkingpad.utils import setup_logging
import asyncio
import yaml
from datetime import date

app = Flask(__name__)

# minimal_cmd_space does not exist in the version we use from pip, thus we define it here.
# This should be removed once we can take it from the controller
minimal_cmd_space = 0.69

log = setup_logging()
pad.logger = log
ctler = Controller()

last_status = {
    "steps": None,
    "distance": None,
    "time": None
}


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
    

async def remote_treadmill(treadmill_status): 
    if (treadmill_status == "" or treadmill_status == "stop") :
        # await finish_walk() 
        await setSpeedManual(0)
        print("Treadmill turn OFF ... ")
    elif (treadmill_status == "start") :
        # await setSpeed(5)
        await start_walk() 
        # print("Treadmill turn ON ... ")
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
async def api_phase():
    args = request.args
    phase_num = args.get("num", default=0, type=int)
    treadmill = args.get("tm", default="", type=str)

    if phase_num < 1:
        print("Undefined phase " + str(phase_num))
        return "Undefined phase. Must be higher than 1"

    print("... Initiating Phase " + str(phase_num))

    # Gather Apples
    if phase_num == 1:
        if (treadmill == "start"):
            # countdown(2, "Starting Treadmill..")
            await remote_treadmill(treadmill) 
            print("Waiting walking stop ..")
        elif(treadmill == "stop"):
            # countdown(5, "Stopping Treadmill..")
            await remote_treadmill(treadmill)
        else:
            print("Unrecognized Treadmill Commands..")


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
            # countdown(5, "Starting Treadmill..")
            await remote_treadmill(treadmill) 
            print("Waiting walking stop ..")
        elif(treadmill == "stop"):
            # countdown(5, "Stopping Treadmill..")
            await remote_treadmill(treadmill)
        else:
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
            # countdown(5, "Starting Treadmill..")
            await remote_treadmill(treadmill) 
            print("Waiting walking stop ..")
        elif(treadmill == "stop"):
            # countdown(5, "Stopping Treadmill..")
            await remote_treadmill(treadmill)
        else:
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

def on_new_status(sender, record):

    distance_in_km = record.dist / 100
    print("Received Record:")
    print('Distance: {0}km'.format(distance_in_km))
    print('Time: {0} seconds'.format(record.time))
    print('Steps: {0}'.format(record.steps))

    last_status['steps'] = record.steps
    last_status['distance'] = distance_in_km
    last_status['time'] = record.time



def load_config():
    with open("config.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def save_config(config):
    with open('config.yaml', 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)


async def connect():
    address = load_config()['address']
    print("Connecting to {0}".format(address))
    await ctler.run(address)
    await asyncio.sleep(minimal_cmd_space)


async def disconnect():
    await ctler.disconnect()
    await asyncio.sleep(minimal_cmd_space)


@app.route("/config/address", methods=['GET'])
def get_config_address():
    config = load_config()
    return str(config['address']), 200


@app.route("/config/address", methods=['POST'])
def set_config_address():
    address = request.args.get('address')
    config = load_config()
    config['address'] = address
    save_config(config)

    return get_config_address()


@app.route("/mode", methods=['GET'])
async def get_pad_mode():
    try:
        await connect()

        await ctler.ask_stats()
        await asyncio.sleep(minimal_cmd_space)
        stats = ctler.last_status
        mode = stats.manual_mode

        if (mode == WalkingPad.MODE_STANDBY):
            return "standby"
        elif (mode == WalkingPad.MODE_MANUAL):
            return "manual"
        elif (mode == WalkingPad.MODE_AUTOMAT):
            return "auto"
        else:
            return "Mode {0} not supported".format(mode), 400
    finally:
        await disconnect()

    return "Error", 500

@app.route("/mode", methods=['POST'])
async def change_pad_mode():
    new_mode = request.args.get('new_mode')
    print("Got mode {0}".format(new_mode))

    if (new_mode.lower() == "standby"):
        pad_mode = WalkingPad.MODE_STANDBY
    elif (new_mode.lower() == "manual"):
        pad_mode = WalkingPad.MODE_MANUAL
    elif (new_mode.lower() == "auto"):
        pad_mode = WalkingPad.MODE_AUTOMAT
    else:
        return "Mode {0} not supported".format(new_mode), 400

    try:
        await connect()

        await ctler.switch_mode(pad_mode)
        await asyncio.sleep(minimal_cmd_space)
    finally:
        await disconnect()

    return new_mode

@app.route("/status", methods=['GET'])
async def get_status():
    try:
        await connect()

        await ctler.ask_stats()
        await asyncio.sleep(minimal_cmd_space)
        stats = ctler.last_status
        mode = stats.manual_mode
        belt_state = stats.belt_state

        if (mode == WalkingPad.MODE_STANDBY):
            mode = "standby"
        elif (mode == WalkingPad.MODE_MANUAL):
            mode = "manual"
        elif (mode == WalkingPad.MODE_AUTOMAT):
            mode = "auto"

        if (belt_state == 5):
            belt_state = "standby"
        elif (belt_state == 0):
            belt_state = "idle"
        elif (belt_state == 1):
            belt_state = "running"
        elif (belt_state >=7):
            belt_state = "starting"

        dist = stats.dist / 100
        time = stats.time
        steps = stats.steps
        speed = stats.speed / 10

        return { "dist": dist, "time": time, "steps": steps, "speed": speed, "belt_state": belt_state }
    finally:
        await disconnect()


@app.route("/startwalk", methods=['POST'])
async def start_walk():
    try:
        await connect()
        await ctler.switch_mode(WalkingPad.MODE_STANDBY) # Ensure we start from a known state, since start_belt is actually toggle_belt
        await asyncio.sleep(minimal_cmd_space)
        await ctler.switch_mode(WalkingPad.MODE_MANUAL)
        await asyncio.sleep(minimal_cmd_space)
        await ctler.start_belt()
        await asyncio.sleep(minimal_cmd_space)
        await ctler.change_speed(5)
        await asyncio.sleep(minimal_cmd_space)
        await ctler.ask_hist(0)
        await asyncio.sleep(minimal_cmd_space)
    finally:
        await disconnect()
    return last_status


async def setSpeedManual(speed):
    try:
        await connect()
        await ctler.switch_mode(WalkingPad.MODE_MANUAL)
        await asyncio.sleep(minimal_cmd_space)
        await ctler.change_speed(speed)
        await asyncio.sleep(minimal_cmd_space)
        await ctler.ask_hist(0)
        await asyncio.sleep(minimal_cmd_space)
    finally:
        await disconnect()
    return last_status

@app.route("/set-speed", methods=['POST'])
async def setSpeed():
    try:
        speed = int(request.args.get('speed'))
        # if (speed >= 30): 
        #     speed = 30 
        # elif (speed <= 5): 
        #     speed = 5
        await connect()
        await ctler.switch_mode(WalkingPad.MODE_MANUAL)
        await asyncio.sleep(minimal_cmd_space)
        await ctler.change_speed(speed)
        await asyncio.sleep(minimal_cmd_space)
        await ctler.ask_hist(0)
        await asyncio.sleep(minimal_cmd_space)
    finally:
        await disconnect()
    return last_status


@app.route("/finishwalk", methods=['POST'])
async def finish_walk():
    try:
        await connect()
        await ctler.switch_mode(WalkingPad.MODE_STANDBY)
        await asyncio.sleep(minimal_cmd_space)
        await ctler.ask_hist(0)
        await asyncio.sleep(minimal_cmd_space)
    finally:
        await disconnect()

    return last_status


ctler.handler_last_status = on_new_status

if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=8081, processes=1, threaded=False)