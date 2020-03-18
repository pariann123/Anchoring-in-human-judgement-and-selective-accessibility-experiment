from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from load_ui import *

def next_page():
    page_index = window.page.currentIndex()
    page_index += 1
    window.page.setCurrentIndex(page_index)

# Page 1 = consent form, checks if consent box is ticked
def consent_form():
    if window.gives_consent_cb.isChecked():
        next_page()
    else:
        window.error_msg_consent_lbl.show()

# Page 2 = demographics, check they're all filled out appropriately
def demographics():
    error=False     # if all errors are false, then can proceed to the next page
    part_age = int(window.age_sb.text())

    if part_age<16:
        window.error_msg_age_lbl.show()
        error = True
    else:
        window.age =window.age_sb.text()
        window.error_msg_age_lbl.hide()

    if not window.female_rb.isChecked() and not window.male_rb.isChecked() and not window.prefer_not_say_rb.isChecked():
        window.error_msg_gender_lbl.show()
        error = True

    if window.female_rb.isChecked():
        window.error_msg_gender_lbl.hide()
        window.gender="Female"
    elif window.male_rb.isChecked():
        window.error_msg_gender_lbl.hide()
        window.gender = "Male"
    elif window.prefer_not_say_rb.isChecked():
        window.error_msg_gender_lbl.hide()
        window.gender = "Prefer not to say"

    if window.education_cb.currentText() == "Select...":
        window.error_msg_education_lbl.show()
        error = True
    else:
        window.error_msg_education_lbl.hide()
        window.education=window.education_cb.currentText()

    if error==False:
        next_page()
    window.repaint()