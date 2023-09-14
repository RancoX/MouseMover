import pyautogui as pg
from datetime import datetime
from time import sleep
from random import randint,random
from screeninfo import get_monitors
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QSpinBox, QVBoxLayout, QHBoxLayout, QWidget, QComboBox
from PySide6.QtCore import Qt
import sys


# =================================== params ===================================
pg.FAILSAFE=False
# stop time
stop_hr=17
stop_min=0
# Iterate through each monitor and print its width and height
max_x=0
min_y=100_000
# get date
now=datetime.now()
# press key
keys=["ctrl","shift","alt","space","tab","enter","esc","capslock","up","down","left","right","add","subtract","divide","multiply"]

# =================================== main function ===================================
def auto_cursor(stop_hr,stop_min,max_x,min_y,flag,now,key):
    print(f'Beeeeeep...zzZZzzZZZzzz...It\'s {now.strftime(r"%A, %Y-%m-%d %H:%M:%S")}\nI\'m your pc scout, automobility initiated until {stop_hr}:{stop_min:02}:00')
    # Get a list of all connected monitors
    monitors = get_monitors()

    for monitor in monitors:
        # print(f"Monitor <{monitor.name}>: Width: {monitor.width} pixels, Height: {monitor.height} pixels")
        max_x+=monitor.width
        min_y=min(min_y,monitor.height)


    while flag:
        # generate the next x,y, moving time, sleep time
        x=randint(0,max_x-1)
        y=randint(0,min_y-1)
        duration=round(2*random(),2)
        sleeping_time=randint(2,120)

        print(f"Now moving cursor to <{x},{y}> and then will sleep for {sleeping_time}s")
        # move cursor
        pg.moveTo(x,y,duration=duration)
        if sleeping_time>90:
            pg.press(key)
            print(f"Key <{key}> has been pressed!")

        # hold off
        sleep(sleeping_time)

        # check if time's up
        now_hr, now_min = datetime.now().hour, datetime.now().minute
        if now_hr > stop_hr:
            flag=False
        if now_hr == stop_hr:
            if now_min >= stop_min:
                flag=False

    print(f"It's {stop_hr}:{stop_min:02}:00! No one's watching anymore...")

# =================================== GUI ===================================
class ZeroPaddedSpinBox(QSpinBox):
    def __init__(self):
        super().__init__()

    def textFromValue(self, value):
        # Customize the display format to add a leading zero if value < 10
        return f'{value:02}'
    
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Auto mouse mover 1.0')
        self.setGeometry(200,300,600,400)

        layout=QVBoxLayout()

        end_time_label=QLabel('End time:')
        font=end_time_label.font()
        font.setBold(True)
        font.setPointSize(13)
        end_time_label.setFont(font)

        self.end_time_hr=QSpinBox()
        self.end_time_hr.setFixedWidth(40)
        self.end_time_hr.setValue(stop_hr)
        self.end_time_hr.setRange(0,23)
        self.end_time_hr.setSingleStep(1)

        end_time_colon=QLabel(' : ')
        font=end_time_colon.font()
        font.setBold(True)
        font.setPointSize(13)
        end_time_colon.setFont(font)
        end_time_colon.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.end_time_min=ZeroPaddedSpinBox()
        self.end_time_min.setFixedWidth(40)
        self.end_time_min.setRange(0,59)
        self.end_time_min.setSingleStep(1)
        self.end_time_min.setValue(stop_min)

        end_time_row=QHBoxLayout()
        end_time_row.setSpacing(10)
        end_time_row.addWidget(end_time_label)
        end_time_row.addWidget(self.end_time_hr,alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        end_time_row.addWidget(end_time_colon)
        end_time_row.addWidget(self.end_time_min,alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        end_time_row.addStretch()

        # key to press
        key_lable=QLabel('Key to press:')
        font=key_lable.font()
        font.setBold(True)
        font.setPointSize(13)
        key_lable.setFont(font)

        self.key_combo=QComboBox()
        for key in keys:
            self.key_combo.addItem(key.upper())
        self.key_combo.setCurrentIndex(0)

        key_row=QHBoxLayout()
        key_row.setSpacing(10)
        key_row.addWidget(key_lable)
        key_row.addWidget(self.key_combo,alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        key_row.addStretch()

        # functional buttons
        run_btn=QPushButton('Run')
        run_btn.clicked.connect(self.run)

        stop_btn=QPushButton('Stop')
        stop_btn.clicked.connect(self.stop)

        btn_layout=QHBoxLayout()
        btn_layout.addWidget(run_btn)
        btn_layout.addWidget(stop_btn)

        container=QWidget()
        layout.addLayout(end_time_row)
        layout.addLayout(key_row)
        layout.addLayout(btn_layout)
        container.setLayout(layout)
        self.setCentralWidget(container)


    def run(self,s):
        flag=True
        key=self.key_combo.currentText()
        stop_hr, stop_min = self.end_time_hr.value(), self.end_time_min.value()
        auto_cursor(stop_hr,stop_min,max_x,min_y,flag,now,key)
    
    def stop(self,s):
        flag=False


app=QApplication(sys.argv)
win=MyMainWindow()
win.show()
app.exec()

