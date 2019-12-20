import os
import sys
import time
import shutil
import filecmp
import datetime
import fileinput
import distutils.dir_util
import win32api
import win32process
import win32con
from win32api import GetSystemMetrics
from PyQt5.QtCore import Qt, QThread, QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QIcon, QFont

priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                   win32process.BELOW_NORMAL_PRIORITY_CLASS,
                   win32process.NORMAL_PRIORITY_CLASS,
                   win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                   win32process.HIGH_PRIORITY_CLASS,
                   win32process.REALTIME_PRIORITY_CLASS]
pid = win32api.GetCurrentProcessId()
handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
win32process.SetPriorityClass(handle, priorityclasses[4])

settings_active = False
thread_var = [(), (), (), (), (), ()]
timer_thread_var = [(), (), (), (), (), ()]
ts_thread_var = [(), (), (), (), (), ()]
path_var = []
dest_path_var = []
path_bool_var = []
dest_path_bool_var = []
source_path_entered = ''
dest_path_entered = ''
source_selected = ()
dest_selected = ()
compare_bool_var = [False, False, False, False, False, False]
compare_clicked = ()
config_src_var = ['ARCHIVE_SOURCE',
                  'DOCUMENT_SOURCE',
                  'MUSIC_SOURCE',
                  'PICTURE_SOURCE',
                  'PROGRAMS_SOURCE',
                  'VIDEO_SOURCE']
config_dst_var = ['ARCHIVE_DESTINATION',
                  'DOCUMENT_DESTINATION',
                  'MUSIC_DESTINATION',
                  'PICTURE_DESTINATION',
                  'PROGRAMS_DESTINATION',
                  'VIDEO_DESTINATION']
btnx_main_var = []
btnx_settings_var = []
comp_cont_button_var = []
stop_thr_button_var = []
info_label_1_var = []
sync_ts_var = []

img_mode_1 = './image/mode_1.png'
img_mode_2 = './image/mode_2.png'
img_settings = './image/settings.png'
img_var = ['./image/archive_icon.png',
           './image/document_icon.png',
           './image/music_icon.png',
           './image/picture_icon.png',
           './image/program_icon.png',
           './image/video_icon.png']
img_active_var = ['./image/archive_icon_active.png',
                  './image/document_icon_active.png',
                  './image/music_icon_active.png',
                  './image/picture_icon_active.png',
                  './image/program_icon_active.png',
                  './image/video_icon_active.png']


def get_conf_funk():
    global path_var, path_bool_var, dest_path_var, dest_path_bool_var
    path_var = []
    path_bool_var = []
    dest_path_var = []
    dest_path_bool_var = []
    with open('config.txt', 'r') as fo:
        for line in fo:
            line = line.strip()
            i = 0
            for config_src_vars in config_src_var:
                if line.startswith(config_src_var[i]):
                    key_word_length = len(config_src_var[i])
                    primary_key = line[:key_word_length]
                    secondary_key = line[key_word_length:]
                    primary_key = primary_key.strip()
                    secondary_key = secondary_key.strip()
                    if primary_key.endswith('_SOURCE'):
                        if os.path.exists(secondary_key):
                            if (primary_key + '_True') not in dest_path_bool_var:
                                path_var.append(secondary_key)
                                path_bool_var.append(primary_key + '_True')
                                # print(primary_key, secondary_key, 'valid')
                        elif not os.path.exists(secondary_key):
                            if (primary_key + '_False') not in dest_path_bool_var:
                                path_var.append('')
                                path_bool_var.append(primary_key + '_False')
                                # print(primary_key, secondary_key, 'invalid')
                i += 1
            i = 0
            for config_dst_vars in config_dst_var:
                if line.startswith(config_dst_var[i]):
                    key_word_length = len(config_dst_var[i])
                    primary_key = line[:key_word_length]
                    secondary_key = line[key_word_length:]
                    primary_key = primary_key.strip()
                    secondary_key = secondary_key.strip()
                    if primary_key.endswith('_DESTINATION'):
                        if os.path.exists(secondary_key):
                            if (primary_key + '_True') not in dest_path_bool_var:
                                dest_path_var.append(secondary_key)
                                dest_path_bool_var.append(primary_key + '_True')
                                # print(primary_key, secondary_key, 'valid')
                        elif not os.path.exists(secondary_key):
                            if (primary_key + '_False') not in dest_path_bool_var:
                                dest_path_var.append('')
                                dest_path_bool_var.append(primary_key + '_False')
                            # print(primary_key, secondary_key, 'invalid')
                i += 1
    fo.close()


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setWindowIcon(QIcon('./icon.png'))
        self.title = ' '
        get_conf_funk()
        self.width = 588
        self.height = 80
        scr_w = GetSystemMetrics(0)
        scr_h = GetSystemMetrics(1)
        self.left = (scr_w / 2) - (self.width / 2)  # centre
        self.top = ((scr_h / 2) - (self.height / 2))  # centre
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        # self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        global thread_var, btnx_main_var, btnx_settings_var, comp_cont_button_var, stop_thr_button_var, info_label_1_var
        global img_var, img_active_var, img_mode_1, img_mode_2, img_settings, timer_thread_var, sync_ts_var, ts_thread_var
        global path_var, dest_path_var
        self.setWindowTitle(' ')
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        i = 0
        while i < 6:
            btnx_name = 'btnx_main' + str(i)  # main function button.
            self.btnx_main = QPushButton(self)
            self.btnx_main.resize(54, 54)
            self.btnx_main.setIcon(QIcon(img_var[i]))
            self.btnx_main.setIconSize(QSize(54, 54))
            self.btnx_main.setStyleSheet(
                    """QPushButton{background-color: rgb(0, 0, 0);
                   border:0px solid rgb(0, 0, 0);}"""
                )
            btnx_main_var.append(self.btnx_main)
            sett_name = 'btnx_settings' + str(i)  # settings button.
            self.sett_name = QPushButton(self)
            self.sett_name.resize(10, 10)
            self.sett_name.setIcon(QIcon(img_settings))
            self.sett_name.setIconSize(QSize(10, 10))
            self.sett_name.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 0, 0);}"""
            )
            btnx_settings_var.append(self.sett_name)
            comp_cont_button = 'comp_cont_button' + str(i)  # mode switch. default only copy missing file names.
            self.comp_cont_button = QPushButton(self)
            self.comp_cont_button.resize(10, 30)
            self.comp_cont_button.setIcon(QIcon(img_mode_1))
            self.comp_cont_button.setIconSize(QSize(10, 30))
            self.comp_cont_button.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 0, 0);}"""
            )
            comp_cont_button_var.append(self.comp_cont_button)
            stop_thr_button = 'stop_thr_button' + str(i)  # stop main thread.
            self.stop_thr_button = QPushButton(self)
            self.stop_thr_button.resize(10, 10)
            self.stop_thr_button.setStyleSheet(
                """QPushButton{background-color: rgb(255, 0, 0);
               border:2px solid rgb(35, 35, 35);}"""
            )
            stop_thr_button_var.append(self.stop_thr_button)
            info_label_1 = 'info_label_1' + str(i)  # some output data.
            self.info_label_1 = QLabel(self)
            self.info_label_1.resize(71, 15)
            newfont = QFont("Times", 7, QFont.Bold)
            self.info_label_1.setFont(newfont)
            self.info_label_1.setText("")
            self.info_label_1.setStyleSheet(
                """QLabel {background-color: rgb(0, 0, 0);
               color: green;
               border:2px solid rgb(35, 35, 35);}"""
            )
            info_label_1_var.append(self.info_label_1)

            sync_ts = 'sync_ts' + str(i)  # main function button.
            self.sync_ts = QPushButton(self)
            self.sync_ts.resize(10, 10)
            # self.sync_ts.setIcon(QIcon(img_var[i]))
            # self.sync_ts.setIconSize(QSize(10, 10))
            self.sync_ts.setStyleSheet(
                """QPushButton{background-color: rgb(255, 255, 0);
               border:0px solid rgb(0, 0, 0);}"""
            )
            sync_ts_var.append(self.sync_ts)

            print('created object:', self.btnx_main, '. naming object:', btnx_name)
            print('created object:', self.sett_name, '. naming object:', sett_name)
            print('created object:', self.comp_cont_button, '. naming object:', comp_cont_button)
            print('created object:', self.stop_thr_button, '. naming object:', stop_thr_button)
            print('created object:', self.info_label_1, '. naming object:', info_label_1)
            print('created object:', self.sync_ts, '. naming object:', sync_ts)
            i += 1

        self.settings_source_label = QLabel(self)
        self.settings_source_label.move(5, 115)
        self.settings_source_label.resize(80, 15)
        newfont = QFont("Times", 7, QFont.Bold)
        self.settings_source_label.setFont(newfont)
        self.settings_source_label.setText('Source:')
        self.settings_source_label.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
        )
        # self.settings_source_label.hide()
        self.settings_dest_label = QLabel(self)
        self.settings_dest_label.move(5, 135)
        self.settings_dest_label.resize(80, 15)
        newfont = QFont("Times", 7, QFont.Bold)
        self.settings_dest_label.setFont(newfont)
        self.settings_dest_label.setText('Destination:')
        self.settings_dest_label.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
        )
        # self.settings_dest_label.hide()
        self.setting_title0 = QLabel(self)
        self.setting_title0.resize(100, 15)
        self.setting_title0.move(5, 90)
        newfont = QFont("Times", 7, QFont.Bold)
        self.setting_title0.setFont(newfont)
        self.setting_title0.setText("Archive Settings")
        self.setting_title0.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
        )
        self.setting_title0.hide()
        self.setting_title1 = QLabel(self)
        self.setting_title1.resize(100, 15)
        self.setting_title1.move(100, 90)
        newfont = QFont("Times", 7, QFont.Bold)
        self.setting_title1.setFont(newfont)
        self.setting_title1.setText("Document Settings")
        self.setting_title1.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
        )
        self.setting_title1.hide()
        self.setting_title2 = QLabel(self)
        self.setting_title2.resize(100, 15)
        self.setting_title2.move(200, 90)
        newfont = QFont("Times", 7, QFont.Bold)
        self.setting_title2.setFont(newfont)
        self.setting_title2.setText("Music Settings")
        self.setting_title2.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
        )
        self.setting_title2.hide()
        self.setting_title3 = QLabel(self)
        self.setting_title3.resize(100, 15)
        self.setting_title3.move(300, 90)
        newfont = QFont("Times", 7, QFont.Bold)
        self.setting_title3.setFont(newfont)
        self.setting_title3.setText("Picture Settings")
        self.setting_title3.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
        )
        self.setting_title3.hide()
        self.setting_title4 = QLabel(self)
        self.setting_title4.resize(100, 15)
        self.setting_title4.move(400, 90)
        newfont = QFont("Times", 7, QFont.Bold)
        self.setting_title4.setFont(newfont)
        self.setting_title4.setText("Program Settings")
        self.setting_title4.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
        )
        self.setting_title4.hide()
        self.setting_title5 = QLabel(self)
        self.setting_title5.resize(100, 15)
        self.setting_title5.move(500, 90)
        newfont = QFont("Times", 7, QFont.Bold)
        self.setting_title5.setFont(newfont)
        self.setting_title5.setText("Video Settings")
        self.setting_title5.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
        )
        self.setting_title5.hide()

        self.settings_source0 = QLineEdit(self)
        self.settings_source0.move(100, 115)
        self.settings_source0.resize(473, 15)
        self.settings_source0.setText(path_var[0])
        self.settings_source0.returnPressed.connect(self.settings_source_pre_funk0)
        self.settings_source0.setStyleSheet(
            """QLineEdit {background-color: rgb(35, 35, 35);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
        )
        self.settings_source0.hide()

        self.settings_source1 = QLineEdit(self)
        self.settings_source1.move(100, 115)
        self.settings_source1.resize(473, 15)
        self.settings_source1.setText(path_var[1])
        self.settings_source1.returnPressed.connect(self.settings_source_pre_funk1)
        self.settings_source1.setStyleSheet(
            """QLineEdit {background-color: rgb(35, 35, 35);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
        )
        self.settings_source1.hide()
        self.settings_source2 = QLineEdit(self)
        self.settings_source2.move(100, 115)
        self.settings_source2.resize(473, 15)
        self.settings_source2.setText(path_var[2])
        self.settings_source2.returnPressed.connect(self.settings_source_pre_funk2)
        self.settings_source2.setStyleSheet(
            """QLineEdit {background-color: rgb(35, 35, 35);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
        )
        self.settings_source2.hide()
        self.settings_source3 = QLineEdit(self)
        self.settings_source3.move(100, 115)
        self.settings_source3.resize(473, 15)
        self.settings_source3.setText(path_var[3])
        self.settings_source3.returnPressed.connect(self.settings_source_pre_funk3)
        self.settings_source3.setStyleSheet(
            """QLineEdit {background-color: rgb(35, 35, 35);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
        )
        self.settings_source3.hide()
        self.settings_source4 = QLineEdit(self)
        self.settings_source4.move(100, 115)
        self.settings_source4.resize(473, 15)
        self.settings_source4.setText(path_var[4])
        self.settings_source4.returnPressed.connect(self.settings_source_pre_funk4)
        self.settings_source4.setStyleSheet(
            """QLineEdit {background-color: rgb(35, 35, 35);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
        )
        self.settings_source4.hide()
        self.settings_source5 = QLineEdit(self)
        self.settings_source5.move(100, 115)
        self.settings_source5.resize(473, 15)
        self.settings_source5.setText(path_var[5])
        self.settings_source5.returnPressed.connect(self.settings_source_pre_funk5)
        self.settings_source5.setStyleSheet(
            """QLineEdit {background-color: rgb(35, 35, 35);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
        )
        self.settings_source5.hide()

        self.settings_dest0 = QLineEdit(self)
        self.settings_dest0.move(100, 135)
        self.settings_dest0.resize(473, 15)
        self.settings_dest0.setText(dest_path_var[0])
        self.settings_dest0.returnPressed.connect(self.settings_dest_pre_funk0)
        self.settings_dest0.setStyleSheet(
            """QLineEdit {background-color: rgb(35, 35, 35);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
        )
        self.settings_dest0.hide()
        self.settings_dest1 = QLineEdit(self)
        self.settings_dest1.move(100, 135)
        self.settings_dest1.resize(473, 15)
        self.settings_dest1.setText(dest_path_var[1])
        self.settings_dest1.returnPressed.connect(self.settings_dest_pre_funk1)
        self.settings_dest1.setStyleSheet(
            """QLineEdit {background-color: rgb(35, 35, 35);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
        )
        self.settings_dest1.hide()
        self.settings_dest2 = QLineEdit(self)
        self.settings_dest2.move(100, 135)
        self.settings_dest2.resize(473, 15)
        self.settings_dest2.setText(dest_path_var[2])
        self.settings_dest2.returnPressed.connect(self.settings_dest_pre_funk2)
        self.settings_dest2.setStyleSheet(
            """QLineEdit {background-color: rgb(35, 35, 35);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
        )
        self.settings_dest2.hide()
        self.settings_dest3 = QLineEdit(self)
        self.settings_dest3.move(100, 135)
        self.settings_dest3.resize(473, 15)
        self.settings_dest3.setText(dest_path_var[3])
        self.settings_dest3.returnPressed.connect(self.settings_dest_pre_funk3)
        self.settings_dest3.setStyleSheet(
            """QLineEdit {background-color: rgb(35, 35, 35);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
        )
        self.settings_dest3.hide()
        self.settings_dest4 = QLineEdit(self)
        self.settings_dest4.move(100, 135)
        self.settings_dest4.resize(473, 15)
        self.settings_dest4.setText(dest_path_var[4])
        self.settings_dest4.returnPressed.connect(self.settings_dest_pre_funk4)
        self.settings_dest4.setStyleSheet(
            """QLineEdit {background-color: rgb(35, 35, 35);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
        )
        self.settings_dest4.hide()
        self.settings_dest5 = QLineEdit(self)
        self.settings_dest5.move(100, 135)
        self.settings_dest5.resize(473, 15)
        # self.settings_dest5.setText(dest_path_var[5])
        self.settings_dest5.returnPressed.connect(self.settings_dest_pre_funk5)
        self.settings_dest5.setStyleSheet(
            """QLineEdit {background-color: rgb(35, 35, 35);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
        )
        self.settings_dest5.hide()

        btnx_main_var[0].move(5, 5)
        btnx_main_var[1].move(100, 5)
        btnx_main_var[2].move(200, 5)
        btnx_main_var[3].move(300, 5)
        btnx_main_var[4].move(400, 5)
        btnx_main_var[5].move(500, 5)

        btnx_settings_var[0].move(64, 5)
        btnx_settings_var[1].move(159, 5)
        btnx_settings_var[2].move(259, 5)
        btnx_settings_var[3].move(359, 5)
        btnx_settings_var[4].move(459, 5)
        btnx_settings_var[5].move(559, 5)

        comp_cont_button_var[0].move(64, 17)
        comp_cont_button_var[1].move(159, 17)
        comp_cont_button_var[2].move(259, 17)
        comp_cont_button_var[3].move(359, 17)
        comp_cont_button_var[4].move(459, 17)
        comp_cont_button_var[5].move(559, 17)

        stop_thr_button_var[0].move(64, 48)
        stop_thr_button_var[1].move(159, 48)
        stop_thr_button_var[2].move(259, 48)
        stop_thr_button_var[3].move(359, 48)
        stop_thr_button_var[4].move(459, 48)
        stop_thr_button_var[5].move(559, 48)

        info_label_1_var[0].move(5, 61)
        info_label_1_var[1].move(100, 61)
        info_label_1_var[2].move(200, 61)
        info_label_1_var[3].move(300, 61)
        info_label_1_var[4].move(400, 61)
        info_label_1_var[5].move(500, 61)

        sync_ts_var[0].move(77, 5)
        sync_ts_var[1].move(173, 5)
        sync_ts_var[2].move(273, 5)
        sync_ts_var[3].move(373, 5)
        sync_ts_var[4].move(473, 5)
        sync_ts_var[5].move(573, 5)

        comp_cont_button_var[0].clicked.connect(self.set_comp_bool_pre_funk0)
        comp_cont_button_var[1].clicked.connect(self.set_comp_bool_pre_funk1)
        comp_cont_button_var[2].clicked.connect(self.set_comp_bool_pre_funk2)
        comp_cont_button_var[3].clicked.connect(self.set_comp_bool_pre_funk3)
        comp_cont_button_var[4].clicked.connect(self.set_comp_bool_pre_funk4)
        comp_cont_button_var[5].clicked.connect(self.set_comp_bool_pre_funk5)

        stop_thr_button_var[0].clicked.connect(self.stop_thr_funk0)
        stop_thr_button_var[1].clicked.connect(self.stop_thr_funk1)
        stop_thr_button_var[2].clicked.connect(self.stop_thr_funk2)
        stop_thr_button_var[3].clicked.connect(self.stop_thr_funk3)
        stop_thr_button_var[4].clicked.connect(self.stop_thr_funk4)
        stop_thr_button_var[5].clicked.connect(self.stop_thr_funk5)

        btnx_main_var[0].clicked.connect(self.thread_funk_0)
        btnx_main_var[1].clicked.connect(self.thread_funk_1)
        btnx_main_var[2].clicked.connect(self.thread_funk_2)
        btnx_main_var[3].clicked.connect(self.thread_funk_3)
        btnx_main_var[4].clicked.connect(self.thread_funk_4)
        btnx_main_var[5].clicked.connect(self.thread_funk_5)

        sync_ts_var[0].clicked.connect(self.set_timestamp_funk0)
        sync_ts_var[1].clicked.connect(self.set_timestamp_funk1)
        sync_ts_var[2].clicked.connect(self.set_timestamp_funk2)
        sync_ts_var[3].clicked.connect(self.set_timestamp_funk3)
        sync_ts_var[4].clicked.connect(self.set_timestamp_funk4)
        sync_ts_var[5].clicked.connect(self.set_timestamp_funk5)

        btnx_settings_var[0].clicked.connect(self.settings_funk0)
        btnx_settings_var[1].clicked.connect(self.settings_funk1)
        btnx_settings_var[2].clicked.connect(self.settings_funk2)
        btnx_settings_var[3].clicked.connect(self.settings_funk3)
        btnx_settings_var[4].clicked.connect(self.settings_funk4)
        btnx_settings_var[5].clicked.connect(self.settings_funk5)

        timer_thread_var[0] = TimerClass0()
        timer_thread_var[1] = TimerClass1()
        timer_thread_var[2] = TimerClass2()
        timer_thread_var[3] = TimerClass3()
        timer_thread_var[4] = TimerClass4()
        timer_thread_var[5] = TimerClass5()

        thread_var[0] = ThreadClass0()
        thread_var[1] = ThreadClass1()
        thread_var[2] = ThreadClass2()
        thread_var[3] = ThreadClass3()
        thread_var[4] = ThreadClass4()
        thread_var[5] = ThreadClass5()

        ts_thread_var[0] = TSClass0()
        ts_thread_var[1] = TSClass1()
        ts_thread_var[2] = TSClass2()
        ts_thread_var[3] = TSClass3()
        ts_thread_var[4] = TSClass4()
        ts_thread_var[5] = TSClass5()

        self.show()

    def settings_source_funk(self):
        global source_path_entered, source_selected, config_src_var, path_var
        print('--', 'source_selected:', source_selected, 'source path entered:', source_path_entered)
        get_conf_funk()
        print(config_src_var)
        before_str = config_src_var[source_selected]+' '+path_var[source_selected]
        after_str = config_src_var[source_selected]+' '+source_path_entered
        print('-- before_str:', before_str)
        print('-- after_str: ', after_str)
        distutils.dir_util.mkpath(source_path_entered)
        if os.path.exists(source_path_entered):
            for line in fileinput.input('./config.txt', inplace=True):
                print(line.rstrip().replace(before_str, after_str)),

            path_var[source_selected] = source_path_entered

    def settings_dest_funk(self):
        global dest_path_entered, dest_selected, config_dst_var
        print('--', 'dest_selected:', dest_selected, 'dest path entered:', dest_path_entered)
        get_conf_funk()
        before_str = config_dst_var[dest_selected] + ' ' + dest_path_var[dest_selected]
        after_str = config_dst_var[dest_selected] + ' ' + dest_path_entered
        print('-- before_str:', before_str)
        print('-- after_str: ', after_str)
        distutils.dir_util.mkpath(dest_path_entered)
        if os.path.exists(dest_path_entered):
            for line in fileinput.input('./config.txt', inplace=True):
                print(line.rstrip().replace(before_str, after_str)),

            dest_path_var[dest_selected] = dest_path_entered

    def settings_source_pre_funk0(self):
        global source_path_entered, source_selected
        source_selected = 0
        source_path_entered = self.settings_source0.text()
        self.settings_source_funk()

    def settings_source_pre_funk1(self):
        global source_path_entered, source_selected
        source_selected = 1
        source_path_entered = self.settings_source1.text()
        self.settings_source_funk()

    def settings_source_pre_funk2(self):
        global source_path_entered, source_selected
        source_selected = 2
        source_path_entered = self.settings_source2.text()
        self.settings_source_funk()

    def settings_source_pre_funk3(self):
        global source_path_entered, source_selected
        source_selected = 3
        source_path_entered = self.settings_source3.text()
        self.settings_source_funk()

    def settings_source_pre_funk4(self):
        global source_path_entered, source_selected
        source_selected = 4
        source_path_entered = self.settings_source4.text()
        self.settings_source_funk()

    def settings_source_pre_funk5(self):
        global source_path_entered, source_selected
        source_selected = 5
        source_path_entered = self.settings_source5.text()
        self.settings_source_funk()

    def settings_dest_pre_funk0(self):
        global dest_path_entered, dest_selected
        dest_selected = 0
        dest_path_entered = self.settings_dest0.text()
        self.settings_dest_funk()

    def settings_dest_pre_funk1(self):
        global dest_path_entered, dest_selected
        dest_selected = 1
        dest_path_entered = self.settings_dest1.text()
        self.settings_dest_funk()

    def settings_dest_pre_funk2(self):
        global dest_path_entered, dest_selected
        dest_selected = 2
        dest_path_entered = self.settings_dest2.text()
        self.settings_dest_funk()

    def settings_dest_pre_funk3(self):
        global dest_path_entered, dest_selected
        dest_selected = 3
        dest_path_entered = self.settings_dest3.text()
        self.settings_dest_funk()

    def settings_dest_pre_funk4(self):
        global dest_path_entered, dest_selected
        dest_selected = 4
        dest_path_entered = self.settings_dest4.text()
        self.settings_dest_funk()

    def settings_dest_pre_funk5(self):
        global dest_path_entered, dest_selected
        dest_selected = 5
        dest_path_entered = self.settings_dest5.text()
        self.settings_dest_funk()

    def hide_settings_funk(self):
        print('-- plugged in: hide_settings_funk')
        self.setting_title0.hide()
        self.setting_title1.hide()
        self.setting_title2.hide()
        self.setting_title3.hide()
        self.setting_title4.hide()
        self.setting_title5.hide()
        self.settings_source0.hide()
        self.settings_source1.hide()
        self.settings_source2.hide()
        self.settings_source3.hide()
        self.settings_source4.hide()
        self.settings_source5.hide()
        self.settings_dest0.hide()
        self.settings_dest1.hide()
        self.settings_dest2.hide()
        self.settings_dest3.hide()
        self.settings_dest4.hide()
        self.settings_dest5.hide()

    def settings_funk0(self):
        print('-- plugged in: settings_funk0')
        global settings_active
        self.hide_settings_funk()
        if settings_active is False:
            self.setFixedSize(588, 160)
            self.setting_title0.show()
            self.settings_source0.show()
            self.settings_dest0.show()
            settings_active = True
        elif settings_active is True:
            self.setFixedSize(588, 80)
            settings_active = False

    def settings_funk1(self):
        print('-- plugged in: settings_funk1')
        global settings_active
        self.hide_settings_funk()
        if settings_active is False:
            self.setFixedSize(588, 160)
            self.setting_title1.show()
            self.settings_source1.show()
            self.settings_dest1.show()
            settings_active = True
        elif settings_active is True:
            self.setFixedSize(588, 80)
            settings_active = False

    def settings_funk2(self):
        print('-- plugged in: settings_funk2')
        global settings_active
        self.hide_settings_funk()
        if settings_active is False:
            self.setFixedSize(588, 160)
            self.setting_title2.show()
            self.settings_source2.show()
            self.settings_dest2.show()
            settings_active = True
        elif settings_active is True:
            self.setFixedSize(588, 80)
            settings_active = False

    def settings_funk3(self):
        print('-- plugged in: settings_funk3')
        global settings_active
        self.hide_settings_funk()
        if settings_active is False:
            self.setFixedSize(588, 160)
            self.setting_title3.show()
            self.settings_source3.show()
            self.settings_dest3.show()
            settings_active = True
        elif settings_active is True:
            self.setFixedSize(588, 80)
            settings_active = False

    def settings_funk4(self):
        print('-- plugged in: settings_funk4')
        global settings_active
        self.hide_settings_funk()
        if settings_active is False:
            self.setFixedSize(588, 160)
            self.setting_title4.show()
            self.settings_source4.show()
            self.settings_dest4.show()
            settings_active = True
        elif settings_active is True:
            self.setFixedSize(588, 80)
            settings_active = False

    def settings_funk5(self):
        print('-- plugged in: settings_funk5')
        global settings_active
        self.hide_settings_funk()
        if settings_active is False:
            self.setFixedSize(588, 160)
            self.setting_title5.show()
            self.settings_source5.show()
            self.settings_dest5.show()
            settings_active = True
        elif settings_active is True:
            self.setFixedSize(588, 80)
            settings_active = False

    def set_timestamp_funk0(self):
        ts_thread_var[0].start()

    def set_timestamp_funk1(self):
        ts_thread_var[1].start()

    def set_timestamp_funk2(self):
        ts_thread_var[2].start()

    def set_timestamp_funk3(self):
        ts_thread_var[3].start()

    def set_timestamp_funk4(self):
        ts_thread_var[4].start()

    def set_timestamp_funk5(self):
        ts_thread_var[5].start()

    def thread_funk_0(self):
        thread_var[0].start()

    def thread_funk_1(self):
        thread_var[1].start()

    def thread_funk_2(self):
        thread_var[2].start()

    def thread_funk_3(self):
        thread_var[3].start()

    def thread_funk_4(self):
        thread_var[4].start()

    def thread_funk_5(self):
        thread_var[5].start()

    def set_comp_bool_pre_funk0(self):
        global compare_clicked
        compare_clicked = 0
        self.set_comp_bool_funk()

    def set_comp_bool_pre_funk1(self):
        global compare_clicked
        compare_clicked = 1
        self.set_comp_bool_funk()

    def set_comp_bool_pre_funk2(self):
        global compare_clicked
        compare_clicked = 2
        self.set_comp_bool_funk()

    def set_comp_bool_pre_funk3(self):
        global compare_clicked
        compare_clicked = 3
        self.set_comp_bool_funk()

    def set_comp_bool_pre_funk4(self):
        global compare_clicked
        compare_clicked = 4
        self.set_comp_bool_funk()

    def set_comp_bool_pre_funk5(self):
        global compare_clicked
        compare_clicked = 5
        self.set_comp_bool_funk()

    def set_comp_bool_funk(self):
        global compare_bool_var, compare_clicked, btnx_main_var
        if compare_bool_var[compare_clicked] is False:
            compare_bool_var[compare_clicked] = True
            # write if file contents changed and write missing file names.
            print('-- compare file contents set to:', compare_bool_var[compare_clicked], comp_cont_button_var[compare_clicked])
            comp_cont_button_var[compare_clicked].setIcon(QIcon("./image/mode_2.png"))
            comp_cont_button_var[compare_clicked].setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(30, 30, 30);}"""
            )
        elif compare_bool_var[compare_clicked] is True:
            compare_bool_var[compare_clicked] = False
            # write only missing file names and do not compare file contents.
            print('-- compare file contents set to:', compare_bool_var[compare_clicked], comp_cont_button_var[compare_clicked])
            comp_cont_button_var[compare_clicked].setIcon(QIcon("./image/mode_1.png"))
            comp_cont_button_var[compare_clicked].setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(30, 30, 30);}"""
            )

    def stop_thr_funk0(self):
        global thread_var
        print('stopping thread 1')
        timer_thread_var[0].start()
        thread_var[0].stop_thr()

    def stop_thr_funk1(self):
        global thread_var
        print('stopping thread 2')
        timer_thread_var[1].start()
        thread_var[1].stop_thr()

    def stop_thr_funk2(self):
        global thread_var
        print('stopping thread 3')
        timer_thread_var[2].start()
        thread_var[2].stop_thr()

    def stop_thr_funk3(self):
        global thread_var
        print('stopping thread 4')
        timer_thread_var[3].start()
        thread_var[3].stop_thr()

    def stop_thr_funk4(self):
        global thread_var
        print('stopping thread 5')
        timer_thread_var[4].start()
        thread_var[4].stop_thr()

    def stop_thr_funk5(self):
        global thread_var
        print('stopping thread 6')
        timer_thread_var[5].start()
        thread_var[5].stop_thr()


class TSClass0(QThread):  # clears info_label_1 text after x time.
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global path_var, dest_path_var, path_bool_var, dest_path_bool_var, sync_ts_var
        print('-- plugged in ts0')
        sync_ts_var[0].setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 255);
           border:0px solid rgb(0, 0, 0);}"""
        )
        get_conf_funk()
        if path_bool_var[0] == 'ARCHIVE_SOURCE_True' and dest_path_bool_var[0] == 'ARCHIVE_DESTINATION_True':
            print('-- ts0 passed checks')
            ts = datetime.datetime.now().timestamp()
            sync_path = [path_var[0], dest_path_var[0]]
            print('Directory timestamp synchronization for:', path_var[0], '&', dest_path_var[0], 'with Timestamp:', ts)
            i = 0
            for sync_paths in sync_path:
                for dirName, subdirList, fileList in os.walk(sync_path[i]):
                    for fname in fileList:
                        fullpath = os.path.join(dirName, fname)
                        print('sync:', fullpath)
                        os.utime(fullpath, (ts, ts))
                i += 1
        sync_ts_var[0].setStyleSheet(
            """QPushButton{background-color: rgb(255, 255, 0);
           border:0px solid rgb(0, 0, 0);}"""
        )


class TSClass1(QThread):  # clears info_label_1 text after x time.
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global path_var, dest_path_var, path_bool_var, dest_path_bool_var, sync_ts_var
        print('-- plugged in ts1')
        sync_ts_var[1].setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 255);
           border:0px solid rgb(0, 0, 0);}"""
        )
        get_conf_funk()
        print('Source:', path_var[1])
        print('Destination:', dest_path_var[1])
        if path_bool_var[1] == 'DOCUMENT_SOURCE_True' and dest_path_bool_var[1] == 'DOCUMENT_DESTINATION_True':
            print('-- ts1 passed checks')
            ts = datetime.datetime.now().timestamp()
            sync_path = [path_var[1], dest_path_var[1]]
            print('Directory timestamp synchronization for:', path_var[1], '&', dest_path_var[1], 'with Timestamp:', ts)
            i = 0
            for sync_paths in sync_path:
                for dirName, subdirList, fileList in os.walk(sync_path[i]):
                    for fname in fileList:
                        fullpath = os.path.join(dirName, fname)
                        print('sync:', fullpath)
                        os.utime(fullpath, (ts, ts))
                i += 1
        sync_ts_var[1].setStyleSheet(
            """QPushButton{background-color: rgb(255, 255, 0);
           border:0px solid rgb(0, 0, 0);}"""
        )


class TSClass2(QThread):  # clears info_label_1 text after x time.
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global path_var, dest_path_var, path_bool_var, dest_path_bool_var, sync_ts_var
        print('-- plugged in ts2')
        sync_ts_var[2].setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 255);
           border:0px solid rgb(0, 0, 0);}"""
        )
        get_conf_funk()
        print('Source:', path_var[2])
        print('Destination:', dest_path_var[2])
        if path_bool_var[2] == 'MUSIC_SOURCE_True' and dest_path_bool_var[2] == 'MUSIC_DESTINATION_True':
            print('-- ts2 passed checks')
            ts = datetime.datetime.now().timestamp()
            sync_path = [path_var[2], dest_path_var[2]]
            print('Directory timestamp synchronization for:', path_var[2], '&', dest_path_var[2], 'with Timestamp:', ts)
            i = 0
            for sync_paths in sync_path:
                for dirName, subdirList, fileList in os.walk(sync_path[i]):
                    for fname in fileList:
                        fullpath = os.path.join(dirName, fname)
                        print('sync:', fullpath)
                        os.utime(fullpath, (ts, ts))
                i += 1
        sync_ts_var[2].setStyleSheet(
            """QPushButton{background-color: rgb(255, 255, 0);
           border:0px solid rgb(0, 0, 0);}"""
        )


class TSClass3(QThread):  # clears info_label_1 text after x time.
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global path_var, dest_path_var, path_bool_var, dest_path_bool_var, sync_ts_var
        print('-- plugged in ts3')
        sync_ts_var[3].setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 255);
           border:0px solid rgb(0, 0, 0);}"""
        )
        get_conf_funk()
        print('Source:', path_var[3])
        print('Destination:', dest_path_var[3])
        if path_bool_var[3] == 'PICTURE_SOURCE_True' and dest_path_bool_var[3] == 'PICTURE_DESTINATION_True':
            print('-- ts3 passed checks')
            ts = datetime.datetime.now().timestamp()
            sync_path = [path_var[3], dest_path_var[3]]
            print('Directory timestamp synchronization for:', path_var[3], '&', dest_path_var[3], 'with Timestamp:', ts)
            i = 0
            for sync_paths in sync_path:
                for dirName, subdirList, fileList in os.walk(sync_path[i]):
                    for fname in fileList:
                        fullpath = os.path.join(dirName, fname)
                        print('sync:', fullpath)
                        os.utime(fullpath, (ts, ts))
                i += 1
        sync_ts_var[3].setStyleSheet(
            """QPushButton{background-color: rgb(255, 255, 0);
           border:0px solid rgb(0, 0, 0);}"""
        )


class TSClass4(QThread):  # clears info_label_1 text after x time.
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global path_var, dest_path_var, path_bool_var, dest_path_bool_var, sync_ts_var
        print('-- plugged in ts4')
        sync_ts_var[4].setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 255);
           border:0px solid rgb(0, 0, 0);}"""
        )
        get_conf_funk()
        print('Source:', path_var[4])
        print('Destination:', dest_path_var[4])
        if path_bool_var[4] == 'PROGRAMS_SOURCE_True' and dest_path_bool_var[4] == 'PROGRAMS_DESTINATION_True':
            print('-- ts4 passed checks')
            ts = datetime.datetime.now().timestamp()
            sync_path = [path_var[4], dest_path_var[4]]
            print('Directory timestamp synchronization for:', path_var[4], '&', dest_path_var[4], 'with Timestamp:', ts)
            i = 0
            for sync_paths in sync_path:
                for dirName, subdirList, fileList in os.walk(sync_path[i]):
                    for fname in fileList:
                        fullpath = os.path.join(dirName, fname)
                        print('sync:', fullpath)
                        os.utime(fullpath, (ts, ts))
                i += 1
        sync_ts_var[4].setStyleSheet(
            """QPushButton{background-color: rgb(255, 255, 0);
           border:0px solid rgb(0, 0, 0);}"""
        )


class TSClass5(QThread):  # clears info_label_1 text after x time.
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global path_var, dest_path_var, path_bool_var, dest_path_bool_var, sync_ts_var
        print('-- plugged in ts5')
        sync_ts_var[5].setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 255);
           border:0px solid rgb(0, 0, 0);}"""
        )
        get_conf_funk()
        print('Source:', path_var[5])
        print('Destination:', dest_path_var[5])
        if path_bool_var[5] == 'VIDEO_SOURCE_True' and dest_path_bool_var[5] == 'VIDEO_DESTINATION_True':
            print('-- ts5 passed checks')
            ts = datetime.datetime.now().timestamp()
            sync_path = [path_var[5], dest_path_var[5]]
            print('Directory timestamp synchronization for:', path_var[5], '&', dest_path_var[5], 'with Timestamp:', ts)
            i = 0
            for sync_paths in sync_path:
                for dirName, subdirList, fileList in os.walk(sync_path[i]):
                    for fname in fileList:
                        fullpath = os.path.join(dirName, fname)
                        print('sync:', fullpath)
                        os.utime(fullpath, (ts, ts))
                i += 1
        sync_ts_var[5].setStyleSheet(
            """QPushButton{background-color: rgb(255, 255, 0);
           border:0px solid rgb(0, 0, 0);}"""
        )


class TimerClass0(QThread):  # clears info_label_1 text after x time.
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global info_label_1_var
        i = 2
        while i > 0:
            time.sleep(1)
            i -= 1
        info_label_1_var[0].setText('')


class TimerClass1(QThread):  # clears info_label_1 text after x time.
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global info_label_1_var
        i = 2
        while i > 0:
            time.sleep(1)
            i -= 1
        info_label_1_var[1].setText('')


class TimerClass2(QThread):  # clears info_label_1 text after x time.
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global info_label_1_var
        i = 2
        while i > 0:
            time.sleep(1)
            i -= 1
        info_label_1_var[2].setText('')


class TimerClass3(QThread):  # clears info_label_1 text after x time.
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global info_label_1_var
        i = 2
        while i > 0:
            time.sleep(1)
            i -= 1
        info_label_1_var[3].setText('')


class TimerClass4(QThread):  # clears info_label_1 text after x time.
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global info_label_1_var
        i = 2
        while i > 0:
            time.sleep(1)
            i -= 1
        info_label_1_var[4].setText('')


class TimerClass5(QThread):  # clears info_label_1 text after x time.
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global info_label_1_var
        i = 2
        while i > 0:
            time.sleep(1)
            i -= 1
        info_label_1_var[5].setText('')


class ThreadClass0(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global btnx_main_var, img_active_var, img_var, path_var, thread_var, info_label_1_var, timer_thread_var
        global path_bool_var, dest_path_bool_var
        btnx_main_var[0].setIcon(QIcon(img_active_var[0]))
        change_var = False
        get_conf_funk()  # potential simultanious calls to unthreaded funk. call when settings write. here is temp.
        print('ThreadClass0 Source:', path_var[0])
        print('ThreadClass0 Destination:', dest_path_var[0])
        if path_bool_var[0] == 'ARCHIVE_SOURCE_True' and dest_path_bool_var[0] == 'ARCHIVE_DESTINATION_True':
            info_label_1_var[0].setText('reading...')
            cp_var = 0
            for dirName, subdirList, fileList in os.walk(path_var[0]):
                for fname in fileList:
                    fullpath = os.path.join(dirName, fname)
                    t_path = fullpath.replace(path_var[0], '')
                    t_path = dest_path_var[0] + t_path
                    if not fullpath.endswith('.ini'):
                        if not os.path.exists(t_path):
                            print('ThreadClass0 -- copy', fullpath, 'to', t_path)
                            change_var = True
                            try:
                                shutil.copy(fullpath, t_path)
                            except IOError:
                                os.makedirs(os.path.dirname(t_path))
                                shutil.copy(fullpath, t_path)
                            cp_var += 1
                        elif os.path.exists(t_path):
                            if compare_bool_var[0] is True:
                                ma = os.path.getmtime(fullpath)
                                mb = os.path.getmtime(t_path)
                                if ma != mb:
                                    print('ThreadClass0 -- copy', fullpath, ma, 'to', t_path, mb)
                                    change_var = True
                                    try:
                                        shutil.copy(fullpath, t_path)
                                    except IOError:
                                        os.makedirs(os.path.dirname(t_path))
                                        shutil.copy(fullpath, t_path)
                                    cp_var += 1
            print('ThreadClass0 -- files copied:', cp_var)
            if change_var is False:
                info_label_1_var[0].setText('unnecessary.')
            elif change_var is True:
                info_label_1_var[0].setText('amended.')
        else:
            info_label_1_var[0].setText('path error!')
        timer_thread_var[0].start()
        btnx_main_var[0].setIcon(QIcon(img_var[0]))

    def stop_thr(self):
        global btnx_main_var, info_label_1_var
        btnx_main_var[0].setIcon(QIcon(img_var[0]))
        info_label_1_var[0].setText('aborted.')
        self.terminate()


class ThreadClass1(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global btnx_main_var, img_active_var, img_var, path_var, thread_var, info_label_1_var, timer_thread_var
        global path_bool_var, dest_path_bool_var
        btnx_main_var[1].setIcon(QIcon(img_active_var[1]))
        change_var = False
        get_conf_funk()
        print('ThreadClass1 Source:', path_var[1])
        print('ThreadClass1 Destination:', dest_path_var[1])
        if path_bool_var[1] == 'DOCUMENT_SOURCE_True' and dest_path_bool_var[1] == 'DOCUMENT_DESTINATION_True':
            info_label_1_var[1].setText('reading...')
            cp_var = 0
            for dirName, subdirList, fileList in os.walk(path_var[1]):
                for fname in fileList:
                    fullpath = os.path.join(dirName, fname)
                    t_path = fullpath.replace(path_var[1], '')
                    t_path = dest_path_var[1] + t_path
                    if not fullpath.endswith('.ini'):
                        if not os.path.exists(t_path):
                            print('ThreadClass1 -- copy', fullpath, 'to', t_path)
                            change_var = True
                            try:
                                shutil.copy(fullpath, t_path)
                            except IOError:
                                os.makedirs(os.path.dirname(t_path))
                                shutil.copy(fullpath, t_path)
                            cp_var += 1
                        elif os.path.exists(t_path):
                            if compare_bool_var[1] is True:
                                ma = os.path.getmtime(fullpath)
                                mb = os.path.getmtime(t_path)
                                if ma != mb:
                                    print('ThreadClass1 -- copy', fullpath, ma, 'to', t_path, mb)
                                    change_var = True
                                    try:
                                        shutil.copy(fullpath, t_path)
                                    except IOError:
                                        os.makedirs(os.path.dirname(t_path))
                                        shutil.copy(fullpath, t_path)
                                    cp_var += 1
            print('ThreadClass1 -- files copied:', cp_var)
            if change_var is False:
                info_label_1_var[1].setText('unnecessary.')
            elif change_var is True:
                info_label_1_var[1].setText('amended.')
        else:
            info_label_1_var[1].setText('path error!')
        timer_thread_var[1].start()
        btnx_main_var[1].setIcon(QIcon(img_var[1]))

    def stop_thr(self):
        global btnx_main_var, info_label_1_var
        btnx_main_var[1].setIcon(QIcon(img_var[1]))
        info_label_1_var[1].setText('aborted.')
        self.terminate()


class ThreadClass2(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global btnx_main_var, img_active_var, img_var, path_var, thread_var, info_label_1_var, timer_thread_var
        global path_bool_var, dest_path_bool_var
        btnx_main_var[2].setIcon(QIcon(img_active_var[2]))
        change_var = False
        get_conf_funk()
        print('ThreadClass2 Source:', path_var[2])
        print('ThreadClass2 Destination:', dest_path_var[2])
        if path_bool_var[2] == 'MUSIC_SOURCE_True' and dest_path_bool_var[2] == 'MUSIC_DESTINATION_True':
            info_label_1_var[2].setText('reading...')
            cp_var = 0
            for dirName, subdirList, fileList in os.walk(path_var[2]):
                for fname in fileList:
                    fullpath = os.path.join(dirName, fname)
                    t_path = fullpath.replace(path_var[2], '')
                    t_path = dest_path_var[2] + t_path
                    if not fullpath.endswith('.ini'):
                        if not os.path.exists(t_path):
                            print('ThreadClass2 -- copy', fullpath, 'to', t_path)
                            change_var = True
                            try:
                                shutil.copy(fullpath, t_path)
                            except IOError:
                                os.makedirs(os.path.dirname(t_path))
                                shutil.copy(fullpath, t_path)
                            cp_var += 1
                        elif os.path.exists(t_path):
                            if compare_bool_var[2] is True:
                                ma = os.path.getmtime(fullpath)
                                mb = os.path.getmtime(t_path)
                                if ma != mb:
                                    print('ThreadClass2 -- copy', fullpath, ma, 'to', t_path, mb)
                                    change_var = True
                                    try:
                                        shutil.copy(fullpath, t_path)
                                    except IOError:
                                        os.makedirs(os.path.dirname(t_path))
                                        shutil.copy(fullpath, t_path)
                                    cp_var += 1
            print('ThreadClass2 -- files copied:', cp_var)
            if change_var is False:
                info_label_1_var[2].setText('unnecessary.')
            elif change_var is True:
                info_label_1_var[2].setText('amended.')
        else:
            info_label_1_var[2].setText('path error!')
        timer_thread_var[2].start()
        btnx_main_var[2].setIcon(QIcon(img_var[2]))

    def stop_thr(self):
        global btnx_main_var, info_label_1_var
        btnx_main_var[2].setIcon(QIcon(img_var[2]))
        info_label_1_var[2].setText('aborted.')
        self.terminate()


class ThreadClass3(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global btnx_main_var, img_active_var, img_var, path_var, thread_var, info_label_1_var, timer_thread_var
        global path_bool_var, dest_path_bool_var
        btnx_main_var[3].setIcon(QIcon(img_active_var[3]))
        change_var = False
        get_conf_funk()
        print('ThreadClass3 Source:', path_var[3])
        print('ThreadClass3 Destination:', dest_path_var[3])
        if path_bool_var[3] == 'PICTURE_SOURCE_True' and dest_path_bool_var[3] == 'PICTURE_DESTINATION_True':
            info_label_1_var[3].setText('reading...')
            cp_var = 0
            for dirName, subdirList, fileList in os.walk(path_var[3]):
                for fname in fileList:
                    fullpath = os.path.join(dirName, fname)
                    t_path = fullpath.replace(path_var[3], '')
                    t_path = dest_path_var[3] + t_path
                    if not fullpath.endswith('.ini'):
                        if not os.path.exists(t_path):
                            print('ThreadClass3 -- copy', fullpath, 'to', t_path)
                            change_var = True
                            try:
                                shutil.copy(fullpath, t_path)
                            except IOError:
                                os.makedirs(os.path.dirname(t_path))
                                shutil.copy(fullpath, t_path)
                            cp_var += 1
                        elif os.path.exists(t_path):
                            if compare_bool_var[3] is True:
                                ma = os.path.getmtime(fullpath)
                                mb = os.path.getmtime(t_path)
                                if ma != mb:
                                    print('ThreadClass3 -- copy', fullpath, ma, 'to', t_path, mb)
                                    change_var = True
                                    try:
                                        shutil.copy(fullpath, t_path)
                                    except IOError:
                                        os.makedirs(os.path.dirname(t_path))
                                        shutil.copy(fullpath, t_path)
                                    cp_var += 1
            print('ThreadClass3 -- files copied:', cp_var)
            if change_var is False:
                info_label_1_var[3].setText('unnecessary.')
            elif change_var is True:
                info_label_1_var[3].setText('amended.')
        else:
            info_label_1_var[3].setText('path error!')
        timer_thread_var[3].start()
        btnx_main_var[3].setIcon(QIcon(img_var[3]))

    def stop_thr(self):
        global btnx_main_var, info_label_1_var
        btnx_main_var[3].setIcon(QIcon(img_var[3]))
        info_label_1_var[3].setText('aborted.')
        self.terminate()


class ThreadClass4(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global btnx_main_var, img_active_var, img_var, path_var, thread_var, info_label_1_var, timer_thread_var
        global path_bool_var, dest_path_bool_var
        btnx_main_var[4].setIcon(QIcon(img_active_var[4]))
        change_var = False
        get_conf_funk()
        print('ThreadClass4 Source:', path_var[4])
        print('ThreadClass4 Destination:', dest_path_var[4])
        if path_bool_var[4] == 'PROGRAMS_SOURCE_True' and dest_path_bool_var[4] == 'PROGRAMS_DESTINATION_True':
            info_label_1_var[4].setText('reading...')
            cp_var = 0
            for dirName, subdirList, fileList in os.walk(path_var[4]):
                for fname in fileList:
                    fullpath = os.path.join(dirName, fname)
                    t_path = fullpath.replace(path_var[4], '')
                    t_path = dest_path_var[4] + t_path
                    if not fullpath.endswith('.ini'):
                        if not os.path.exists(t_path):
                            print('ThreadClass4 -- copy', fullpath, 'to', t_path)
                            change_var = True
                            try:
                                shutil.copy(fullpath, t_path)
                            except IOError:
                                os.makedirs(os.path.dirname(t_path))
                                shutil.copy(fullpath, t_path)
                            cp_var += 1
                        elif os.path.exists(t_path):
                            if compare_bool_var[4] is True:
                                ma = os.path.getmtime(fullpath)
                                mb = os.path.getmtime(t_path)
                                if ma != mb:
                                    print('ThreadClass4 -- copy', fullpath, ma, 'to', t_path, mb)
                                    change_var = True
                                    try:
                                        shutil.copy(fullpath, t_path)
                                    except IOError:
                                        os.makedirs(os.path.dirname(t_path))
                                        shutil.copy(fullpath, t_path)
                                    cp_var += 1
            print('ThreadClass4 -- files copied:', cp_var)
            if change_var is False:
                info_label_1_var[4].setText('unnecessary.')
            elif change_var is True:
                info_label_1_var[4].setText('amended.')
        else:
            info_label_1_var[4].setText('path error!')
        timer_thread_var[4].start()
        btnx_main_var[4].setIcon(QIcon(img_var[4]))

    def stop_thr(self):
        global btnx_main_var, info_label_1_var
        btnx_main_var[4].setIcon(QIcon(img_var[4]))
        info_label_1_var[4].setText('aborted.')
        self.terminate()


class ThreadClass5(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global btnx_main_var, img_active_var, img_var, path_var, thread_var, info_label_1_var, timer_thread_var
        global path_bool_var, dest_path_bool_var
        btnx_main_var[5].setIcon(QIcon(img_active_var[5]))
        change_var = False
        get_conf_funk()
        print('ThreadClass5 Source:', path_var[5])
        print('ThreadClass5 Destination:', dest_path_var[5])
        if path_bool_var[5] == 'VIDEO_SOURCE_True' and dest_path_bool_var[5] == 'VIDEO_DESTINATION_True':
            info_label_1_var[5].setText('reading...')
            cp_var = 0
            for dirName, subdirList, fileList in os.walk(path_var[5]):
                for fname in fileList:
                    fullpath = os.path.join(dirName, fname)
                    t_path = fullpath.replace(path_var[5], '')
                    t_path = dest_path_var[5] + t_path
                    if not fullpath.endswith('.ini'):
                        if not os.path.exists(t_path):
                            print('ThreadClass5 -- copy', fullpath, 'to', t_path)
                            change_var = True
                            try:
                                shutil.copy(fullpath, t_path)
                            except IOError:
                                os.makedirs(os.path.dirname(t_path))
                                shutil.copy(fullpath, t_path)
                            cp_var += 1
                        elif os.path.exists(t_path):
                            if compare_bool_var[5] is True:
                                ma = os.path.getmtime(fullpath)
                                mb = os.path.getmtime(t_path)
                                if ma != mb:
                                    print('ThreadClass5 -- copy', fullpath, ma, 'to', t_path, mb)
                                    change_var = True
                                    try:
                                        shutil.copy(fullpath, t_path)
                                    except IOError:
                                        os.makedirs(os.path.dirname(t_path))
                                        shutil.copy(fullpath, t_path)
                                    cp_var += 1
            print('ThreadClass5 -- files copied:', cp_var)
            if change_var is False:
                info_label_1_var[5].setText('unnecessary.')
            elif change_var is True:
                info_label_1_var[5].setText('amended.')
        else:
            info_label_1_var[5].setText('path error!')
        timer_thread_var[5].start()
        btnx_main_var[5].setIcon(QIcon(img_var[5]))

    def stop_thr(self):
        global btnx_main_var, info_label_1_var
        btnx_main_var[5].setIcon(QIcon(img_var[5]))
        info_label_1_var[5].setText('aborted.')
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
