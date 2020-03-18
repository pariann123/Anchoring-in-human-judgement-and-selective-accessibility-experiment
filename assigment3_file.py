import random
from random import randint
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from custom_widgets import *
from load_ui import *
from demographics_consent_check import *
from saving_results import *
from starting_experiment import *
from checking_CIT_task import *

## Hiding error messages until they are needed
window.error_msg_consent_lbl.hide()
window.error_msg_age_lbl.hide()
window.error_msg_gender_lbl.hide()
window.error_msg_education_lbl.hide()
window.wait_10secs_lbl.hide()

## Setting variables
window.condition_index=0                  # Condition 0 means participants see lower values, condition 1 means pariticpants see higher values
window.condition_name="low"
window.absolute_answer=""                 # Absolute answer for temperature estimate in anchoring task
window.results_file= "result_file.csv"
window.first_position="lower"             # Randomly changes the position for 'higher' and 'lower' in text
window.second_position="higher"
window.instr_h_l_keys.setText("Press 'L' button for lower and 'H' button for higher ")
positions=randint(0,1)                    # 0 = Position 1:lower , Position 2: higher      1 = Position 1:higher , Position 2: lower
if positions==1:                          # Change default of first and second position for 'higher' and 'lower' instructions in task - counterbalancing variables
    window.first_position = "higher"
    window.second_position = "lower"
    window.instr_h_l_keys.setText("Press 'H' button for higher and 'L' button for lower ")

start_experiment()

## Setting the texts according to conditions
if window.condition_index==0:      # If participant is in the lower condition then sees all the lower values
    window.comparative = "5"
    window.comparative_percent="5"

if window.condition_index==1:      # If participant is in the higher condition then sees all the higher values
    window.comparative="20"
    window.comparative_percent="70"
    window.condition_name = "high"

#If you want to increase, decrease, or change any of the comparative and absolute questions, you can change them here.
#Starts with an empty string because we begin by setting the text before we start the function, each time the function is called it moves to the next string (so the first item is not seen).
comparative_q_list = ["",f"Is the average price of a new German car {window.first_position} or {window.second_position} than {window.comparative} 000€?",f"Is the proportion of African countries in the UN {window.first_position} or {window.second_position} than {window.comparative_percent}%?",f"Is the average weight of a giraffe {window.first_position} or {window.second_position} than {window.comparative}0 Kg?",f"Is the chance of nuclear war between United States and Iran {window.first_position} or {window.second_position} than {window.comparative_percent}%?",f"Is the average temperature of England {window.first_position} or {window.second_position} than {window.comparative} degree celsius?"]
absolute_q_list = ["","What is the average price of a new German car?", "What proportion of African countries are in the UN?","What is the average weight of a giraffe?","What is the chance of nuclear war between the Unites States and Iran?","What is the average temperature of England?"]


#---------------------------------------------------------------------------
# Anchoring Task
#---------------------------------------------------------------------------

window.comparative_q_lbl.setText(comparative_q_list[0])   #Sets the first comparative question before the function is called
def comparative_q():
    window.page.setCurrentIndex(3)
    statement = comparative_q_list.index(window.comparative_q_lbl.text())   #Getting the index of the question each time, so that the next statement can be set
    if comparative_q_list[statement] != comparative_q_list[-1]:             # If it is not the last item, then set the next one
        window.absolute_te.clear()  # Clearing the last answer so that a new answer can be provided each time
        statement += 1
        window.comparative_q_lbl.setText(comparative_q_list[statement])
    else:
        window.page.setCurrentIndex(5)     # When all the questions are complete, move onto the instructions of CIT task
        window.absolute_answer = window.absolute_te.toPlainText()  #Saving FINAL answer, as this is the only one we are interested in

def absolute_q():  # Setting the first absolute question, based on which comparative question is being shown.
    next_page()
    window.absolute_q_lbl.setText(absolute_q_list[comparative_q_list.index(window.comparative_q_lbl.text())])


##---------------------------------------------------------------------------
# Continuous Identification Task
#---------------------------------------------------------------------------

# Opening the data which contain the congruent, incongruent, and neutral words
data=[]
with open("CIT_words.csv") as f:  # Opening file this way to get rid of \n
    for line in f:
        st_line = line.strip('\n')
        data.append(st_line)
data.remove(data[0])

# Opening neutral words for the practice rounds
practice_data=[]
with open("practice_words.csv") as f:
    for line in f:
        st_line = line.strip('\n')
        practice_data.append(st_line)


#Practice CIT Task
#---------------------------------------------------------------------------
window.seen_practice_words=[]   # append words here so that there are not selected more than once
def start_practice_CIT():
    window.page.setCurrentIndex(7)
    window.CIT_next_prac_pb.show()    # Use different Next button to real CIT task, as different functions are called
    window.CIT_next_exp_pb.hide()
    window.my_blinking_label.millisec = 0    # Setting blinking count to zero every time
    window.timer_correct_pract_page.stop()    # Stopping the timer for correct page every time
    window.timer_incorrect_pract_page.stop()  # Stopping the timer for incorrect page every time
    window.wait_10secs_lbl.hide()             # Hiding label that says wait 10 seconds
    window.type_guess_lbl.clear()             # Clear text every time

    if len(window.seen_practice_words) != len(practice_data):   # If all the words have not been presented yet then do the following
        window.words=random.choice(practice_data)               # Choose a word at random
        if window.words not in window.seen_practice_words:      # If it hasn't been seen yet then:
            window.seen_practice_words.append(window.words)     # add it to the list of seen words
            hash = ""
            window.hash_length = hash.ljust(len(window.words), "#")    # Create a mask of the same size with hash keys
            window.my_blinking_label.setText(window.hash_length)              # Set intial text of blinking label to the mask
            window.my_blinking_label.blink(window.words, window.hash_length)  # Call the blinking label custom widget
            window.too_slow_pract_timer.start(20000)                   # If participants take too long to answer, gives them 'Too slow' message.
        else:
            start_practice_CIT()     # If a random word is chosen at random which has already been seen, then repeat these steps

    else:                             # If all words have been seen, start real task
        window.page.setCurrentIndex(6)



# Actual CIT task
#---------------------------------------------------------------------------
# Similar to practice round
window.seen_before_words=[]
window.type_list=[]           # Add word type to this list so it can be used later on in the analysis
def start_CIT():
    window.page.setCurrentIndex(7)
    window.CIT_next_exp_pb.show()
    window.CIT_next_prac_pb.hide()
    window.my_blinking_label.millisec = 0
    window.timer_correct_page.stop()
    window.timer_incorrect_page.stop()
    window.wait_10secs_lbl.hide()
    window.type_guess_lbl.clear()

    if len(window.seen_before_words) != len(data):
        random_word=random.choice(data)
        type_word=random_word.split(",")
        type=type_word[0]      # These random_words two information, type and word, so we separate them and store them both
        window.words=type_word[1]
        if window.words not in window.seen_before_words:
            window.too_slow_timer.start(20000) # 20 seconds for participants to answer
            window.seen_before_words.append(window.words)
            window.type_list.append(type)
            hash = ""
            window.hash_length = hash.ljust(len(window.words) , "#")
            window.my_blinking_label.setText(window.hash_length)
            window.my_blinking_label.blink(window.words, window.hash_length)
        else:
            start_CIT()

    else: # If all the words have been seen then move to the debrief page and calculate reaction times
        window.page.setCurrentIndex(10)
        reaction_times()

def incorrect_page():
    window.time_completed = window.my_blinking_label.millisec    #Save time for incorrect trials with the added 10 seconds from this page
    window.each_word_time_taken.append(window.time_completed)
    start_CIT()

def l_h_keys(key):     # Only respond if H or L keys pressed
    if key == Qt.Key_L or key==Qt.Key_H:
        absolute_q()

def spacebar_key(key):  # Only respond if spacebar key pressed
    if key ==Qt.Key_Space:
        next_page()

# Timers
window.timer_incorrect_pract_page=QTimer()
window.timer_incorrect_pract_page.timeout.connect(start_practice_CIT)
window.timer_correct_pract_page=QTimer()
window.timer_correct_pract_page.timeout.connect(start_practice_CIT)
window.too_slow_pract_timer = QTimer()
window.too_slow_pract_timer.timeout.connect(too_slow_practice)
window.timer_incorrect_page=QTimer()
window.timer_incorrect_page.timeout.connect(incorrect_page)
window.timer_correct_page=QTimer()
window.timer_correct_page.timeout.connect(start_CIT)
window.too_slow_timer = QTimer()
window.too_slow_timer.timeout.connect(too_slow)

# Creating my custom widgets
my_l_h_keys=keyboard_widget(window.anchor_comparative)
my_l_h_keys.setFocus()
my_l_h_keys.keyPressed.connect(l_h_keys)

my_spacebar_widget=keyboard_widget(window.CIT_word_viewing)
my_spacebar_widget.setFocus()
my_spacebar_widget.keyPressed.connect(spacebar_key)

window.my_blinking_label = changing_label(window.CIT_word_viewing)
window.my_blinking_label.setGeometry(450,50,500,500)
window.my_blinking_label.setWordWrap(True)
window.my_blinking_label.setFont(QFont("AppleSystemUIFont", 45))
window.my_blinking_label.millisec=0

# Connecting the buttons to their functions
window.submit_consent_pb.clicked.connect(consent_form)
window.submit_demo_pb.clicked.connect(demographics)
window.start_anchor_pb.clicked.connect(comparative_q)
window.next_pb.clicked.connect(comparative_q)
window.start_CIT_pract_pb.clicked.connect(start_practice_CIT)
window.CIT_next_exp_pb.clicked.connect(check)
window.CIT_next_prac_pb.clicked.connect(check_pract)
window.start_CIT_pb.clicked.connect(start_CIT)
window.terminate_pb.clicked.connect(exit)

window.show()
app.exec_()