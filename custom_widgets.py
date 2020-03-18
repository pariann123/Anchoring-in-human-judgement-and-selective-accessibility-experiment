from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class changing_label(QLabel):

    def blink(self, text, hash_keys):
        self.text = text
        self.hash_keys = hash_keys
        self.current_label = self.text
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.switch)
        self.blink_timer.start(1)

    def switch(self):
        ### Every 0.25 seconds (233ms+17ms) it flashes twice - so to do the maths later on, times the number by 0.125
        self.millisec += 1
        if self.current_label == self.text:
            self.current_label = self.hash_keys
            self.blink_timer.start(233)
            self.blink_timer.setInterval(233 - self.millisec)
        else:
            self.current_label = self.text
            self.blink_timer.start(17)
            self.blink_timer.setInterval(17 + self.millisec)
        self.setText(self.current_label)


class keyboard_widget(QWidget):
    keyPressed = pyqtSignal(int)

    def keyPressEvent(self, event):
        super(keyboard_widget, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())
