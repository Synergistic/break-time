import time
import winsound #Need alternative for osx
#from AppKit import NSBeep
import sys #to exit
import webbrowser #for url launching


"""This was my first ever Python program :)"""

def print_time(): #function to print current time with a border
    print "=============================================="
    print "=== Current Time: " + str(time.ctime()) + " ==="
    print "=============================================="
def print_breaktime(): #function to print current time with a border
    print "============================================"
    print "=== Break Time: " + str(time.ctime(work_time)) + " ==="
    print "============================================"
def store_user_worktime(): #work time input, checks for valid answer and makes int
    loop = 1
    while loop == 1:
        print "Cool beans. How long do you want to work for? In minutes please:"
        input1 = raw_input("")
        if input1.isdigit() and input1 != '0': #make sure its not a letter or space
            user_wmin_int = int(input1)
            loop = loop - 1
        elif input1 == '0':
            print "We should try to do SOME work."
        else: #if it is valid, make it an int and end the loop
           print "Try again." 
    return user_wmin_int
def store_user_breaktime(): #break time input, checks for valid answer and makes int
    loop = 1
    while loop == 1:
        print "Okay, how long do you want to break for? minutes:"
        input2 = raw_input("")
        if input2.isdigit() and input2 != '0': #check for num & not zero
            user_bmin_int = int(input2)
            loop = loop - 1
        elif input2 == '0':
            print "Well that would defeat the purpose, wouldn't it?"
        else: #if it is valid, make it an int and end the loop
            print "Try again."
    return user_bmin_int
def alarm(): #alarm function, asks about start/end alarms & returns
    print "Would you like an alarm for the start of your break?"
    alarm_start = alarms()
    print "How about one at the end of your break?"
    alarm_end = alarms()
    return [alarm_start,alarm_end]
def alarms(): #loop answer check for answer
    looper = 1
    while looper == 1:
        alarm_answer = raw_input("")
        if alarm_answer == "y" or alarm_answer == "yes" or alarm_answer == "yeah":
            alarm = 1
            looper -= 1
        elif alarm_answer == "no" or alarm_answer == "n" or alarm_answer == "nope":
            alarm = 0
            looper -= 1
        else:
            print "Sorry, I didn't understand your answer"
    return alarm

def timer_mode(): #prints the menu and stores the mode/break quantity
    loop = 1
    while loop == 1:
        print "(1)Single Break (2)Repeating Breaks"
        print "(3)More Info    (4)Exit"
        user_mode = raw_input("Enter Selection: ")
        if user_mode == "1":
            mode = 1
            break_quantity = 1
            loop = 0
        elif user_mode == "2":
            subloop = 1
            while subloop == 1:
                print "How many breaks?"
                break_quantity = raw_input("")
                if break_quantity.isdigit() and break_quantity != '0':
                    mode = 2
                    loop = 0
                    subloop = 0
                else:
                    print "Try again."
        elif user_mode == "3":
            webbrowser.open('http://www.aicr.org/learn-more-about-cancer/make-time-break-time.html')
        elif user_mode == "4":
            print "Farewell!"
            sys.exit()
        else:
            print "Sorry, I didn't understand your answer."
    return [mode,int(break_quantity)]
print".  . .-. . . .-.   .-. .-. .  . .-."
print"|\/| |-| |<  |-     |   |  |\/| |- "
print"'  ` ` ' ' ` `-'    '  `-' '  ` `-'"
print"              .-. .-. .-."
print"              |-  | | |( "
print"              '   `-' ' '"
print".-. .-. .-. .-. . .   .-. .-. .  . .-."
print"|(  |(  |-  |-| |<     |   |  |\/| |- "
print"`-' ' ' `-' ` ' ' `    '  `-' '  ` `-'"
print"======================================"
print"|  If you sit at a computer all day  |"
print"|taking frequent breaks is important |"
print"|for your longterm health. AICR found|"
print"|  that moving frequently is key to  |"
print"|lower your risk of cancer. Suggested|"
print"|times are 10m breaks/50m work, but  |"
print"|         try what you'd like!       |"
print"|                                    |"
print"|      Make Time For Break Time      |"
print"|       by Cinderous                 |"
print"======================================"
main_loop = 1
while main_loop > 0:
    mode = timer_mode()
    print_time() 
    user_wmin = store_user_worktime() #prompt user for desired work and break time
    user_bmin = store_user_breaktime()
    alarm = alarm()
    user_wsec = user_wmin * 60 #work minutes -> seconds
    user_bsec = user_bmin * 60 #break minutes -> seconds
    if mode[0] == 1 or mode[0] == 2:
        while mode[1] > 0:
            work_time = time.time() + user_wsec #determine end time for work
            print_breaktime()
            wdiv = ((float(user_wmin)/4.0)) #convert min to float & divide by update intervals(4)
            bdiv = ((float(user_bmin)/4.0))
            remain = user_wmin
            while remain >0: #prints updates with time remaining until break/4
                print str(remain) + " minute(s) until your next break."
                time.sleep(user_wsec/4)
                remain = remain - wdiv
                if remain == 0:
                    print "~~~~~~~~~~~~~~Break time!~~~~~~~~~~~~~~"
                    if alarm[0] == 1:
                        winsound.Beep(600,550)#windows
                        #NSBeep()
                    raw_input('Ready? Press Enter to start your break.')
                    break_remain = user_bmin
                    while break_remain >0: #print updates with remaining time/4
                        print str(break_remain) + " more minute(s) of chillaxin'."
                        time.sleep(user_bsec/4)
                        break_remain = break_remain - bdiv
                        if break_remain == 0:
                            if alarm[1] == 1:
                                winsound.Beep(600,550)#windows
                                #NSBeep()
                            raw_input("Break over, get back to work! (Enter to continue)")
                            mode[1] = mode[1] - 1
                            print"======================================"
