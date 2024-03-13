'''Configuration'''

'''TIMINGS '''
pulsebeat = 0.04
time_delay_seconds = 0.05
time_calibrate = 0.1

HOST="192.168.0.11"
PORT=65432

index = 1

state = {
	1: "OK",
	0: "ERROR"
}

keyboard = {
    "w": index,   #move_forward
    "s": index + 1,   #move_backward
    "a": index + 2,   #tank_turn_left
    "d": index + 3,   #tanl_turn_right
    "q": index + 4,   #wheel_turn_left
    "e": index + 5,   #wheel_turn_right
    "1": index + 6,   #cam_down
    "2": index + 7,   #cam_up
    "u": index + 8,   #man1_up
    "h": index + 9,   #man1_down
    "i": index + 10,  #man2_up
    "j": index + 11,  #man2_down
    "o": index + 12,  #man3_up
    "k": index + 13,  #man3_down
    "p": index + 14,  #man4_up
    "l": index + 15,  #man4_down
    "x": index + 16,  #speed_increase
    "z": index + 17,  #speed_deacrease
    "r": index + 18,  #reset
    "v": index + 19,  #lamp_on
    "b": index + 20,  #lamp_off
    "t": index + 21,  #romb_wheel
}

servoName = {
	"wheel1": 0,
	"wheel2": 1,
	"wheel3": 2,
	"wheel4": 3,
	"cam":    4,
	"man1":   5,
	"man2":   6,
	"man3":   7,
	"man4":   8
}
