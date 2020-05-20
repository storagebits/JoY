#!/usr/bin/env python

import evdev
import mido
import time
import dbus
import dbus.mainloop.glib
import gobject
from optparse import OptionParser
 
proxSensorsVal=[0,0,0,0,0]
actualSpeed=0
 
def Braitenberg():
    #get the values of the sensors
    network.GetVariable("thymio-II", "prox.horizontal",reply_handler=get_variables_reply,error_handler=get_variables_error)
 
    #print the proximity sensors value in the terminal
    print proxSensorsVal[0],proxSensorsVal[1],proxSensorsVal[2],proxSensorsVal[3],proxSensorsVal[4]
 
    #Parameters of the Braitenberg, to give weight to each wheels
    leftWheel=[-0.01,-0.005,-0.0001,0.006,0.015]
    rightWheel=[0.012,+0.007,-0.0002,-0.0055,-0.011]
 
    #Braitenberg algorithm
    totalLeft=0
    totalRight=0
    for i in range(5):
         totalLeft=totalLeft+(proxSensorsVal[i]*leftWheel[i])
         totalRight=totalRight+(proxSensorsVal[i]*rightWheel[i])
 
    #add a constant speed to each wheels so the robot moves always forward
    totalRight=totalRight+50
    totalLeft=totalLeft+50
 
    #print in terminal the values that is sent to each motor
    print "totalLeft"
    print totalLeft
    print "totalRight"
    print totalRight
 
    #send motor value to the robot
    network.SetVariable("thymio-II", "motor.left.target", [totalLeft])
    network.SetVariable("thymio-II", "motor.right.target", [totalRight])    
 
    return True
 
def get_variables_reply(r):
    global proxSensorsVal
    proxSensorsVal[0]=r[0]
    print proxSensorVal[0]
 
def get_variables_error(e):
    print 'error:'
    print str(e)
    loop.quit()
 
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-s", "--system", action="store_true", dest="system", default=False,help="use the system bus instead of the session bus")
 
    (options, args) = parser.parse_args()
 
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
 
    if options.system:
        bus = dbus.SystemBus()
    else:
        bus = dbus.SessionBus()
 
    #Create Aseba network 
    network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
    
    #print in the terminal the name of each Aseba NOde
    print network.GetNodesList()
    #network.SetVariable("thymio-II", "motor.left.target", [20])
    #network.SetVariable("thymio-II", "motor.right.target",[20]) 
    #time.sleep(5)
    #network.SetVariable("thymio-II", "motor.left.target", [0])
    #network.SetVariable("thymio-II", "motor.right.target",[0]) 

    #devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    #for device in devices:
        #print(device.fn, device.name, device.phys)

    device = evdev.InputDevice("/dev/input/event3")
    #print(device)
    for event in device.read_loop(): 
        
        #print("speed")
        #print(actualSpeed)

        #print(event) 
 	if event.type == evdev.ecodes.EV_KEY:
		print(evdev.categorize(event))
                #print(event.code)
                #print(event.value)

        if event.code == 103 and event.value == 1:
            # on avance
            if actualSpeed < 0:
                actualSpeed=abs(actualSpeed)
            else:
                actualSpeed=actualSpeed+20
        if event.code == 108 and event.value == 1:
            # on recule
            if actualSpeed > 0:
                actualSpeed=(0-actualSpeed)
            else:
                actualSpeed=actualSpeed-20
        if event.code == 28 and event.value == 1:
            # on s'arrete
            actualSpeed=0
      
        print("Actual speed")
        print(actualSpeed)
        # send speed to robot
        if event.code == 105 and event.value == 1:
            # on tourne a gauche
	    network.SetVariable("thymio-II", "motor.left.target", [0])    
            network.SetVariable("thymio-II", "motor.right.target",[actualSpeed])
        elif event.code == 106 and event.value == 1:
            # on tourne a droite
	    network.SetVariable("thymio-II", "motor.left.target", [actualSpeed])
            network.SetVariable("thymio-II", "motor.right.target",[0])
        else:
            # ligne droite avant ou arriere
	    network.SetVariable("thymio-II", "motor.left.target", [actualSpeed])
            network.SetVariable("thymio-II", "motor.right.target",[actualSpeed])

    # midi loop
    #with mido.open_input("Launch Control XL MIDI 1") as inport:
    #	for msg in inport:
		# accelerator has been pushed
#		if(msg.control == 77):
#			speed = msg.value
#        		print(speed)
			# send motor value to the robot
    			#network.SetVariable("thymio-II", "motor.left.target", [totalLeft])
    			#network.SetVariable("thymio-II", "motor.right.target", [totalRight]) 
 
    #GObject loop
    #print 'starting loop'
    #loop = gobject.MainLoop()
    #call the callback of Braitenberg algorithm
    #handle = gobject.timeout_add (100, Braitenberg) #every 0.1 sec
    #loop.run()
