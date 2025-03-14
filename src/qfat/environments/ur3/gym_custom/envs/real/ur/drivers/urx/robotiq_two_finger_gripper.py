"""
Python library to control Robotiq Two Finger Gripper connected to UR robot via Python-URX

Tested using a UR5 Version CB3 and Robotiq 2-Finger Gripper Version 85

SETUP

You must install the driver first (http://support.robotiq.com/pages/viewpage.action?pageId=5963876) and then power on the gripper from the gripper UI

FAQ

Why does this class group all the commands together and run them as a single program as opposed to running each line seperately (like most of URX)?

- The gripper is controlled by connecting to the robot's computer (TCP/IP) and then communicating with the gripper via a socket (127.0.0.1:63352).  The scope of the socket is at the program level.  It will be automatically closed whenever a program finishes.  Therefore it's important that we run all commands as a single program.

DOCUMENTATION

- This code was developed by downloading the "gripper package" on http://support.robotiq.com/pages/viewpage.action?pageId=5963876
- Open folder "robotiq_2f_gripper_programs_CB3"
- robotiq_2f_gripper_programs_CB3/advanced_template_test.script was referenced to create this class

Future Features

- Though I haven't developed it yet if you look in robotiq_2f_gripper_programs_CB3/advanced_template_test.script and view function "rq_get_var" there is an example of how to determine the current state of the gripper and if it's holding an object.
"""

import logging


class Robotiq_Two_Finger_Gripper(object):
    complete_program = ""
    header = "def myProg():" + "\n"
    end = "\n" + "end"
    logger = False

    def __init__(
        self,
        robot=None,
        payload=0.85,
        speed=255,
        force=255,
        socket_host="192.168.5.101",
        socket_name="gripper_socket",
    ):
        self.logger = logging.getLogger("urx")

        # TODO : modify code to use below kwargs in add_line_to_program()
        self.payload = payload
        self.speed = speed
        self.force = force
        self.socket_host = socket_host
        self.socket_port = 63352
        self.socket_name = socket_name

        self.reset()

    def reset(self):
        self.complete_program = ""
        self.add_line_to_program("  set_analog_inputrange(0, 0)")
        self.add_line_to_program("  set_analog_inputrange(1, 0)")
        self.add_line_to_program("  set_analog_inputrange(2, 0)")
        self.add_line_to_program("  set_analog_inputrange(3, 0)")
        self.add_line_to_program("  set_analog_outputdomain(0, 0)")
        self.add_line_to_program("  set_analog_outputdomain(1, 0)")
        self.add_line_to_program("  set_tool_voltage(0)")
        self.add_line_to_program("  set_runstate_outputs([])")
        self.add_line_to_program(
            "  set_payload(0.85)"
        )  # 0.85 is the weight of the gripper in KG

        self.add_line_to_program("  ")

        self.add_line_to_program("  #aliases for the gripper variable names")
        self.add_line_to_program("  ACT = 1")
        self.add_line_to_program("  GTO = 2")
        self.add_line_to_program("  ATR = 3")
        self.add_line_to_program("  ARD = 4")
        self.add_line_to_program("  FOR = 5")
        self.add_line_to_program("  SPE = 6")
        self.add_line_to_program("  OBJ = 7")
        self.add_line_to_program("  STA = 8")
        self.add_line_to_program("  FLT = 9")
        self.add_line_to_program("  POS = 10")
        self.add_line_to_program("  PRE = 11")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_init_connection(gripper_sid=9, gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program(
            '  socket_open("%s",%s, gripper_socket)'
            % (self.socket_host, self.socket_port)
        )
        self.add_line_to_program(
            '  socket_set_var("SID", gripper_sid,  gripper_socket)'
        )
        self.add_line_to_program("  ack = socket_read_byte_list(3, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program('  def rq_activate(gripper_socket="gripper_socket"):')
        self.add_line_to_program("  rq_gripper_act = 0")
        self.add_line_to_program("  rq_set_var(ACT,1, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_activate_and_wait(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  rq_activate(gripper_socket)")
        self.add_line_to_program("  ")
        self.add_line_to_program(
            "  while(not rq_is_gripper_activated(gripper_socket)):"
        )
        self.add_line_to_program("  # wait for activation completed")
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program('  def rq_stop(gripper_socket="gripper_socket"):')
        self.add_line_to_program("  rq_set_var(GTO,0, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program('  def rq_reset(gripper_socket="gripper_socket"):')
        self.add_line_to_program("  rq_gripper_act = 0")
        self.add_line_to_program("  rq_obj_detect = 0")
        self.add_line_to_program("  rq_mov_complete = 0")
        self.add_line_to_program("  ")
        self.add_line_to_program("  rq_set_var(ACT,0, gripper_socket)")
        self.add_line_to_program("  rq_set_var(ATR,0, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_auto_release_open_and_wait(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  ")
        self.add_line_to_program("  rq_set_var(ARD,0, gripper_socket)")
        self.add_line_to_program("  rq_set_var(ACT,1, gripper_socket)")
        self.add_line_to_program("  rq_set_var(ATR,1, gripper_socket)")
        self.add_line_to_program("  ")
        self.add_line_to_program("  gFLT = rq_get_var(FLT, 2, gripper_socket)")
        self.add_line_to_program("  ")
        self.add_line_to_program("  while(not is_FLT_autorelease_completed(gFLT)):")
        self.add_line_to_program("  gFLT = rq_get_var(FLT, 2, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_auto_release_close_and_wait(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  rq_set_var(ARD,1, gripper_socket)")
        self.add_line_to_program("  rq_set_var(ACT,1, gripper_socket)")
        self.add_line_to_program("  rq_set_var(ATR,1, gripper_socket)")
        self.add_line_to_program("  ")
        self.add_line_to_program("  gFLT = rq_get_var(FLT, 2, gripper_socket)")
        self.add_line_to_program("  ")
        self.add_line_to_program("  while(not is_FLT_autorelease_completed(gFLT)):")
        self.add_line_to_program("  gFLT = rq_get_var(FLT, 2, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_set_force(force, gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  rq_set_var(FOR,force, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_set_speed(speed, gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  rq_set_var(SPE,speed, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program('  def rq_open(gripper_socket="gripper_socket"):')
        self.add_line_to_program("  rq_move(0, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program('  def rq_close(gripper_socket="gripper_socket"):')
        self.add_line_to_program("  rq_move(255, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_open_and_wait(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  rq_move_and_wait(0, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_close_and_wait(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  rq_move_and_wait(255, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program('  def rq_move(pos, gripper_socket="gripper_socket"):')
        self.add_line_to_program("  rq_mov_complete = 0")
        self.add_line_to_program("  rq_obj_detect = 0")
        self.add_line_to_program("  ")
        self.add_line_to_program("  rq_set_pos(pos, gripper_socket)")
        self.add_line_to_program("  rq_go_to(gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_move_and_wait(pos, gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  rq_move(pos, gripper_socket)")
        self.add_line_to_program("  ")
        self.add_line_to_program("  while (not rq_is_motion_complete(gripper_socket)):")
        self.add_line_to_program("  # wait for motion completed")
        self.add_line_to_program("  sleep(0.01)")
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program(
            "  # following code used for compatibility with previous versions"
        )
        self.add_line_to_program("  rq_is_object_detected(gripper_socket)")
        self.add_line_to_program("  ")
        self.add_line_to_program("  if (rq_obj_detect != 1):")
        self.add_line_to_program("  rq_mov_complete = 1")
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program('  def rq_go_to(gripper_socket="gripper_socket"):')
        self.add_line_to_program("  rq_set_var(GTO,1, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # reset the rGTO to prevent movement and")
        self.add_line_to_program("  # set the position")

        self.add_line_to_program(
            '  def rq_set_pos(pos, gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  rq_set_var(GTO,0, gripper_socket)")
        self.add_line_to_program("  ")
        self.add_line_to_program("  rq_set_var(POS, pos, gripper_socket)")
        self.add_line_to_program("  ")
        self.add_line_to_program("  gPRE = rq_get_var(PRE, 3, gripper_socket)")
        self.add_line_to_program(
            "  pre = (gPRE[1] - 48)*100 + (gPRE[2] -48)*10 + gPRE[3] - 48"
        )
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  while (pre != pos):")
        self.add_line_to_program("  rq_set_var(POS, pos, gripper_socket)")
        self.add_line_to_program("  gPRE = rq_get_var(PRE, 3, gripper_socket)")
        self.add_line_to_program(
            "  pre = (gPRE[1] - 48)*100 + (gPRE[2] -48)*10 + gPRE[3] - 48"
        )
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_is_motion_complete(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  rq_mov_complete = 0")
        self.add_line_to_program("  ")
        self.add_line_to_program("  gOBJ = rq_get_var(OBJ, 1, gripper_socket)")
        self.add_line_to_program("  sleep(0.01)")
        self.add_line_to_program("  ")
        self.add_line_to_program("  if (is_OBJ_gripper_at_position(gOBJ)):")
        self.add_line_to_program("  rq_mov_complete = 1")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  if (is_OBJ_object_detected(gOBJ)):")
        self.add_line_to_program("  rq_mov_complete = 1")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  ")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_is_gripper_activated(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  gSTA = rq_get_var(STA, 1, gripper_socket)")
        self.add_line_to_program("  ")
        self.add_line_to_program("  if(is_STA_gripper_activated(gSTA)):")
        self.add_line_to_program("  rq_gripper_act = 1")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  else:")
        self.add_line_to_program("  rq_gripper_act = 0")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_is_object_detected(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  gOBJ = rq_get_var(OBJ, 1, gripper_socket)")
        self.add_line_to_program("  ")
        self.add_line_to_program("  if(is_OBJ_object_detected(gOBJ)):")
        self.add_line_to_program("  rq_obj_detect = 1")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  else:")
        self.add_line_to_program("  rq_obj_detect = 0")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_current_pos(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program('  rq_pos = socket_get_var("POS",gripper_socket)')
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  return rq_pos")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_print_gripper_fault_code(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  gFLT = rq_get_var(FLT, 2, gripper_socket)")
        self.add_line_to_program("  ")
        self.add_line_to_program("  if(is_FLT_no_fault(gFLT)):")
        self.add_line_to_program('  textmsg("Gripper Fault : ", "No Fault (0x00)")')
        self.add_line_to_program("  elif (is_FLT_action_delayed(gFLT)):")
        self.add_line_to_program(
            '  textmsg("Gripper Fault : ", "Priority Fault: Action delayed, initialization must be completed prior to action (0x05)")'
        )
        self.add_line_to_program("  elif (is_FLT_not_activated(gFLT)):")
        self.add_line_to_program(
            '  textmsg("Gripper Fault : ", "Priority Fault: The activation must be set prior to action (0x07)")'
        )
        self.add_line_to_program("  elif (is_FLT_autorelease_in_progress(gFLT)):")
        self.add_line_to_program(
            '  textmsg("Gripper Fault : ", "Minor Fault: Automatic release in progress (0x0B)")'
        )
        self.add_line_to_program("  elif (is_FLT_overcurrent(gFLT)):")
        self.add_line_to_program(
            '  textmsg("Gripper Fault : ", "Minor Fault: Overcurrent protection tiggered (0x0E)")'
        )
        self.add_line_to_program("  elif (is_FLT_autorelease_completed(gFLT)):")
        self.add_line_to_program(
            '  textmsg("Gripper Fault : ", "Major Fault: Automatic release completed (0x0F)")'
        )
        self.add_line_to_program("  else:")
        self.add_line_to_program('  textmsg("Gripper Fault : ", "Unkwown Fault")')
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program(
            '  def rq_print_gripper_num_cycles(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program('  socket_send_string("GET NCY",gripper_socket)')
        self.add_line_to_program("  sync()")
        self.add_line_to_program(
            "  string_from_server = socket_read_string(gripper_socket)"
        )
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  ")
        self.add_line_to_program('  if(string_from_server == "0"):')
        self.add_line_to_program(
            '  textmsg("Gripper Cycle Number : ", "Number of cycles is unreachable.")'
        )
        self.add_line_to_program("  else:")
        self.add_line_to_program(
            '  textmsg("Gripper Cycle Number : ", string_from_server)'
        )
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program(
            '  def rq_print_gripper_driver_state(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program('  socket_send_string("GET DST",gripper_socket)')
        self.add_line_to_program("  sync()")
        self.add_line_to_program(
            "  string_from_server = socket_read_string(gripper_socket)"
        )
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  ")
        self.add_line_to_program('  if(string_from_server == "0"):')
        self.add_line_to_program(
            '  textmsg("Gripper Driver State : ", "RQ_STATE_INIT")'
        )
        self.add_line_to_program('  elif(string_from_server == "1"):')
        self.add_line_to_program(
            '  textmsg("Gripper Driver State : ", "RQ_STATE_LISTEN")'
        )
        self.add_line_to_program('  elif(string_from_server == "2"):')
        self.add_line_to_program(
            '  textmsg("Gripper Driver State : ", "RQ_STATE_READ_INFO")'
        )
        self.add_line_to_program('  elif(string_from_server == "3"):')
        self.add_line_to_program(
            '  textmsg("Gripper Driver State : ", "RQ_STATE_ACTIVATION")'
        )
        self.add_line_to_program("  else:")
        self.add_line_to_program('  textmsg("Gripper Driver State : ", "RQ_STATE_RUN")')
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program("  def rq_print_gripper_serial_number():")
        self.add_line_to_program('  #socket_send_string("GET SNU",gripper_socket)')
        self.add_line_to_program("  #sync()")
        self.add_line_to_program(
            "  #string_from_server = socket_read_string(gripper_socket)"
        )
        self.add_line_to_program("  #sync()")
        self.add_line_to_program(
            '  #textmsg("Gripper Serial Number : ", string_from_server)'
        )
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program(
            '  def rq_print_gripper_firmware_version(gripper_socket="gripper_socket"):'
        )

        self.add_line_to_program('  socket_send_string("GET FWV",gripper_socket)')
        self.add_line_to_program("  sync()")
        self.add_line_to_program(
            "  string_from_server = socket_read_string(gripper_socket)"
        )
        self.add_line_to_program("  sync()")
        self.add_line_to_program(
            '  textmsg("Gripper Firmware Version : ", string_from_server)'
        )
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program(
            '  def rq_print_gripper_driver_version(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program('  socket_send_string("GET VER",gripper_socket)')
        self.add_line_to_program("  sync()")
        self.add_line_to_program(
            "  string_from_server = socket_read_string(gripper_socket)"
        )
        self.add_line_to_program("  sync()")
        self.add_line_to_program(
            '  textmsg("Gripper Driver Version : ", string_from_server)'
        )
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_print_gripper_probleme_connection(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program('  socket_send_string("GET PCO",gripper_socket)')
        self.add_line_to_program("  sync()")
        self.add_line_to_program(
            "  string_from_server = socket_read_string(gripper_socket)"
        )
        self.add_line_to_program("  sync()")
        self.add_line_to_program('  if (string_from_server == "0"):')
        self.add_line_to_program(
            '  textmsg("Gripper Connection State : ", "No connection problem detected")'
        )
        self.add_line_to_program("  else:")
        self.add_line_to_program(
            '  textmsg("Gripper Connection State : ", "Connection problem detected")'
        )
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program(
            "  # Returns True if list_of_bytes is [3, 'a', 'c', 'k']"
        )

        self.add_line_to_program("  def is_ack(list_of_bytes):")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # list length is not 3")
        self.add_line_to_program("  if (list_of_bytes[0] != 3):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # first byte not is 'a'?")
        self.add_line_to_program("  if (list_of_bytes[1] != 97):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # first byte not is 'c'?")
        self.add_line_to_program("  if (list_of_bytes[2] != 99):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # first byte not is 'k'?")
        self.add_line_to_program("  if (list_of_bytes[3] != 107):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program(
            "  # Returns True if list_of_bytes is not [3, 'a', 'c', 'k']"
        )

        self.add_line_to_program("  def is_not_ack(list_of_bytes):")
        self.add_line_to_program("  if (is_ack(list_of_bytes)):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  else:")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program("  def is_STA_gripper_activated (list_of_bytes):")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # list length is not 1")
        self.add_line_to_program("  if (list_of_bytes[0] != 1):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # byte is '3'?")
        self.add_line_to_program("  if (list_of_bytes[1] == 51):")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            "  # Returns True if list_of_byte is [1, '1'] or [1, '2']"
        )
        self.add_line_to_program("  # Used to test OBJ = 0x1 or OBJ = 0x2")
        self.add_line_to_program("  def is_OBJ_object_detected (list_of_bytes):")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # list length is not 1")
        self.add_line_to_program("  if (list_of_bytes[0] != 1):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # byte is '2'?")
        self.add_line_to_program("  if (list_of_bytes[1] == 50):")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # byte is '1'?")
        self.add_line_to_program("  if (list_of_bytes[1]  == 49):")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  ")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program("  # Returns True if list_of_byte is [1, '3']")
        self.add_line_to_program("  # Used to test OBJ = 0x3")
        self.add_line_to_program("  def is_OBJ_gripper_at_position (list_of_bytes):")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # list length is not 1")
        self.add_line_to_program("  if (list_of_bytes[0] != 1):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # byte is '3'?")
        self.add_line_to_program("  if (list_of_bytes[1] == 51):")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            "  def is_not_OBJ_gripper_at_position (list_of_bytes):"
        )
        self.add_line_to_program("  ")
        self.add_line_to_program("  if (is_OBJ_gripper_at_position(list_of_bytes)):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  else:")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program("  def is_FLT_no_fault(list_of_bytes):")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # list length is not 2")
        self.add_line_to_program("  if (list_of_bytes[0] != 2):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # first byte is '0'?")
        self.add_line_to_program("  if (list_of_bytes[1] != 48):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # second byte is '0'?")
        self.add_line_to_program("  if (list_of_bytes[2] != 48):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  ")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program("  def is_FLT_action_delayed(list_of_bytes):")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # list length is not 2")
        self.add_line_to_program("  if (list_of_bytes[0] != 2):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # first byte is '0'?")
        self.add_line_to_program("  if (list_of_bytes[1] != 48):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # second byte is '5'?")
        self.add_line_to_program("  if (list_of_bytes[2] != 53):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program("  def is_FLT_not_activated(list_of_bytes):")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # list length is not 2")
        self.add_line_to_program("  if (list_of_bytes[0] != 2):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # first byte is '0'?")
        self.add_line_to_program("  if (list_of_bytes[1] != 48):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # second byte is '7'?")
        self.add_line_to_program("  if (list_of_bytes[2] != 55):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program("  def is_FLT_autorelease_in_progress(list_of_bytes):")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # list length is not 2")
        self.add_line_to_program("  if (list_of_bytes[0] != 2):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # first byte is '1'?")
        self.add_line_to_program("  if (list_of_bytes[1] != 49):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # second byte is '1'?")
        self.add_line_to_program("  if (list_of_bytes[2] != 49):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  ")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  def is_FLT_overcurrent(list_of_bytes):")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # list length is not 2")
        self.add_line_to_program("  if (list_of_bytes[0] != 2):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # first byte is '1'?")
        self.add_line_to_program("  if (list_of_bytes[1] != 49):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # second byte is '4'?")
        self.add_line_to_program("  if (list_of_bytes[2] != 52):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  ")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  def is_FLT_autorelease_completed(list_of_bytes):")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # list length is not 2")
        self.add_line_to_program("  if (list_of_bytes[0] != 2):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # first byte is '1'?")
        self.add_line_to_program("  if (list_of_bytes[1] != 49):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  # second byte is '5'?")
        self.add_line_to_program("  if (list_of_bytes[2] != 53):")
        self.add_line_to_program("  return False")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  return True")
        self.add_line_to_program("  ")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program(
            '  def rq_set_var(var_name, var_value, gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  ")
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  if (var_name == ACT):")
        self.add_line_to_program('  socket_set_var("ACT", var_value, gripper_socket)')
        self.add_line_to_program("  elif (var_name == GTO):")
        self.add_line_to_program('  socket_set_var("GTO", var_value, gripper_socket)')
        self.add_line_to_program("  elif (var_name == ATR):")
        self.add_line_to_program('  socket_set_var("ATR", var_value, gripper_socket)')
        self.add_line_to_program("  elif (var_name == ARD):")
        self.add_line_to_program('  socket_set_var("ARD", var_value, gripper_socket)')
        self.add_line_to_program("  elif (var_name == FOR):")
        self.add_line_to_program('  socket_set_var("FOR", var_value, gripper_socket)')
        self.add_line_to_program("  elif (var_name == SPE):")
        self.add_line_to_program('  socket_set_var("SPE", var_value, gripper_socket)')
        self.add_line_to_program("  elif (var_name == POS):")
        self.add_line_to_program('  socket_set_var("POS", var_value, gripper_socket)')
        self.add_line_to_program("  else:")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  ack = socket_read_byte_list(3, gripper_socket)")
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  ")
        self.add_line_to_program("  while(is_not_ack(ack)):")
        self.add_line_to_program("  ")
        self.add_line_to_program('  textmsg("rq_set_var : retry", " ...")')
        self.add_line_to_program('  textmsg("rq_set_var : var_name = ", var_name)')
        self.add_line_to_program('  textmsg("rq_set_var : var_value = ", var_value)')
        self.add_line_to_program("  ")
        self.add_line_to_program("  if (ack[0] != 0):")
        self.add_line_to_program('  textmsg("rq_set_var : invalid ack value = ", ack)')
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program(
            "  socket_set_var(var_name , var_value,gripper_socket)"
        )
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  ack = socket_read_byte_list(3, gripper_socket)")
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  end")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  ")
        self.add_line_to_program(
            '  def rq_get_var(var_name, nbr_bytes, gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  ")
        self.add_line_to_program("  if (var_name == FLT):")
        self.add_line_to_program('  socket_send_string("GET FLT",gripper_socket)')
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  elif (var_name == OBJ):")
        self.add_line_to_program('  socket_send_string("GET OBJ",gripper_socket)')
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  elif (var_name == STA):")
        self.add_line_to_program('  socket_send_string("GET STA",gripper_socket)')
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  elif (var_name == PRE):")
        self.add_line_to_program('  socket_send_string("GET PRE",gripper_socket)')
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  else:")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program(
            "  var_value = socket_read_byte_list(nbr_bytes, gripper_socket)"
        )
        self.add_line_to_program("  sync()")
        self.add_line_to_program("  ")
        self.add_line_to_program("  return var_value")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program("  ############################################")
        self.add_line_to_program("  # normalized functions (maps 0-100 to 0-255)")
        self.add_line_to_program("  ############################################")
        self.add_line_to_program(
            '  def rq_set_force_norm(force_norm, gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  force_gripper = norm_to_gripper(force_norm)")
        self.add_line_to_program("  rq_set_force(force_gripper, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_set_speed_norm(speed_norm, gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  speed_gripper = norm_to_gripper(speed_norm)")
        self.add_line_to_program("  rq_set_speed(speed_gripper, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_move_norm(pos_norm, gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  pos_gripper = norm_to_gripper(pos_norm)")
        self.add_line_to_program("  rq_move(pos_gripper, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_move_and_wait_norm(pos_norm, gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  pos_gripper = norm_to_gripper(pos_norm)")
        self.add_line_to_program("  rq_move_and_wait(pos_gripper, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_set_pos_norm(pos_norm, gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  pos_gripper = norm_to_gripper(pos_norm)")
        self.add_line_to_program("  rq_set_pos(pos_gripper, gripper_socket)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("  ")

        self.add_line_to_program(
            '  def rq_current_pos_norm(gripper_socket="gripper_socket"):'
        )
        self.add_line_to_program("  pos_gripper = rq_current_pos(gripper_socket)")
        self.add_line_to_program("  pos_norm = gripper_to_norm(pos_gripper)")
        self.add_line_to_program("  return pos_norm")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program("  def gripper_to_norm(value_gripper):")
        self.add_line_to_program("  value_norm = (value_gripper / 255) * 100")
        self.add_line_to_program("  return floor(value_norm)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program("  def norm_to_gripper(value_norm):")
        self.add_line_to_program("  value_gripper = (value_norm / 100) * 255")
        self.add_line_to_program("  return ceil(value_gripper)")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")

        self.add_line_to_program("  def rq_get_position():")
        self.add_line_to_program("  return rq_current_pos_norm()")
        self.add_line_to_program("  end")
        self.add_line_to_program("  ")
        self.add_line_to_program("rq_init_connection()")
        self.add_line_to_program("rq_obj_detect = 0 #legacy artifact")

    def reset_gripper(self):
        self.add_line_to_program("rq_reset()")

    def activate_gripper(self):
        self.add_line_to_program("rq_activate_and_wait()")

    def open_gripper(self, wait=True):
        if wait:
            self.add_line_to_program("rq_open_and_wait()")
        else:
            self.add_line_to_program("rq_open()")

    def close_gripper(self, wait=True):
        if wait:
            self.add_line_to_program("rq_close_and_wait()")
        else:
            self.add_line_to_program("rq_close()")

    def get_gripper_position(self):
        raise NotImplementedError
        self.add_line_to_program("rq_get_position()")

    def add_line_to_program(self, new_line):
        if self.complete_program != "":
            self.complete_program += "\n"
        self.complete_program += new_line

    def ret_program_to_run(self):
        if self.complete_program == "":
            self.logger.debug("robotiq_two_finger_gripper's program is empty")
            return ""

        prog = self.header
        prog += self.complete_program
        prog += self.end
        # print(prog)
        return prog
