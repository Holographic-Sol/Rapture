import os
import sys
import time
import shutil
import win32api
import win32process
import win32con
from win32api import GetSystemMetrics
from PyQt5.QtCore import Qt, QThread, QSize, QTimer, QPoint, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont, QPixmap

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

priority_classes = [win32process.IDLE_PRIORITY_CLASS,
                   win32process.BELOW_NORMAL_PRIORITY_CLASS,
                   win32process.NORMAL_PRIORITY_CLASS,
                   win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                   win32process.HIGH_PRIORITY_CLASS,
                   win32process.REALTIME_PRIORITY_CLASS]
pid = win32api.GetCurrentProcessId()
handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
win32process.SetPriorityClass(handle, priority_classes[4])

settings_input_response_thread = ()
update_settings_window_thread = ()
thread_var = [(), (), (), (), (), ()]
timer_thread_var = [(), (), (), (), (), ()]

source_path_entered = ''
dest_path_entered = ''

settings_input_response_source_bool = None
settings_input_response_dest_bool = None
configuration_engaged = False
settings_active = False
compare_bool_var = [False, False, False, False, False, False]
confirm_op0_bool = False
confirm_op0_wait = True
confirm_op1_bool = False
confirm_op1_wait = True
confirm_op2_bool = False
confirm_op2_wait = True
confirm_op3_bool = False
confirm_op3_wait = True
confirm_op4_bool = False
confirm_op4_wait = True
confirm_op5_bool = False
confirm_op5_wait = True

source_selected = ()
dest_selected = ()
settings_active_int = 0
settings_active_int_prev = ()
pressed_int = ()
compare_clicked = ()
back_label_ankor_w0 = ()
back_label_ankor_h0 = ()

path_var = []
dest_path_var = []
path_bool_var = []
dest_path_bool_var = []
btnx_main_var = []
info_label_1_var = []
stop_thr_button_var = []
comp_cont_button_var = []
back_label_var = []
btnx_settings_var = []
settings_source_edit_var = []
settings_dest_edit_var = []
settings_input_response_label = [(), ()]

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
background_img = ['./image/background_img_black_label_0.png',
                  './image/background_img_black_label_1.png']
img_var = ['./image/img_archives.png',
           './image/img_document.png',
           './image/img_music.png',
           './image/img_pictures.png',
           './image/img_program.png',
           './image/img_video.png']
img_active_var = ['./image/img_archives_active.png',
                  './image/img_document_active.png',
                  './image/img_music_active.png',
                  './image/img_pictures_active.png',
                  './image/img_program_active.png',
                  './image/img_video_active.png']
small_image = ['./image/small_img_menu_down.png',
               './image/small_img_menu_up.png',
               './image/small_img_menu_left.png',
               './image/small_img_menu_right.png',
               './image/small_img_mode_0.png',
               './image/small_img_mode_1.png',
               './image/small_img_read_ony_false.png',
               './image/small_img_read_ony_true.png',
               './image/small_img_stop_thread.png']

# Read Configuration File
def get_conf_funk():
    global path_var, path_bool_var, dest_path_var, dest_path_bool_var
    path_var = []
    path_bool_var = []
    dest_path_var = []
    dest_path_bool_var = []
    if os.path.exists('config.txt'):
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
                                if (primary_key + '_True') not in path_bool_var:
                                    path_var.append(secondary_key)
                                    path_bool_var.append(primary_key + '_True')
                                    print(primary_key + '_True')
                            elif not os.path.exists(secondary_key):
                                if (primary_key + '_False') not in path_bool_var:
                                    path_var.append('')
                                    path_bool_var.append(primary_key + '_False')
                                    print(primary_key + '_False')
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
                            elif not os.path.exists(secondary_key):
                                if (primary_key + '_False') not in dest_path_bool_var:
                                    dest_path_var.append('')
                                    dest_path_bool_var.append(primary_key + '_False')
                    i += 1
        fo.close()


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setWindowIcon(QIcon('./icon.png'))
        self.title = 'Rapture Extreme Backup Solution'
        get_conf_funk()
        self.width = 605
        self.height = 110
        scr_w = GetSystemMetrics(0)
        scr_h = GetSystemMetrics(1)
        self.left = (scr_w / 2) - (self.width / 2)
        self.top = ((scr_h / 2) - (self.height / 2))
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setPalette(p)
        self.initUI()

    def initUI(self):
        global thread_var, btnx_main_var, btnx_settings_var, comp_cont_button_var, stop_thr_button_var, info_label_1_var
        global img_var, img_active_var, img_settings, timer_thread_var, settings_input_response_thread
        global path_var, dest_path_var, back_label_var, pressed_int, settings_source_edit_var, settings_dest_edit_var
        global settings_input_response_label, update_settings_window_thread, confirm_op0_bool, confirm_op0_wait
        global confirm_op1_bool, confirm_op1_wait, confirm_op2_bool, confirm_op2_wait, confirm_op3_bool, confirm_op3_wait
        global confirm_op4_bool, confirm_op4_wait, confirm_op5_bool, confirm_op5_wait

        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        # Font Setup. Cambria Math, Candara, Consolas, Corbel, Segoe UI
        font_s6 = QFont("Segoe UI", 6, QFont.Normal)
        font_s8 = QFont("Segoe UI", 8, QFont.Normal)

        # Title Bar: Close
        self.close_button = QPushButton(self)
        self.close_button.move((self.width - 20), 0)
        self.close_button.resize(20, 20)
        self.close_button.setIcon(QIcon("./image/img_close.png"))
        self.close_button.setIconSize(QSize(8, 8))
        self.close_button.clicked.connect(QCoreApplication.instance().quit)
        self.close_button.setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 0, 0);}"""
               )

        # Title Bar: Minimize
        self.minimize_button = QPushButton(self)
        self.minimize_button.move((self.width - 50), 0)
        self.minimize_button.resize(20, 20)
        self.minimize_button.setIcon(QIcon("./image/img_minimize.png"))
        self.minimize_button.setIconSize(QSize(50, 20))
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 0, 0);}"""
               )

        # Sector 2: File Path Validation LED Source
        self.settings_input_response_label_src = QLabel(self)
        self.settings_input_response_label_src.move(550, 135)
        self.settings_input_response_label_src.resize(5, 15)
        self.settings_input_response_label_src.setStyleSheet(
            """QLabel {background-color: rgb(15, 15, 15);
           border:1px solid rgb(15, 15, 15);}"""
           )
        settings_input_response_label[0] = self.settings_input_response_label_src

        # Sector 2: File Path Validation LED Destination
        self.settings_input_response_label_dst = QLabel(self)
        self.settings_input_response_label_dst.move(550, 155)
        self.settings_input_response_label_dst.resize(5, 15)
        self.settings_input_response_label_dst.setStyleSheet(
            """QLabel {background-color: rgb(15, 15, 15);
           border:1px solid rgb(15, 15, 15);}"""
           )
        settings_input_response_label[1] = self.settings_input_response_label_dst

        # Sector 1: Background Colour
        self.back_label_main = QLabel(self)
        self.back_label_main.move(0, 20)
        self.back_label_main.resize(self.width, 90)
        self.back_label_main.setStyleSheet(
            """QLabel {background-color: rgb(30, 30, 30);
           border:0px solid rgb(35, 35, 35);}"""
           )

        # Sector 1: Background Tiles
        i = 0
        while i < 6:
            back_label = 'back_label' + str(i)
            self.back_label = QLabel(self)
            self.back_label.resize(95, 80)
            pixmap = QPixmap(background_img[0])
            self.back_label.setPixmap(pixmap)
            self.back_label.setStyleSheet(
                """QLabel {background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 0, 0);}"""
               )
            back_label_var.append(self.back_label)
            i += 1

        # Sector 1: Background Tiles Positions W
        back_label_ankor_w0 = 5
        back_label_ankor_w1 = 105
        back_label_ankor_w2 = 205
        back_label_ankor_w3 = 305
        back_label_ankor_w4 = 405
        back_label_ankor_w5 = 505

        # Sector 1: Background Tiles Positions H
        back_label_ankor_h0 = 25
        back_label_ankor_h1 = 25
        back_label_ankor_h2 = 25
        back_label_ankor_h3 = 25
        back_label_ankor_h4 = 25
        back_label_ankor_h5 = 25

        # Sector 1: Background Tiles Moved Into Positions, W & H
        back_label_var[0].move(back_label_ankor_w0, back_label_ankor_h0)
        back_label_var[1].move(back_label_ankor_w1, back_label_ankor_h1)
        back_label_var[2].move(back_label_ankor_w2, back_label_ankor_h2)
        back_label_var[3].move(back_label_ankor_w3, back_label_ankor_h3)
        back_label_var[4].move(back_label_ankor_w4, back_label_ankor_h4)
        back_label_var[5].move(back_label_ankor_w5, back_label_ankor_h5)

        # Sector 1: Objects Placed On Top Background Tiles
        i = 0
        while i < 6:

            # Sector 1: Main Function Button(s)
            btnx_name = 'btnx_main' + str(i)
            self.btnx_main = QPushButton(self)
            self.btnx_main.resize(54, 54)
            self.btnx_main.setIcon(QIcon(img_var[i]))
            self.btnx_main.setIconSize(QSize(54, 54))
            self.btnx_main.setStyleSheet(
                    """QPushButton{background-color: rgb(0, 0, 0);
                   border:0px solid rgb(0, 0, 0);}"""
                   )
            btnx_main_var.append(self.btnx_main)

            # Sector 1: Drop Down Setting's Button(s)
            sett_name = 'btnx_settings' + str(i)
            self.sett_name = QPushButton(self)
            self.sett_name.resize(30, 10)
            self.sett_name.setIcon(QIcon(small_image[0]))
            self.sett_name.setIconSize(QSize(15, 15))
            self.sett_name.setStyleSheet(
                """QPushButton{background-color: rgb(35, 35, 35);
               border:0px solid rgb(0, 0, 0);}"""
               )
            btnx_settings_var.append(self.sett_name)

            # Sector 1: Switch Main Function Mode Button(s)
            comp_cont_button = 'comp_cont_button' + str(i)
            self.comp_cont_button = QPushButton(self)
            self.comp_cont_button.resize(30, 26)
            self.comp_cont_button.setIcon(QIcon(small_image[4]))
            self.comp_cont_button.setIconSize(QSize(18, 18))
            self.comp_cont_button.setStyleSheet(
                """QPushButton{background-color: rgb(35, 35, 35);
               border:0px solid rgb(0, 0, 0);}"""
               )
            comp_cont_button_var.append(self.comp_cont_button)

            # Sector 1: Stop Main Functions(s) Button(s)
            stop_thr_button = 'stop_thr_button' + str(i)
            self.stop_thr_button = QPushButton(self)
            self.stop_thr_button.resize(30, 10)
            self.stop_thr_button.setIcon(QIcon(small_image[8]))
            self.stop_thr_button.setIconSize(QSize(15, 15))
            self.stop_thr_button.setStyleSheet(
                """QPushButton{background-color: rgb(35, 35, 35);
               border:0px solid rgb(35, 35, 35);}"""
               )
            stop_thr_button_var.append(self.stop_thr_button)

            # Sector 1: Main Function(s) Output Label(s)
            info_label_1 = 'info_label_1' + str(i)
            self.info_label_1 = QLabel(self)
            self.info_label_1.resize(85, 15)
            self.info_label_1.setFont(font_s6)
            self.info_label_1.setText("")
            self.info_label_1.setStyleSheet(
                """QLabel {background-color: rgb(0, 0, 0);
               color: green;
               border:0px solid rgb(35, 35, 35);}"""
               )
            info_label_1_var.append(self.info_label_1)

            i += 1

        # Sector 2: Hide Drop Down Settings
        self.hide_settings_button = QPushButton(self)
        self.hide_settings_button.resize(self.width, 10)
        self.hide_settings_button.move(0, 180)
        self.hide_settings_button.setIcon(QIcon(small_image[1]))
        self.hide_settings_button.clicked.connect(self.hide_settings_page_funk)
        self.hide_settings_button.setIconSize(QSize(15, 15))
        self.hide_settings_button.setStyleSheet(
            """QPushButton{background-color: rgb(35, 35, 35);
           border:0px solid rgb(0, 0, 0);}"""
           )

        # Sector 2: Enable/Disable ReadOnly Path Settings
        self.paths_readonly_button = QPushButton(self)
        self.paths_readonly_button.resize(15, 35)
        self.paths_readonly_button.move(560, 135)
        self.paths_readonly_button.setIcon(QIcon(small_image[7]))
        self.paths_readonly_button.setIconSize(QSize(15, 35))
        self.paths_readonly_button.clicked.connect(self.paths_readonly_funk)
        self.paths_readonly_button.setStyleSheet(
            """QPushButton{background-color: rgb(35, 35, 35);
           border:0px solid rgb(0, 0, 0);}"""
           )

        # Sector 2: Settings Page Left
        self.scr_left = QPushButton(self)
        self.scr_left.resize(10, 35)
        self.scr_left.move(0, 135)
        self.scr_left.setIcon(QIcon(small_image[2]))
        self.scr_left.setIconSize(QSize(15, 35))
        self.scr_left.clicked.connect(self.scr_left_funk)
        self.scr_left.setStyleSheet(
            """QPushButton{background-color: rgb(35, 35, 35);
           border:0px solid rgb(0, 0, 0);}"""
           )

        # Sector 2: Settings Page Right
        self.scr_right = QPushButton(self)
        self.scr_right.resize(10, 35)
        self.scr_right.move((self.width - 10), 135)
        self.scr_right.setIcon(QIcon(small_image[3]))
        self.scr_right.setIconSize(QSize(15, 35))
        self.scr_right.clicked.connect(self.scr_right_funk)
        self.scr_right.setStyleSheet(
            """QPushButton{background-color: rgb(35, 35, 35);
           border:0px solid rgb(0, 0, 0);}"""
           )

        # Sector 2: A Label To Signify Source Path Configuration
        self.settings_source_label = QLabel(self)
        self.settings_source_label.move(30, 135)
        self.settings_source_label.resize(60, 15)
        self.settings_source_label.setFont(font_s6)
        self.settings_source_label.setText('Source:')
        self.settings_source_label.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
           )

        # Sector 2: A Label To Signify Destination Path Configuration
        self.settings_dest_label = QLabel(self)
        self.settings_dest_label.move(30, 155)
        self.settings_dest_label.resize(60, 15)
        self.settings_dest_label.setFont(font_s6)
        self.settings_dest_label.setText('Destination:')
        self.settings_dest_label.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
           )

        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 0
        self.setting_title0 = QLabel(self)
        self.setting_title0.resize(605, 15)
        self.setting_title0.move(back_label_ankor_w0, 115)
        self.setting_title0.setFont(font_s6)
        self.setting_title0.setText("Archive")
        self.setting_title0.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
           )
        self.setting_title0.hide()

        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 1
        self.setting_title1 = QLabel(self)
        self.setting_title1.resize(605, 15)
        self.setting_title1.move(back_label_ankor_w1, 115)
        self.setting_title1.setFont(font_s6)
        self.setting_title1.setText("Document")
        self.setting_title1.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
           )

        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 2
        self.setting_title1.hide()
        self.setting_title2 = QLabel(self)
        self.setting_title2.resize(605, 15)
        self.setting_title2.move(back_label_ankor_w2, 115)
        self.setting_title2.setFont(font_s6)
        self.setting_title2.setText("Music")
        self.setting_title2.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
           )

        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 3
        self.setting_title2.hide()
        self.setting_title3 = QLabel(self)
        self.setting_title3.resize(605, 15)
        self.setting_title3.move(back_label_ankor_w3, 115)
        self.setting_title3.setFont(font_s6)
        self.setting_title3.setText("Picture")
        self.setting_title3.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
           )

        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 4
        self.setting_title3.hide()
        self.setting_title4 = QLabel(self)
        self.setting_title4.resize(605, 15)
        self.setting_title4.move(back_label_ankor_w4, 115)
        self.setting_title4.setFont(font_s6)
        self.setting_title4.setText("Program")
        self.setting_title4.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
           )

        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 5
        self.setting_title4.hide()
        self.setting_title5 = QLabel(self)
        self.setting_title5.resize(605, 15)
        self.setting_title5.move(back_label_ankor_w5, 115)
        self.setting_title5.setFont(font_s6)
        self.setting_title5.setText("Video")
        self.setting_title5.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: green;
           border:0px solid rgb(35, 35, 35);}"""
           )
        self.setting_title5.hide()

        set_src_dst_w = 450
        set_src_dst_pos_w = 95

        # Sector 2: Source Path Configuration Edit 0
        self.settings_source0 = QLineEdit(self)
        self.settings_source0.move(set_src_dst_pos_w, 135)
        self.settings_source0.resize(set_src_dst_w, 15)
        self.settings_source0.setFont(font_s6)
        self.settings_source0.setText(path_var[0])
        self.settings_source0.setReadOnly(True)
        self.settings_source0.returnPressed.connect(self.settings_source_pre_funk0)
        self.settings_source0.setStyleSheet(
            """QLineEdit {background-color: rgb(10, 10, 10);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
            )
        settings_source_edit_var.append(self.settings_source0)
        self.settings_source0.hide()

        # Sector 2: Source Path Configuration Edit 1
        self.settings_source1 = QLineEdit(self)
        self.settings_source1.move(set_src_dst_pos_w, 135)
        self.settings_source1.resize(set_src_dst_w, 15)
        self.settings_source1.setFont(font_s6)
        self.settings_source1.setText(path_var[1])
        self.settings_source1.setReadOnly(True)
        self.settings_source1.returnPressed.connect(self.settings_source_pre_funk1)
        self.settings_source1.setStyleSheet(
            """QLineEdit {background-color: rgb(10, 10, 10);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
            )
        settings_source_edit_var.append(self.settings_source1)
        self.settings_source1.hide()

        # Sector 2: Source Path Configuration Edit 2
        self.settings_source2 = QLineEdit(self)
        self.settings_source2.move(set_src_dst_pos_w, 135)
        self.settings_source2.resize(set_src_dst_w, 15)
        self.settings_source2.setFont(font_s6)
        self.settings_source2.setText(path_var[2])
        self.settings_source2.setReadOnly(True)
        self.settings_source2.returnPressed.connect(self.settings_source_pre_funk2)
        self.settings_source2.setStyleSheet(
            """QLineEdit {background-color: rgb(10, 10, 10);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
            )
        settings_source_edit_var.append(self.settings_source2)
        self.settings_source2.hide()

        # Sector 2: Source Path Configuration Edit 3
        self.settings_source3 = QLineEdit(self)
        self.settings_source3.move(set_src_dst_pos_w, 135)
        self.settings_source3.resize(set_src_dst_w, 15)
        self.settings_source3.setFont(font_s6)
        self.settings_source3.setText(path_var[3])
        self.settings_source3.setReadOnly(True)
        self.settings_source3.returnPressed.connect(self.settings_source_pre_funk3)
        self.settings_source3.setStyleSheet(
            """QLineEdit {background-color: rgb(10, 10, 10);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
            )
        settings_source_edit_var.append(self.settings_source3)
        self.settings_source3.hide()

        # Sector 2: Source Path Configuration Edit 4
        self.settings_source4 = QLineEdit(self)
        self.settings_source4.move(set_src_dst_pos_w, 135)
        self.settings_source4.resize(set_src_dst_w, 15)
        self.settings_source4.setFont(font_s6)
        self.settings_source4.setText(path_var[4])
        self.settings_source4.setReadOnly(True)
        self.settings_source4.returnPressed.connect(self.settings_source_pre_funk4)
        self.settings_source4.setStyleSheet(
            """QLineEdit {background-color: rgb(10, 10, 10);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
            )
        settings_source_edit_var.append(self.settings_source4)
        self.settings_source4.hide()

        # Sector 2: Source Path Configuration Edit 5
        self.settings_source5 = QLineEdit(self)
        self.settings_source5.move(set_src_dst_pos_w, 135)
        self.settings_source5.resize(set_src_dst_w, 15)
        self.settings_source5.setFont(font_s6)
        self.settings_source5.setText(path_var[5])
        self.settings_source5.setReadOnly(True)
        self.settings_source5.returnPressed.connect(self.settings_source_pre_funk5)
        self.settings_source5.setStyleSheet(
            """QLineEdit {background-color: rgb(10, 10, 10);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
            )
        settings_source_edit_var.append(self.settings_source5)
        self.settings_source5.hide()

        # Sector 2: Destination Path Configuration Edit 0
        self.settings_dest0 = QLineEdit(self)
        self.settings_dest0.move(set_src_dst_pos_w, 155)
        self.settings_dest0.resize(set_src_dst_w, 15)
        self.settings_dest0.setFont(font_s6)
        self.settings_dest0.setText(dest_path_var[0])
        self.settings_dest0.setReadOnly(True)
        self.settings_dest0.returnPressed.connect(self.settings_dest_pre_funk0)
        self.settings_dest0.setStyleSheet(
            """QLineEdit {background-color: rgb(10, 10, 10);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
            )
        settings_dest_edit_var.append(self.settings_dest0)
        self.settings_dest0.hide()

        # Sector 2: Destination Path Configuration Edit 1
        self.settings_dest1 = QLineEdit(self)
        self.settings_dest1.move(set_src_dst_pos_w, 155)
        self.settings_dest1.resize(set_src_dst_w, 15)
        self.settings_dest1.setFont(font_s6)
        self.settings_dest1.setText(dest_path_var[1])
        self.settings_dest1.setReadOnly(True)
        self.settings_dest1.returnPressed.connect(self.settings_dest_pre_funk1)
        self.settings_dest1.setStyleSheet(
            """QLineEdit {background-color: rgb(10, 10, 10);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
            )
        settings_dest_edit_var.append(self.settings_dest1)
        self.settings_dest1.hide()

        # Sector 2: Destination Path Configuration Edit 2
        self.settings_dest2 = QLineEdit(self)
        self.settings_dest2.move(set_src_dst_pos_w, 155)
        self.settings_dest2.resize(set_src_dst_w, 15)
        self.settings_dest2.setFont(font_s6)
        self.settings_dest2.setText(dest_path_var[2])
        self.settings_dest2.setReadOnly(True)
        self.settings_dest2.returnPressed.connect(self.settings_dest_pre_funk2)
        self.settings_dest2.setStyleSheet(
            """QLineEdit {background-color: rgb(10, 10, 10);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
            )
        settings_dest_edit_var.append(self.settings_dest2)
        self.settings_dest2.hide()

        # Sector 2: Destination Path Configuration Edit 3
        self.settings_dest3 = QLineEdit(self)
        self.settings_dest3.move(set_src_dst_pos_w, 155)
        self.settings_dest3.resize(set_src_dst_w, 15)
        self.settings_dest3.setFont(font_s6)
        self.settings_dest3.setText(dest_path_var[3])
        self.settings_dest3.setReadOnly(True)
        self.settings_dest3.returnPressed.connect(self.settings_dest_pre_funk3)
        self.settings_dest3.setStyleSheet(
            """QLineEdit {background-color: rgb(10, 10, 10);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
            )
        settings_dest_edit_var.append(self.settings_dest3)
        self.settings_dest3.hide()

        # Sector 2: Destination Path Configuration Edit 4
        self.settings_dest4 = QLineEdit(self)
        self.settings_dest4.move(set_src_dst_pos_w, 155)
        self.settings_dest4.resize(set_src_dst_w, 15)
        self.settings_dest4.setFont(font_s6)
        self.settings_dest4.setText(dest_path_var[4])
        self.settings_dest4.setReadOnly(True)
        self.settings_dest4.returnPressed.connect(self.settings_dest_pre_funk4)
        self.settings_dest4.setStyleSheet(
            """QLineEdit {background-color: rgb(10, 10, 10);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
            )
        settings_dest_edit_var.append(self.settings_dest4)
        self.settings_dest4.hide()

        # Sector 2: Destination Path Configuration Edit 5
        self.settings_dest5 = QLineEdit(self)
        self.settings_dest5.move(set_src_dst_pos_w, 155)
        self.settings_dest5.resize(set_src_dst_w, 15)
        self.settings_dest5.setFont(font_s6)
        self.settings_dest5.setText(dest_path_var[5])
        self.settings_dest5.setReadOnly(True)
        self.settings_dest5.returnPressed.connect(self.settings_dest_pre_funk5)
        self.settings_dest5.setStyleSheet(
            """QLineEdit {background-color: rgb(10, 10, 10);
            border:0px solid rgb(0, 0, 0);
            selection-color: green;
            selection-background-color: black;
            color: grey;}"""
            )
        settings_dest_edit_var.append(self.settings_dest5)
        self.settings_dest5.hide()

        # Sector 1: Attatch Main Function Buttons To Background Tiles Position
        btnx_main_var[0].move((back_label_ankor_w0 + 5), (back_label_ankor_h0 + 5))
        btnx_main_var[1].move((back_label_ankor_w1 + 5), (back_label_ankor_h1 + 5))
        btnx_main_var[2].move((back_label_ankor_w2 + 5), (back_label_ankor_h2 + 5))
        btnx_main_var[3].move((back_label_ankor_w3 + 5), (back_label_ankor_h3 + 5))
        btnx_main_var[4].move((back_label_ankor_w4 + 5), (back_label_ankor_h4 + 5))
        btnx_main_var[5].move((back_label_ankor_w5 + 5), (back_label_ankor_h5 + 5))

        # Sector 1: Attatch Drop Down Settings Buttons To Background Tiles Position
        btnx_settings_var[0].move((back_label_ankor_w0 + 62), (back_label_ankor_h0 + 49))
        btnx_settings_var[1].move((back_label_ankor_w1 + 62), (back_label_ankor_h1 + 49))
        btnx_settings_var[2].move((back_label_ankor_w2 + 62), (back_label_ankor_h2 + 49))
        btnx_settings_var[3].move((back_label_ankor_w3 + 62), (back_label_ankor_h3 + 49))
        btnx_settings_var[4].move((back_label_ankor_w4 + 62), (back_label_ankor_h4 + 49))
        btnx_settings_var[5].move((back_label_ankor_w5 + 62), (back_label_ankor_h5 + 49))

        # Sector 1: Attatch Main Function Mode Buttons To Background Tiles Position
        comp_cont_button_var[0].move((back_label_ankor_w0 + 62), (back_label_ankor_h0 + 19))
        comp_cont_button_var[1].move((back_label_ankor_w1 + 62), (back_label_ankor_h1 + 19))
        comp_cont_button_var[2].move((back_label_ankor_w2 + 62), (back_label_ankor_h2 + 19))
        comp_cont_button_var[3].move((back_label_ankor_w3 + 62), (back_label_ankor_h3 + 19))
        comp_cont_button_var[4].move((back_label_ankor_w4 + 62), (back_label_ankor_h4 + 19))
        comp_cont_button_var[5].move((back_label_ankor_w5 + 62), (back_label_ankor_h5 + 19))

        # Sector 1: Attatch Stop Main Function Buttons To Background Tiles Position
        stop_thr_button_var[0].move((back_label_ankor_w0 + 62), (back_label_ankor_h0 + 5))
        stop_thr_button_var[1].move((back_label_ankor_w1 + 62), (back_label_ankor_h1 + 5))
        stop_thr_button_var[2].move((back_label_ankor_w2 + 62), (back_label_ankor_h2 + 5))
        stop_thr_button_var[3].move((back_label_ankor_w3 + 62), (back_label_ankor_h3 + 5))
        stop_thr_button_var[4].move((back_label_ankor_w4 + 62), (back_label_ankor_h4 + 5))
        stop_thr_button_var[5].move((back_label_ankor_w5 + 62), (back_label_ankor_h5 + 5))

        # Sector 1: Attatch Main Function Information Output Labels To Background Tiles Position
        info_label_1_var[0].move((back_label_ankor_w0 + 5), (back_label_ankor_h0 + 61))
        info_label_1_var[1].move((back_label_ankor_w1 + 5), (back_label_ankor_h1 + 61))
        info_label_1_var[2].move((back_label_ankor_w2 + 5), (back_label_ankor_h2 + 61))
        info_label_1_var[3].move((back_label_ankor_w3 + 5), (back_label_ankor_h3 + 61))
        info_label_1_var[4].move((back_label_ankor_w4 + 5), (back_label_ankor_h4 + 61))
        info_label_1_var[5].move((back_label_ankor_w5 + 5), (back_label_ankor_h5 + 61))

        # Sector 1: Plug Main Function Mode Buttons Into Functions
        comp_cont_button_var[0].clicked.connect(self.set_comp_bool_pre_funk0)
        comp_cont_button_var[1].clicked.connect(self.set_comp_bool_pre_funk1)
        comp_cont_button_var[2].clicked.connect(self.set_comp_bool_pre_funk2)
        comp_cont_button_var[3].clicked.connect(self.set_comp_bool_pre_funk3)
        comp_cont_button_var[4].clicked.connect(self.set_comp_bool_pre_funk4)
        comp_cont_button_var[5].clicked.connect(self.set_comp_bool_pre_funk5)

        # Sector 1: Plug Stop Main Function Buttons Into Functions
        stop_thr_button_var[0].clicked.connect(self.stop_thr_funk0)
        stop_thr_button_var[1].clicked.connect(self.stop_thr_funk1)
        stop_thr_button_var[2].clicked.connect(self.stop_thr_funk2)
        stop_thr_button_var[3].clicked.connect(self.stop_thr_funk3)
        stop_thr_button_var[4].clicked.connect(self.stop_thr_funk4)
        stop_thr_button_var[5].clicked.connect(self.stop_thr_funk5)

        # Sector 1: Plug Main Function Buttons Into Main Function Button Threads
        btnx_main_var[0].clicked.connect(self.thread_funk_0)
        btnx_main_var[1].clicked.connect(self.thread_funk_1)
        btnx_main_var[2].clicked.connect(self.thread_funk_2)
        btnx_main_var[3].clicked.connect(self.thread_funk_3)
        btnx_main_var[4].clicked.connect(self.thread_funk_4)
        btnx_main_var[5].clicked.connect(self.thread_funk_5)

        # Sector 1: Plug Main Function Buttons Into Drop Down Settings Functions
        btnx_main_var[0].clicked.connect(self.settings_funk0)
        btnx_main_var[1].clicked.connect(self.settings_funk1)
        btnx_main_var[2].clicked.connect(self.settings_funk2)
        btnx_main_var[3].clicked.connect(self.settings_funk3)
        btnx_main_var[4].clicked.connect(self.settings_funk4)
        btnx_main_var[5].clicked.connect(self.settings_funk5)

        # Sector 1: Plug Drop Down Settings Buttons Into Functions
        btnx_settings_var[0].clicked.connect(self.settings_funk0)
        btnx_settings_var[1].clicked.connect(self.settings_funk1)
        btnx_settings_var[2].clicked.connect(self.settings_funk2)
        btnx_settings_var[3].clicked.connect(self.settings_funk3)
        btnx_settings_var[4].clicked.connect(self.settings_funk4)
        btnx_settings_var[5].clicked.connect(self.settings_funk5)

        # Sector 1: Main Function Confirmation 0
        self.confirm_op0_tru = QPushButton(self)
        self.confirm_op0_tru.resize(40, 15)
        self.confirm_op0_tru.setFont(font_s6)
        self.confirm_op0_tru.setText("Yes")
        self.confirm_op0_tru.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
                border:2px solid rgb(30, 30, 30);
                color: green}"""
                )
        self.confirm_op0_tru.move((back_label_ankor_w0 + 5), (back_label_ankor_h0 + 62))
        self.confirm_op0_tru.clicked.connect(self.confirm_op0_funk0)
        self.confirm_op0_tru.hide()

        # Sector 1: Main Function Declination 0
        self.confirm_op0_fal = QPushButton(self)
        self.confirm_op0_fal.resize(40, 15)
        self.confirm_op0_fal.setFont(font_s6)
        self.confirm_op0_fal.setText("No")
        self.confirm_op0_fal.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
                border:2px solid rgb(30, 30, 30);
                color: green}"""
                )
        self.confirm_op0_fal.move((95 - 38), (back_label_ankor_h0 + 62))
        self.confirm_op0_fal.clicked.connect(self.confirm_op0_funk1)
        self.confirm_op0_fal.hide()

        # Sector 1: Main Function Confirmation 1
        self.confirm_op1_tru = QPushButton(self)
        self.confirm_op1_tru.resize(40, 15)
        self.confirm_op1_tru.setFont(font_s6)
        self.confirm_op1_tru.setText("Yes")
        self.confirm_op1_tru.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
                border:2px solid rgb(30, 30, 30);
                color: green}"""
                )
        self.confirm_op1_tru.move((back_label_ankor_w1 + 5), (back_label_ankor_h1 + 62))
        self.confirm_op1_tru.clicked.connect(self.confirm_op1_funk0)
        self.confirm_op1_tru.hide()

        # Sector 1: Main Function Declination 1
        self.confirm_op1_fal = QPushButton(self)
        self.confirm_op1_fal.resize(40, 15)
        self.confirm_op1_fal.setFont(font_s6)
        self.confirm_op1_fal.setText("No")
        self.confirm_op1_fal.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
                border:2px solid rgb(30, 30, 30);
                color: green}"""
                )
        self.confirm_op1_fal.move((195 - 38), (back_label_ankor_h1 + 62))
        self.confirm_op1_fal.clicked.connect(self.confirm_op1_funk1)
        self.confirm_op1_fal.hide()

        # Sector 1: Main Function Confirmation 2
        self.confirm_op2_tru = QPushButton(self)
        self.confirm_op2_tru.resize(40, 15)
        self.confirm_op2_tru.setFont(font_s6)
        self.confirm_op2_tru.setText("Yes")
        self.confirm_op2_tru.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
                border:2px solid rgb(30, 30, 30);
                color: green}"""
                )
        self.confirm_op2_tru.move((back_label_ankor_w2 + 5), (back_label_ankor_h2 + 62))
        self.confirm_op2_tru.clicked.connect(self.confirm_op2_funk0)
        self.confirm_op2_tru.hide()

        # Sector 1: Main Function Declination 2
        self.confirm_op2_fal = QPushButton(self)
        self.confirm_op2_fal.resize(40, 15)
        self.confirm_op2_fal.setFont(font_s6)
        self.confirm_op2_fal.setText("No")
        self.confirm_op2_fal.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
                border:2px solid rgb(30, 30, 30);
                color: green}"""
                )
        self.confirm_op2_fal.move((295 - 38), (back_label_ankor_h2 + 62))
        self.confirm_op2_fal.clicked.connect(self.confirm_op2_funk1)
        self.confirm_op2_fal.hide()

        # Sector 1: Main Function Confirmation 3
        self.confirm_op3_tru = QPushButton(self)
        self.confirm_op3_tru.resize(40, 15)
        self.confirm_op3_tru.setFont(font_s6)
        self.confirm_op3_tru.setText("Yes")
        self.confirm_op3_tru.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
                border:2px solid rgb(30, 30, 30);
                color: green}"""
                )
        self.confirm_op3_tru.move((back_label_ankor_w3 + 5), (back_label_ankor_h3 + 62))
        self.confirm_op3_tru.clicked.connect(self.confirm_op3_funk0)
        self.confirm_op3_tru.hide()

        # Sector 1: Main Function Declination 3
        self.confirm_op3_fal = QPushButton(self)
        self.confirm_op3_fal.resize(40, 15)
        self.confirm_op3_fal.setFont(font_s6)
        self.confirm_op3_fal.setText("No")
        self.confirm_op3_fal.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
                border:2px solid rgb(30, 30, 30);
                color: green}"""
                )
        self.confirm_op3_fal.move((395 - 38), (back_label_ankor_h3 + 62))
        self.confirm_op3_fal.clicked.connect(self.confirm_op3_funk1)
        self.confirm_op3_fal.hide()

        # Sector 1: Main Function Confirmation 4
        self.confirm_op4_tru = QPushButton(self)
        self.confirm_op4_tru.resize(40, 15)
        self.confirm_op4_tru.setFont(font_s6)
        self.confirm_op4_tru.setText("Yes")
        self.confirm_op4_tru.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
                border:2px solid rgb(30, 30, 30);
                color: green}"""
                )
        self.confirm_op4_tru.move((back_label_ankor_w4 + 5), (back_label_ankor_h4 + 62))
        self.confirm_op4_tru.clicked.connect(self.confirm_op4_funk0)
        self.confirm_op4_tru.hide()

        # Sector 1: Main Function Declination 4
        self.confirm_op4_fal = QPushButton(self)
        self.confirm_op4_fal.resize(40, 15)
        self.confirm_op4_fal.setFont(font_s6)
        self.confirm_op4_fal.setText("No")
        self.confirm_op4_fal.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
                border:2px solid rgb(30, 30, 30);
                color: green}"""
                )
        self.confirm_op4_fal.move((495 - 38), (back_label_ankor_h4 + 62))
        self.confirm_op4_fal.clicked.connect(self.confirm_op4_funk1)
        self.confirm_op4_fal.hide()

        # Sector 1: Main Function Confirmation 5
        self.confirm_op5_tru = QPushButton(self)
        self.confirm_op5_tru.resize(40, 15)
        self.confirm_op5_tru.setFont(font_s6)
        self.confirm_op5_tru.setText("Yes")
        self.confirm_op5_tru.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
                border:2px solid rgb(30, 30, 30);
                color: green}"""
                )
        self.confirm_op5_tru.move((back_label_ankor_w5 + 5), (back_label_ankor_h5 + 62))
        self.confirm_op5_tru.clicked.connect(self.confirm_op5_funk0)
        self.confirm_op5_tru.hide()

        # Sector 1: Main Function Declination 5
        self.confirm_op5_fal = QPushButton(self)
        self.confirm_op5_fal.resize(40, 15)
        self.confirm_op5_fal.setFont(font_s6)
        self.confirm_op5_fal.setText("No")
        self.confirm_op5_fal.setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
                border:2px solid rgb(30, 30, 30);
                color: green}"""
                )
        self.confirm_op5_fal.move((595 - 38), (back_label_ankor_h5 + 62))
        self.confirm_op5_fal.clicked.connect(self.confirm_op5_funk1)
        self.confirm_op5_fal.hide()

        # Thread: Adjusts App Geometry To Account For Display Re-Scaling
        self.oldPos = self.pos()
        scaling_thread = ScalingClass(self.setGeometry, self.width, self.height, self.pos)
        scaling_thread.start()

        # Thread: Checks The Validity Of Directory Paths Set In Sector 2 As Source & Destination And Updates GUI Accordingly
        update_settings_window_thread = UpdateSettingsWindow()
        update_settings_window_thread.start()

        # Threads: Clears Sector 1 Information Output Label(s) After X Amount Of Time
        timer_thread_var[0] = TimerClass0()
        timer_thread_var[1] = TimerClass1()
        timer_thread_var[2] = TimerClass2()
        timer_thread_var[3] = TimerClass3()
        timer_thread_var[4] = TimerClass4()
        timer_thread_var[5] = TimerClass5()

        # Threads: Main Function Threads. Read/Write Operations & Time Stamp Comparing
        thread_var[0] = ThreadClass0(self.confirm_op0_tru, self.confirm_op0_fal)
        thread_var[1] = ThreadClass1(self.confirm_op1_tru, self.confirm_op1_fal)
        thread_var[2] = ThreadClass2(self.confirm_op2_tru, self.confirm_op2_fal)
        thread_var[3] = ThreadClass3(self.confirm_op3_tru, self.confirm_op3_fal)
        thread_var[4] = ThreadClass4(self.confirm_op4_tru, self.confirm_op4_fal)
        thread_var[5] = ThreadClass5(self.confirm_op5_tru, self.confirm_op5_fal)

        # Thread: 2x LED In Sector 2 Displays Source & Destination Path Validity
        settings_input_response_thread = SettingsInputResponse()

        self.show()

    # Funtion: Centering Windows
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Funtion: Mouse Press Event
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    # Funtion: Mouse Move Event
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    # Section 1 Funtion: Main Function Confirmation 0
    def confirm_op0_funk0(self):
        global confirm_op0_bool, confirm_op0_wait
        print('-- plugged in: confirm_op0_funk0: accepted')
        confirm_op0_bool = True
        confirm_op0_wait = False

    # Section 1 Funtion: Main Function Declination 0
    def confirm_op0_funk1(self):
        global confirm_op0_bool, confirm_op0_wait
        print('-- plugged in: confirm_op0_funk1: declined')
        confirm_op0_bool = False
        confirm_op0_wait = False

    # Section 1 Funtion: Main Function Confirmation 1
    def confirm_op1_funk0(self):
        global confirm_op1_bool, confirm_op1_wait
        print('-- plugged in: confirm_op1_funk0: accepted')
        confirm_op1_bool = True
        confirm_op1_wait = False

    # Section 1 Funtion: Main Function Declination 1
    def confirm_op1_funk1(self):
        global confirm_op1_bool, confirm_op1_wait
        print('-- plugged in: confirm_op1_funk1: declined')
        confirm_op1_bool = False
        confirm_op1_wait = False

    # Section 1 Funtion: Main Function Confirmation 2
    def confirm_op2_funk0(self):
        global confirm_op2_bool, confirm_op2_wait
        print('-- plugged in: confirm_op2_funk0: accepted')
        confirm_op2_bool = True
        confirm_op2_wait = False

    # Section 1 Funtion: Main Function Declination 2
    def confirm_op2_funk1(self):
        global confirm_op2_bool, confirm_op2_wait
        print('-- plugged in: confirm_op2_funk0: declined')
        confirm_op2_bool = False
        confirm_op2_wait = False

    # Section 1 Funtion: Main Function Confirmation 3
    def confirm_op3_funk0(self):
        global confirm_op3_bool, confirm_op3_wait
        print('-- plugged in: confirm_op3_funk0: accepted')
        confirm_op3_bool = True
        confirm_op3_wait = False

    # Section 1 Funtion: Main Function Declination 3
    def confirm_op3_funk1(self):
        global confirm_op3_bool, confirm_op3_wait
        print('-- plugged in: confirm_op3_funk1: declined')
        confirm_op3_bool = False
        confirm_op3_wait = False

    # Section 1 Funtion: Main Function Confirmation 4
    def confirm_op4_funk0(self):
        global confirm_op4_bool, confirm_op4_wait
        print('-- plugged in: confirm_op4_funk0: accepted')
        confirm_op4_bool = True
        confirm_op4_wait = False

    # Section 1 Funtion: Main Function Declination 4
    def confirm_op4_funk1(self):
        global confirm_op4_bool, confirm_op4_wait
        print('-- plugged in: confirm_op4_funk1: declined')
        confirm_op4_bool = False
        confirm_op4_wait = False

    # Section 1 Funtion: Main Function Confirmation 5
    def confirm_op5_funk0(self):
        global confirm_op5_bool, confirm_op5_wait
        print('-- plugged in: confirm_op5_funk0: accepted')
        confirm_op5_bool = True
        confirm_op5_wait = False

    # Section 1 Funtion: Main Function Declination 5
    def confirm_op5_funk1(self):
        global confirm_op5_bool, confirm_op5_wait
        print('-- plugged in: confirm_op5_funk1: declined')
        confirm_op5_bool = False
        confirm_op5_wait = False

    # Section 2 Funtion: Set's ReadOnly For Source And Settings Configuration And Configures Display To Reflect ReadOnly State
    def paths_readonly_funk(self):
        global settings_source_edit_vars
        read_only = True

        if settings_source_edit_var[0].isReadOnly() is True:
            read_only = True
        elif settings_source_edit_var[0].isReadOnly() is False:
            read_only = False

        if read_only is True:
            i = 0
            for settings_source_edit_vars in settings_source_edit_var:
                settings_source_edit_var[i].setReadOnly(False)
                settings_source_edit_var[i].setStyleSheet(
                    """QLineEdit {background-color: rgb(20, 20, 20);
                    border:0px solid rgb(0, 0, 0);
                    selection-color: green;
                    selection-background-color: black;
                    color: grey;}"""
                    )
                i += 1
            i = 0
            for settings_dest_edit_vars in settings_dest_edit_var:
                settings_dest_edit_var[i].setReadOnly(False)
                settings_dest_edit_var[i].setStyleSheet(
                    """QLineEdit {background-color: rgb(20, 20, 20);
                    border:0px solid rgb(0, 0, 0);
                    selection-color: green;
                    selection-background-color: black;
                    color: grey;}"""
                    )
                i += 1
            self.paths_readonly_button.setIcon(QIcon(small_image[6]))

        elif read_only is False:
            i = 0
            for settings_source_edit_vars in settings_source_edit_var:
                settings_source_edit_var[i].setReadOnly(True)
                settings_source_edit_var[i].setStyleSheet(
                    """QLineEdit {background-color: rgb(10, 10, 10);
                    border:0px solid rgb(0, 0, 0);
                    selection-color: green;
                    selection-background-color: black;
                    color: grey;}"""
                    )
                i += 1
            i = 0
            for settings_dest_edit_vars in settings_dest_edit_var:
                settings_dest_edit_var[i].setReadOnly(True)
                settings_dest_edit_var[i].setStyleSheet(
                    """QLineEdit {background-color: rgb(10, 10, 10);
                    border:0px solid rgb(0, 0, 0);
                    selection-color: green;
                    selection-background-color: black;
                    color: grey;}"""
                    )
                i += 1
            self.paths_readonly_button.setIcon(QIcon(small_image[7]))

    # Sector 2 Funtion: Moves To Next Settings Page Left
    def scr_left_funk(self):
        global settings_active_int
        if settings_active_int is 0:
            settings_active_int = 5
            self.settings_funk5()
        elif settings_active_int is 1:
            settings_active_int = 0
            self.settings_funk0()
        elif settings_active_int is 2:
            settings_active_int = 1
            self.settings_funk1()
        elif settings_active_int is 3:
            settings_active_int = 2
            self.settings_funk2()
        elif settings_active_int is 4:
            settings_active_int = 3
            self.settings_funk3()
        elif settings_active_int is 5:
            settings_active_int = 4
            self.settings_funk4()

    # Sector 2 Funtion: Moves To Next Settings Page Right
    def scr_right_funk(self):
        global settings_active_int
        if settings_active_int is 0:
            settings_active_int = 1
            self.settings_funk1()
        elif settings_active_int is 1:
            settings_active_int = 2
            self.settings_funk2()
        elif settings_active_int is 2:
            settings_active_int = 3
            self.settings_funk3()
        elif settings_active_int is 3:
            settings_active_int = 4
            self.settings_funk4()
        elif settings_active_int is 4:
            settings_active_int = 5
            self.settings_funk5()
        elif settings_active_int is 5:
            settings_active_int = 0
            self.settings_funk0()

    # Sector 2 Funtion: Writes Source Changes To Configuration File
    def settings_source_funk(self):
        global source_path_entered, source_selected, config_src_var, path_var, settings_source_edit_var
        global settings_input_response_thread, settings_input_response_source_bool
        if os.path.exists(source_path_entered):
            settings_input_response_source_bool = True
            path_item = []
            with open('config.txt', 'r') as fo:
                for line in fo:
                    line = line.strip()
                    if not line.startswith(config_src_var[source_selected]):
                        path_item.append(line)
                    elif line.startswith(config_src_var[source_selected]):
                        new_line = config_src_var[source_selected]+' '+source_path_entered
                        path_item.append(new_line)
            open('config.txt', 'w').close()
            with open('config.txt', 'a') as fo:
                i = 0
                for path_items in path_item:
                    fo.writelines(path_item[i]+'\n')
                    i += 1
            fo.close()
            path_var[source_selected] = source_path_entered
            settings_input_response_thread.start()
        elif not os.path.exists(source_path_entered):
            settings_input_response_source_bool = False
            settings_source_edit_var[source_selected].setText(path_var[source_selected])
            settings_input_response_thread.start()

    # Sector 2 Funtion: Writes Destination Changes To Configuration File
    def settings_dest_funk(self):
        global dest_path_entered, dest_selected, config_dst_var, dest_path_var, settings_dest_edit_var
        global settings_input_response_thread, settings_input_response_dest_bool
        if os.path.exists(dest_path_entered):
            settings_input_response_dest_bool = True
            path_item = []
            with open('config.txt', 'r') as fo:
                for line in fo:
                    line = line.strip()
                    if not line.startswith(config_dst_var[dest_selected]):
                        path_item.append(line)
                    elif line.startswith(config_dst_var[dest_selected]):
                        new_line = config_dst_var[dest_selected] + ' ' + dest_path_entered
                        path_item.append(new_line)
            open('config.txt', 'w').close()
            with open('config.txt', 'a') as fo:
                i = 0
                for path_items in path_item:
                    fo.writelines(path_item[i] + '\n')
                    i += 1
            fo.close()
            dest_path_var[dest_selected] = dest_path_entered
            settings_input_response_thread.start()

        elif not os.path.exists(dest_path_entered):
            settings_input_response_dest_bool = False
            settings_dest_edit_var[dest_selected].setText(dest_path_var[dest_selected])
            settings_input_response_thread.start()

    # Sector 2 Funtion: Provides settings_source_funk With Information From Source Path Edit 0
    def settings_source_pre_funk0(self):
        global source_path_entered, source_selected
        source_selected = 0
        source_path_entered = self.settings_source0.text()
        self.settings_source_funk()

    # Sector 2 Funtion: Provides settings_source_funk With Information From Source Path Edit 1
    def settings_source_pre_funk1(self):
        global source_path_entered, source_selected
        source_selected = 1
        source_path_entered = self.settings_source1.text()
        self.settings_source_funk()

    # Sector 2 Funtion: Provides settings_source_funk With Information From Source Path Edit 2
    def settings_source_pre_funk2(self):
        global source_path_entered, source_selected
        source_selected = 2
        source_path_entered = self.settings_source2.text()
        self.settings_source_funk()

    # Sector 2 Funtion: Provides settings_source_funk With Information From Source Path Edit 3
    def settings_source_pre_funk3(self):
        global source_path_entered, source_selected
        source_selected = 3
        source_path_entered = self.settings_source3.text()
        self.settings_source_funk()

    # Sector 2 Funtion: Provides settings_source_funk With Information From Source Path Edit 4
    def settings_source_pre_funk4(self):
        global source_path_entered, source_selected
        source_selected = 4
        source_path_entered = self.settings_source4.text()
        self.settings_source_funk()

    # Sector 2 Funtion: Provides settings_source_funk With Information From Source Path Edit 5
    def settings_source_pre_funk5(self):
        global source_path_entered, source_selected
        source_selected = 5
        source_path_entered = self.settings_source5.text()
        self.settings_source_funk()

    # Sector 2 Funtion: Provides settings_dest_funk With Information From Destination Path Edit 0
    def settings_dest_pre_funk0(self):
        global dest_path_entered, dest_selected
        dest_selected = 0
        dest_path_entered = self.settings_dest0.text()
        self.settings_dest_funk()

    # Sector 2 Funtion: Provides settings_dest_funk With Information From Destination Path Edit 1
    def settings_dest_pre_funk1(self):
        global dest_path_entered, dest_selected
        dest_selected = 1
        dest_path_entered = self.settings_dest1.text()
        self.settings_dest_funk()

    # Sector 2 Funtion: Provides settings_dest_funk With Information From Destination Path Edit 2
    def settings_dest_pre_funk2(self):
        global dest_path_entered, dest_selected
        dest_selected = 2
        dest_path_entered = self.settings_dest2.text()
        self.settings_dest_funk()

    # Sector 2 Funtion: Provides settings_dest_funk With Information From Destination Path Edit 3
    def settings_dest_pre_funk3(self):
        global dest_path_entered, dest_selected
        dest_selected = 3
        dest_path_entered = self.settings_dest3.text()
        self.settings_dest_funk()

    # Sector 2 Funtion: Provides settings_dest_funk With Information From Destination Path Edit 4
    def settings_dest_pre_funk4(self):
        global dest_path_entered, dest_selected
        dest_selected = 4
        dest_path_entered = self.settings_dest4.text()
        self.settings_dest_funk()

    # Sector 2 Funtion: Provides settings_dest_funk With Information From Destination Path Edit 5
    def settings_dest_pre_funk5(self):
        global dest_path_entered, dest_selected
        dest_selected = 5
        dest_path_entered = self.settings_dest5.text()
        self.settings_dest_funk()

    # Sector 2 Funtion: Hides Objects in Sector 2, Resizes Sector One Background Labels, Rotates Sector 1 Drop Down Settings Arrows
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

        back_label_var[0].resize(95, 80)
        pixmap = QPixmap(background_img[0])
        back_label_var[0].setPixmap(pixmap)
        back_label_var[0].setStyleSheet(
                    """QLabel {background-color: rgb(0, 0, 0);
                    border-top:1px solid rgb(0, 0, 0);
                    border-left:1px solid rgb(0, 0, 0);
                    border-right:1px solid rgb(0, 0, 0)}"""
                    )

        back_label_var[1].resize(95, 80)
        pixmap = QPixmap(background_img[0])
        back_label_var[1].setPixmap(pixmap)
        back_label_var[1].setStyleSheet(
                    """QLabel {background-color: rgb(0, 0, 0);
                    border-top:1px solid rgb(0, 0, 0);
                    border-left:1px solid rgb(0, 0, 0);
                    border-right:1px solid rgb(0, 0, 0)}"""
                    )

        back_label_var[2].resize(95, 80)
        pixmap = QPixmap(background_img[0])
        back_label_var[2].setPixmap(pixmap)
        back_label_var[2].setStyleSheet(
                    """QLabel {background-color: rgb(0, 0, 0);
                    border-top:1px solid rgb(0, 0, 0);
                    border-left:1px solid rgb(0, 0, 0);
                    border-right:1px solid rgb(0, 0, 0)}"""
                    )

        back_label_var[3].resize(95, 80)
        pixmap = QPixmap(background_img[0])
        back_label_var[3].setPixmap(pixmap)
        back_label_var[3].setStyleSheet(
                    """QLabel {background-color: rgb(0, 0, 0);
                    border-top:1px solid rgb(0, 0, 0);
                    border-left:1px solid rgb(0, 0, 0);
                    border-right:1px solid rgb(0, 0, 0)}"""
                    )

        back_label_var[4].resize(95, 80)
        pixmap = QPixmap(background_img[0])
        back_label_var[4].setPixmap(pixmap)
        back_label_var[4].setStyleSheet(
                    """QLabel {background-color: rgb(0, 0, 0);
                    border-top:1px solid rgb(0, 0, 0);
                    border-left:1px solid rgb(0, 0, 0);
                    border-right:1px solid rgb(0, 0, 0)}"""
                    )

        back_label_var[5].resize(95, 80)
        pixmap = QPixmap(background_img[0])
        back_label_var[5].setPixmap(pixmap)
        back_label_var[5].setStyleSheet(
                    """QLabel {background-color: rgb(0, 0, 0);
                    border-top:1px solid rgb(0, 0, 0);
                    border-left:1px solid rgb(0, 0, 0);
                    border-right:1px solid rgb(0, 0, 0)}"""
                    )

        btnx_settings_var[0].setIcon(QIcon(small_image[0]))
        btnx_settings_var[1].setIcon(QIcon(small_image[0]))
        btnx_settings_var[2].setIcon(QIcon(small_image[0]))
        btnx_settings_var[3].setIcon(QIcon(small_image[0]))
        btnx_settings_var[4].setIcon(QIcon(small_image[0]))
        btnx_settings_var[5].setIcon(QIcon(small_image[0]))

    # Sector 2 Funtion: Calls hide_settings_funk Then Hides Settings Page By Resizing Window
    def hide_settings_page_funk(self):
        self.hide_settings_funk()
        self.setFixedSize(self.width, 110)

    # Sector 2 Funtion: Displays Drop Down Settings In Sector 2 For Source & Destination Path Configuration 0
    def settings_funk0(self):
        global settings_active, settings_active_int, settings_active_int_prev
        settings_active_int = 0
        self.hide_settings_funk()
        if settings_active is False:
            if settings_active_int != settings_active_int_prev:
                print('0.1')
                self.setFixedSize(self.width, 190)
                print('1')

                btnx_settings_var[0].setIcon(QIcon(small_image[1]))

                back_label_var[0].resize(95, 85)
                pixmap = QPixmap(background_img[1])
                back_label_var[0].setPixmap(pixmap)

                back_label_var[0].setStyleSheet(
                    """QLabel {background-color: rgb(0, 0, 0);
                    border-top:2px solid rgb(0, 0, 0);}"""
                    )

                self.setting_title0.show()
                self.settings_source0.show()
                self.settings_dest0.show()

                settings_active_int_prev = settings_active_int

            elif settings_active_int == settings_active_int_prev:
                self.hide_settings_page_funk()
                settings_active_int_prev = ()

    # Sector 2 Funtion: Displays Drop Down Settings In Sector 2 For Source & Destination Path Configuration 1
    def settings_funk1(self):
        global settings_active, settings_active_int, settings_active_int_prev
        settings_active_int = 1
        self.hide_settings_funk()
        if settings_active is False:
            if settings_active_int != settings_active_int_prev:
                self.setFixedSize(self.width, 190)

                btnx_settings_var[1].setIcon(QIcon(small_image[1]))

                back_label_var[1].resize(95, 85)
                pixmap = QPixmap(background_img[1])
                back_label_var[1].setPixmap(pixmap)

                back_label_var[1].setStyleSheet(
                    """QLabel {background-color: rgb(0, 0, 0);
                    border-top:2px solid rgb(0, 0, 0);}"""
                    )

                self.setting_title1.show()
                self.settings_source1.show()
                self.settings_dest1.show()

                settings_active_int_prev = settings_active_int

            elif settings_active_int == settings_active_int_prev:
                self.hide_settings_page_funk()
                settings_active_int_prev = ()

    # Sector 2 Funtion: Displays Drop Down Settings In Sector 2 For Source & Destination Path Configuration 2
    def settings_funk2(self):
        global settings_active, settings_active_int, settings_active_int_prev
        settings_active_int = 2
        self.hide_settings_funk()
        if settings_active is False:
            if settings_active_int != settings_active_int_prev:
                self.setFixedSize(self.width, 190)

                btnx_settings_var[2].setIcon(QIcon(small_image[1]))

                back_label_var[2].resize(95, 85)
                pixmap = QPixmap(background_img[1])
                back_label_var[2].setPixmap(pixmap)

                back_label_var[2].setStyleSheet(
                    """QLabel {background-color: rgb(0, 0, 0);
                    border-top:2px solid rgb(0, 0, 0);}"""
                    )

                self.setting_title2.show()
                self.settings_source2.show()
                self.settings_dest2.show()
                settings_active_int_prev = settings_active_int

            elif settings_active_int == settings_active_int_prev:
                self.hide_settings_page_funk()
                settings_active_int_prev = ()

    # Sector 2 Funtion: Displays Drop Down Settings In Sector 2 For Source & Destination Path Configuration 3
    def settings_funk3(self):
        global settings_active, settings_active_int, settings_active_int_prev
        settings_active_int = 3
        self.hide_settings_funk()
        if settings_active is False:
            if settings_active_int != settings_active_int_prev:
                self.setFixedSize(self.width, 190)

                btnx_settings_var[3].setIcon(QIcon(small_image[1]))

                back_label_var[3].resize(95, 85)
                pixmap = QPixmap(background_img[1])
                back_label_var[3].setPixmap(pixmap)

                back_label_var[3].setStyleSheet(
                    """QLabel {background-color: rgb(0, 0, 0);
                    border-top:2px solid rgb(0, 0, 0);}"""
                    )

                self.setting_title3.show()
                self.settings_source3.show()
                self.settings_dest3.show()
                settings_active_int_prev = settings_active_int

            elif settings_active_int == settings_active_int_prev:
                self.hide_settings_page_funk()
                settings_active_int_prev = ()

    # Sector 2 Funtion: Displays Drop Down Settings In Sector 2 For Source & Destination Path Configuration 4
    def settings_funk4(self):
        global settings_active, settings_active_int, settings_active_int_prev
        settings_active_int = 4
        self.hide_settings_funk()
        if settings_active is False:
            if settings_active_int != settings_active_int_prev:
                self.setFixedSize(self.width, 190)

                btnx_settings_var[4].setIcon(QIcon(small_image[1]))

                back_label_var[4].resize(95, 85)
                pixmap = QPixmap(background_img[1])
                back_label_var[4].setPixmap(pixmap)

                back_label_var[4].setStyleSheet(
                    """QLabel {background-color: rgb(0, 0, 0);
                    border-top:2px solid rgb(0, 0, 0);}"""
                    )

                self.setting_title4.show()
                self.settings_source4.show()
                self.settings_dest4.show()
                settings_active_int_prev = settings_active_int

            elif settings_active_int == settings_active_int_prev:
                self.hide_settings_page_funk()
                settings_active_int_prev = ()

    # Sector 2 Funtion: Displays Drop Down Settings In Sector 2 For Source & Destination Path Configuration 5
    def settings_funk5(self):
        global settings_active, settings_active_int, settings_active_int_prev
        settings_active_int = 5
        self.hide_settings_funk()
        if settings_active is False:
            if settings_active_int != settings_active_int_prev:
                self.setFixedSize(self.width, 190)

                btnx_settings_var[5].setIcon(QIcon(small_image[1]))

                back_label_var[5].resize(95, 85)
                pixmap = QPixmap(background_img[1])
                back_label_var[5].setPixmap(pixmap)

                back_label_var[5].setStyleSheet(
                    """QLabel {background-color: rgb(0, 0, 0);
                    border-top:2px solid rgb(0, 0, 0);}"""
                    )

                self.setting_title5.show()
                self.settings_source5.show()
                self.settings_dest5.show()
                self.settings_dest5.show()
                settings_active_int_prev = settings_active_int

            elif settings_active_int == settings_active_int_prev:
                self.hide_settings_page_funk()
                settings_active_int_prev = ()

    # Sector 1 Function: Starts Main Sector 1 Thread 0
    def thread_funk_0(self):
        thread_var[0].start()

    # Sector 1 Function: Starts Main Sector 1 Thread 1
    def thread_funk_1(self):
        thread_var[1].start()

    # Sector 1 Function: Starts Main Sector 1 Thread 2
    def thread_funk_2(self):
        thread_var[2].start()

    # Sector 1 Function: Starts Main Sector 1 Thread 3
    def thread_funk_3(self):
        thread_var[3].start()

    # Sector 1 Function: Starts Main Sector 1 Thread 4
    def thread_funk_4(self):
        thread_var[4].start()

    # Sector 1 Function: Starts Main Sector 1 Thread 5
    def thread_funk_5(self):
        thread_var[5].start()

    # Sector 1 Function: Provides Relative Information To set_comp_bool_funk From Section 1 Main Function Mode Switch Button 0
    def set_comp_bool_pre_funk0(self):
        global compare_clicked
        compare_clicked = 0
        self.set_comp_bool_funk()

    # Sector 1 Function: Provides Relative Information To set_comp_bool_funk From Section 1 Main Function Mode Switch Button 1
    def set_comp_bool_pre_funk1(self):
        global compare_clicked
        compare_clicked = 1
        self.set_comp_bool_funk()

    # Sector 1 Function: Provides Relative Information To set_comp_bool_funk From Section 1 Main Function Mode Switch Button 2
    def set_comp_bool_pre_funk2(self):
        global compare_clicked
        compare_clicked = 2
        self.set_comp_bool_funk()

    # Sector 1 Function: Provides Relative Information To set_comp_bool_funk From Section 1 Main Function Mode Switch Button 3
    def set_comp_bool_pre_funk3(self):
        global compare_clicked
        compare_clicked = 3
        self.set_comp_bool_funk()

    # Sector 1 Function: Provides Relative Information To set_comp_bool_funk From Section 1 Main Function Mode Switch Button 4
    def set_comp_bool_pre_funk4(self):
        global compare_clicked
        compare_clicked = 4
        self.set_comp_bool_funk()

    # Sector 1 Function: Provides Relative Information To set_comp_bool_funk From Section 1 Main Function Mode Switch Button 5
    def set_comp_bool_pre_funk5(self):
        global compare_clicked
        compare_clicked = 5
        self.set_comp_bool_funk()

    # Sector 1 Function: Uses Integer To Switch Main Function Mode Relative To Mode Button Clicked
    def set_comp_bool_funk(self):
        global compare_bool_var, compare_clicked, btnx_main_var
        if compare_bool_var[compare_clicked] is False:
            compare_bool_var[compare_clicked] = True
            comp_cont_button_var[compare_clicked].setIcon(QIcon(small_image[5]))
            comp_cont_button_var[compare_clicked].setStyleSheet(
                """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(30, 30, 30);}"""
               )
        elif compare_bool_var[compare_clicked] is True:
            compare_bool_var[compare_clicked] = False
            comp_cont_button_var[compare_clicked].setIcon(QIcon(small_image[4]))
            comp_cont_button_var[compare_clicked].setStyleSheet(
                """QPushButton{background-color: rgb(35, 35, 35);
               border:0px solid rgb(30, 30, 30);}"""
               )

    # Sector 1 Function: Stops Sector 1 Main Function Thread 0
    def stop_thr_funk0(self):
        global thread_var
        timer_thread_var[0].start()
        thread_var[0].stop_thr()

    # Sector 1 Function: Stops Sector 1 Main Function Thread 1
    def stop_thr_funk1(self):
        global thread_var
        timer_thread_var[1].start()
        thread_var[1].stop_thr()

    # Sector 1 Function: Stops Sector 1 Main Function Thread 2
    def stop_thr_funk2(self):
        global thread_var
        timer_thread_var[2].start()
        thread_var[2].stop_thr()

    # Sector 1 Function: Stops Sector 1 Main Function Thread 3
    def stop_thr_funk3(self):
        global thread_var
        timer_thread_var[3].start()
        thread_var[3].stop_thr()

    # Sector 1 Function: Stops Sector 1 Main Function Thread 4
    def stop_thr_funk4(self):
        global thread_var
        timer_thread_var[4].start()
        thread_var[4].stop_thr()

    # Sector 1 Function: Stops Sector 1 Main Function Thread 5
    def stop_thr_funk5(self):
        global thread_var
        timer_thread_var[5].start()
        thread_var[5].stop_thr()


# Scaling Class: Automatically Adjusts Form's Geometry Accounting For Changes In Display Scaling Settings
class ScalingClass(QThread):
    def __init__(self, setGeometry, width, height, pos):
        QThread.__init__(self)
        self.setGeometry = setGeometry
        self.width = width
        self.height = height
        self.pos = pos

    def run(self):
        print('-- plugged in: ScalingClass')
        while True:
            time.sleep(0.01)
            self.setGeometry(self.pos().x(), self.pos().y(), self.width, self.height)

# Input Respons Class: LED's Dsilpay Valid/Invalid Paths Attempted At Being Set In Sector 2 Source & Destination Path Configuration
class SettingsInputResponse(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global settings_input_response_source_bool, settings_input_response_dest_bool
        global settings_source_edit_var, settings_dest_edit_var, settings_input_response_label
        global source_selected, dest_selected

        if settings_input_response_source_bool is True:
            settings_input_response_label[0].setStyleSheet(
                """QLabel {background-color: rgb(0, 255, 0);
                border:1px solid rgb(15, 15, 15);}"""
                )
            settings_input_response_source_bool = None
            time.sleep(1)
            settings_input_response_label[0].setStyleSheet(
                """QLabel {background-color: rgb(15, 15, 15);
                border:1px solid rgb(15, 15, 15);}"""
                )

        elif settings_input_response_source_bool is False:
            settings_input_response_label[0].setStyleSheet(
                """QLabel {background-color: rgb(255, 0, 0);
                border:1px solid rgb(15, 15, 15);}"""
                )
            settings_input_response_source_bool = None
            time.sleep(1)
            settings_input_response_label[0].setStyleSheet(
                """QLabel {background-color: rgb(15, 15, 15);
                border:1px solid rgb(15, 15, 15);}"""
                )

        elif settings_input_response_dest_bool is True:
            settings_input_response_label[1].setStyleSheet(
                """QLabel {background-color: rgb(0, 255, 0);
                border:1px solid rgb(15, 15, 15);}"""
                )
            settings_input_response_dest_bool = None
            time.sleep(1)
            settings_input_response_label[1].setStyleSheet(
                """QLabel {background-color: rgb(15, 15, 15);
                border:1px solid rgb(15, 15, 15);}"""
                )

        elif settings_input_response_dest_bool is False:
            settings_input_response_label[1].setStyleSheet(
                """QLabel {background-color: rgb(255, 0, 0);
                border:1px solid rgb(15, 15, 15);}"""
                )
            settings_input_response_dest_bool = None
            time.sleep(1)
            settings_input_response_label[1].setStyleSheet(
                """QLabel {background-color: rgb(15, 15, 15);
                border:1px solid rgb(15, 15, 15);}"""
                )

# Update Sector 2 Settings Window: Sources & Destination Paths Displayed Only When Last Valid Path Entered Still Actually Exists
class UpdateSettingsWindow(QThread):
    def __init__(self):
        QThread.__init__(self)

    # Run This Thread While Program Is Alive And Read Configuration File
    def run(self):
        while __name__ == '__main__':
            self.get_conf_funk()
            time.sleep(1)

    # While Source And Destination Path Configuration Edit ReadOnly, Check Configured Paths Existance And Set Boolean Accordingly
    def get_conf_funk(self):
        global path_var, path_bool_var, dest_path_var, dest_path_bool_var, settings_source_edit_var,\
            settings_dest_edit_var, configuration_engaged
        configuration_engaged = True

        # Only Update Displayed Source & Destination Paths If Source & Destination Paths Not Being Edited
        if settings_source_edit_var[0].isReadOnly() is True:
            path_var = []
            path_bool_var = []
            dest_path_var = []
            dest_path_bool_var = []
            if os.path.exists('config.txt'):
                with open('config.txt', 'r') as fo:
                    configuration_engaged = True
                    for line in fo:
                        line = line.strip()

                        # Check If Source Paths In Configuration File Are Valid 
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
                                        if (primary_key + '_True') not in path_bool_var:

                                            # Append Source Path To List
                                            path_var.append(secondary_key)

                                            # Set Boolean Value To Compliment Source Path Existance
                                            path_bool_var.append(primary_key + '_True')

                                    elif not os.path.exists(secondary_key):
                                        if (primary_key + '_False') not in path_bool_var:
                                            path_var.append('')
                                            path_bool_var.append(primary_key + '_False')
                            i += 1

                        # Check If Destination Paths In Configuration File Are Valid
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

                                            # Append Destination Path To List
                                            dest_path_var.append(secondary_key)

                                            # Set Boolean Value To Compliment Destination Path Existance
                                            dest_path_bool_var.append(primary_key + '_True')

                                    elif not os.path.exists(secondary_key):
                                        if (primary_key + '_False') not in dest_path_bool_var:
                                            dest_path_var.append('')
                                            dest_path_bool_var.append(primary_key + '_False')
                            i += 1
                fo.close()

                # Set Displayed Source Path(s)
                i = 0
                for settings_source_edit_vars in settings_source_edit_var:
                    if path_var[i] != settings_source_edit_var[i]:
                        settings_source_edit_var[i].setText(path_var[i])
                    i += 1

                # Set Displayed Destination Path(s)
                i = 0
                for settings_dest_edit_vars in settings_dest_edit_var:
                    if dest_path_var[i] != settings_dest_edit_var[i]:
                        settings_dest_edit_var[i].setText(dest_path_var[i])
                    i += 1

        configuration_engaged = False

# Sector 1 Class: Clears Information Output Label 0
class TimerClass0(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global info_label_1_var
        i = 2
        while i > 0:
            time.sleep(1)
            i -= 1
        info_label_1_var[0].setText('')

# Sector 1 Class: Clears Information Output Label 1
class TimerClass1(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global info_label_1_var
        i = 2
        while i > 0:
            time.sleep(1)
            i -= 1
        info_label_1_var[1].setText('')

# Sector 1 Class: Clears Information Output Label 2
class TimerClass2(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global info_label_1_var
        i = 2
        while i > 0:
            time.sleep(1)
            i -= 1
        info_label_1_var[2].setText('')

# Sector 1 Class: Clears Information Output Label 3
class TimerClass3(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global info_label_1_var
        i = 2
        while i > 0:
            time.sleep(1)
            i -= 1
        info_label_1_var[3].setText('')

# Sector 1 Class: Clears Information Output Label 4
class TimerClass4(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global info_label_1_var
        i = 2
        while i > 0:
            time.sleep(1)
            i -= 1
        info_label_1_var[4].setText('')

# Sector 1 Class: Clears Information Output Label 5
class TimerClass5(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global info_label_1_var
        i = 2
        while i > 0:
            time.sleep(1)
            i -= 1
        info_label_1_var[5].setText('')


# Sector 1 Class: Main Function Button Thread 0
class ThreadClass0(QThread):
    def __init__(self, confirm_op0_tru, confirm_op0_fal):
        QThread.__init__(self)
        self.confirm_op0_tru = confirm_op0_tru
        self.confirm_op0_fal = confirm_op0_fal

    def run(self):
        global btnx_main_var, img_active_var, img_var, path_var, thread_var, info_label_1_var, timer_thread_var
        global path_bool_var, dest_path_bool_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool

        # Allow To Run Only When Source & Destination Configuration Is Disengaged
        zero = '0'
        centillionth_str = str('0.' + zero * 303 + '1')
        centillionth = float(centillionth_str)
        if configuration_engaged is True:
            while configuration_engaged is True:
                time.sleep(centillionth)

        # If Source & Destination Configuration Is Disengaged Then Continue
        elif configuration_engaged is False:

            # Set Paths In Stone Before Continuing. Asigns Source & Destination Variables To New Variables That Cannot Be Changed Once Function Exectutes
            path = path_var[0]
            dest = dest_path_var[0]
            path_bool = path_bool_var[0]
            dest_bool = dest_path_bool_var[0]
            compare_bool = compare_bool_var[0]

            # Provide Confirmation/Declination Buttons & Wait For Confirmation/Declination Then Reset Global confirm_op0_wait Boolean Back to True
            btnx_main_var[0].setIcon(QIcon('./image/img_archives_amber.png'))
            info_label_1_var[0].hide()
            self.confirm_op0_tru.show()
            self.confirm_op0_fal.show()
            while confirm_op0_wait is True:
                time.sleep(0.3)
            confirm_op0_wait = True

            # Confirmation/Declination Occured, Hide Confirmation/Declination Buttons
            self.confirm_op0_tru.hide()
            self.confirm_op0_fal.hide()
            btnx_main_var[0].setIcon(QIcon(img_var[0]))
            info_label_1_var[0].show()

            # If Confirmed Run Main Function
            if confirm_op0_bool is True:
                print('-- ThreadClass0: confirm_op0_bool: accepted')
                btnx_main_var[0].setIcon(QIcon(img_active_var[0]))
                change_var = False
                print('-- Source Path:', path)
                print('-- Destination Path:', dest)
                if path_bool == 'ARCHIVE_SOURCE_True' and dest_bool == 'ARCHIVE_DESTINATION_True':
                    info_label_1_var[0].setText('working...')
                    cp_var = 0
                    for dirname, subdirlist, filelist in os.walk(path):
                        for fname in filelist:
                            fullpath = os.path.join(dirname, fname)
                            t_path = fullpath.replace(path, '')
                            t_path = dest + t_path
                            if not fullpath.endswith('.ini'):
                                if not os.path.exists(t_path):
                                    change_var = True
                                    try:
                                        shutil.copy(fullpath, t_path)
                                    except IOError:
                                        os.makedirs(os.path.dirname(t_path))
                                        shutil.copy(fullpath, t_path)
                                    cp_var += 1
                                elif os.path.exists(t_path):
                                    if compare_bool is True:
                                        ma = os.path.getmtime(fullpath)
                                        mb = os.path.getmtime(t_path)
                                        if mb < ma:
                                            change_var = True
                                            try:
                                                shutil.copy(fullpath, t_path)
                                            except ioerror:
                                                os.makedirs(os.path.dirname(t_path))
                                                shutil.copy(fullpath, t_path)
                                            cp_var += 1
                    if change_var is False:
                        info_label_1_var[0].setText('unnecessary.')
                    elif change_var is True:
                        info_label_1_var[0].seText('amended.')
                else:
                    info_label_1_var[0].setText('path error!')
            elif confirm_op0_bool is False:
                print('-- ThreadClass0: confirm_op0_bool: declined')
            timer_thread_var[0].start()
            btnx_main_var[0].setIcon(QIcon(img_var[0]))

    def stop_thr(self):
        global btnx_main_var, info_label_1_var
        btnx_main_var[0].setIcon(QIcon(img_var[0]))
        info_label_1_var[0].setText('aborted.')
        self.terminate()


# Sector 1 Class: Main Function Button Thread 1
class ThreadClass1(QThread):
    def __init__(self, confirm_op1_tru, confirm_op1_fal):
        QThread.__init__(self)
        self.confirm_op1_tru = confirm_op1_tru
        self.confirm_op1_fal = confirm_op1_fal

    def run(self):
        global btnx_main_var, img_active_var, img_var, path_var, thread_var, info_label_1_var, timer_thread_var
        global path_bool_var, dest_path_bool_var, configuration_engaged, confirm_op1_wait, confirm_op1_bool

        # Allow To Run Only When Source & Destination Configuration Is Disengaged
        zero = '0'
        centillionth_str = str('0.' + zero * 303 + '1')
        centillionth = float(centillionth_str)
        if configuration_engaged is True:
            while configuration_engaged is True:
                time.sleep(centillionth)

        # If Source & Destination Configuration Is Disengaged Then Continue
        elif configuration_engaged is False:

            # Set Paths In Stone Before Continuing. Asigns Source & Destination Variables To New Variables That Cannot Be Changed Once Function Exectutes
            path = path_var[1]
            dest = dest_path_var[1]
            path_bool = path_bool_var[1]
            dest_bool = dest_path_bool_var[1]
            compare_bool = compare_bool_var[1]

            # Provide Confirmation/Declination Buttons & Wait For Confirmation/Declination Then Reset Global confirm_op0_wait Boolean Back to True
            btnx_main_var[1].setIcon(QIcon('./image/img_document_amber.png'))
            info_label_1_var[1].hide()
            self.confirm_op1_tru.show()
            self.confirm_op1_fal.show()
            while confirm_op1_wait is True:
                time.sleep(0.3)
            confirm_op1_wait = True

            # Confirmation/Declination Occured, Hide Confirmation/Declination Buttons
            self.confirm_op1_tru.hide()
            self.confirm_op1_fal.hide()
            btnx_main_var[1].setIcon(QIcon(img_var[1]))
            info_label_1_var[1].show()

            # If Confirmed Run Main Function
            if confirm_op1_bool is True:
                print('-- ThreadClass1: confirm_op1_bool: accepted')
                btnx_main_var[1].setIcon(QIcon(img_active_var[1]))
                change_var = False
                if path_bool == 'DOCUMENT_SOURCE_True' and dest_bool == 'DOCUMENT_DESTINATION_True':
                    info_label_1_var[1].setText('working...')
                    cp_var = 0
                    for dirName, subdirList, fileList in os.walk(path):
                        for fname in fileList:
                            fullpath = os.path.join(dirName, fname)
                            t_path = fullpath.replace(path, '')
                            t_path = dest + t_path
                            if not fullpath.endswith('.ini'):
                                if not os.path.exists(t_path):
                                    change_var = True
                                    try:
                                        shutil.copy(fullpath, t_path)
                                    except IOError:
                                        os.makedirs(os.path.dirname(t_path))
                                        shutil.copy(fullpath, t_path)
                                    cp_var += 1
                                elif os.path.exists(t_path):
                                    if compare_bool is True:
                                        ma = os.path.getmtime(fullpath)
                                        mb = os.path.getmtime(t_path)
                                        if mb < ma:
                                            change_var = True
                                            try:
                                                shutil.copy(fullpath, t_path)
                                            except IOError:
                                                os.makedirs(os.path.dirname(t_path))
                                                shutil.copy(fullpath, t_path)
                                            cp_var += 1
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


# Sector 1 Class: Main Function Button Thread 2
class ThreadClass2(QThread):
    def __init__(self, confirm_op2_tru, confirm_op2_fal):
        QThread.__init__(self)
        self.confirm_op2_tru = confirm_op2_tru
        self.confirm_op2_fal = confirm_op2_fal

    def run(self):
        global btnx_main_var, img_active_var, img_var, path_var, thread_var, info_label_1_var, timer_thread_var
        global path_bool_var, dest_path_bool_var, configuration_engaged, confirm_op2_wait, confirm_op2_bool

        # Allow To Run Only When Source & Destination Configuration Is Disengaged
        zero = '0'
        centillionth_str = str('0.' + zero * 303 + '1')
        centillionth = float(centillionth_str)
        if configuration_engaged is True:
            while configuration_engaged is True:
                time.sleep(centillionth)

        # If Source & Destination Configuration Is Disengaged Then Continue
        elif configuration_engaged is False:

            # Set Paths In Stone Before Continuing. Asigns Source & Destination Variables To New Variables That Cannot Be Changed Once Function Exectutes
            path = path_var[2]
            dest = dest_path_var[2]
            path_bool = path_bool_var[2]
            dest_bool = dest_path_bool_var[2]
            compare_bool = compare_bool_var[2]

            # Provide Confirmation/Declination Buttons & Wait For Confirmation/Declination Then Reset Global confirm_op0_wait Boolean Back to True
            btnx_main_var[2].setIcon(QIcon('./image/img_music_amber.png'))
            info_label_1_var[2].hide()
            self.confirm_op2_tru.show()
            self.confirm_op2_fal.show()
            while confirm_op2_wait is True:
                time.sleep(0.3)
            confirm_op2_wait = True

            # Confirmation/Declination Occured, Hide Confirmation/Declination Buttons
            self.confirm_op2_tru.hide()
            self.confirm_op2_fal.hide()
            btnx_main_var[2].setIcon(QIcon(img_var[2]))
            info_label_1_var[2].show()

            # If Confirmed Run Main Function
            if confirm_op2_bool is True:
                print('-- ThreadClass2: confirm_op2_bool: accepted')
                btnx_main_var[2].setIcon(QIcon(img_active_var[2]))
                change_var = False
                if path_bool == 'MUSIC_SOURCE_True' and dest_bool == 'MUSIC_DESTINATION_True':
                    info_label_1_var[2].setText('working...')
                    cp_var = 0
                    for dirName, subdirList, fileList in os.walk(path):
                        for fname in fileList:
                            fullpath = os.path.join(dirName, fname)
                            t_path = fullpath.replace(path, '')
                            t_path = dest + t_path
                            if not fullpath.endswith('.ini'):
                                if not os.path.exists(t_path):
                                    change_var = True
                                    try:
                                        shutil.copy(fullpath, t_path)
                                    except IOError:
                                        os.makedirs(os.path.dirname(t_path))
                                        shutil.copy(fullpath, t_path)
                                    cp_var += 1
                                elif os.path.exists(t_path):
                                    if compare_bool is True:
                                        ma = os.path.getmtime(fullpath)
                                        mb = os.path.getmtime(t_path)
                                        if mb < ma:
                                            change_var = True
                                            try:
                                                shutil.copy(fullpath, t_path)
                                            except IOError:
                                                os.makedirs(os.path.dirname(t_path))
                                                shutil.copy(fullpath, t_path)
                                            cp_var += 1
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


# Sector 1 Class: Main Function Button Thread 3
class ThreadClass3(QThread):
    def __init__(self, confirm_op3_tru, confirm_op3_fal):
        QThread.__init__(self)
        self.confirm_op3_tru = confirm_op3_tru
        self.confirm_op3_fal = confirm_op3_fal

    def run(self):
        global btnx_main_var, img_active_var, img_var, path_var, thread_var, info_label_1_var, timer_thread_var
        global path_bool_var, dest_path_bool_var, configuration_engaged, confirm_op3_wait, confirm_op3_bool

        # Allow To Run Only When Source & Destination Configuration Is Disengaged
        zero = '0'
        centillionth_str = str('0.' + zero * 303 + '1')
        centillionth = float(centillionth_str)
        if configuration_engaged is True:
            while configuration_engaged is True:
                time.sleep(centillionth)

        # If Source & Destination Configuration Is Disengaged Then Continue
        elif configuration_engaged is False:

            # Set Paths In Stone Before Continuing. Asigns Source & Destination Variables To New Variables That Cannot Be Changed Once Function Exectutes
            path = path_var[3]
            dest = dest_path_var[3]
            path_bool = path_bool_var[3]
            dest_bool = dest_path_bool_var[3]
            compare_bool = compare_bool_var[3]

            # Provide Confirmation/Declination Buttons & Wait For Confirmation/Declination Then Reset Global confirm_op0_wait Boolean Back to True
            btnx_main_var[3].setIcon(QIcon('./image/img_pictures_amber.png'))
            info_label_1_var[3].hide()
            self.confirm_op3_tru.show()
            self.confirm_op3_fal.show()
            while confirm_op3_wait is True:
                time.sleep(0.3)
            confirm_op3_wait = True

            # Confirmation/Declination Occured, Hide Confirmation/Declination Buttons
            self.confirm_op3_tru.hide()
            self.confirm_op3_fal.hide()
            btnx_main_var[3].setIcon(QIcon(img_var[3]))
            info_label_1_var[3].show()

            # If Confirmed Run Main Function
            if confirm_op3_bool is True:
                print('-- ThreadClass3: confirm_op3_bool: accepted')
                btnx_main_var[3].setIcon(QIcon(img_active_var[3]))
                change_var = False
                if path_bool == 'PICTURE_SOURCE_True' and dest_bool == 'PICTURE_DESTINATION_True':
                    info_label_1_var[3].setText('working...')
                    cp_var = 0
                    for dirName, subdirList, fileList in os.walk(path):
                        for fname in fileList:
                            fullpath = os.path.join(dirName, fname)
                            t_path = fullpath.replace(path, '')
                            t_path = dest + t_path
                            if not fullpath.endswith('.ini'):
                                if not os.path.exists(t_path):
                                    change_var = True
                                    try:
                                        shutil.copy(fullpath, t_path)
                                    except IOError:
                                        os.makedirs(os.path.dirname(t_path))
                                        shutil.copy(fullpath, t_path)
                                    cp_var += 1
                                elif os.path.exists(t_path):
                                    if compare_bool is True:
                                        ma = os.path.getmtime(fullpath)
                                        mb = os.path.getmtime(t_path)
                                        if mb < ma:
                                            change_var = True
                                            try:
                                                shutil.copy(fullpath, t_path)
                                            except IOError:
                                                os.makedirs(os.path.dirname(t_path))
                                                shutil.copy(fullpath, t_path)
                                            cp_var += 1
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


# Sector 1 Class: Main Function Button Thread 4
class ThreadClass4(QThread):
    def __init__(self, confirm_op4_tru, confirm_op4_fal):
        QThread.__init__(self)
        self.confirm_op4_tru = confirm_op4_tru
        self.confirm_op4_fal = confirm_op4_fal

    def run(self):
        global btnx_main_var, img_active_var, img_var, path_var, thread_var, info_label_1_var, timer_thread_var
        global path_bool_var, dest_path_bool_var, configuration_engaged, confirm_op4_wait, confirm_op4_bool

        # Allow To Run Only When Source & Destination Configuration Is Disengaged
        zero = '0'
        centillionth_str = str('0.' + zero * 303 + '1')
        centillionth = float(centillionth_str)
        if configuration_engaged is True:
            while configuration_engaged is True:
                time.sleep(centillionth)

        # If Source & Destination Configuration Is Disengaged Then Continue
        elif configuration_engaged is False:

            # Set Paths In Stone Before Continuing. Asigns Source & Destination Variables To New Variables That Cannot Be Changed Once Function Exectutes
            path = path_var[4]
            dest = dest_path_var[4]
            path_bool = path_bool_var[4]
            dest_bool = dest_path_bool_var[4]
            compare_bool = compare_bool_var[4]

            # Provide Confirmation/Declination Buttons & Wait For Confirmation/Declination Then Reset Global confirm_op0_wait Boolean Back to True
            btnx_main_var[4].setIcon(QIcon('./image/img_program_amber.png'))
            info_label_1_var[4].hide()
            self.confirm_op4_tru.show()
            self.confirm_op4_fal.show()
            while confirm_op4_wait is True:
                time.sleep(0.3)
            confirm_op4_wait = True

            # Confirmation/Declination Occured, Hide Confirmation/Declination Buttons
            self.confirm_op4_tru.hide()
            self.confirm_op4_fal.hide()
            btnx_main_var[4].setIcon(QIcon(img_var[4]))
            info_label_1_var[4].show()

            # If Confirmed Run Main Function
            if confirm_op4_bool is True:
                print('-- ThreadClass4: confirm_op4_bool: accepted')
                btnx_main_var[4].setIcon(QIcon(img_active_var[4]))
                change_var = False
                if path_bool == 'PROGRAMS_SOURCE_True' and dest_bool == 'PROGRAMS_DESTINATION_True':
                    info_label_1_var[4].setText('working...')
                    cp_var = 0
                    for dirName, subdirList, fileList in os.walk(path):
                        for fname in fileList:
                            fullpath = os.path.join(dirName, fname)
                            t_path = fullpath.replace(path, '')
                            t_path = dest + t_path
                            if not fullpath.endswith('.ini'):
                                if not os.path.exists(t_path):
                                    change_var = True
                                    try:
                                        shutil.copy(fullpath, t_path)
                                    except IOError:
                                        os.makedirs(os.path.dirname(t_path))
                                        shutil.copy(fullpath, t_path)
                                    cp_var += 1
                                elif os.path.exists(t_path):
                                    if compare_bool is True:
                                        ma = os.path.getmtime(fullpath)
                                        mb = os.path.getmtime(t_path)
                                        if mb < ma:
                                            change_var = True
                                            try:
                                                shutil.copy(fullpath, t_path)
                                            except IOError:
                                                os.makedirs(os.path.dirname(t_path))
                                                shutil.copy(fullpath, t_path)
                                            cp_var += 1
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


# Sector 1 Class: Main Function Button Thread 5
class ThreadClass5(QThread):
    def __init__(self, confirm_op5_tru, confirm_op5_fal):
        QThread.__init__(self)
        self.confirm_op5_tru = confirm_op5_tru
        self.confirm_op5_fal = confirm_op5_fal

    def run(self):
        global btnx_main_var, img_active_var, img_var, path_var, thread_var, info_label_1_var, timer_thread_var
        global path_bool_var, dest_path_bool_var, configuration_engaged, confirm_op5_wait, confirm_op5_bool

        # Allow To Run Only When Source & Destination Configuration Is Disengaged
        zero = '0'
        centillionth_str = str('0.' + zero * 303 + '1')
        centillionth = float(centillionth_str)
        if configuration_engaged is True:
            while configuration_engaged is True:
                time.sleep(centillionth)

        # If Source & Destination Configuration Is Disengaged Then Continue
        elif configuration_engaged is False:

            # Set Paths In Stone Before Continuing. Asigns Source & Destination Variables To New Variables That Cannot Be Changed Once Function Exectutes
            path = path_var[5]
            dest = dest_path_var[5]
            path_bool = path_bool_var[5]
            dest_bool = dest_path_bool_var[5]
            compare_bool = compare_bool_var[5]

            # Provide Confirmation/Declination Buttons & Wait For Confirmation/Declination Then Reset Global confirm_op0_wait Boolean Back to True
            btnx_main_var[5].setIcon(QIcon('./image/img_video_amber.png'))
            info_label_1_var[5].hide()
            self.confirm_op5_tru.show()
            self.confirm_op5_fal.show()
            while confirm_op5_wait is True:
                time.sleep(0.3)
            confirm_op5_wait = True

            # Confirmation/Declination Occured, Hide Confirmation/Declination Buttons
            self.confirm_op5_tru.hide()
            self.confirm_op5_fal.hide()
            btnx_main_var[5].setIcon(QIcon(img_var[5]))
            info_label_1_var[5].show()

            # If Confirmed Run Main Function
            if confirm_op5_bool is True:
                print('-- ThreadClass5: confirm_op5_bool: accepted')
                btnx_main_var[5].setIcon(QIcon(img_active_var[5]))
                change_var = False
                if path_bool == 'VIDEO_SOURCE_True' and dest_bool == 'VIDEO_DESTINATION_True':
                    info_label_1_var[5].setText('working...')
                    cp_var = 0
                    for dirName, subdirList, fileList in os.walk(path):
                        for fname in fileList:
                            fullpath = os.path.join(dirName, fname)
                            t_path = fullpath.replace(path, '')
                            t_path = dest + t_path
                            if not fullpath.endswith('.ini'):
                                if not os.path.exists(t_path):
                                    change_var = True
                                    try:
                                        shutil.copy(fullpath, t_path)
                                    except IOError:
                                        os.makedirs(os.path.dirname(t_path))
                                        shutil.copy(fullpath, t_path)
                                    cp_var += 1
                                elif os.path.exists(t_path):
                                    if compare_bool is True:
                                        ma = os.path.getmtime(fullpath)
                                        mb = os.path.getmtime(t_path)
                                        if mb < ma:
                                            change_var = True
                                            try:
                                                shutil.copy(fullpath, t_path)
                                            except IOError:
                                                os.makedirs(os.path.dirname(t_path))
                                                shutil.copy(fullpath, t_path)
                                            cp_var += 1
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
