# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 15:09:05 2022

@author: Pauline + Alexia

Experiment: Radial adaptation: Gratings

This is the 1st part of the experiment.

This program simply measures the BASELINE RADIAL BIAS

- 1 ecc = 15°

- 4AFC TASK !! 
"""

#%%#   Import packages

from psychopy import core, visual, gui, data, event, monitors, sound
import numpy as np
import pandas as pd
import os
import random

practice = 'no' #whether to do the practice (yes or no)


#%%#  Path stuff

# Print the current working directory
print("Current working directory: {0}".format(os.getcwd()))

# Change the current working directory HERE
#cwd = os.chdir(r'C:\Users\alexi\OneDrive - UCL\Rprojects\2022_RadApt_gratings\...experiment')
cwd = os.chdir(r'C:\Users\humanvisionlab\Documents\dossierpartageubuntu\Pauline\RadApt_gratings\...experiment')


print("Current working directory: {0}".format(os.getcwd()))
cwd = format(os.getcwd())

stimdir = cwd + '\stim\\' #directory where the stimuli are
datadir = cwd + '\data\\' #directory to save data in


#%%#  Open dlg box, Store info about the experiment session 

# Get subject's info through a dialog box
exp_name = 'RadApt_4AFC'
exp_info = {
    'subj_ID': '',
    'session':'',
    }

dlg = gui.DlgFromDict(dictionary = exp_info, title = exp_name) # Open a dialog box
if dlg.OK == False: # If 'Cancel' is pressed, quit
    core.quit()
        
# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name
subj_ID = exp_info['subj_ID']
date = exp_info['date']


#%%#  Define some variables

timelimit = 10 # max time (in s) to wait for a response

eccentricity = "15dva"

# Number of instructions slides
NBinstructions = list(range(4))


# fixation color
neutralColor = (-1, -1, -1)
waitColor = (-0.2, -0.2, -0.2) #for when waiting for a response
OKcolor = (-1, 1, -1) #green
notOKcolor = (1, -1, -1) #red

timer = core.Clock()

# size of instructions images
instrWIDTH = 1600
instrHEIGHT = 900

# size of the adapter + gaussian background
bgSize = 2199 


#%%#  Define parameters of the Gabor stim
gaborSizeDVA = 3
gaborSize15 = 100 # Size in pixels (15° ecc condition)
gaborSFDVA = 4
gaborSF = 0.1320 # Spatial frequency (cycles per pixels)

# Where to present the stim (eccentricity)
left_xpos15 = -502
right_xpos15 = 502
up_ypos15 = 502
down_ypos15 = -502


gaborDuration = 0.25 # Presentation duration

# Contrasts levels, just for the demo/training phase 
contrastLevels = np.around(list(np.arange(0.1,1,0.1)),1)
contrastLevels = contrastLevels.tolist()            
highContrastLevels = np.around(list(np.arange(0.1,0.6,0.025)),2)
highContrastLevels = highContrastLevels.tolist()    
np.random.shuffle(highContrastLevels)
#NB 0 = uniform (no contrast), 1 = maximum contrast


#%%#  Experimental design
eccentricity = ['15dva']
meridians = ['meridianH','meridianV']
Hsides = ['left','right']
Vsides = ['up','down']
gaborOrientations = ['oriH','oriV']

# Create the condition list: 
conditions = [{'VF':'left','ori':'oriH'},
              {'VF':'left','ori':'oriV'},
              {'VF':'right','ori':'oriH'},
              {'VF':'right','ori':'oriV'},
              {'VF':'up','ori':'oriH'},
              {'VF':'up','ori':'oriV'},
              {'VF':'down','ori':'oriH'},
              {'VF':'down','ori':'oriV'}]
  
# training
nCond = len(conditions)
ntrialsPerCond_Training = 5
ntrialsTotal_Training = ntrialsPerCond_Training * nCond

# nb trials...
nStaircaise = len(conditions)  
nTrialsPerStaircase = 100
nTrialsTotal = nTrialsPerStaircase * nStaircaise
# nBlock = len(conditionBlocks)
# nTrialsPerBlock = nTrialsPerStaircase*nBlock #1 block = 1 eccentricity*meridian, i.e. 4 staircases: 2 VF and 2 ori


# Create the trial list that will be followed within each block
triallist = [{'VF':'left','ori':'oriH'},
             {'VF':'left','ori':'oriV'},
             {'VF':'right','ori':'oriH'},
             {'VF':'right','ori':'oriV'},
             {'VF':'up','ori':'oriH'},
             {'VF':'up','ori':'oriV'},
             {'VF':'down','ori':'oriH'},
             {'VF':'down','ori':'oriV'}]
  
for i in range(nTrialsPerStaircase-1):
    condition_template = [{'VF':'left','ori':'oriH'},
                          {'VF':'left','ori':'oriV'},
                          {'VF':'right','ori':'oriH'},
                          {'VF':'right','ori':'oriV'},
                          {'VF':'up','ori':'oriH'},
                          {'VF':'up','ori':'oriV'},
                          {'VF':'down','ori':'oriH'},
                          {'VF':'down','ori':'oriV'}]
    triallist.extend(condition_template)
random.shuffle(triallist)

    
#%%#  Create arrays to append data in # THIS IS FOR TRAINING ONLY SO TO TIDY UP

subject_array = []
exp_name_array = []
date_array = [] 
session_array = []
trainingtest_array = []
trial_array = []
eccentricity_array = []
xPos_array = []
yPos_array = []
meridian_array = []
contrast_array = []
gabor_ori_array = []
VF_array = []
resp_array = []
accuracy_array = []


for n in range(18): #range(ntrialsTotal):
    subject_array.append(subj_ID)
    exp_name_array.append(exp_name)
    date_array.append(exp_info['date'])
    session_array.append(exp_info['session'])
    
    
#%%#  Window object + monitor settings

# Window object = DEBUGGING / TEST XP
# testmon = monitors.Monitor('testmonitor') #on changera ça après avoir mesuré la gamma
# testmon.setSizePix((1920, 1080)) 
# win = visual.Window(monitor = testmon,
#                     color = (-1, -1,-1),
#                     units = 'pix',
#                     fullscr = True,
#                     allowGUI = False)

# Window object = THE REAL ONE, OLED, full screen, no GUI
OLED = monitors.Monitor('testmonitor') #on changera ça après avoir mesuré la gamma
OLED.setSizePix((3840, 2160)) 
win = visual.Window(monitor = OLED,
                    color = (-1, -1,-1),
                    units = 'pix',
                    fullscr = True,
                    allowGUI = False)
win.setMouseVisible(False)
#%%#  Prepare stimuli

# Create the fixation dot
#########################
fixation = visual.Circle(win, units = 'pix', radius = 5,
                          pos = (0,0),
                          fillColor = neutralColor)

# fix = np.ones((20, 20))*(-1)
# fixation = visual.GratingStim(win, tex=fix, mask='gauss', units='pix', size=20)

# 1 - Instructions images
#########################
instructions = visual.ImageStim(win, units = 'pix',
                               pos = (0,0), size = (instrWIDTH,instrHEIGHT)) 

# 2 - Little gabor stimuli
##########################
# Create base object to host the different versions of the gabor stimulus
lilGabor = visual.GratingStim(win, units = 'pix',
                              #color = (0,0,0), #
                              sf = gaborSF, mask = 'gauss')

# 4 - Little Bip sound
######################
bleepf = os.path.join(stimdir + 'blip.wav')
bleep = sound.Sound(value=bleepf) 

# 5 - Gaussian Gray background
##############################
gaussianGrayf = os.path.join(stimdir + 'gaussianGray.bmp') 
gaussianGray = visual.ImageStim(win, image = gaussianGrayf,
                                units = 'pix', pos = (0,0), 
                                size = (bgSize,bgSize))

# 6 - Pause text
################
pause = visual.TextStim(win, color = (-1, -1, -0.5))






#%%#  Define Staircase parameters
ndown = 2 # Nb of correct responses before decreasing the contrast
nup = 1 # Nb of incorrect responses before increasing the contrast
down_step = 0.02
up_step = 0.03
maxContrast = 0.1
goContrast = 0.2



#%%#  Prepare Staircases for the test loop

# initializes some dictionaries used by the staircase() function
thisCond = [] 
contrast_dict = {
    'left_oriH': 0,
    'left_oriV': 0,
    'right_oriH': 0,
    'right_oriV': 0,
    'up_oriH': 0,
    'up_oriV': 0,
    'down_oriH': 0,
    'down_oriV': 0
    }
reversal_dict = {
    'left_oriH': 0,
    'left_oriV': 0,
    'right_oriH': 0,
    'right_oriV': 0,
    'up_oriH': 0,
    'up_oriV': 0,
    'down_oriH': 0,
    'down_oriV': 0
    }
acc_count_dict = {
    'left_oriH': 0,
    'left_oriV': 0,
    'right_oriH': 0,
    'right_oriV': 0,
    'up_oriH': 0,
    'up_oriV': 0,
    'down_oriH': 0,
    'down_oriV': 0
    }
trial_count_dict = {
    'left_oriH': 0,
    'left_oriV': 0,
    'right_oriH': 0,
    'right_oriV': 0,
    'up_oriH': 0,
    'up_oriV': 0,
    'down_oriH': 0,
    'down_oriV': 0
    }


# ###  Define staircase function
def staircase(condition):
    # we need to work with the global variables (so that they can be used 
    # outside of the function)
    global thisCond
    global contrast_dict
    global reversal_dict
    global acc_count_dict
    global trial_count_dict
  

    # 1st trial: set the initial contrast value as the value defined in maxContrast
    if trial_count_dict[thisCond] == 1: 
        contrast_dict[thisCond] = contrast_dict[thisCond] + maxContrast
    
    # From the 2nd trial:
    elif trial_count_dict[thisCond] > 1: 
        
            # if acc = 0 at last trial, increases contrast level
            if acc_count_dict[thisCond] == 0: 
                contrast_dict[thisCond] = abs(contrast_dict[thisCond] + up_step)
            # if acc = 1 at last trial, first time, keep the same contrast level
            elif (acc_count_dict[thisCond] > 0) & (acc_count_dict[thisCond] < ndown): 
                contrast_dict[thisCond] = abs(contrast_dict[thisCond]) 
            # if acc = 1 at last trial, second time, decrease contrast level
            else: # (acc_count_dict[thisCond] == ndown):
                contrast_dict[thisCond] = abs(contrast_dict[thisCond] - down_step)
                acc_count_dict[thisCond] = 0  



#%%#  
#%%#  Begin Experiment

# Draw the windows onto the screen
win.flip()

# %%#   Instructions:
# "Welcome! Adujst the position of the seat..."
# "This experiment aims to study how your brain..."
# "During the experiment, you are requested to fixate..."
# "On some trials, you will see clearly the stimulus... Let's try (horizontal)"

# #=============================================================================
for i in NBinstructions:
    x = i+1
    instr_fname = os.path.join(stimdir + 'instructions' + str(x) + '.bmp')
    instructions.setImage(instr_fname)
    instructions.draw()
    win.flip() 
    event.clearEvents()
    keys = event.waitKeys(keyList=['space', 'q'])
    if 'q' in keys:
        win.close()
        core.quit()
    elif 'space' in keys :
        continue
win.flip(clearBuffer=True)
core.wait(1)


#%%#   Small practice
# Let's try the task on the horizontal meridian, then on the vertical meridian

if practice == 'yes':
    for theMeridian in meridians:
        if theMeridian == "meridianH":
            sides = Hsides
            yPos = 0 # horizontal meridian --> y = 0
        else:
            sides = Vsides
            xPos = 0 # vertical meridian --> x = 0
            
            
        for trial in range(6): # 6 demonstration trials
          
            # Draw fixation
            gaussianGray.draw()
            fixation.color = neutralColor
            fixation.draw()
            win.flip()
            core.wait(2) # wait for 2 sec
        
            # Set gabor position            
            theVF = random.choice(sides) 
            if theVF == 'left':
                xPos = left_xpos15
            elif theVF == 'right':
                xPos = right_xpos15    
            elif theVF == 'up':
                yPos = up_ypos15
            else:
                yPos = down_ypos15
            lilGabor.pos = (xPos,yPos)
        
            # Set gabor orientation
            theOri = random.choice(gaborOrientations)
            if theOri == 'oriH':
                ori = 90
            else:
                ori = 0    
            lilGabor.ori = ori
            
            # Set gabor contrast 
            theContrast = random.choice(contrastLevels)
            lilGabor.contrast = theContrast
            
            # Set gabor size 
            lilGabor.size = gaborSize15
                   
            # Draw stimulus
            gaussianGray.draw()
            lilGabor.draw()
            fixation.draw()
            win.flip()
            core.wait(gaborDuration) 
            gaussianGray.draw()
            fixation.color = waitColor
            fixation.draw()
            win.flip()
            event.clearEvents()
            keys = event.waitKeys(maxWait=timelimit, keyList=['left', 'right', 'up', 'down', 'q'])
        
        
            # If a key is pressed, take the response. If not, just remove the images from the screen    
            if keys:
                resp = keys[0]
                                            
                #At this point, there are still no keys pressed. So "if not keys" is definitely 
                #going to be processed.
                #After removing the images from the screen, still listening for a keypress. 
                #Record the reaction time if a key is pressed.
                                            
            if not keys:
                keys = event.waitKeys(maxWait = timelimit, keyList=['left', 'right', 'up', 'down', 'q'])
                                                
            # If the key is pressed analyze the keypress.
            if keys:
                if 'q' in keys:
                    break
                else:
                    resp = keys[0]
            else: 
                resp = 'noResp'
                
            # Check accuracy
            if resp == theVF:
                acc = 1
            elif resp == 'noResp':
                acc = 0
            else:
                acc = 0
            
            # ISI ... (+ change fixation dot color depending on accuracy)
            if acc == 1:
                accColor = OKcolor
            else:
                accColor = notOKcolor
                
    
            
            gaussianGray.draw()
            fixation.color = accColor
            fixation.draw()
            win.flip()
            core.wait(0.5) # wait for 2 sec
    
    
            # Save info about that trial
            trainingtest_array.append('training')
            trial_array.append(trial)
            eccentricity_array.append('15dva')
            xPos_array.append(xPos)
            yPos_array.append(yPos)
            meridian_array.append(theMeridian)
            contrast_array.append(theContrast)
            gabor_ori_array.append(theOri)
            VF_array.append(theVF)
            resp_array.append(resp)
            accuracy_array.append(acc)
    
    
            # If it is the 6th trial of the demo loop, go to instruction slide
            # "Great, now let's try on the vertical axis"
            if (trial == 5) & (theMeridian == "meridianH"):
                instr_fname = os.path.join(stimdir + 'instructions5.bmp')
                instructions.setImage(instr_fname)
                instructions.draw()
                win.flip() 
                event.clearEvents()
                keys = event.waitKeys(keyList=['space', 'q'])
                if 'q' in keys:
                    win.close()
                    core.quit()
                elif 'space' in keys :
                    continue





# #%%#  Save info about the training phase

# if not os.path.isdir(datadir):
#     os.makedirs(datadir)
# data_fname = 'training_' + exp_name + '_' + exp_info['subj_ID']+ '_session'+ exp_info['session'] + '_' + exp_info['date'] + '.csv'
# data_fname = os.path.join(datadir, data_fname)

# subj_ID = exp_info['subj_ID']
# exp_date = exp_info['date']

# output_file = pd.DataFrame({'subj_ID': subject_array,
#                             'exp_name': exp_name_array,
#                             'date': date_array,
#                             'session': session_array,
#                             'training-test': trainingtest_array,
#                             'trial': trial_array,
#                             'eccentricity': eccentricity_array,
#                             'xPosition': xPos_array,
#                             'yPosition': yPos_array,
#                             'meridian': meridian_array,
#                             'contrast': contrast_array,
#                             'ori': gabor_ori_array,
#                             'VF': VF_array,
#                             'resp': resp_array,
#                             'accuracy': accuracy_array
#                             })

# # save the csv file + pickle

# # CSV file
# output_file.to_csv(data_fname, index = False)

# # # Pickle
# # # with open(data_fname + ".pkl", 'wb') as f:
# # #     pickle.dump(output_file, f, pickle.HIGHEST_PROTOCOL)
# # print('FILES SAVED')






#%%#  Reinitialize output arrays

trainingtest_array = []
trial_array = []
eccentricity_array = []
xPos_array = []
yPos_array = []
meridian_array = []
contrast_array = []
gabor_ori_array = []
VF_array = []
resp_array = []
accuracy_array = []
accCount_array = []
thisCond_array = []
trialCount_array = []
reversal_array = []
contrastRule_array = []



#%%#  Test loop


# instruction: "Now do the task..."
instr_fname = os.path.join(stimdir + 'instructions7.bmp')
instructions.setImage(instr_fname)
instructions.draw()
win.flip() 
event.clearEvents()
keys = event.waitKeys(keyList=['space', 'q'])
if 'q' in keys:
    win.close()
    core.quit()
win.flip() 
            


trial = 0

# Create ZH (='zeHigh') variables for the high contrasts trials    
ZH_left_oriH = 0
ZH_right_oriH = 0
ZH_up_oriH = 0
ZH_down_oriH = 0
ZH_left_oriV = 0
ZH_right_oriV = 0
ZH_up_oriV = 0
ZH_down_oriV = 0
    
    
for thisTrial in range(len(triallist)): 
    trial = trial + 1
    theTrial = triallist[thisTrial]
    theVF = theTrial['VF']
    theOri = theTrial['ori']
    thisCond = theVF + '_' + theOri
    trial_count_dict[thisCond] = trial_count_dict[thisCond] + 1
    gaborSize = (gaborSize15,gaborSize15)
    if (theVF == 'left') or (theVF == 'right'):
        theMeridian = "meridianH"
    else:
        theMeridian  = "meridianV"


    # set gabor position depending on the condition
    if (theVF == 'left'):
        yPos = 0 # horizontal meridian --> y = 0
        xPos = left_xpos15
    elif (theVF == 'right'):
        yPos = 0 # horizontal meridian --> y = 0
        xPos = right_xpos15
    elif (theVF == 'up'):
        xPos = 0 # vertical meridian --> x = 0
        yPos = up_ypos15
    elif (theVF == 'down'):
        xPos = 0 # vertical meridian --> x = 0
        yPos = down_ypos15
    lilGabor.pos = (xPos,yPos)

    # Set gabor orientation
    if theOri == 'oriH':
        ori = 90
    else:
        ori = 0    
    lilGabor.ori = ori
    
    # Set gabor orientation
    lilGabor.size = gaborSize
        
        
    # Set gabor contrast 
    # either pick within higher contrast range
    if (trial_count_dict[thisCond]%5 == 0):

        if theOri == 'oriH':
            if theVF == 'left':
                zecontrast = highContrastLevels[ZH_left_oriH]
                ZH_left_oriH = ZH_left_oriH + 1
                lilGabor.contrast = zecontrast    
            if theVF == 'right':
                zecontrast = highContrastLevels[ZH_right_oriH]
                ZH_right_oriH = ZH_right_oriH + 1
                lilGabor.contrast = zecontrast
            if theVF == 'up':
                zecontrast = highContrastLevels[ZH_up_oriH]
                ZH_up_oriH = ZH_up_oriH + 1
                lilGabor.contrast = zecontrast               
            if theVF == 'down':
                zecontrast = highContrastLevels[ZH_down_oriH]
                ZH_down_oriH = ZH_down_oriH + 1
                lilGabor.contrast = zecontrast
        elif theOri == 'oriV':
            if theVF == 'left':
                zecontrast = highContrastLevels[ZH_left_oriV]
                ZH_left_oriV = ZH_left_oriV + 1
                lilGabor.contrast = zecontrast    
            if theVF == 'right':
                zecontrast = highContrastLevels[ZH_right_oriV]
                ZH_right_oriV = ZH_right_oriV + 1
                lilGabor.contrast = zecontrast
            if theVF == 'up':
                zecontrast = highContrastLevels[ZH_up_oriV]
                ZH_up_oriV = ZH_up_oriV + 1
                lilGabor.contrast = zecontrast               
            if theVF == 'down':
                zecontrast = highContrastLevels[ZH_down_oriV]
                ZH_down_oriV = ZH_down_oriV + 1
                lilGabor.contrast = zecontrast  
                
        contrast_array.append(zecontrast)
        contrastRule_array.append("highCont")  
    
    # or use staircase rules      
    else:
        staircase(thisCond)
        lilGabor.contrast = abs(contrast_dict[thisCond])            
        contrast_array.append(contrast_dict[thisCond])
        contrastRule_array.append("staircase")

    # Draw fixation
    gaussianGray.draw()
    fixation.color = neutralColor
    fixation.draw()
    win.flip()
    core.wait(0.5) # wait for 500ms
        
    # Draw stimulus
    gaussianGray.draw()
    lilGabor.draw()
    fixation.draw()
    win.flip()
    core.wait(gaborDuration) 
    gaussianGray.draw()
    fixation.color = waitColor
    fixation.draw()
    win.flip()
    event.clearEvents()
    keys = event.waitKeys(maxWait=timelimit, keyList=['left', 'right', 'up', 'down', 'q'])

    # If a key is pressed, take the response. If not, just remove the images from the screen    
    if keys:
        resp = keys[0]
                                    
        #At this point, there are still no keys pressed. So "if not keys" is definitely 
        #going to be processed.
        #After removing the images from the screen, still listening for a keypress. 
        #Record the reaction time if a key is pressed.
                                    
    if not keys:            
        keys = event.waitKeys(maxWait = timelimit, keyList=['left', 'right', 'up', 'down', 'q'])
    

                              
    # If the key is pressed analyze the keypress.
    if keys:
        if 'q' in keys:
            win.close()
            core.quit()
        else:
            resp = keys[0]
    else: 
        resp = 'noResp'
        
    # Check accuracy
    if resp == theVF:
        acc = 1
        acc_count_dict[thisCond] = acc_count_dict[thisCond] + 1
    elif resp == 'noResp':
        acc = 0
        acc_count_dict[thisCond] = 0
        reversal_dict[thisCond] = reversal_dict[thisCond] + 1
    else:
        acc = 0
        acc_count_dict[thisCond] = 0
        reversal_dict[thisCond] = reversal_dict[thisCond] + 1
    
    # ISI ... (+ change fixation dot color depending on accuracy)
    if acc == 1:
        accColor = OKcolor
    else:
        accColor = notOKcolor
    
    gaussianGray.draw()
    fixation.color = accColor
    fixation.draw()
    win.flip()
    core.wait(0.5) # wait 
    gaussianGray.draw()
    fixation.color = neutralColor
    fixation.draw()
    win.flip()
    core.wait(1) # wait 
            
    
    # Save info about that trial
    trainingtest_array.append('test')
    trial_array.append(trial)
    eccentricity_array.append(eccentricity)
    xPos_array.append(xPos)
    yPos_array.append(yPos)
    meridian_array.append(theMeridian)
    gabor_ori_array.append(theOri)
    VF_array.append(theVF)
    resp_array.append(resp)
    accuracy_array.append(acc)
    accCount_array.append(acc_count_dict[thisCond])
    thisCond_array.append(thisCond)
    trialCount_array.append(trial_count_dict[thisCond])
    reversal_array.append(reversal_dict[thisCond])

    if (trial%25 == 0):
        # PAUSE
        progression = thisTrial*100/nTrialsTotal
        pause_txt = 'Take a little break : ) \n progression' + str(progression) + '%' + '\n \n Press SPACE to resume'
        pause.setText(pause_txt)
        gaussianGray.draw()
        pause.draw()
        win.flip() 
        event.clearEvents()
        keys = event.waitKeys(keyList=['space', 'q'])
        if 'q' in keys:
            win.close()
            core.quit()
        if 'space' in keys:
            gaussianGray.draw()
            win.flip()
            core.wait(2)







#%%#  Create the data file + its file name

if not os.path.isdir(datadir):
    os.makedirs(datadir)
data_fname = exp_name + '_' + exp_info['subj_ID']+ '_session'+ exp_info['session'] + '_' + exp_info['date'] + '.csv'
data_fname = os.path.join(datadir, data_fname)

subj_ID = exp_info['subj_ID']
exp_date = exp_info['date']


actualNtrials = len(contrastRule_array)

subject_array = []
exp_name_array = []
date_array = [] 
session_array = []
gaborSize_array = []
gaborSizeDVA_array = []
gaborSFDVA_array = []
for n in range(actualNtrials):
    subject_array.append(subj_ID)
    exp_name_array.append(exp_name)
    date_array.append(exp_info['date'])
    session_array.append(exp_info['session'])
    gaborSize_array.append(gaborSize15)
    gaborSizeDVA_array.append(gaborSizeDVA)
    gaborSFDVA_array.append(gaborSFDVA)
    
    

output_file = pd.DataFrame({'subj_ID': subject_array,
                            'exp_name': exp_name_array,
                            'date': date_array,
                            'session': session_array,
                            'training-test': trainingtest_array,
                            'trial': trial_array,
                            'eccentricity': eccentricity_array,
                            'xPosition': xPos_array,
                            'yPosition': yPos_array,
                            'meridian': meridian_array,
                            'contrast': contrast_array,
                            'ori': gabor_ori_array,
                            'VF': VF_array,
                            'resp': resp_array,
                            'accuracy': accuracy_array,
                            'accCount': accCount_array,
                            'condition': thisCond_array,
                            'trialCount': trialCount_array,
                            'reversal': reversal_array,
                            'contrastRule': contrastRule_array
                            })

# save the csv file + pickle

# CSV file
output_file.to_csv(data_fname, index = False)

# Pickle
# with open(data_fname + ".pkl", 'wb') as f:
#     pickle.dump(output_file, f, pickle.HIGHEST_PROTOCOL)
print('FILES SAVED')


win.close()