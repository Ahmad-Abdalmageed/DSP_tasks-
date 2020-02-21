import sys

from PyQt5.QtWidgets import QApplication, QPushButton

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

app = QApplication(sys.argv)


# define a new slot that receives a string and has

# 'saySomeWords' as its name

@pyqtSlot(str)
def say_some_words(words):
    print(words)


class Communicate(QObject):
    # create a new signal on the fly and name it 'speak'

    speak = pyqtSignal(str)


someone = Communicate()

# connect signal and slot

someone.speak.connect(say_some_words)

# emit 'speak' signal

someone.speak.emit("Hello everybody!")
