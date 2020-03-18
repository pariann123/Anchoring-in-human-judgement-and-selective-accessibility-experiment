from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from load_ui import *
from demographics_consent_check import next_page
from custom_widgets import *

#Practice CIT Task
#---------------------------------------------------------------------------
def check_pract():  # This function checks the words in the practice round
    answer=window.type_guess_lbl.toPlainText()
    if window.words in answer.lower(): # Incase people type in capital and in case they enter a space or enter key, the word is still recognised
        window.feedback_lbl.setText("Correct!")
        window.too_slow_pract_timer.stop()
        correct_pract_page()

    elif window.words not in answer.lower():  #This also includes not enterring any word
        window.feedback_lbl.setText("Incorrect!")
        window.wait_10secs_lbl.show()
        window.too_slow_pract_timer.stop()
        next_page()
        window.timer_incorrect_pract_page.start(10000)

def correct_pract_page():
    next_page()
    window.timer_correct_pract_page.start(1000)

def too_slow_practice():
    window.feedback_lbl.setText("Too slow!")
    window.wait_10secs_lbl.show()
    window.page.setCurrentIndex(9)
    window.timer_incorrect_pract_page.start(10000)


# Actual CIT task
#---------------------------------------------------------------------------

def correct_page():  #Stays on the correct page for 1 seconds
    next_page()
    window.timer_correct_page.start(1000)

def too_slow():   #Slows too slow message and stays on this page for 10 seconds
    window.feedback_lbl.setText("Too slow!")
    window.wait_10secs_lbl.show()
    window.page.setCurrentIndex(9)
    window.timer_incorrect_page.start(10000)

window.each_word_time_taken=[]
def check():
    answer=window.type_guess_lbl.toPlainText()
    if window.words in answer.lower(): # Incase people type in capital and press the spacebar or enter after they type the word
        window.time_completed = window.my_blinking_label.millisec
        window.each_word_time_taken.append(window.time_completed)
        window.my_blinking_label.millisec=0
        window.feedback_lbl.setText("Correct!")
        correct_page()
        window.too_slow_timer.stop()

    elif window.words not in answer.lower():
        window.feedback_lbl.setText("Incorrect!")
        window.wait_10secs_lbl.show()
        next_page()
        window.timer_incorrect_page.start(10000)
        window.too_slow_timer.stop() #Stopping timer here as sometimes it switches from incorrect label to too slow label
