def start():
    print "\nThe journey begins."
    print  
    while(1):
        prompt = raw_input('''Type "start":\n''')
        prompt = prompt.lower()   
        try:
            if prompt == 'start':
                wake_up()
                break;
            elif prompt == 'begin':
                print '''Type 'start'. Not the brightest, are you?'''
            else:
                print '''That's not an option. Type "start" '''
        except ValueError:
            print ""
    
def wake_up():
    print '''You wake up feeling dizzy. What happened? You think to yourself. The past few days is a blur. \nPlaying table tennis with alcohol.\nNaming plastic cups after royalty. \nWatching too much Netflix...'''
    print

    while(1):
        prompt = raw_input('''Will you "sit up" or just "lay there"?\n''')
        prompt = prompt.lower()
        try:
            if prompt == "sit up":
                sit_up()
            elif prompt == 'lay there':
                lay_there()
            else:
                wake_up()
        except ValueError:
            print ""

def sit_up():
    print '''You sit up'''

def lay_there():
    print '''You lie in your pool of metaphorical filth and contemplate your broken dreams.'''
    
start()
