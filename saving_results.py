from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from load_ui import *
from os import listdir

# Saving results at the end of the experiment
def save_results():
    if window.results_file in listdir():
        file = open(window.results_file, 'a')
        info=f"\n{window.age},{window.gender},{window.education},{window.condition_name},{window.absolute_answer},{window.average_congruent_RT},{window.average_incongruent_RT},{window.average_neutral_RT}"
        file.write(info)
        file.close()

# Saving reaction times
def reaction_times():
    # Getting actual seconds by multiplying 0.125ms by self.millisec variable (explained in document)
    window.each_word_time_taken_seconds=[]
    for each_time in window.each_word_time_taken:
        new_time=each_time*0.125
        window.each_word_time_taken_seconds.append(new_time)

    neutral_trial=0
    congruent_trial=0
    incongruent_trial=0
    neutral_count=0
    congruent_count=0
    incongrunet_count=0

    for i, each_type in enumerate(window.type_list):  # since a lot of the types were the same and the index would therefore be the same, I had to loop like this
        if each_type == "neutral":
            neutral_trial += window.each_word_time_taken_seconds[i]
            neutral_count +=1
        if window.condition_index == 0:    # If participants are in condition 0 ("low") and they see "low temperature" words - this is the congruent condition
            if each_type == "low":
                congruent_trial += window.each_word_time_taken_seconds[i]
                congruent_count+=1
            elif each_type =="high":      # If participants are in condition 0 ("low") and they see "high temperature" words - this is the incongruent condition
                incongruent_trial += window.each_word_time_taken_seconds[i]
                incongrunet_count+=1
        elif window.condition_index == 1:
            if each_type == "low":
                incongruent_trial += window.each_word_time_taken_seconds[i]
                incongrunet_count+=1
            elif each_type =="high":
                congruent_trial += window.each_word_time_taken_seconds[i]
                congruent_count+=1

    window.average_neutral_RT=neutral_trial/neutral_count
    window.average_congruent_RT=congruent_trial/congruent_count
    window.average_incongruent_RT=incongruent_trial/incongrunet_count
    save_results()