from os import listdir
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from load_ui import *

## Creating or Opening file
# If first time running experiment, creates the file, otherwise it reads file to know which condition has the lowest amount of participants
def start_experiment():
    window.page.setCurrentIndex(0)            # Experiment starts on page 1, consent form
    if window.results_file in listdir():
        file = open(window.results_file, 'r')
        read_data = file.readlines()
        all_part_data=[]
        for data in read_data:
            all_part_data.append(data.split(","))

        cond1=0
        cond2=0
        for each_data in all_part_data:   # count how many participants in each condition and choose the next condition according to the condition with fewer participants
            old_cond=each_data[3]
            if old_cond=="low":
                cond1+=1
            elif old_cond=="high":
                cond2+=1
        if cond1 > cond2:
            window.condition_index = 1
        else:
            window.condition_index = 0

    else:
        file = open(window.results_file, 'w')
        columns=("Age,Gender,Education,Condition,Temperature Estimate,Congruent RT,Incongruent RT,Neutral RT")
        file.write(columns)