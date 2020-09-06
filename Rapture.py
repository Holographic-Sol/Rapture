import os
import sys
import time
import shutil
import datetime
import win32api
import win32process
import win32con
from win32api import GetSystemMetrics
from PyQt5.QtCore import Qt, QThread, QSize, QTimer, QPoint, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit, QDesktopWidget, QTextBrowser
from PyQt5.QtGui import QIcon, QFont, QPixmap
import distutils.dir_util

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

cfg_f = './config.txt'
img_path = './image/default/'
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
thread_engaged_var = [False, False, False, False, False, False]

source_selected = ()
dest_selected = ()
settings_active_int = 0
settings_active_int_prev = ()
pressed_int = ()
compare_clicked = ()

path_var = []
dest_path_var = []
btnx_main_var = []
stop_thr_button_var = []
comp_cont_button_var = []
back_label_var = []
btnx_settings_var = []
settings_source_edit_var = []
settings_dest_edit_var = []
settings_input_response_label = [(), ()]
paths_readonly_button_var = []

config_src_var = ['SOURCE 0:',
                  'SOURCE 1:',
                  'SOURCE 2:',
                  'SOURCE 3:',
                  'SOURCE 4:',
                  'SOURCE 5:']

config_dst_var = ['DESTINATION 0:',
                  'DESTINATION 1:',
                  'DESTINATION 2:',
                  'DESTINATION 3:',
                  'DESTINATION 4:',
                  'DESTINATION 5:']


# Read Configuration File
def get_conf_funk():
    global path_var, dest_path_var, img_path
    path_var = []
    dest_path_var = []

    if os.path.exists(cfg_f):
        print('-- found configuration file')
        with open(cfg_f, 'r') as fo:

            for line in fo:
                line = line.strip()

                # Read Image Path
                if line.startswith('IMAGE PATH: '):
                    line = line.replace('IMAGE PATH: ', '')
                    if line.startswith('./image/'):
                        if os.path.exists(line):
                            if not line.endswith('/'):
                                line = line + '/'
                            print('config image path exists:', line)
                            img_path = line
                        elif not os.path.exists(line):
                            print('config image path does not exist:', line)
                            print('using image path:', img_path)

                # Read Source Paths
                if line.startswith('SOURCE 0: '):
                    line = line.replace('SOURCE 0: ', '')
                    if os.path.exists(line) and len(path_var) <= 6:
                        print('config source path exists:', line)
                        path_var.append(line)
                    elif not os.path.exists(line) and len(path_var) <= 6:
                        print('config source path does not exist', line)
                        path_var.append('')

                if line.startswith('SOURCE 1: '):
                    line = line.replace('SOURCE 1: ', '')
                    if os.path.exists(line) and len(path_var) <= 6:
                        print('config source path exists:', line)
                        path_var.append(line)
                    elif not os.path.exists(line) and len(path_var) <= 6:
                        print('config source path does not exist', line)
                        path_var.append('')

                if line.startswith('SOURCE 2: '):
                    line = line.replace('SOURCE 2: ', '')
                    if os.path.exists(line) and len(path_var) <= 6:
                        print('config source path exists:', line)
                        path_var.append(line)
                    elif not os.path.exists(line) and len(path_var) <= 6:
                        print('config source path does not exist', line)
                        path_var.append('')

                if line.startswith('SOURCE 3: '):
                    line = line.replace('SOURCE 3: ', '')
                    if os.path.exists(line) and len(path_var) <= 6:
                        print('config source path exists:', line)
                        path_var.append(line)
                    elif not os.path.exists(line) and len(path_var) <= 6:
                        print('config source path does not exist', line)
                        path_var.append('')

                if line.startswith('SOURCE 4: '):
                    line = line.replace('SOURCE 4: ', '')
                    if os.path.exists(line) and len(path_var) <= 6:
                        print('config source path exists:', line)
                        path_var.append(line)
                    elif not os.path.exists(line) and len(path_var) <= 6:
                        print('config source path does not exist', line)
                        path_var.append('')

                if line.startswith('SOURCE 5: '):
                    line = line.replace('SOURCE 5: ', '')
                    if os.path.exists(line) and len(path_var) <= 6:
                        print('config source path exists:', line)
                        path_var.append(line)
                    elif not os.path.exists(line) and len(path_var) <= 6:
                        print('config source path does not exist', line)
                        path_var.append('')
                        
                # Read Destination Paths
                if line.startswith('DESTINATION 0: '):
                    line = line.replace('DESTINATION 0: ', '')
                    if os.path.exists(line) and len(dest_path_var) <= 6:
                        print('config destination path exists:', line)
                        dest_path_var.append(line)
                    elif not os.path.exists(line) and len(dest_path_var) <= 6:
                        print('config destination path does not exist', line)
                        dest_path_var.append('')

                if line.startswith('DESTINATION 1: '):
                    line = line.replace('DESTINATION 1: ', '')
                    if os.path.exists(line) and len(dest_path_var) <= 6:
                        print('config destination path exists:', line)
                        dest_path_var.append(line)
                    elif not os.path.exists(line) and len(dest_path_var) <= 6:
                        print('config destination path does not exist', line)
                        dest_path_var.append('')

                if line.startswith('DESTINATION 2: '):
                    line = line.replace('DESTINATION 2: ', '')
                    if os.path.exists(line) and len(dest_path_var) <= 6:
                        print('config destination path exists:', line)
                        dest_path_var.append(line)
                    elif not os.path.exists(line) and len(dest_path_var) <= 6:
                        print('config destination path does not exist', line)
                        dest_path_var.append('')

                if line.startswith('DESTINATION 3: '):
                    line = line.replace('DESTINATION 3: ', '')
                    if os.path.exists(line) and len(dest_path_var) <= 6:
                        print('config destination path exists:', line)
                        dest_path_var.append(line)
                    elif not os.path.exists(line) and len(dest_path_var) <= 6:
                        print('config destination path does not exist', line)
                        dest_path_var.append('')

                if line.startswith('DESTINATION 4: '):
                    line = line.replace('DESTINATION 4: ', '')
                    if os.path.exists(line) and len(dest_path_var) <= 6:
                        print('config destination path exists:', line)
                        dest_path_var.append(line)
                    elif not os.path.exists(line) and len(dest_path_var) <= 6:
                        print('config destination path does not exist', line)
                        dest_path_var.append('')

                if line.startswith('DESTINATION 5: '):
                    line = line.replace('DESTINATION 5: ', '')
                    if os.path.exists(line) and len(dest_path_var) <= 6:
                        print('config destination path exists:', line)
                        dest_path_var.append(line)
                    elif not os.path.exists(line) and len(dest_path_var) <= 6:
                        print('config destination path does not exist', line)
                        dest_path_var.append('')
        fo.close()

    # Write A New Configuration File
    elif not os.path.exists(cfg_f):
        print('-- creating new configuration file')
        open(cfg_f, 'w').close()
        with open(cfg_f, 'a') as fo:
            i = 0
            for config_src_vars in config_src_var:
                fo.writelines(config_src_var[i] + ' x' + '\n')
                i += 1
            i = 0
            for config_dst_vars in config_dst_var:
                fo.writelines(config_dst_var[i] + ' x' + '\n')
                i += 1
            fo.writelines('IMAGE PATH: ./image/default/')
        fo.close()
        get_conf_funk()


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        global img_path

        # Set Program Icon & Program Title
        self.setWindowIcon(QIcon('./icon.png'))
        self.title = 'Rapture Extreme Backup Solution'

        # Set Window Width And Height
        self.width = 605
        self.height = 110

        # Position Window On The Display
        scr_w = GetSystemMetrics(0)
        scr_h = GetSystemMetrics(1)
        self.left = (scr_w / 2) - (self.width / 2)
        self.top = ((scr_h / 2) - (self.height / 2))

        # Set Window Title Bar Frameless Windows Hint
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        # Set Font
        self.font_s5 = QFont("Segoe UI", 5, QFont.Normal)
        self.font_s6 = QFont("Segoe UI", 6, QFont.Normal)
        self.font_s8 = QFont("Segoe UI", 8, QFont.Normal)
        self.font_s5b = QFont("Segoe UI", 5, QFont.Bold)
        self.font_s6b = QFont("Segoe UI", 6, QFont.Bold)
        self.font_s8b = QFont("Segoe UI", 8, QFont.Bold)

        # Run Read Configuration File Function
        get_conf_funk()

        # Run Set Style Sheet Function
        self.set_style_sheet_funk()

        # Run Function That Pre-Appends Image Path Variable To Static Image Names
        self.set_images_funk()

        # Run initUI Function
        self.initUI()

    def initUI(self):
        global pressed_int
        global thread_var, settings_input_response_thread, update_settings_window_thread
        global btnx_main_var, btnx_settings_var, comp_cont_button_var, stop_thr_button_var, back_label_var, paths_readonly_button_var
        global settings_source_edit_var, settings_dest_edit_var, settings_input_response_label
        global path_var, dest_path_var
        global confirm_op0_bool, confirm_op0_wait, confirm_op1_bool, confirm_op1_wait, confirm_op2_bool, confirm_op2_wait
        global confirm_op3_bool, confirm_op3_wait, confirm_op4_bool, confirm_op4_wait, confirm_op5_bool, confirm_op5_wait

        # Set A Fixed Window Size
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.output_verbosity = 1

        # Title Bar: Close
        self.close_button = QPushButton(self)
        self.close_button.move((self.width - 20), 0)
        self.close_button.resize(20, 20)
        self.close_button.setIcon(QIcon("./image/default/img_titlebar_close.png"))
        self.close_button.setIconSize(QSize(8, 8))
        self.close_button.clicked.connect(QCoreApplication.instance().quit)
        self.close_button.setStyleSheet(self.default_title_qpb_style)

        # Title Bar: Minimize
        self.minimize_button = QPushButton(self)
        self.minimize_button.move((self.width - 50), 0)
        self.minimize_button.resize(20, 20)
        self.minimize_button.setIcon(QIcon("./image/default/img_titlebar_minimize.png"))
        self.minimize_button.setIconSize(QSize(50, 20))
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setStyleSheet(self.default_title_qpb_style)

        # Sector 1: Background Colour
        self.back_label_main = QLabel(self)
        self.back_label_main.move(0, 20)
        self.back_label_main.resize(self.width, 90)
        self.back_label_main.setStyleSheet(self.default_bg_0_style)

        # Sector 1: Background Tiles
        i = 0
        while i < 6:
            back_label = 'back_label' + str(i)
            self.back_label = QLabel(self)
            self.back_label.resize(95, 80)
            self.back_label.setStyleSheet(self.default_bg_tile_style)
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

        set_src_dst_w = (self.width - 152)
        set_src_dst_pos_w = 107

        # Sector 1: Objects Placed On Top Background Tiles
        i = 0
        while i < 6:

            # Sector 1: Main Function Button(s)
            btnx_name = 'btnx_main' + str(i)
            self.btnx_main = QPushButton(self)
            self.btnx_main.resize(54, 54)
            self.btnx_main.setIconSize(QSize(54, 54))
            self.btnx_main.setStyleSheet(self.btnx_main_style)
            btnx_main_var.append(self.btnx_main)

            # Sector 1: Drop Down Setting's Button(s)
            sett_name = 'btnx_settings' + str(i)
            self.sett_name = QPushButton(self)
            self.sett_name.resize(30, 10)
            self.sett_name.setIcon(QIcon(self.img_show_menu_false))
            self.sett_name.setIconSize(QSize(15, 15))
            self.sett_name.setStyleSheet(self.default_qpbtn_style)
            btnx_settings_var.append(self.sett_name)

            # Sector 1: Switch Main Function Mode Button(s)
            comp_cont_button = 'comp_cont_button' + str(i)
            self.comp_cont_button = QPushButton(self)
            self.comp_cont_button.resize(30, 26)
            self.comp_cont_button.setIcon(QIcon(self.img_mode_0))
            self.comp_cont_button.setIconSize(QSize(18, 18))
            self.comp_cont_button.setStyleSheet(self.default_qpbtn_style)
            comp_cont_button_var.append(self.comp_cont_button)

            # Sector 1: Stop Main Functions(s) Button(s)
            stop_thr_button = 'stop_thr_button' + str(i)
            self.stop_thr_button = QPushButton(self)
            self.stop_thr_button.resize(30, 10)
            self.stop_thr_button.setIcon(QIcon(self.img_stop_thread_false))
            self.stop_thr_button.setIconSize(QSize(15, 15))
            self.stop_thr_button.setStyleSheet(self.default_qpbtn_style)
            stop_thr_button_var.append(self.stop_thr_button)
            self.stop_thr_button.setEnabled(False)

            # Sector 2: Enable/Disable ReadOnly Path Settings
            paths_readonly_button = 'paths_readonly_button' + str(i)
            self.paths_readonly_button = QPushButton(self)
            self.paths_readonly_button.resize(15, 35)
            self.paths_readonly_button.move((set_src_dst_pos_w + set_src_dst_w + 15), 126)
            self.paths_readonly_button.setIcon(QIcon(self.img_read_ony_true))
            self.paths_readonly_button.setIconSize(QSize(8, 8))
            self.paths_readonly_button.setStyleSheet(self.default_qpbtn_style)
            paths_readonly_button_var.append(self.paths_readonly_button)
            paths_readonly_button_var[i].hide()

            i += 1

        # Setctor 1: Set Btnx Images
        btnx_main_var[0].setIcon(QIcon(self.img_btnx_led_0))
        btnx_main_var[1].setIcon(QIcon(self.img_btnx_led_0))
        btnx_main_var[2].setIcon(QIcon(self.img_btnx_led_0))
        btnx_main_var[3].setIcon(QIcon(self.img_btnx_led_0))
        btnx_main_var[4].setIcon(QIcon(self.img_btnx_led_0))
        btnx_main_var[5].setIcon(QIcon(self.img_btnx_led_0))

        # Sector 2: Hide Drop Down Settings
        self.hide_settings_button = QPushButton(self)
        self.hide_settings_button.resize(self.width, 10)
        self.hide_settings_button.move(0, 310)
        self.hide_settings_button.setIcon(QIcon(self.img_show_menu_true))
        self.hide_settings_button.clicked.connect(self.hide_settings_page_funk)
        self.hide_settings_button.setIconSize(QSize(15, 15))
        self.hide_settings_button.setStyleSheet(self.default_qpbtn_style)

        # Sector 2: Settings Page Left
        self.scr_left = QPushButton(self)
        self.scr_left.resize(10, 35)
        self.scr_left.move(0, 126)
        self.scr_left.setIcon(QIcon(self.img_menu_left))
        self.scr_left.setIconSize(QSize(15, 35))
        self.scr_left.clicked.connect(self.scr_left_funk)
        self.scr_left.setStyleSheet(self.default_qpbtn_style)

        # Sector 2: Settings Page Right
        self.scr_right = QPushButton(self)
        self.scr_right.resize(10, 35)
        self.scr_right.move((self.width - 10), 126)
        self.scr_right.setIcon(QIcon(self.img_menu_right))
        self.scr_right.setIconSize(QSize(15, 35))
        self.scr_right.clicked.connect(self.scr_right_funk)
        self.scr_right.setStyleSheet(self.default_qpbtn_style)

        # Sector 2: A Label To Signify Source Path Configuration
        self.settings_source_label = QLabel(self)
        self.settings_source_label.move(15, 126)
        self.settings_source_label.resize(87, 15)
        self.settings_source_label.setFont(self.font_s6b)
        self.settings_source_label.setText('Source:')
        self.settings_source_label.setStyleSheet(self.default_qlbl_style)
        self.settings_source_label.setAlignment(Qt.AlignCenter) 

        # Sector 2: A Label To Signify Destination Path Configuration
        self.settings_dest_label = QLabel(self)
        self.settings_dest_label.move(15, 145)
        self.settings_dest_label.resize(87, 15)
        self.settings_dest_label.setFont(self.font_s6b)
        self.settings_dest_label.setText('Destination:')
        self.settings_dest_label.setStyleSheet(self.default_qlbl_style)
        self.settings_dest_label.setAlignment(Qt.AlignCenter) 

        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 0
        self.setting_title0 = QLabel(self)
        self.setting_title0.resize(87, 14)
        self.setting_title0.move((back_label_ankor_w0 + 5), 105)
        self.setting_title0.setFont(self.font_s6b)
        self.setting_title0.setText("Archives")
        self.setting_title0.setStyleSheet(self.default_qlbl_style)
        self.setting_title0.setAlignment(Qt.AlignCenter) 
        self.setting_title0.hide()

        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 1
        self.setting_title1 = QLabel(self)
        self.setting_title1.resize(87, 14)
        self.setting_title1.move((back_label_ankor_w1 + 5), 105)
        self.setting_title1.setFont(self.font_s6b)
        self.setting_title1.setText("Documents")
        self.setting_title1.setStyleSheet(self.default_qlbl_style)
        self.setting_title1.setAlignment(Qt.AlignCenter)
        self.setting_title1.hide()

        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 2
        self.setting_title2 = QLabel(self)
        self.setting_title2.resize(87, 14)
        self.setting_title2.move((back_label_ankor_w2 + 5), 105)
        self.setting_title2.setFont(self.font_s6b)
        self.setting_title2.setText("Music")
        self.setting_title2.setStyleSheet(self.default_qlbl_style)
        self.setting_title2.setAlignment(Qt.AlignCenter)
        self.setting_title2.hide()

        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 3
        self.setting_title3 = QLabel(self)
        self.setting_title3.resize(87, 14)
        self.setting_title3.move((back_label_ankor_w3 + 5), 105)
        self.setting_title3.setFont(self.font_s6b)
        self.setting_title3.setText("Pictures")
        self.setting_title3.setStyleSheet(self.default_qlbl_style)
        self.setting_title3.setAlignment(Qt.AlignCenter)
        self.setting_title3.hide()

        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 4
        self.setting_title4 = QLabel(self)
        self.setting_title4.resize(87, 14)
        self.setting_title4.move((back_label_ankor_w4 + 5), 105)
        self.setting_title4.setFont(self.font_s6b)
        self.setting_title4.setText("Videos")
        self.setting_title4.setStyleSheet(self.default_qlbl_style)
        self.setting_title4.setAlignment(Qt.AlignCenter)
        self.setting_title4.hide()

        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 5
        self.setting_title5 = QLabel(self)
        self.setting_title5.resize(87, 14)
        self.setting_title5.move((back_label_ankor_w5 + 5), 105)
        self.setting_title5.setFont(self.font_s6b)
        self.setting_title5.setText("Programs")
        self.setting_title5.setStyleSheet(self.default_qlbl_style)
        self.setting_title5.setAlignment(Qt.AlignCenter) 
        self.setting_title5.hide()

        # Sector 2: Source Path Configuration Edit 0
        self.settings_source0 = QLineEdit(self)
        self.settings_source0.move(set_src_dst_pos_w, 126)
        self.settings_source0.resize(set_src_dst_w, 15)
        self.settings_source0.setFont(self.font_s6b)
        self.settings_source0.setText(path_var[0])
        self.settings_source0.setReadOnly(True)
        self.settings_source0.returnPressed.connect(self.settings_source_pre_funk0)
        self.settings_source0.setStyleSheet(self.default_qle_style)
        settings_source_edit_var.append(self.settings_source0)
        self.settings_source0.hide()

        # Sector 2: Source Path Configuration Edit 1
        self.settings_source1 = QLineEdit(self)
        self.settings_source1.move(set_src_dst_pos_w, 126)
        self.settings_source1.resize(set_src_dst_w, 15)
        self.settings_source1.setFont(self.font_s6b)
        self.settings_source1.setText(path_var[1])
        self.settings_source1.setReadOnly(True)
        self.settings_source1.returnPressed.connect(self.settings_source_pre_funk1)
        self.settings_source1.setStyleSheet(self.default_qle_style)
        settings_source_edit_var.append(self.settings_source1)
        self.settings_source1.hide()

        # Sector 2: Source Path Configuration Edit 2
        self.settings_source2 = QLineEdit(self)
        self.settings_source2.move(set_src_dst_pos_w, 126)
        self.settings_source2.resize(set_src_dst_w, 15)
        self.settings_source2.setFont(self.font_s6b)
        self.settings_source2.setText(path_var[2])
        self.settings_source2.setReadOnly(True)
        self.settings_source2.returnPressed.connect(self.settings_source_pre_funk2)
        self.settings_source2.setStyleSheet(self.default_qle_style)
        settings_source_edit_var.append(self.settings_source2)
        self.settings_source2.hide()

        # Sector 2: Source Path Configuration Edit 3
        self.settings_source3 = QLineEdit(self)
        self.settings_source3.move(set_src_dst_pos_w, 126)
        self.settings_source3.resize(set_src_dst_w, 15)
        self.settings_source3.setFont(self.font_s6b)
        self.settings_source3.setText(path_var[3])
        self.settings_source3.setReadOnly(True)
        self.settings_source3.returnPressed.connect(self.settings_source_pre_funk3)
        self.settings_source3.setStyleSheet(self.default_qle_style)
        settings_source_edit_var.append(self.settings_source3)
        self.settings_source3.hide()

        # Sector 2: Source Path Configuration Edit 4
        self.settings_source4 = QLineEdit(self)
        self.settings_source4.move(set_src_dst_pos_w, 126)
        self.settings_source4.resize(set_src_dst_w, 15)
        self.settings_source4.setFont(self.font_s6b)
        self.settings_source4.setText(path_var[4])
        self.settings_source4.setReadOnly(True)
        self.settings_source4.returnPressed.connect(self.settings_source_pre_funk4)
        self.settings_source4.setStyleSheet(self.default_qle_style)
        settings_source_edit_var.append(self.settings_source4)
        self.settings_source4.hide()

        # Sector 2: Source Path Configuration Edit 5
        self.settings_source5 = QLineEdit(self)
        self.settings_source5.move(set_src_dst_pos_w, 126)
        self.settings_source5.resize(set_src_dst_w, 15)
        self.settings_source5.setFont(self.font_s6b)
        self.settings_source5.setText(path_var[5])
        self.settings_source5.setReadOnly(True)
        self.settings_source5.returnPressed.connect(self.settings_source_pre_funk5)
        self.settings_source5.setStyleSheet(self.default_qle_style)
        settings_source_edit_var.append(self.settings_source5)
        self.settings_source5.hide()

        # Sector 2: Destination Path Configuration Edit 0
        self.settings_dest0 = QLineEdit(self)
        self.settings_dest0.move(set_src_dst_pos_w, 145)
        self.settings_dest0.resize(set_src_dst_w, 15)
        self.settings_dest0.setFont(self.font_s6b)
        self.settings_dest0.setText(dest_path_var[0])
        self.settings_dest0.setReadOnly(True)
        self.settings_dest0.returnPressed.connect(self.settings_dest_pre_funk0)
        self.settings_dest0.setStyleSheet(self.default_qle_style)
        settings_dest_edit_var.append(self.settings_dest0)
        self.settings_dest0.hide()

        # Sector 2: Destination Path Configuration Edit 1
        self.settings_dest1 = QLineEdit(self)
        self.settings_dest1.move(set_src_dst_pos_w, 145)
        self.settings_dest1.resize(set_src_dst_w, 15)
        self.settings_dest1.setFont(self.font_s6b)
        self.settings_dest1.setText(dest_path_var[1])
        self.settings_dest1.setReadOnly(True)
        self.settings_dest1.returnPressed.connect(self.settings_dest_pre_funk1)
        self.settings_dest1.setStyleSheet(self.default_qle_style)
        settings_dest_edit_var.append(self.settings_dest1)
        self.settings_dest1.hide()

        # Sector 2: Destination Path Configuration Edit 2
        self.settings_dest2 = QLineEdit(self)
        self.settings_dest2.move(set_src_dst_pos_w, 145)
        self.settings_dest2.resize(set_src_dst_w, 15)
        self.settings_dest2.setFont(self.font_s6b)
        self.settings_dest2.setText(dest_path_var[2])
        self.settings_dest2.setReadOnly(True)
        self.settings_dest2.returnPressed.connect(self.settings_dest_pre_funk2)
        self.settings_dest2.setStyleSheet(self.default_qle_style)
        settings_dest_edit_var.append(self.settings_dest2)
        self.settings_dest2.hide()

        # Sector 2: Destination Path Configuration Edit 3
        self.settings_dest3 = QLineEdit(self)
        self.settings_dest3.move(set_src_dst_pos_w, 145)
        self.settings_dest3.resize(set_src_dst_w, 15)
        self.settings_dest3.setFont(self.font_s6b)
        self.settings_dest3.setText(dest_path_var[3])
        self.settings_dest3.setReadOnly(True)
        self.settings_dest3.returnPressed.connect(self.settings_dest_pre_funk3)
        self.settings_dest3.setStyleSheet(self.default_qle_style)
        settings_dest_edit_var.append(self.settings_dest3)
        self.settings_dest3.hide()

        # Sector 2: Destination Path Configuration Edit 4
        self.settings_dest4 = QLineEdit(self)
        self.settings_dest4.move(set_src_dst_pos_w, 145)
        self.settings_dest4.resize(set_src_dst_w, 15)
        self.settings_dest4.setFont(self.font_s6b)
        self.settings_dest4.setText(dest_path_var[4])
        self.settings_dest4.setReadOnly(True)
        self.settings_dest4.returnPressed.connect(self.settings_dest_pre_funk4)
        self.settings_dest4.setStyleSheet(self.default_qle_style)
        settings_dest_edit_var.append(self.settings_dest4)
        self.settings_dest4.hide()

        # Sector 2: Destination Path Configuration Edit 5
        self.settings_dest5 = QLineEdit(self)
        self.settings_dest5.move(set_src_dst_pos_w, 145)
        self.settings_dest5.resize(set_src_dst_w, 15)
        self.settings_dest5.setFont(self.font_s6b)
        self.settings_dest5.setText(dest_path_var[5])
        self.settings_dest5.setReadOnly(True)
        self.settings_dest5.returnPressed.connect(self.settings_dest_pre_funk5)
        self.settings_dest5.setStyleSheet(self.default_qle_style)
        settings_dest_edit_var.append(self.settings_dest5)
        self.settings_dest5.hide()

        # Sector 2: File Path Validation LED Source
        self.settings_input_response_label_src = QLabel(self)
        self.settings_input_response_label_src.move((set_src_dst_pos_w + set_src_dst_w + 5), 126)
        self.settings_input_response_label_src.resize(5, 15)
        self.settings_input_response_label_src.setStyleSheet(self.default_valid_path_led)
        settings_input_response_label[0] = self.settings_input_response_label_src

        # Sector 2: File Path Validation LED Destination
        self.settings_input_response_label_dst = QLabel(self)
        self.settings_input_response_label_dst.move((set_src_dst_pos_w + set_src_dst_w + 5), 145)
        self.settings_input_response_label_dst.resize(5, 15)
        self.settings_input_response_label_dst.setStyleSheet(self.default_valid_path_led)
        settings_input_response_label[1] = self.settings_input_response_label_dst

         # Sector 1: Main Function Confirmation 0
        self.confirm_op0_tru = QPushButton(self)
        self.confirm_op0_tru.resize(87, 13)
        self.confirm_op0_tru.setIcon(QIcon(self.img_execute_false))
        self.confirm_op0_tru.setIconSize(QSize(45, 10))
        self.confirm_op0_tru.setStyleSheet(self.default_qpbtn_style)
        self.confirm_op0_tru.move((back_label_ankor_w0 + 5), (back_label_ankor_h0 + 63))
        self.confirm_op0_tru.clicked.connect(self.confirm_op0_funk0)
        self.confirm_op0_tru.setEnabled(False)
        self.confirm_op0_tru.show()

        # Sector 1: Main Function Confirmation 1
        self.confirm_op1_tru = QPushButton(self)
        self.confirm_op1_tru.resize(87, 13)
        self.confirm_op1_tru.setIcon(QIcon(self.img_execute_false))
        self.confirm_op1_tru.setIconSize(QSize(45, 10))
        self.confirm_op1_tru.setStyleSheet(self.default_qpbtn_style)
        self.confirm_op1_tru.move((back_label_ankor_w1 + 5), (back_label_ankor_h1 + 63))
        self.confirm_op1_tru.clicked.connect(self.confirm_op1_funk0)
        self.confirm_op1_tru.setEnabled(False)
        self.confirm_op1_tru.show()

        # Sector 1: Main Function Confirmation 2
        self.confirm_op2_tru = QPushButton(self)
        self.confirm_op2_tru.resize(87, 13)
        self.confirm_op2_tru.setIcon(QIcon(self.img_execute_false))
        self.confirm_op2_tru.setIconSize(QSize(45, 10))
        self.confirm_op2_tru.setStyleSheet(self.default_qpbtn_style)
        self.confirm_op2_tru.move((back_label_ankor_w2 + 5), (back_label_ankor_h2 + 63))
        self.confirm_op2_tru.clicked.connect(self.confirm_op2_funk0)
        self.confirm_op2_tru.setEnabled(False)
        self.confirm_op2_tru.show()

        # Sector 1: Main Function Confirmation 3
        self.confirm_op3_tru = QPushButton(self)
        self.confirm_op3_tru.resize(87, 13)
        self.confirm_op3_tru.setIcon(QIcon(self.img_execute_false))
        self.confirm_op3_tru.setIconSize(QSize(45, 10))
        self.confirm_op3_tru.setStyleSheet(self.default_qpbtn_style)
        self.confirm_op3_tru.move((back_label_ankor_w3 + 5), (back_label_ankor_h3 + 63))
        self.confirm_op3_tru.clicked.connect(self.confirm_op3_funk0)
        self.confirm_op3_tru.setEnabled(False)
        self.confirm_op3_tru.show()

        # Sector 1: Main Function Confirmation 4
        self.confirm_op4_tru = QPushButton(self)
        self.confirm_op4_tru.resize(87, 13)
        self.confirm_op4_tru.setIcon(QIcon(self.img_execute_false))
        self.confirm_op4_tru.setIconSize(QSize(45, 10))
        self.confirm_op4_tru.setStyleSheet(self.default_qpbtn_style)
        self.confirm_op4_tru.move((back_label_ankor_w4 + 5), (back_label_ankor_h4 + 63))
        self.confirm_op4_tru.clicked.connect(self.confirm_op4_funk0)
        self.confirm_op4_tru.setEnabled(False)
        self.confirm_op4_tru.show()

        # Sector 1: Main Function Confirmation 5
        self.confirm_op5_tru = QPushButton(self)
        self.confirm_op5_tru.resize(87, 13)
        self.confirm_op5_tru.setIcon(QIcon(self.img_execute_false))
        self.confirm_op5_tru.setIconSize(QSize(45, 10))
        self.confirm_op5_tru.setStyleSheet(self.default_qpbtn_style)
        self.confirm_op5_tru.move((back_label_ankor_w5 + 5), (back_label_ankor_h5 + 63))
        self.confirm_op5_tru.clicked.connect(self.confirm_op5_funk0)
        self.confirm_op5_tru.setEnabled(False)
        self.confirm_op5_tru.show()

        # Sector 3: Output Text Browser Dimensions
        self.tb_w = self.width - 10
        self.tb_h = 115
        self.tb_pos_w = 5
        self.tb_pos_h = 185

        # Sector 3: Output Text Browser Label 0
        self.tb_label_0 = QLabel(self)
        self.tb_label_0.move(5, (self.tb_pos_h - 14))
        self.tb_label_0.resize(87, 14)
        self.tb_label_0.setFont(self.font_s6b)
        self.tb_label_0.setStyleSheet(self.default_qlbl_style)
        self.tb_label_0.setAlignment(Qt.AlignCenter)
        self.tb_label_0.hide()

        # Sector 3: Output Text Browser 0
        self.tb_0 = QTextBrowser(self)
        self.tb_0.move(self.tb_pos_w, self.tb_pos_h)
        self.tb_0.resize(self.tb_w, self.tb_h)
        self.tb_0.setFont(self.font_s6b)
        self.tb_0.setObjectName("tb_0")
        self.tb_0.setStyleSheet(self.default_qtbb_style)
        self.tb_0.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_0.horizontalScrollBar().setValue(0)

        # Sector 3: Output Text Browser 1
        self.tb_1 = QTextBrowser(self)
        self.tb_1.move(self.tb_pos_w, self.tb_pos_h)
        self.tb_1.resize(self.tb_w, self.tb_h)
        self.tb_1.setFont(self.font_s6b)
        self.tb_1.setObjectName("tb_1")
        self.tb_1.setStyleSheet(self.default_qtbb_style)
        self.tb_1.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_1.horizontalScrollBar().setValue(0)

        # Sector 3: Output Text Browser 2
        self.tb_2 = QTextBrowser(self)
        self.tb_2.move(self.tb_pos_w, self.tb_pos_h)
        self.tb_2.resize(self.tb_w, self.tb_h)
        self.tb_2.setFont(self.font_s6b)
        self.tb_2.setObjectName("tb_2")
        self.tb_2.setStyleSheet(self.default_qtbb_style)
        self.tb_2.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_2.horizontalScrollBar().setValue(0)

        # Sector 3: Output Text Browser 3
        self.tb_3 = QTextBrowser(self)
        self.tb_3.move(self.tb_pos_w, self.tb_pos_h)
        self.tb_3.resize(self.tb_w, self.tb_h)
        self.tb_3.setFont(self.font_s6b)
        self.tb_3.setObjectName("tb_3")
        self.tb_3.setStyleSheet(self.default_qtbb_style)
        self.tb_3.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_3.horizontalScrollBar().setValue(0)

        # Sector 3: Output Text Browser 4
        self.tb_4 = QTextBrowser(self)
        self.tb_4.move(self.tb_pos_w, self.tb_pos_h)
        self.tb_4.resize(self.tb_w, self.tb_h)
        self.tb_4.setFont(self.font_s6b)
        self.tb_4.setObjectName("tb_4")
        self.tb_4.setStyleSheet(self.default_qtbb_style)
        self.tb_4.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_4.horizontalScrollBar().setValue(0)

        # Sector 3: Output Text Browser 5
        self.tb_5 = QTextBrowser(self)
        self.tb_5.move(self.tb_pos_w, self.tb_pos_h)
        self.tb_5.resize(self.tb_w, self.tb_h)
        self.tb_5.setFont(self.font_s6b)
        self.tb_5.setObjectName("tb_5")
        self.tb_5.setStyleSheet(self.default_qtbb_style)
        self.tb_5.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_5.horizontalScrollBar().setValue(0)

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
        btnx_main_var[0].clicked.connect(self.btnx_set_focus_funk_0)
        btnx_main_var[1].clicked.connect(self.btnx_set_focus_funk_1)
        btnx_main_var[2].clicked.connect(self.btnx_set_focus_funk_2)
        btnx_main_var[3].clicked.connect(self.btnx_set_focus_funk_3)
        btnx_main_var[4].clicked.connect(self.btnx_set_focus_funk_4)
        btnx_main_var[5].clicked.connect(self.btnx_set_focus_funk_5)

        # Sector 1: Plug Drop Down Settings Buttons Into Functions
        btnx_settings_var[0].clicked.connect(self.settings_funk0)
        btnx_settings_var[1].clicked.connect(self.settings_funk1)
        btnx_settings_var[2].clicked.connect(self.settings_funk2)
        btnx_settings_var[3].clicked.connect(self.settings_funk3)
        btnx_settings_var[4].clicked.connect(self.settings_funk4)
        btnx_settings_var[5].clicked.connect(self.settings_funk5)

        # Sector 2: Plug Read Only Buttons Into Read Only Functions
        paths_readonly_button_var[0].clicked.connect(self.paths_readonly_button_funk_0)
        paths_readonly_button_var[1].clicked.connect(self.paths_readonly_button_funk_1)
        paths_readonly_button_var[2].clicked.connect(self.paths_readonly_button_funk_2)
        paths_readonly_button_var[3].clicked.connect(self.paths_readonly_button_funk_3)
        paths_readonly_button_var[4].clicked.connect(self.paths_readonly_button_funk_4)
        paths_readonly_button_var[5].clicked.connect(self.paths_readonly_button_funk_5)

        # Thread: Adjusts App Geometry To Account For Display Re-Scaling
        self.oldPos = self.pos()
        scaling_thread = ScalingClass(self.setGeometry, self.width, self.height, self.pos)
        scaling_thread.start()

        # Thread: Checks The Validity Of Directory Paths Set In Sector 2 As Source & Destination And Updates GUI Accordingly
        update_settings_window_thread = UpdateSettingsWindow()
        update_settings_window_thread.start()

        # Thread: Main Function Thread - Read/Write Thread 0
        thread_var[0] = ThreadClass0(self.tb_0,
                                     self.confirm_op0_tru,
                                     self.img_btnx_led_0,
                                     self.img_btnx_led_1,
                                     self.img_btnx_led_2,
                                     self.img_execute_false,
                                     self.img_execute_true,
                                     self.img_stop_thread_false,
                                     self.img_stop_thread_true,
                                     self.output_verbosity)

        # Thread: Main Function Thread - Read/Write Thread 1
        thread_var[1] = ThreadClass1(self.tb_1,
                                     self.confirm_op1_tru,
                                     self.img_btnx_led_0,
                                     self.img_btnx_led_1,
                                     self.img_btnx_led_2,
                                     self.img_execute_false,
                                     self.img_execute_true,
                                     self.img_stop_thread_false,
                                     self.img_stop_thread_true,
                                     self.output_verbosity)

        # Thread: Main Function Thread - Read/Write Thread 2
        thread_var[2] = ThreadClass2(self.tb_2,
                                     self.confirm_op2_tru,
                                     self.img_btnx_led_0,
                                     self.img_btnx_led_1,
                                     self.img_btnx_led_2,
                                     self.img_execute_false,
                                     self.img_execute_true,
                                     self.img_stop_thread_false,
                                     self.img_stop_thread_true,
                                     self.output_verbosity)

        # Thread: Main Function Thread - Read/Write Thread 3
        thread_var[3] = ThreadClass3(self.tb_3,
                                     self.confirm_op3_tru,
                                     self.img_btnx_led_0,
                                     self.img_btnx_led_1,
                                     self.img_btnx_led_2,
                                     self.img_execute_false,
                                     self.img_execute_true,
                                     self.img_stop_thread_false,
                                     self.img_stop_thread_true,
                                     self.output_verbosity)

        # Thread: Main Function Thread - Read/Write Thread 4
        thread_var[4] = ThreadClass4(self.tb_4,
                                     self.confirm_op4_tru,
                                     self.img_btnx_led_0,
                                     self.img_btnx_led_1,
                                     self.img_btnx_led_2,
                                     self.img_execute_false,
                                     self.img_execute_true,
                                     self.img_stop_thread_false,
                                     self.img_stop_thread_true,
                                     self.output_verbosity)

        # Thread: Main Function Thread - Read/Write Thread 5
        thread_var[5] = ThreadClass5(self.tb_5,
                                     self.confirm_op5_tru,
                                     self.img_btnx_led_0,
                                     self.img_btnx_led_1,
                                     self.img_btnx_led_2,
                                     self.img_execute_false,
                                     self.img_execute_true,
                                     self.img_stop_thread_false,
                                     self.img_stop_thread_true,
                                     self.output_verbosity)

        # Thread: LEDs In Sector 2 Indicate Source & Destination Path Validity
        settings_input_response_thread = SettingsInputResponse(self.default_valid_path_led_green,
                                                               self.default_valid_path_led_red,
                                                               self.default_valid_path_led)

        # Plugged In & Threaded: Display The Application
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

    # Function: Sets StyleSheets And Window Pallette
    def set_style_sheet_funk(self):
        print('-- plugged in: set_style_sheet_funk')

        # Default Window Colour
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        # Default Stylesheet: Scrollbars
        self.setStyleSheet("""
                    QScrollBar:vertical {width: 11px;
                    margin: 11px 0 11px 0;
                    background-color: black;
                    }
                    QScrollBar::handle:vertical {
                    background-color: black;
                    min-height: 11px;
                    }
                    QScrollBar::add-line:vertical {
                    background-color: black;
                    height: 11px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                    }
                    QScrollBar::sub-line:vertical {
                    background-color: black;
                    height: 11px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                    }
                    QScrollBar::up-arrow:vertical {
                    image:url('./image/default/img_scrollbar_up.png');
                    height: 11px;
                    width: 11px;
                    }
                    QScrollBar::down-arrow:vertical {
                    image:url('./image/default/img_scrollbar_down.png');
                    height: 11px;
                    width: 11px;
                    }
                    QScrollBar::add-page:vertical {
                    background: rgb(25, 25, 25);
                    }
                    QScrollBar::sub-page:vertical {
                    background: rgb(25, 25, 25);
                    }

                    QScrollBar:horizontal {
                    height: 11px;
                    margin: 0px 11px 0 11px;
                    background-color: black;
                    }
                    QScrollBar::handle:horizontal {
                    background-color: black;
                    min-width: 11px;
                    }
                    QScrollBar::add-line:horizontal {
                    background-color: black;
                    width: 11px;
                    subcontrol-position: right;
                    subcontrol-origin: margin;
                    }
                    QScrollBar::sub-line:horizontal {
                    background-color: black;
                    width: 11px;
                    subcontrol-position: top left;
                    subcontrol-origin: margin;
                    position: absolute;
                    }
                    QScrollBar::left-arrow:horizontal {
                    image:url('./image/default/img_scrollbar_left.png');
                    height: 11px;
                    width: 11px;
                    }
                    QScrollBar::right-arrow:horizontal {
                    image:url('./image/default/img_scrollbar_right.png');
                    height: 11px;
                    width: 11px;
                    }
                    QScrollBar::add-page:horizontal {
                    background: rgb(25, 25, 25);
                    }
                    QScrollBar::sub-page:horizontal {
                    background: rgb(25, 25, 25);
                    }
                    """)

        # Default Stylesheet: Title Bar QPushButtons
        self.default_title_qpb_style = """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 0, 0);}"""

        # Default StyleSheet: Background Tiles
        self.default_bg_tile_style = """QLabel {background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 0, 0);}"""

        # Default StyleSheet: Background Colour
        self.default_bg_0_style = """QLabel {background-color: rgb(30, 30, 30);
           border:0px solid rgb(35, 35, 35);}"""

        # Default Stylesheet: Valid Path LED
        self.default_valid_path_led = """QLabel {background-color: rgb(15, 15, 15);
           border:1px solid rgb(15, 15, 15);}"""

        # Default Stylesheet: Valid Source Path LED Green
        self.default_valid_path_led_green = """QLabel {background-color: rgb(0, 255, 0);
           border:2px solid rgb(35, 35, 35);}"""

        # Default Stylesheet: Valid Source Path LED Red
        self.default_valid_path_led_red = """QLabel {background-color: rgb(255, 0, 0);
           border:2px solid rgb(35, 35, 35);}"""

        # Default StyleSheet: QLabels
        self.default_qlbl_style = """QLabel {background-color: rgb(30, 30, 30);
           color: grey;
           border:0px solid rgb(35, 35, 35);}"""

        # Default StyleSheet: QPushButtons
        self.default_qpbtn_style = """QPushButton{background-color: rgb(35, 35, 35);
               border:0px solid rgb(0, 0, 0);}"""

        # Default StyleSheet: QPushButtons Pressed
        self.default_qpbtn_prsd_style = """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 0, 0);}"""

        # Default Stylesheet: QLineEdit
        self.default_qle_style = """QLineEdit {background-color: rgb(30, 30, 30);
            border:0px solid rgb(0, 0, 0);
            selection-color: white;
            selection-background-color: rgb(0, 100, 255);
            color: grey;}"""

        # Default StyleSheet: QTextBoxBrowsers
        self.default_qtbb_style = """QTextBrowser {background-color: black;
            border-top:2px solid rgb(35, 35, 35);
            border-bottom:2px solid rgb(35, 35, 35);
            border-left:2px solid rgb(35, 35, 35);
            border-right:2px solid rgb(35, 35, 35);
            selection-color: white;
            selection-background-color: rgb(0, 100, 255);
            color: grey;}"""

        # Default Stylesheet: btnx_main
        self.btnx_main_style = """QPushButton{background-color: rgb(0, 0, 0);
                   border:2px solid rgb(30, 30, 30);}"""

    # Function: Concatinates Static Image Values With Variable Image Path
    def set_images_funk(self):
        print('-- plugged in: set_images_funk')

        # Set Static Image Names
        self.img_var = ['img_btnx_led_0.png',         # 0
                        'img_btnx_led_1.png',         # 1
                        'img_btnx_led_2.png',         # 2
                        'img_execute_false.png',      # 3
                        'img_execute_true.png',       # 4
                        'img_menu_left.png',          # 5
                        'img_menu_right.png',         # 6
                        'img_mode_0.png',             # 7
                        'img_mode_1.png',             # 8
                        'img_read_ony_false.png',     # 9
                        'img_read_ony_true.png',      # 10
                        'img_scrollbar_down.png',     # 11
                        'img_scrollbar_left.png',     # 12
                        'img_scrollbar_right.png',    # 13
                        'img_scrollbar_up.png',       # 14
                        'img_show_menu_false.png',    # 15
                        'img_show_menu_true.png',     # 16
                        'img_stop_thread_false.png',  # 17
                        'img_stop_thread_true.png']   # 18

        # Concatinate Static Image Values With Variable Image Path
        self.img_path = img_path
        self.img_btnx_led_0 = str(self.img_path + self.img_var[0])
        self.img_btnx_led_1 = str(self.img_path + self.img_var[1])
        self.img_btnx_led_2 = str(self.img_path + self.img_var[2])
        self.img_execute_false = str(self.img_path + self.img_var[3])
        self.img_execute_true = str(self.img_path + self.img_var[4])
        self.img_menu_left = str(self.img_path + self.img_var[5])
        self.img_menu_right = str(self.img_path + self.img_var[6])
        self.img_mode_0 = str(self.img_path + self.img_var[7])
        self.img_mode_1 = str(self.img_path + self.img_var[8])
        self.img_read_ony_false = str(self.img_path + self.img_var[9])
        self.img_read_ony_true = str(self.img_path + self.img_var[10])
        self.img_scrollbar_down = str(self.img_path + self.img_var[11])
        self.img_scrollbar_left = str(self.img_path + self.img_var[12])
        self.img_scrollbar_right = str(self.img_path + self.img_var[13])
        self.img_scrollbar_up = str(self.img_path + self.img_var[14])
        self.img_show_menu_false = str(self.img_path + self.img_var[15])
        self.img_show_menu_true = str(self.img_path + self.img_var[16])
        self.img_stop_thread_false = str(self.img_path + self.img_var[17])
        self.img_stop_thread_true = str(self.img_path + self.img_var[18])

    # Section 1 Funtion: Main Function Confirmation 0
    def confirm_op0_funk0(self):
        global confirm_op0_bool, confirm_op0_wait
        print('-- plugged in: confirm_op0_funk0: accepted')
        confirm_op0_bool = True
        confirm_op0_wait = False

    # Section 1 Funtion: Main Function Confirmation 1
    def confirm_op1_funk0(self):
        global confirm_op1_bool, confirm_op1_wait
        print('-- plugged in: confirm_op1_funk0: accepted')
        confirm_op1_bool = True
        confirm_op1_wait = False

    # Section 1 Funtion: Main Function Confirmation 2
    def confirm_op2_funk0(self):
        global confirm_op2_bool, confirm_op2_wait
        print('-- plugged in: confirm_op2_funk0: accepted')
        confirm_op2_bool = True
        confirm_op2_wait = False

    # Section 1 Funtion: Main Function Confirmation 3
    def confirm_op3_funk0(self):
        global confirm_op3_bool, confirm_op3_wait
        print('-- plugged in: confirm_op3_funk0: accepted')
        confirm_op3_bool = True
        confirm_op3_wait = False

    # Section 1 Funtion: Main Function Confirmation 4
    def confirm_op4_funk0(self):
        global confirm_op4_bool, confirm_op4_wait
        print('-- plugged in: confirm_op4_funk0: accepted')
        confirm_op4_bool = True
        confirm_op4_wait = False

    # Section 1 Funtion: Main Function Confirmation 5
    def confirm_op5_funk0(self):
        global confirm_op5_bool, confirm_op5_wait
        print('-- plugged in: confirm_op5_funk0: accepted')
        confirm_op5_bool = True
        confirm_op5_wait = False

    # Section 2 Funtion: Set Source & Destination ReadOnly Bool 0 #
    def paths_readonly_button_funk_0(self):
        print('-- plugged in: paths_readonly_button_funk_0')
        global settings_source_edit_vars

        if settings_source_edit_var[0].isReadOnly() is True:
            settings_source_edit_var[0].setReadOnly(False)
            settings_dest_edit_var[0].setReadOnly(False)
            paths_readonly_button_var[0].setIcon(QIcon(self.img_read_ony_false))
            paths_readonly_button_var[0].setIconSize(QSize(8, 21))

        elif settings_source_edit_var[0].isReadOnly() is False:
            settings_source_edit_var[0].setReadOnly(True)
            settings_dest_edit_var[0].setReadOnly(True)
            paths_readonly_button_var[0].setIcon(QIcon(self.img_read_ony_true))
            paths_readonly_button_var[0].setIconSize(QSize(8, 8))

    # Section 2 Funtion: Set Source & Destination ReadOnly Bool 1
    def paths_readonly_button_funk_1(self):
        print('-- plugged in: paths_readonly_button_funk_1')
        global settings_source_edit_vars

        if settings_source_edit_var[1].isReadOnly() is True:
            settings_source_edit_var[1].setReadOnly(False)
            settings_dest_edit_var[1].setReadOnly(False)
            paths_readonly_button_var[1].setIcon(QIcon(self.img_read_ony_false))
            paths_readonly_button_var[1].setIconSize(QSize(8, 21))

        elif settings_source_edit_var[1].isReadOnly() is False:
            settings_source_edit_var[1].setReadOnly(True)
            settings_dest_edit_var[1].setReadOnly(True)
            paths_readonly_button_var[1].setIcon(QIcon(self.img_read_ony_true))
            paths_readonly_button_var[1].setIconSize(QSize(8, 8))

    # Section 2 Funtion: Set Source & Destination ReadOnly Bool 2
    def paths_readonly_button_funk_2(self):
        print('-- plugged in: paths_readonly_button_funk_2')
        global settings_source_edit_vars

        if settings_source_edit_var[2].isReadOnly() is True:
            settings_source_edit_var[2].setReadOnly(False)
            settings_dest_edit_var[2].setReadOnly(False)
            paths_readonly_button_var[2].setIcon(QIcon(self.img_read_ony_false))
            paths_readonly_button_var[2].setIconSize(QSize(8, 21))

        elif settings_source_edit_var[2].isReadOnly() is False:
            settings_source_edit_var[2].setReadOnly(True)
            settings_dest_edit_var[2].setReadOnly(True)
            paths_readonly_button_var[2].setIcon(QIcon(self.img_read_ony_true))
            paths_readonly_button_var[2].setIconSize(QSize(8, 8))

    # Section 2 Funtion: Set Source & Destination ReadOnly Bool 3
    def paths_readonly_button_funk_3(self):
        print('-- plugged in: paths_readonly_button_funk_3')
        global settings_source_edit_vars

        if settings_source_edit_var[3].isReadOnly() is True:
            settings_source_edit_var[3].setReadOnly(False)
            settings_dest_edit_var[3].setReadOnly(False)
            paths_readonly_button_var[3].setIcon(QIcon(self.img_read_ony_false))
            paths_readonly_button_var[3].setIconSize(QSize(8, 21))

        elif settings_source_edit_var[3].isReadOnly() is False:
            settings_source_edit_var[3].setReadOnly(True)
            settings_dest_edit_var[3].setReadOnly(True)
            paths_readonly_button_var[3].setIcon(QIcon(self.img_read_ony_true))
            paths_readonly_button_var[3].setIconSize(QSize(8, 8))

    # Section 2 Funtion: Set Source & Destination ReadOnly Bool 4
    def paths_readonly_button_funk_4(self):
        print('-- plugged in: paths_readonly_button_funk_4')
        global settings_source_edit_vars

        if settings_source_edit_var[4].isReadOnly() is True:
            settings_source_edit_var[4].setReadOnly(False)
            settings_dest_edit_var[4].setReadOnly(False)
            paths_readonly_button_var[4].setIcon(QIcon(self.img_read_ony_false))
            paths_readonly_button_var[4].setIconSize(QSize(8, 21))

        elif settings_source_edit_var[4].isReadOnly() is False:
            settings_source_edit_var[4].setReadOnly(True)
            settings_dest_edit_var[4].setReadOnly(True)
            paths_readonly_button_var[4].setIcon(QIcon(self.img_read_ony_true))
            paths_readonly_button_var[4].setIconSize(QSize(8, 8))

    # Section 2 Funtion: Set Source & Destination ReadOnly Bool 5
    def paths_readonly_button_funk_5(self):
        print('-- plugged in: paths_readonly_button_funk_5')
        global settings_source_edit_vars

        if settings_source_edit_var[5].isReadOnly() is True:
            settings_source_edit_var[5].setReadOnly(False)
            settings_dest_edit_var[5].setReadOnly(False)
            paths_readonly_button_var[5].setIcon(QIcon(self.img_read_ony_false))
            paths_readonly_button_var[5].setIconSize(QSize(8, 21))

        elif settings_source_edit_var[5].isReadOnly() is False:
            settings_source_edit_var[5].setReadOnly(True)
            settings_dest_edit_var[5].setReadOnly(True)
            paths_readonly_button_var[5].setIcon(QIcon(self.img_read_ony_true))
            paths_readonly_button_var[5].setIconSize(QSize(8, 8))

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
            with open(cfg_f, 'r') as fo:
                for line in fo:
                    line = line.strip()
                    if not line.startswith(config_src_var[source_selected]):
                        path_item.append(line)
                    elif line.startswith(config_src_var[source_selected]):
                        new_line = config_src_var[source_selected]+' '+source_path_entered
                        path_item.append(new_line)
            open(cfg_f, 'w').close()
            with open(cfg_f, 'a') as fo:
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
            with open(cfg_f, 'r') as fo:
                for line in fo:
                    line = line.strip()
                    if not line.startswith(config_dst_var[dest_selected]):
                        path_item.append(line)
                    elif line.startswith(config_dst_var[dest_selected]):
                        new_line = config_dst_var[dest_selected] + ' ' + dest_path_entered
                        path_item.append(new_line)
            open(cfg_f, 'w').close()
            with open(cfg_f, 'a') as fo:
                i = 0
                for path_items in path_item:
                    fo.writelines(path_item[i] + '\n')
                    i += 1
            fo.close()
            dest_path_var[dest_selected] = dest_path_entered
            settings_input_response_thread.start()

        elif not os.path.exists(dest_path_entered):
            try:
                # Attempt Path Creation
                var = dest_path_entered[0]
                var = str(var + ':\\')
                if os.path.exists(var):
                    dest_path_entered = str(dest_path_entered).strip()
                    print('-- creating directory(s):', dest_path_entered)

                    # Only Partially Sanitized Path!
                    distutils.dir_util.mkpath(dest_path_entered)
                    settings_input_response_dest_bool = True
                    path_item = []
                    with open(cfg_f, 'r') as fo:
                        for line in fo:
                            line = line.strip()
                            if not line.startswith(config_dst_var[dest_selected]):
                                path_item.append(line)
                            elif line.startswith(config_dst_var[dest_selected]):
                                new_line = config_dst_var[dest_selected] + ' ' + dest_path_entered
                                path_item.append(new_line)
                    open(cfg_f, 'w').close()
                    with open(cfg_f, 'a') as fo:
                        i = 0
                        for path_items in path_item:
                            fo.writelines(path_item[i] + '\n')
                            i += 1
                    fo.close()
                    dest_path_var[dest_selected] = dest_path_entered
                    settings_input_response_thread.start()
                elif not os.path.exists(var):
                    print('-- cannot create directory(s) on drive that does not exist')
                    settings_input_response_dest_bool = False
                    settings_dest_edit_var[dest_selected].setText(dest_path_var[dest_selected])
                    settings_input_response_thread.start()
            except Exception as e:
                print(str(e))
                print('-- could not create destination path')
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

        self.tb_0.hide()
        self.tb_1.hide()
        self.tb_2.hide()
        self.tb_3.hide()
        self.tb_4.hide()
        self.tb_5.hide()

        self.tb_label_0.hide()

        back_label_var[0].resize(95, 80)
        back_label_var[1].resize(95, 80)
        back_label_var[2].resize(95, 80)
        back_label_var[3].resize(95, 80)
        back_label_var[4].resize(95, 80)
        back_label_var[5].resize(95, 80)

        btnx_settings_var[0].setIcon(QIcon(self.img_show_menu_false))
        btnx_settings_var[1].setIcon(QIcon(self.img_show_menu_false))
        btnx_settings_var[2].setIcon(QIcon(self.img_show_menu_false))
        btnx_settings_var[3].setIcon(QIcon(self.img_show_menu_false))
        btnx_settings_var[4].setIcon(QIcon(self.img_show_menu_false))
        btnx_settings_var[5].setIcon(QIcon(self.img_show_menu_false))

        paths_readonly_button_var[0].hide()
        paths_readonly_button_var[1].hide()
        paths_readonly_button_var[2].hide()
        paths_readonly_button_var[3].hide()
        paths_readonly_button_var[4].hide()
        paths_readonly_button_var[5].hide()

    # Sector 2: Funtion: Calls hide_settings_funk Then Hides Settings Page By Resizing Window
    def hide_settings_page_funk(self):
        self.hide_settings_funk()
        self.setFixedSize(self.width, 110)

    # Sector 1: Focus In Settings When Priming To Write 0
    def btnx_set_focus_funk_0(self):
        global settings_active_int

        settings_active_int = 0
        self.hide_settings_funk()
        self.setFixedSize(self.width, 320)

        btnx_settings_var[0].setIcon(QIcon(self.img_show_menu_true))
        back_label_var[0].resize(95, 85)

        self.setting_title0.show()
        self.settings_source0.show()
        self.settings_dest0.show()
        self.tb_0.show()
        self.tb_label_0.setText('Archives Output')
        self.tb_label_0.show()
        settings_source_edit_var[0].setReadOnly(True)
        settings_dest_edit_var[0].setReadOnly(True)
        paths_readonly_button_var[0].setIconSize(QSize(8, 8))
        paths_readonly_button_var[0].setIcon(QIcon(self.img_read_ony_true))
        paths_readonly_button_var[0].show()
        paths_readonly_button_var[0].setEnabled(False)

    # Sector 1: Focus In Settings When Priming To Write 1
    def btnx_set_focus_funk_1(self):
        global settings_active_int

        settings_active_int = 1
        self.hide_settings_funk()

        self.setFixedSize(self.width, 320)
        btnx_settings_var[1].setIcon(QIcon(self.img_show_menu_true))
        back_label_var[1].resize(95, 85)

        self.setting_title1.show()
        self.settings_source1.show()
        self.settings_dest1.show()
        self.tb_1.show()
        self.tb_label_0.setText('Documents Output')
        self.tb_label_0.show()
        settings_source_edit_var[1].setReadOnly(True)
        settings_dest_edit_var[1].setReadOnly(True)
        paths_readonly_button_var[1].setIconSize(QSize(8, 8))
        paths_readonly_button_var[1].setIcon(QIcon(self.img_read_ony_true))
        paths_readonly_button_var[1].show()
        paths_readonly_button_var[1].setEnabled(False)

    # Sector 1: Focus In Settings When Priming To Write 2
    def btnx_set_focus_funk_2(self):
        global settings_active_int

        settings_active_int = 2
        self.hide_settings_funk()

        self.setFixedSize(self.width, 320)
        btnx_settings_var[2].setIcon(QIcon(self.img_show_menu_true))
        back_label_var[2].resize(95, 85)

        self.setting_title2.show()
        self.settings_source2.show()
        self.settings_dest2.show()
        self.tb_2.show()
        self.tb_label_0.setText('Music Output')
        self.tb_label_0.show()
        settings_source_edit_var[2].setReadOnly(True)
        settings_dest_edit_var[2].setReadOnly(True)
        paths_readonly_button_var[2].setIconSize(QSize(8, 8))
        paths_readonly_button_var[2].setIcon(QIcon(self.img_read_ony_true))
        paths_readonly_button_var[2].show()
        paths_readonly_button_var[2].setEnabled(False)

    # Sector 1: Focus In Settings When Priming To Write 3
    def btnx_set_focus_funk_3(self):
        global settings_active_int

        settings_active_int = 3
        self.hide_settings_funk()

        self.setFixedSize(self.width, 320)
        btnx_settings_var[3].setIcon(QIcon(self.img_show_menu_true))
        back_label_var[3].resize(95, 85)

        self.setting_title3.show()
        self.settings_source3.show()
        self.settings_dest3.show()
        self.tb_3.show()
        self.tb_label_0.setText('Pictures Output')
        self.tb_label_0.show()
        settings_source_edit_var[3].setReadOnly(True)
        settings_dest_edit_var[3].setReadOnly(True)
        paths_readonly_button_var[3].setIconSize(QSize(8, 8))
        paths_readonly_button_var[3].setIcon(QIcon(self.img_read_ony_true))
        paths_readonly_button_var[3].show()
        paths_readonly_button_var[3].setEnabled(False)

    # Sector 1: Focus In Settings When Priming To Write 4
    def btnx_set_focus_funk_4(self):
        global settings_active_int

        settings_active_int = 4
        self.hide_settings_funk()

        self.setFixedSize(self.width, 320)
        btnx_settings_var[4].setIcon(QIcon(self.img_show_menu_true))
        back_label_var[4].resize(95, 85)

        self.setting_title4.show()
        self.settings_source4.show()
        self.settings_dest4.show()
        self.tb_4.show()
        self.tb_label_0.setText('Video Output')
        self.tb_label_0.show()
        settings_source_edit_var[4].setReadOnly(True)
        settings_dest_edit_var[4].setReadOnly(True)
        paths_readonly_button_var[4].setIconSize(QSize(8, 8))
        paths_readonly_button_var[4].setIcon(QIcon(self.img_read_ony_true))
        paths_readonly_button_var[4].show()
        paths_readonly_button_var[4].setEnabled(False)

    # Sector 1: Focus In Settings When Priming To Write 5
    def btnx_set_focus_funk_5(self):
        global settings_active_int

        settings_active_int = 5
        self.hide_settings_funk()

        self.setFixedSize(self.width, 320)
        btnx_settings_var[5].setIcon(QIcon(self.img_show_menu_true))
        back_label_var[5].resize(95, 85)

        self.setting_title5.show()
        self.settings_source5.show()
        self.settings_dest5.show()
        self.tb_5.show()
        self.tb_label_0.setText('Programs Output')
        self.tb_label_0.show()
        settings_source_edit_var[5].setReadOnly(True)
        settings_dest_edit_var[5].setReadOnly(True)
        paths_readonly_button_var[5].setIconSize(QSize(8, 8))
        paths_readonly_button_var[5].setIcon(QIcon(self.img_read_ony_true))
        paths_readonly_button_var[5].show()
        paths_readonly_button_var[5].setEnabled(False)


    # Sector 2 Funtion: Displays Drop Down Settings In Sector 2 For Source & Destination Path Configuration 0
    def settings_funk0(self):
        global settings_active, settings_active_int, settings_active_int_prev
        settings_active_int = 0
        self.hide_settings_funk()
        if settings_active is False:
            if settings_active_int != settings_active_int_prev:
                self.setFixedSize(self.width, 320)

                btnx_settings_var[0].setIcon(QIcon(self.img_show_menu_true))

                back_label_var[0].resize(95, 85)

                self.setting_title0.show()
                self.settings_source0.show()
                self.settings_dest0.show()

                self.tb_0.show()
                self.tb_label_0.setText('Archives Output')
                self.tb_label_0.show()

                paths_readonly_button_var[0].show()

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
                self.setFixedSize(self.width, 320)

                btnx_settings_var[1].setIcon(QIcon(self.img_show_menu_true))

                back_label_var[1].resize(95, 85)

                self.setting_title1.show()
                self.settings_source1.show()
                self.settings_dest1.show()

                self.tb_1.show()
                self.tb_label_0.setText('Documents Output')
                self.tb_label_0.show()

                paths_readonly_button_var[1].show()

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
                self.setFixedSize(self.width, 320)

                btnx_settings_var[2].setIcon(QIcon(self.img_show_menu_true))

                back_label_var[2].resize(95, 85)

                self.setting_title2.show()
                self.settings_source2.show()
                self.settings_dest2.show()

                self.tb_2.show()
                self.tb_label_0.setText('Music Output')
                self.tb_label_0.show()

                paths_readonly_button_var[2].show()

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
                self.setFixedSize(self.width, 320)

                btnx_settings_var[3].setIcon(QIcon(self.img_show_menu_true))

                back_label_var[3].resize(95, 85)

                self.setting_title3.show()
                self.settings_source3.show()
                self.settings_dest3.show()

                self.tb_3.show()
                self.tb_label_0.setText('Pictures Output')
                self.tb_label_0.show()

                paths_readonly_button_var[3].show()

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
                self.setFixedSize(self.width, 320)

                btnx_settings_var[4].setIcon(QIcon(self.img_show_menu_true))

                back_label_var[4].resize(95, 85)

                self.setting_title4.show()
                self.settings_source4.show()
                self.settings_dest4.show()

                self.tb_4.show()
                self.tb_label_0.setText('Videos Output')
                self.tb_label_0.show()

                paths_readonly_button_var[4].show()

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
                self.setFixedSize(self.width, 320)

                btnx_settings_var[5].setIcon(QIcon(self.img_show_menu_true))

                back_label_var[5].resize(95, 85)

                self.setting_title5.show()
                self.settings_source5.show()
                self.settings_dest5.show()
                self.settings_dest5.show()

                self.tb_5.show()
                self.tb_label_0.setText('Programs Output')
                self.tb_label_0.show()

                paths_readonly_button_var[5].show()

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
        global compare_bool_var, compare_clicked, thread_engaged_var 

        if thread_engaged_var[compare_clicked] is False:
            if compare_bool_var[compare_clicked] is False:
                compare_bool_var[compare_clicked] = True
                comp_cont_button_var[compare_clicked].setIcon(QIcon(self.img_mode_1))
                comp_cont_button_var[compare_clicked].setStyleSheet(self.default_qpbtn_prsd_style)
            elif compare_bool_var[compare_clicked] is True:
                compare_bool_var[compare_clicked] = False
                comp_cont_button_var[compare_clicked].setIcon(QIcon(self.img_mode_0))
                comp_cont_button_var[compare_clicked].setStyleSheet(self.default_qpbtn_style)
        if thread_engaged_var[compare_clicked] is True:
            print('-- thread engaged: setting mode unavailable')

    # Sector 1 Function: Stops Sector 1 Main Function Thread 0
    def stop_thr_funk0(self):
        global thread_var
        thread_var[0].stop_thr()

    # Sector 1 Function: Stops Sector 1 Main Function Thread 1
    def stop_thr_funk1(self):
        global thread_var
        thread_var[1].stop_thr()

    # Sector 1 Function: Stops Sector 1 Main Function Thread 2
    def stop_thr_funk2(self):
        global thread_var
        thread_var[2].stop_thr()

    # Sector 1 Function: Stops Sector 1 Main Function Thread 3
    def stop_thr_funk3(self):
        global thread_var
        thread_var[3].stop_thr()

    # Sector 1 Function: Stops Sector 1 Main Function Thread 4
    def stop_thr_funk4(self):
        global thread_var
        thread_var[4].stop_thr()

    # Sector 1 Function: Stops Sector 1 Main Function Thread 5
    def stop_thr_funk5(self):
        global thread_var
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
    def __init__(self, default_valid_path_led_green, default_valid_path_led_red, default_valid_path_led):
        QThread.__init__(self)
        self.default_valid_path_led_green = default_valid_path_led_green
        self.default_valid_path_led_red = default_valid_path_led_red
        self.default_valid_path_led = default_valid_path_led

    def run(self):
        global settings_input_response_source_bool, settings_input_response_dest_bool
        global settings_input_response_label

        if settings_input_response_source_bool is True:
            settings_input_response_label[0].setStyleSheet(self.default_valid_path_led_green)
            settings_input_response_source_bool = None
            time.sleep(1)
            settings_input_response_label[0].setStyleSheet(self.default_valid_path_led)

        elif settings_input_response_source_bool is False:
            settings_input_response_label[0].setStyleSheet(self.default_valid_path_led_red)
            settings_input_response_source_bool = None
            time.sleep(1)
            settings_input_response_label[0].setStyleSheet(self.default_valid_path_led)

        elif settings_input_response_dest_bool is True:
            settings_input_response_label[1].setStyleSheet(self.default_valid_path_led_green)
            settings_input_response_dest_bool = None
            time.sleep(1)
            settings_input_response_label[1].setStyleSheet(self.default_valid_path_led)

        elif settings_input_response_dest_bool is False:
            settings_input_response_label[1].setStyleSheet(self.default_valid_path_led_red)
            settings_input_response_dest_bool = None
            time.sleep(1)
            settings_input_response_label[1].setStyleSheet(self.default_valid_path_led)

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
        global path_var, dest_path_var, settings_source_edit_var,\
            settings_dest_edit_var, configuration_engaged
        configuration_engaged = True

        # Only Update Displayed Source & Destination Paths If Source & Destination Paths Not Being Edited
        check_var = []
        i = 0
        for settings_source_edit_vars in settings_source_edit_var:
            if settings_source_edit_var[i].isReadOnly() is False:
                check_var.append(False)
            elif settings_source_edit_var[i].isReadOnly() is True:
                check_var.append(True)
            i += 1

        if not False in check_var:
            path_var = []
            dest_path_var = []
            if os.path.exists(cfg_f):
                with open(cfg_f, 'r') as fo:

                    for line in fo:
                        line = line.strip()

                        if line.startswith('SOURCE 0: '):
                            line = line.replace('SOURCE 0: ', '')
                            if os.path.exists(line) and len(path_var) <= 6:
                                # print('config source path exists:', line)
                                path_var.append(line)
                            elif not os.path.exists(line) and len(path_var) <= 6:
                                # print('config source path does not exist', line)
                                path_var.append('')

                        if line.startswith('SOURCE 1: '):
                            line = line.replace('SOURCE 1: ', '')
                            if os.path.exists(line) and len(path_var) <= 6:
                                # print('config source path exists:', line)
                                path_var.append(line)
                            elif not os.path.exists(line) and len(path_var) <= 6:
                                # print('config source path does not exist', line)
                                path_var.append('')

                        if line.startswith('SOURCE 2: '):
                            line = line.replace('SOURCE 2: ', '')
                            if os.path.exists(line) and len(path_var) <= 6:
                                # print('config source path exists:', line)
                                path_var.append(line)
                            elif not os.path.exists(line) and len(path_var) <= 6:
                                # print('config source path does not exist', line)
                                path_var.append('')

                        if line.startswith('SOURCE 3: '):
                            line = line.replace('SOURCE 3: ', '')
                            if os.path.exists(line) and len(path_var) <= 6:
                                # print('config source path exists:', line)
                                path_var.append(line)
                            elif not os.path.exists(line) and len(path_var) <= 6:
                                # print('config source path does not exist', line)
                                path_var.append('')

                        if line.startswith('SOURCE 4: '):
                            line = line.replace('SOURCE 4: ', '')
                            if os.path.exists(line) and len(path_var) <= 6:
                                # print('config source path exists:', line)
                                path_var.append(line)
                            elif not os.path.exists(line) and len(path_var) <= 6:
                                # print('config source path does not exist', line)
                                path_var.append('')

                        if line.startswith('SOURCE 5: '):
                            line = line.replace('SOURCE 5: ', '')
                            if os.path.exists(line) and len(path_var) <= 6:
                                # print('config source path exists:', line)
                                path_var.append(line)
                            elif not os.path.exists(line) and len(path_var) <= 6:
                                # print('config source path does not exist', line)
                                path_var.append('')

                        # Read Destination
                        if line.startswith('DESTINATION 0: '):
                            line = line.replace('DESTINATION 0: ', '')
                            if os.path.exists(line) and len(dest_path_var) <= 6:
                                # print('config destination path exists:', line)
                                dest_path_var.append(line)
                            elif not os.path.exists(line) and len(dest_path_var) <= 6:
                                # print('config destination path does not exist', line)
                                dest_path_var.append('')

                        if line.startswith('DESTINATION 1: '):
                            line = line.replace('DESTINATION 1: ', '')
                            if os.path.exists(line) and len(dest_path_var) <= 6:
                                # print('config destination path exists:', line)
                                dest_path_var.append(line)
                            elif not os.path.exists(line) and len(dest_path_var) <= 6:
                                # print('config destination path does not exist', line)
                                dest_path_var.append('')

                        if line.startswith('DESTINATION 2: '):
                            line = line.replace('DESTINATION 2: ', '')
                            if os.path.exists(line) and len(dest_path_var) <= 6:
                                # print('config destination path exists:', line)
                                dest_path_var.append(line)
                            elif not os.path.exists(line) and len(dest_path_var) <= 6:
                                # print('config destination path does not exist', line)
                                dest_path_var.append('')

                        if line.startswith('DESTINATION 3: '):
                            line = line.replace('DESTINATION 3: ', '')
                            if os.path.exists(line) and len(dest_path_var) <= 6:
                                # print('config destination path exists:', line)
                                dest_path_var.append(line)
                            elif not os.path.exists(line) and len(dest_path_var) <= 6:
                                # print('config destination path does not exist', line)
                                dest_path_var.append('')

                        if line.startswith('DESTINATION 4: '):
                            line = line.replace('DESTINATION 4: ', '')
                            if os.path.exists(line) and len(dest_path_var) <= 6:
                                # print('config destination path exists:', line)
                                dest_path_var.append(line)
                            elif not os.path.exists(line) and len(dest_path_var) <= 6:
                                # print('config destination path does not exist', line)
                                dest_path_var.append('')

                        if line.startswith('DESTINATION 5: '):
                            line = line.replace('DESTINATION 5: ', '')
                            if os.path.exists(line) and len(dest_path_var) <= 6:
                                # print('config destination path exists:', line)
                                dest_path_var.append(line)
                            elif not os.path.exists(line) and len(dest_path_var) <= 6:
                                # print('config destination path does not exist', line)
                                dest_path_var.append('')
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


# Sector 1 Class: Main Function Button Thread 0  self.stop_thr_button.setIcon(QIcon(self.img_stop_thread_false))  settings_source_edit_var
class ThreadClass0(QThread):
    def __init__(self, tb_0, confirm_op0_tru, img_btnx_led_0, img_btnx_led_1, img_btnx_led_2, img_execute_false, img_execute_true, img_stop_thread_false, img_stop_thread_true, output_verbosity):
        QThread.__init__(self)
        self.tb_0 = tb_0
        self.confirm_op0_tru = confirm_op0_tru
        self.img_btnx_led_0 = img_btnx_led_0
        self.img_btnx_led_1 = img_btnx_led_1
        self.img_btnx_led_2 = img_btnx_led_2
        self.img_execute_false = img_execute_false
        self.img_execute_true = img_execute_true
        self.img_stop_thread_false = img_stop_thread_false
        self.img_stop_thread_true = img_stop_thread_true
        self.output_verbosity = output_verbosity

    def run(self):
        global btnx_main_var, path_var, dest_path_var, stop_thr_button_var
        global configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var, settings_source_edit_var, paths_readonly_button_var

        # If Source & Destination Configuration Is Disengaged Then Continue
        if configuration_engaged is False:

            thread_engaged_var[0] = True

            # Set Paths In Stone Before Continuing. Asigns Source & Destination Variables To New Variables That Cannot Be Changed Once Function Exectutes
            path = path_var[0]
            dest = dest_path_var[0]
            compare_bool = compare_bool_var[0]

            # Provide Confirmation/Declination Buttons & Wait For Confirmation/Declination Then Reset Global confirm_op0_wait Boolean Back to True
            btnx_main_var[0].setIcon(QIcon(self.img_btnx_led_1))
            self.confirm_op0_tru.setIcon(QIcon(self.img_execute_true))
            self.confirm_op0_tru.setEnabled(True)

            # Enable Stop thread Button
            stop_thr_button_var[0].setEnabled(True)
            stop_thr_button_var[0].setIcon(QIcon(self.img_stop_thread_true))

            while confirm_op0_wait is True:
                time.sleep(0.3)
            confirm_op0_wait = True

            # Confirmation/Declination Occured, Hide Confirmation/Declination Buttons
            self.confirm_op0_tru.setIcon(QIcon(self.img_execute_false))
            self.confirm_op0_tru.setEnabled(False)

            # If Confirmed Run Main Function
            if confirm_op0_bool is True:
                print('-- ThreadClass0: confirm_op0_bool: accepted')
                btnx_main_var[0].setIcon(QIcon(self.img_btnx_led_2))
                change_var = False

                # Set Counters For Output Summary
                cp0_count = 0
                cp0_fail_count = 0
                cp1_count = 0
                cp1_fail_count = 0

                if os.path.exists(path) and os.path.exists(dest):
                    for dirname, subdirlist, filelist in os.walk(path):
                        for fname in filelist:

                            fullpath = os.path.join(dirname, fname)
                            t_path = fullpath.replace(path, '')
                            t_path = dest + t_path
                            if not fullpath.endswith('.ini'):

                                # Mode 0: Write Missing Files Only
                                if not os.path.exists(t_path):
                                    change_var = True
                                    try:
                                        shutil.copy2(fullpath, t_path)
                                    except IOError:
                                        try:
                                            os.makedirs(os.path.dirname(t_path))
                                            shutil.copy2(fullpath, t_path)
                                        except:
                                            output_str = str('error: ' + t_path).strip()
                                            self.tb_0.append(output_str)

                                    # Mode 0: Check File
                                    if os.path.exists(t_path) and os.path.exists(fullpath):
                                        siz_src = str(os.path.getsize(fullpath))
                                        siz_dest = str(os.path.getsize(t_path))

                                        if siz_src == siz_dest:
                                            if self.output_verbosity is 0:
                                                output_str = str('copied new: ' + t_path).strip()
                                            elif self.output_verbosity is 1:
                                                output_str = str('copied new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                            self.tb_0.append(output_str)
                                            cp0_count += 1

                                        elif siz_src != siz_dest:
                                            output_str = str('failed to copy new (failed bytes check): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                            self.tb_0.append(output_str)
                                            cp0_fail_count += 1

                                    elif not os.path.exists(t_path):
                                        output_str = str('failed to copy new (file does no exist in destination): ' + t_path).strip()
                                        self.tb_0.append(output_str)
                                        cp0_fail_count += 1

                                # Mode 1: Write Missing & Write Predicated Upon Time Stamp Comparison Results
                                elif os.path.exists(t_path):
                                    if compare_bool is True:
                                        ma = os.path.getmtime(fullpath)
                                        mb = os.path.getmtime(t_path)
                                        if mb < ma:
                                            change_var = True
                                            try:
                                                shutil.copy2(fullpath, t_path)
                                            except IOError:
                                                try:
                                                    os.makedirs(os.path.dirname(t_path))
                                                    shutil.copy2(fullpath, t_path)
                                                except:
                                                    output_str = str('error: ' + t_path).strip()
                                                    self.tb_0.append(output_str)

                                            # Mode 1: Check File
                                            if os.path.exists(t_path) and os.path.exists(fullpath):
                                                mb = os.path.getmtime(t_path)
                                                ma_str = str(ma)
                                                mb_str = str(mb)
                                                siz_src = str(os.path.getsize(fullpath))
                                                siz_dest = str(os.path.getsize(t_path))
                                                if mb >= ma and siz_src == siz_dest:
                                                    if self.output_verbosity is 0:
                                                        output_str = str('updated new: ' + t_path).strip()
                                                    elif self.output_verbosity is 1:
                                                        output_str = str('updated new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                                    self.tb_0.append(output_str)
                                                    cp1_count += 1
                                                elif mb < ma or siz_src != siz_dest:
                                                    if siz_src != siz_dest:
                                                        output_str = str('failed to copy new (failed bytes check): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                                        self.tb_0.append(output_str)
                                                        cp1_fail_count += 1
                                                    elif mb < ma:
                                                        output_str = str('failed to copy new (failed timestamp check): (Source: ' + ma_str + ' Destination:' + mb_str + ') ' + t_path).strip()
                                                        self.tb_0.append(output_str)
                                                        cp1_fail_count += 1
                                            elif not os.path.exists(t_path):
                                                output_str = str('failed to update file (file does no exist in destination): ' + t_path).strip()
                                                self.tb_0.append(output_str)
                                                cp1_fail_count += 1

            # Output Summary
            cp0_count_str = str(cp0_count)
            cp0_fail_count_str = str(cp0_fail_count)
            cp1_count_str = str(cp1_count)
            cp1_fail_count_str = str(cp1_fail_count)

            output_sum =  str('copied new: (' + cp0_count_str + ') | failed to copy new: (' + cp0_fail_count_str + ') | updated: (' + cp1_count_str + ')  | failed to update: (' + cp1_fail_count_str + ')').strip()
            print('-- ThreadClass0: ' + output_sum)
            self.tb_0.append(output_sum)

            # Disengage
            btnx_main_var[0].setIcon(QIcon(self.img_btnx_led_0))
            stop_thr_button_var[0].setIcon(QIcon(self.img_stop_thread_false))
            stop_thr_button_var[0].setEnabled(False)
            thread_engaged_var[0] = False
            paths_readonly_button_var[0].setEnabled(True)

    def stop_thr(self):
        global btnx_main_var
        global confirm_op0_bool, confirm_op0_wait
        
        confirm_op0_bool = False
        confirm_op0_wait = True
        print('-- confirm_op0 declined: (confirm_op0_bool)', confirm_op0_bool)
        btnx_main_var[0].setIcon(QIcon(self.img_btnx_led_0))
        self.confirm_op0_tru.setEnabled(False)
        self.confirm_op0_tru.setIcon(QIcon(self.img_execute_false))
        stop_thr_button_var[0].setIcon(QIcon(self.img_stop_thread_false))
        stop_thr_button_var[0].setEnabled(False)
        thread_engaged_var[0] = False
        paths_readonly_button_var[0].setEnabled(True)

        self.terminate()


# Sector 1 Class: Main Function Button Thread 1
class ThreadClass1(QThread):
    def __init__(self, tb_1, confirm_op1_tru, img_btnx_led_0, img_btnx_led_1, img_btnx_led_2, img_execute_false, img_execute_true, img_stop_thread_false, img_stop_thread_true, output_verbosity):
        QThread.__init__(self)
        self.tb_1 = tb_1
        self.confirm_op1_tru = confirm_op1_tru
        self.img_btnx_led_0 = img_btnx_led_0
        self.img_btnx_led_1 = img_btnx_led_1
        self.img_btnx_led_2 = img_btnx_led_2
        self.img_execute_false = img_execute_false
        self.img_execute_true = img_execute_true
        self.img_stop_thread_false = img_stop_thread_false
        self.img_stop_thread_true = img_stop_thread_true
        self.output_verbosity = output_verbosity

    def run(self):
        global btnx_main_var, path_var, dest_path_var, stop_thr_button_var
        global configuration_engaged, confirm_op1_wait, confirm_op1_bool, thread_engaged_var, settings_source_edit_var, paths_readonly_button_var

        # If Source & Destination Configuration Is Disengaged Then Continue
        if configuration_engaged is False:

            thread_engaged_var[1] = True

            # Set Paths In Stone Before Continuing. Asigns Source & Destination Variables To New Variables That Cannot Be Changed Once Function Exectutes
            path = path_var[1]
            dest = dest_path_var[1]
            compare_bool = compare_bool_var[1]

            # Provide Confirmation/Declination Buttons & Wait For Confirmation/Declination Then Reset Global confirm_op0_wait Boolean Back to True
            btnx_main_var[1].setIcon(QIcon(self.img_btnx_led_1))
            self.confirm_op1_tru.setIcon(QIcon(self.img_execute_true))
            self.confirm_op1_tru.setEnabled(True)

            # Enable Stop thread Button
            stop_thr_button_var[1].setEnabled(True)
            stop_thr_button_var[1].setIcon(QIcon(self.img_stop_thread_true))

            while confirm_op1_wait is True:
                time.sleep(0.3)
            confirm_op1_wait = True

            # Confirmation/Declination Occured, Hide Confirmation/Declination Buttons
            self.confirm_op1_tru.setIcon(QIcon(self.img_execute_false))
            self.confirm_op1_tru.setEnabled(False)

            # If Confirmed Run Main Function
            if confirm_op1_bool is True:
                print('-- ThreadClass1: confirm_op1_bool: accepted')
                btnx_main_var[1].setIcon(QIcon(self.img_btnx_led_2))
                change_var = False

                # Set Counters For Output Summary
                cp0_count = 0
                cp0_fail_count = 0
                cp1_count = 0
                cp1_fail_count = 0

                if os.path.exists(path) and os.path.exists(dest):
                    for dirname, subdirlist, filelist in os.walk(path):
                        for fname in filelist:
                            fullpath = os.path.join(dirname, fname)
                            t_path = fullpath.replace(path, '')
                            t_path = dest + t_path

                            if not fullpath.endswith('.ini'):

                                # Mode 0: Write Missing Files Only
                                if not os.path.exists(t_path):
                                    change_var = True
                                    try:
                                        shutil.copy2(fullpath, t_path)
                                    except IOError:
                                        try:
                                            os.makedirs(os.path.dirname(t_path))
                                            shutil.copy2(fullpath, t_path)
                                        except:
                                            output_str = str('error: ' + t_path).strip()
                                            self.tb_1.append(output_str)

                                    # Mode 0: Check File
                                    if os.path.exists(t_path) and os.path.exists(fullpath):
                                        siz_src = str(os.path.getsize(fullpath))
                                        siz_dest = str(os.path.getsize(t_path))

                                        if siz_src == siz_dest:
                                            if self.output_verbosity is 0:
                                                output_str = str('copied new: ' + t_path).strip()
                                            elif self.output_verbosity is 1:
                                                output_str = str('copied new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                            self.tb_1.append(output_str)
                                            cp0_count += 1

                                        elif siz_src != siz_dest:
                                            output_str = str('failed to copy new (failed bytes check): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                            self.tb_1.append(output_str)
                                            cp0_fail_count += 1

                                    elif not os.path.exists(t_path):
                                        output_str = str('failed to copy new (file does no exist in destination): ' + t_path).strip()
                                        self.tb_1.append(output_str)
                                        cp0_fail_count += 1

                                # Mode 1: Write Missing & Write Predicated Upon Time Stamp Comparison Results
                                elif os.path.exists(t_path):
                                    if compare_bool is True:
                                        ma = os.path.getmtime(fullpath)
                                        mb = os.path.getmtime(t_path)
                                        if mb < ma:
                                            change_var = True
                                            try:
                                                shutil.copy2(fullpath, t_path)
                                            except IOError:
                                                try:
                                                    os.makedirs(os.path.dirname(t_path))
                                                    shutil.copy2(fullpath, t_path)
                                                except:
                                                    output_str = str('error: ' + t_path).strip()
                                                    self.tb_1.append(output_str)

                                            # Mode 1: Check File
                                            if os.path.exists(t_path) and os.path.exists(fullpath):
                                                mb = os.path.getmtime(t_path)
                                                ma_str = str(ma)
                                                mb_str = str(mb)
                                                siz_src = str(os.path.getsize(fullpath))
                                                siz_dest = str(os.path.getsize(t_path))
                                                if mb >= ma and siz_src == siz_dest:
                                                    if self.output_verbosity is 0:
                                                        output_str = str('updated new: ' + t_path).strip()
                                                    elif self.output_verbosity is 1:
                                                        output_str = str('updated new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                                    self.tb_1.append(output_str)
                                                    cp1_count += 1
                                                elif mb < ma or siz_src != siz_dest:
                                                    if siz_src != siz_dest:
                                                        output_str = str('failed to copy new (failed bytes check): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                                        self.tb_1.append(output_str)
                                                        cp1_fail_count += 1
                                                    elif mb < ma:
                                                        output_str = str('failed to copy new (failed timestamp check): (Source: ' + ma_str + ' Destination:' + mb_str + ') ' + t_path).strip()
                                                        self.tb_1.append(output_str)
                                                        cp1_fail_count += 1
                                            elif not os.path.exists(t_path):
                                                output_str = str('failed to update file (file does no exist in destination): ' + t_path).strip()
                                                self.tb_1.append(output_str)
                                                cp1_fail_count += 1

            # Output Summary
            cp0_count_str = str(cp0_count)
            cp0_fail_count_str = str(cp0_fail_count)
            cp1_count_str = str(cp1_count)
            cp1_fail_count_str = str(cp1_fail_count)

            output_sum =  str('copied new: (' + cp0_count_str + ') | failed to copy new: (' + cp0_fail_count_str + ') | updated: (' + cp1_count_str + ')  | failed to update: (' + cp1_fail_count_str + ')').strip()
            print('-- ThreadClass1: ' + output_sum)
            self.tb_1.append(output_sum)

            # Disengage
            btnx_main_var[1].setIcon(QIcon(self.img_btnx_led_0))
            stop_thr_button_var[1].setIcon(QIcon(self.img_stop_thread_false))
            stop_thr_button_var[1].setEnabled(False)
            thread_engaged_var[1] = False
            paths_readonly_button_var[1].setEnabled(True)

    def stop_thr(self):
        global btnx_main_var
        global confirm_op1_bool, confirm_op1_wait
        
        confirm_op1_bool = False
        confirm_op1_wait = True
        print('-- confirm_op1 declined: (confirm_op1_bool)', confirm_op1_bool)
        btnx_main_var[1].setIcon(QIcon(self.img_btnx_led_0))
        self.confirm_op1_tru.setEnabled(False)
        self.confirm_op1_tru.setIcon(QIcon(self.img_execute_false))
        stop_thr_button_var[1].setIcon(QIcon(self.img_stop_thread_false))
        stop_thr_button_var[1].setEnabled(False)
        thread_engaged_var[1] = False
        paths_readonly_button_var[1].setEnabled(True)

        self.terminate()


# Sector 1 Class: Main Function Button Thread 2
class ThreadClass2(QThread):
    def __init__(self, tb_2, confirm_op2_tru, img_btnx_led_0, img_btnx_led_1, img_btnx_led_2, img_execute_false, img_execute_true, img_stop_thread_false, img_stop_thread_true, output_verbosity):
        QThread.__init__(self)
        self.tb_2 = tb_2
        self.confirm_op2_tru = confirm_op2_tru
        self.img_btnx_led_0 = img_btnx_led_0
        self.img_btnx_led_1 = img_btnx_led_1
        self.img_btnx_led_2 = img_btnx_led_2
        self.img_execute_false = img_execute_false
        self.img_execute_true = img_execute_true
        self.img_stop_thread_false = img_stop_thread_false
        self.img_stop_thread_true = img_stop_thread_true
        self.output_verbosity = output_verbosity

    def run(self):
        global btnx_main_var, path_var, dest_path_var, stop_thr_button_var
        global configuration_engaged, confirm_op2_wait, confirm_op2_bool, thread_engaged_var, settings_source_edit_var, paths_readonly_button_var

        # If Source & Destination Configuration Is Disengaged Then Continue
        if configuration_engaged is False:

            thread_engaged_var[2] = True

            # Set Paths In Stone Before Continuing. Asigns Source & Destination Variables To New Variables That Cannot Be Changed Once Function Exectutes
            path = path_var[2]
            dest = dest_path_var[2]
            compare_bool = compare_bool_var[2]

            # Provide Confirmation/Declination Buttons & Wait For Confirmation/Declination Then Reset Global confirm_op0_wait Boolean Back to True
            btnx_main_var[2].setIcon(QIcon(self.img_btnx_led_1))
            self.confirm_op2_tru.setIcon(QIcon(self.img_execute_true))
            self.confirm_op2_tru.setEnabled(True)

            # Enable Stop thread Button
            stop_thr_button_var[2].setEnabled(True)
            stop_thr_button_var[2].setIcon(QIcon(self.img_stop_thread_true))

            while confirm_op2_wait is True:
                time.sleep(0.3)
            confirm_op2_wait = True

            # Confirmation/Declination Occured, Hide Confirmation/Declination Buttons
            self.confirm_op2_tru.setIcon(QIcon(self.img_execute_false))
            self.confirm_op2_tru.setEnabled(False)

            # If Confirmed Run Main Function
            if confirm_op2_bool is True:
                print('-- ThreadClass2: confirm_op2_bool: accepted')
                btnx_main_var[2].setIcon(QIcon(self.img_btnx_led_2))
                change_var = False

                # Set Counters For Output Summary
                cp0_count = 0
                cp0_fail_count = 0
                cp1_count = 0
                cp1_fail_count = 0

                if os.path.exists(path) and os.path.exists(dest):
                    for dirname, subdirlist, filelist in os.walk(path):
                        for fname in filelist:
                            fullpath = os.path.join(dirname, fname)
                            t_path = fullpath.replace(path, '')
                            t_path = dest + t_path
                            if not fullpath.endswith('.ini'):

                                # Mode 0: Write Missing Files Only
                                if not os.path.exists(t_path):
                                    change_var = True
                                    try:
                                        shutil.copy2(fullpath, t_path)
                                    except IOError:
                                        try:
                                            os.makedirs(os.path.dirname(t_path))
                                            shutil.copy2(fullpath, t_path)
                                        except:
                                            output_str = str('error: ' + t_path).strip()
                                            self.tb_2.append(output_str)

                                    # Mode 0: Check File
                                    if os.path.exists(t_path) and os.path.exists(fullpath):
                                        siz_src = str(os.path.getsize(fullpath))
                                        siz_dest = str(os.path.getsize(t_path))

                                        if siz_src == siz_dest:
                                            if self.output_verbosity is 0:
                                                output_str = str('copied new: ' + t_path).strip()
                                            elif self.output_verbosity is 1:
                                                output_str = str('copied new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                            self.tb_2.append(output_str)
                                            cp0_count += 1

                                        elif siz_src != siz_dest:
                                            output_str = str('failed to copy new (failed bytes check): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                            self.tb_2.append(output_str)
                                            cp0_fail_count += 1

                                    elif not os.path.exists(t_path):
                                        output_str = str('failed to copy new (file does no exist in destination): ' + t_path).strip()
                                        self.tb_2.append(output_str)
                                        cp0_fail_count += 1

                                # Mode 1: Write Missing & Write Predicated Upon Time Stamp Comparison Results
                                elif os.path.exists(t_path):
                                    if compare_bool is True:
                                        ma = os.path.getmtime(fullpath)
                                        mb = os.path.getmtime(t_path)
                                        if mb < ma:
                                            change_var = True
                                            try:
                                                shutil.copy2(fullpath, t_path)
                                            except IOError:
                                                try:
                                                    os.makedirs(os.path.dirname(t_path))
                                                    shutil.copy2(fullpath, t_path)
                                                except:
                                                    output_str = str('error: ' + t_path).strip()
                                                    self.tb_2.append(output_str)

                                            # Mode 1: Check File
                                            if os.path.exists(t_path) and os.path.exists(fullpath):
                                                mb = os.path.getmtime(t_path)
                                                ma_str = str(ma)
                                                mb_str = str(mb)
                                                siz_src = str(os.path.getsize(fullpath))
                                                siz_dest = str(os.path.getsize(t_path))
                                                if mb >= ma and siz_src == siz_dest:
                                                    if self.output_verbosity is 0:
                                                        output_str = str('updated new: ' + t_path).strip()
                                                    elif self.output_verbosity is 1:
                                                        output_str = str('updated new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                                    self.tb_2.append(output_str)
                                                    cp1_count += 1
                                                elif mb < ma or siz_src != siz_dest:
                                                    if siz_src != siz_dest:
                                                        output_str = str('failed to copy new (failed bytes check): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                                        self.tb_2.append(output_str)
                                                        cp1_fail_count += 1
                                                    elif mb < ma:
                                                        output_str = str('failed to copy new (failed timestamp check): (Source: ' + ma_str + ' Destination:' + mb_str + ') ' + t_path).strip()
                                                        self.tb_2.append(output_str)
                                                        cp1_fail_count += 1
                                            elif not os.path.exists(t_path):
                                                output_str = str('failed to update file (file does no exist in destination): ' + t_path).strip()
                                                self.tb_2.append(output_str)
                                                cp1_fail_count += 1

            # Output Summary
            cp0_count_str = str(cp0_count)
            cp0_fail_count_str = str(cp0_fail_count)
            cp1_count_str = str(cp1_count)
            cp1_fail_count_str = str(cp1_fail_count)

            output_sum =  str('copied new: (' + cp0_count_str + ') | failed to copy new: (' + cp0_fail_count_str + ') | updated: (' + cp1_count_str + ')  | failed to update: (' + cp1_fail_count_str + ')').strip()
            print('-- ThreadClass2: ' + output_sum)
            self.tb_2.append(output_sum)

            # Disengage
            btnx_main_var[2].setIcon(QIcon(self.img_btnx_led_0))
            stop_thr_button_var[2].setIcon(QIcon(self.img_stop_thread_false))
            stop_thr_button_var[2].setEnabled(False)
            thread_engaged_var[2] = False
            paths_readonly_button_var[2].setEnabled(True)

    def stop_thr(self):
        global btnx_main_var
        global confirm_op2_bool, confirm_op2_wait
        
        confirm_op2_bool = False
        confirm_op2_wait = True
        print('-- confirm_op2 declined: (confirm_op2_bool)', confirm_op2_bool)
        btnx_main_var[2].setIcon(QIcon(self.img_btnx_led_0))
        self.confirm_op2_tru.setEnabled(False)
        self.confirm_op2_tru.setIcon(QIcon(self.img_execute_false))
        stop_thr_button_var[2].setIcon(QIcon(self.img_stop_thread_false))
        stop_thr_button_var[2].setEnabled(False)
        thread_engaged_var[2] = False
        paths_readonly_button_var[2].setEnabled(True)

        self.terminate()


# Sector 1 Class: Main Function Button Thread 3
class ThreadClass3(QThread):
    def __init__(self, tb_3, confirm_op3_tru, img_btnx_led_0, img_btnx_led_1, img_btnx_led_2, img_execute_false, img_execute_true, img_stop_thread_false, img_stop_thread_true, output_verbosity):
        QThread.__init__(self)
        self.tb_3 = tb_3
        self.confirm_op3_tru = confirm_op3_tru
        self.img_btnx_led_0 = img_btnx_led_0
        self.img_btnx_led_1 = img_btnx_led_1
        self.img_btnx_led_2 = img_btnx_led_2
        self.img_execute_false = img_execute_false
        self.img_execute_true = img_execute_true
        self.img_stop_thread_false = img_stop_thread_false
        self.img_stop_thread_true = img_stop_thread_true
        self.output_verbosity = output_verbosity

    def run(self):
        global btnx_main_var, path_var, dest_path_var, stop_thr_button_var
        global configuration_engaged, confirm_op3_wait, confirm_op3_bool, thread_engaged_var, settings_source_edit_var, paths_readonly_button_var

        # If Source & Destination Configuration Is Disengaged Then Continue
        if configuration_engaged is False:

            thread_engaged_var[3] = True

            # Set Paths In Stone Before Continuing. Asigns Source & Destination Variables To New Variables That Cannot Be Changed Once Function Exectutes
            path = path_var[3]
            dest = dest_path_var[3]
            compare_bool = compare_bool_var[3]

            # Provide Confirmation/Declination Buttons & Wait For Confirmation/Declination Then Reset Global confirm_op0_wait Boolean Back to True
            btnx_main_var[3].setIcon(QIcon(self.img_btnx_led_1))
            self.confirm_op3_tru.setIcon(QIcon(self.img_execute_true))
            self.confirm_op3_tru.setEnabled(True)

            # Enable Stop thread Button
            stop_thr_button_var[3].setEnabled(True)
            stop_thr_button_var[3].setIcon(QIcon(self.img_stop_thread_true))

            while confirm_op3_wait is True:
                time.sleep(0.3)
            confirm_op3_wait = True

            # Confirmation/Declination Occured, Hide Confirmation/Declination Buttons
            self.confirm_op3_tru.setIcon(QIcon(self.img_execute_false))
            self.confirm_op3_tru.setEnabled(False)

            # If Confirmed Run Main Function
            if confirm_op3_bool is True:
                print('-- ThreadClass3: confirm_op3_bool: accepted')
                btnx_main_var[3].setIcon(QIcon(self.img_btnx_led_2))
                change_var = False

                # Set Counters For Output Summary
                cp0_count = 0
                cp0_fail_count = 0
                cp1_count = 0
                cp1_fail_count = 0

                if os.path.exists(path) and os.path.exists(dest):
                    for dirname, subdirlist, filelist in os.walk(path):
                        for fname in filelist:
                            fullpath = os.path.join(dirname, fname)
                            t_path = fullpath.replace(path, '')
                            t_path = dest + t_path
                            if not fullpath.endswith('.ini'):

                                # Mode 0: Write Missing Files Only
                                if not os.path.exists(t_path):
                                    change_var = True
                                    try:
                                        shutil.copy2(fullpath, t_path)
                                    except IOError:
                                        try:
                                            os.makedirs(os.path.dirname(t_path))
                                            shutil.copy2(fullpath, t_path)
                                        except:
                                            output_str = str('error: ' + t_path).strip()
                                            self.tb_3.append(output_str)

                                    # Mode 0: Check File
                                    if os.path.exists(t_path) and os.path.exists(fullpath):
                                        siz_src = str(os.path.getsize(fullpath))
                                        siz_dest = str(os.path.getsize(t_path))

                                        if siz_src == siz_dest:
                                            if self.output_verbosity is 0:
                                                output_str = str('copied new: ' + t_path).strip()
                                            elif self.output_verbosity is 1:
                                                output_str = str('copied new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                            self.tb_3.append(output_str)
                                            cp0_count += 1

                                        elif siz_src != siz_dest:
                                            output_str = str('failed to copy new (failed bytes check): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                            self.tb_3.append(output_str)
                                            cp0_fail_count += 1

                                    elif not os.path.exists(t_path):
                                        output_str = str('failed to copy new (file does no exist in destination): ' + t_path).strip()
                                        self.tb_3.append(output_str)
                                        cp0_fail_count += 1

                                # Mode 1: Write Missing & Write Predicated Upon Time Stamp Comparison Results
                                elif os.path.exists(t_path):
                                    if compare_bool is True:
                                        ma = os.path.getmtime(fullpath)
                                        mb = os.path.getmtime(t_path)
                                        if mb < ma:
                                            change_var = True
                                            try:
                                                shutil.copy2(fullpath, t_path)
                                            except IOError:
                                                try:
                                                    os.makedirs(os.path.dirname(t_path))
                                                    shutil.copy2(fullpath, t_path)
                                                except:
                                                    output_str = str('error: ' + t_path).strip()
                                                    self.tb_3.append(output_str)

                                            # Mode 1: Check File
                                            if os.path.exists(t_path) and os.path.exists(fullpath):
                                                mb = os.path.getmtime(t_path)
                                                ma_str = str(ma)
                                                mb_str = str(mb)
                                                siz_src = str(os.path.getsize(fullpath))
                                                siz_dest = str(os.path.getsize(t_path))
                                                if mb >= ma and siz_src == siz_dest:
                                                    if self.output_verbosity is 0:
                                                        output_str = str('updated new: ' + t_path).strip()
                                                    elif self.output_verbosity is 1:
                                                        output_str = str('updated new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                                    self.tb_3.append(output_str)
                                                    cp1_count += 1
                                                elif mb < ma or siz_src != siz_dest:
                                                    if siz_src != siz_dest:
                                                        output_str = str('failed to copy new (failed bytes check): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                                        self.tb_3.append(output_str)
                                                        cp1_fail_count += 1
                                                    elif mb < ma:
                                                        output_str = str('failed to copy new (failed timestamp check): (Source: ' + ma_str + ' Destination:' + mb_str + ') ' + t_path).strip()
                                                        self.tb_3.append(output_str)
                                                        cp1_fail_count += 1
                                            elif not os.path.exists(t_path):
                                                output_str = str('failed to update file (file does no exist in destination): ' + t_path).strip()
                                                self.tb_3.append(output_str)
                                                cp1_fail_count += 1

            # Output Summary
            cp0_count_str = str(cp0_count)
            cp0_fail_count_str = str(cp0_fail_count)
            cp1_count_str = str(cp1_count)
            cp1_fail_count_str = str(cp1_fail_count)

            output_sum =  str('copied new: (' + cp0_count_str + ') | failed to copy new: (' + cp0_fail_count_str + ') | updated: (' + cp1_count_str + ')  | failed to update: (' + cp1_fail_count_str + ')').strip()
            print('-- ThreadClass3: ' + output_sum)
            self.tb_3.append(output_sum)

            # Disengage
            btnx_main_var[3].setIcon(QIcon(self.img_btnx_led_0))
            stop_thr_button_var[3].setIcon(QIcon(self.img_stop_thread_false))
            stop_thr_button_var[3].setEnabled(False)
            thread_engaged_var[3] = False
            paths_readonly_button_var[3].setEnabled(True)

    def stop_thr(self):
        global btnx_main_var
        global confirm_op3_bool, confirm_op3_wait
        
        confirm_op3_bool = False
        confirm_op3_wait = True
        print('-- confirm_op3 declined: (confirm_op3_bool)', confirm_op3_bool)
        btnx_main_var[3].setIcon(QIcon(self.img_btnx_led_0))
        self.confirm_op3_tru.setEnabled(False)
        self.confirm_op3_tru.setIcon(QIcon(self.img_execute_false))
        stop_thr_button_var[3].setIcon(QIcon(self.img_stop_thread_false))
        stop_thr_button_var[3].setEnabled(False)
        thread_engaged_var[3] = False
        paths_readonly_button_var[3].setEnabled(True)

        self.terminate()


# Sector 1 Class: Main Function Button Thread 4
class ThreadClass4(QThread):
    def __init__(self, tb_4, confirm_op4_tru, img_btnx_led_0, img_btnx_led_1, img_btnx_led_2, img_execute_false, img_execute_true, img_stop_thread_false, img_stop_thread_true, output_verbosity):
        QThread.__init__(self)
        self.tb_4 = tb_4
        self.confirm_op4_tru = confirm_op4_tru
        self.img_btnx_led_0 = img_btnx_led_0
        self.img_btnx_led_1 = img_btnx_led_1
        self.img_btnx_led_2 = img_btnx_led_2
        self.img_execute_false = img_execute_false
        self.img_execute_true = img_execute_true
        self.img_stop_thread_false = img_stop_thread_false
        self.img_stop_thread_true = img_stop_thread_true
        self.output_verbosity = output_verbosity

    def run(self):
        global btnx_main_var, path_var, dest_path_var, stop_thr_button_var
        global configuration_engaged, confirm_op4_wait, confirm_op4_bool, thread_engaged_var, settings_source_edit_var, paths_readonly_button_var

        # If Source & Destination Configuration Is Disengaged Then Continue
        if configuration_engaged is False:

            thread_engaged_var[4] = True

            # Set Paths In Stone Before Continuing. Asigns Source & Destination Variables To New Variables That Cannot Be Changed Once Function Exectutes
            path = path_var[4]
            dest = dest_path_var[4]
            compare_bool = compare_bool_var[4]

            # Provide Confirmation/Declination Buttons & Wait For Confirmation/Declination Then Reset Global confirm_op0_wait Boolean Back to True
            btnx_main_var[4].setIcon(QIcon(self.img_btnx_led_1))
            self.confirm_op4_tru.setIcon(QIcon(self.img_execute_true))
            self.confirm_op4_tru.setEnabled(True)

            # Enable Stop thread Button
            stop_thr_button_var[4].setEnabled(True)
            stop_thr_button_var[4].setIcon(QIcon(self.img_stop_thread_true))

            while confirm_op4_wait is True:
                time.sleep(0.3)
            confirm_op4_wait = True

            # Confirmation/Declination Occured, Hide Confirmation/Declination Buttons
            self.confirm_op4_tru.setIcon(QIcon(self.img_execute_false))
            self.confirm_op4_tru.setEnabled(False)

            # If Confirmed Run Main Function
            if confirm_op4_bool is True:
                print('-- ThreadClass4: confirm_op4_bool: accepted')
                btnx_main_var[4].setIcon(QIcon(self.img_btnx_led_2))
                change_var = False

                # Set Counters For Output Summary
                cp0_count = 0
                cp0_fail_count = 0
                cp1_count = 0
                cp1_fail_count = 0

                if os.path.exists(path) and os.path.exists(dest):
                    for dirname, subdirlist, filelist in os.walk(path):
                        for fname in filelist:
                            fullpath = os.path.join(dirname, fname)
                            t_path = fullpath.replace(path, '')
                            t_path = dest + t_path
                            if not fullpath.endswith('.ini'):

                                # Mode 0: Write Missing Files Only
                                if not os.path.exists(t_path):
                                    change_var = True
                                    try:
                                        shutil.copy2(fullpath, t_path)
                                    except IOError:
                                        try:
                                            os.makedirs(os.path.dirname(t_path))
                                            shutil.copy2(fullpath, t_path)
                                        except:
                                            output_str = str('error: ' + t_path).strip()
                                            self.tb_4.append(output_str)

                                    # Mode 0: Check File
                                    if os.path.exists(t_path) and os.path.exists(fullpath):
                                        siz_src = str(os.path.getsize(fullpath))
                                        siz_dest = str(os.path.getsize(t_path))

                                        if siz_src == siz_dest:
                                            if self.output_verbosity is 0:
                                                output_str = str('copied new: ' + t_path).strip()
                                            elif self.output_verbosity is 1:
                                                output_str = str('copied new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                            self.tb_4.append(output_str)
                                            cp0_count += 1

                                        elif siz_src != siz_dest:
                                            output_str = str('failed to copy new (failed bytes check): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                            self.tb_4.append(output_str)
                                            cp0_fail_count += 1

                                    elif not os.path.exists(t_path):
                                        output_str = str('failed to copy new (file does no exist in destination): ' + t_path).strip()
                                        self.tb_4.append(output_str)
                                        cp0_fail_count += 1

                                # Mode 1: Write Missing & Write Predicated Upon Time Stamp Comparison Results
                                elif os.path.exists(t_path):
                                    if compare_bool is True:
                                        ma = os.path.getmtime(fullpath)
                                        mb = os.path.getmtime(t_path)
                                        if mb < ma:
                                            change_var = True
                                            try:
                                                shutil.copy2(fullpath, t_path)
                                            except IOError:
                                                try:
                                                    os.makedirs(os.path.dirname(t_path))
                                                    shutil.copy2(fullpath, t_path)
                                                except:
                                                    output_str = str('error: ' + t_path).strip()
                                                    self.tb_4.append(output_str)

                                            # Mode 1: Check File
                                            if os.path.exists(t_path) and os.path.exists(fullpath):
                                                mb = os.path.getmtime(t_path)
                                                ma_str = str(ma)
                                                mb_str = str(mb)
                                                siz_src = str(os.path.getsize(fullpath))
                                                siz_dest = str(os.path.getsize(t_path))
                                                if mb >= ma and siz_src == siz_dest:
                                                    if self.output_verbosity is 0:
                                                        output_str = str('updated new: ' + t_path).strip()
                                                    elif self.output_verbosity is 1:
                                                        output_str = str('updated new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                                    self.tb_4.append(output_str)
                                                    cp1_count += 1
                                                elif mb < ma or siz_src != siz_dest:
                                                    if siz_src != siz_dest:
                                                        output_str = str('failed to copy new (failed bytes check): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                                        self.tb_4.append(output_str)
                                                        cp1_fail_count += 1
                                                    elif mb < ma:
                                                        output_str = str('failed to copy new (failed timestamp check): (Source: ' + ma_str + ' Destination:' + mb_str + ') ' + t_path).strip()
                                                        self.tb_4.append(output_str)
                                                        cp1_fail_count += 1
                                            elif not os.path.exists(t_path):
                                                output_str = str('failed to update file (file does no exist in destination): ' + t_path).strip()
                                                self.tb_4.append(output_str)
                                                cp1_fail_count += 1

            # Output Summary
            cp0_count_str = str(cp0_count)
            cp0_fail_count_str = str(cp0_fail_count)
            cp1_count_str = str(cp1_count)
            cp1_fail_count_str = str(cp1_fail_count)

            output_sum =  str('copied new: (' + cp0_count_str + ') | failed to copy new: (' + cp0_fail_count_str + ') | updated: (' + cp1_count_str + ')  | failed to update: (' + cp1_fail_count_str + ')').strip()
            print('-- ThreadClass4: ' + output_sum)
            self.tb_4.append(output_sum)

            # Disengage
            btnx_main_var[4].setIcon(QIcon(self.img_btnx_led_0))
            stop_thr_button_var[4].setIcon(QIcon(self.img_stop_thread_false))
            stop_thr_button_var[4].setEnabled(False)
            thread_engaged_var[4] = False
            paths_readonly_button_var[4].setEnabled(True)

    def stop_thr(self):
        global btnx_main_var
        global confirm_op4_bool, confirm_op4_wait
        
        confirm_op4_bool = False
        confirm_op4_wait = True
        print('-- confirm_op4 declined: (confirm_op4_bool)', confirm_op4_bool)
        btnx_main_var[4].setIcon(QIcon(self.img_btnx_led_0))
        self.confirm_op4_tru.setEnabled(False)
        self.confirm_op4_tru.setIcon(QIcon(self.img_execute_false))
        stop_thr_button_var[4].setIcon(QIcon(self.img_stop_thread_false))
        stop_thr_button_var[4].setEnabled(False)
        thread_engaged_var[4] = False
        paths_readonly_button_var[4].setEnabled(True)

        self.terminate()


# Sector 1 Class: Main Function Button Thread 5
class ThreadClass5(QThread):
    def __init__(self, tb_5, confirm_op5_tru, img_btnx_led_0, img_btnx_led_1, img_btnx_led_2, img_execute_false, img_execute_true, img_stop_thread_false, img_stop_thread_true, output_verbosity):
        QThread.__init__(self)
        self.tb_5 = tb_5
        self.confirm_op5_tru = confirm_op5_tru
        self.img_btnx_led_0 = img_btnx_led_0
        self.img_btnx_led_1 = img_btnx_led_1
        self.img_btnx_led_2 = img_btnx_led_2
        self.img_execute_false = img_execute_false
        self.img_execute_true = img_execute_true
        self.img_stop_thread_false = img_stop_thread_false
        self.img_stop_thread_true = img_stop_thread_true
        self.output_verbosity = output_verbosity

    def run(self):
        global btnx_main_var, path_var, dest_path_var, stop_thr_button_var
        global configuration_engaged, confirm_op5_wait, confirm_op5_bool, thread_engaged_var, settings_source_edit_var, paths_readonly_button_var

        # If Source & Destination Configuration Is Disengaged Then Continue
        if configuration_engaged is False:

            thread_engaged_var[5] = True

            # Set Paths In Stone Before Continuing. Asigns Source & Destination Variables To New Variables That Cannot Be Changed Once Function Exectutes
            path = path_var[5]
            dest = dest_path_var[5]
            compare_bool = compare_bool_var[5]

            # Provide Confirmation/Declination Buttons & Wait For Confirmation/Declination Then Reset Global confirm_op0_wait Boolean Back to True
            btnx_main_var[5].setIcon(QIcon(self.img_btnx_led_1))
            self.confirm_op5_tru.setIcon(QIcon(self.img_execute_true))
            self.confirm_op5_tru.setEnabled(True)

            # Enable Stop thread Button
            stop_thr_button_var[5].setEnabled(True)
            stop_thr_button_var[5].setIcon(QIcon(self.img_stop_thread_true))

            while confirm_op5_wait is True:
                time.sleep(0.3)
            confirm_op5_wait = True

            # Confirmation/Declination Occured, Hide Confirmation/Declination Buttons
            self.confirm_op5_tru.setIcon(QIcon(self.img_execute_false))
            self.confirm_op5_tru.setEnabled(False)

            # If Confirmed Run Main Function
            if confirm_op5_bool is True:
                print('-- ThreadClass5: confirm_op5_bool: accepted')
                btnx_main_var[5].setIcon(QIcon(self.img_btnx_led_2))
                change_var = False

                # Set Counters For Output Summary
                cp0_count = 0
                cp0_fail_count = 0
                cp1_count = 0
                cp1_fail_count = 0

                if os.path.exists(path) and os.path.exists(dest):
                    for dirname, subdirlist, filelist in os.walk(path):
                        for fname in filelist:
                            fullpath = os.path.join(dirname, fname)
                            t_path = fullpath.replace(path, '')
                            t_path = dest + t_path
                            if not fullpath.endswith('.ini'):

                                # Mode 0: Write Missing Files Only
                                if not os.path.exists(t_path):
                                    change_var = True
                                    try:
                                        shutil.copy2(fullpath, t_path)
                                    except IOError:
                                        try:
                                            os.makedirs(os.path.dirname(t_path))
                                            shutil.copy2(fullpath, t_path)
                                        except:
                                            output_str = str('error: ' + t_path).strip()
                                            self.tb_5.append(output_str)

                                    # Mode 0: Check File
                                    if os.path.exists(t_path) and os.path.exists(fullpath):
                                        siz_src = str(os.path.getsize(fullpath))
                                        siz_dest = str(os.path.getsize(t_path))

                                        if siz_src == siz_dest:
                                            if self.output_verbosity is 0:
                                                output_str = str('copied new: ' + t_path).strip()
                                            elif self.output_verbosity is 1:
                                                output_str = str('copied new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                            self.tb_5.append(output_str)
                                            cp0_count += 1

                                        elif siz_src != siz_dest:
                                            output_str = str('failed to copy new (failed bytes check): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                            self.tb_5.append(output_str)
                                            cp0_fail_count += 1

                                    elif not os.path.exists(t_path):
                                        output_str = str('failed to copy new (file does no exist in destination): ' + t_path).strip()
                                        self.tb_5.append(output_str)
                                        cp0_fail_count += 1

                                # Mode 1: Write Missing & Write Predicated Upon Time Stamp Comparison Results
                                elif os.path.exists(t_path):
                                    if compare_bool is True:
                                        ma = os.path.getmtime(fullpath)
                                        mb = os.path.getmtime(t_path)
                                        if mb < ma:
                                            change_var = True
                                            try:
                                                shutil.copy2(fullpath, t_path)
                                            except IOError:
                                                try:
                                                    os.makedirs(os.path.dirname(t_path))
                                                    shutil.copy2(fullpath, t_path)
                                                except:
                                                    output_str = str('error: ' + t_path).strip()
                                                    self.tb_5.append(output_str)

                                            # Mode 1: Check File
                                            if os.path.exists(t_path) and os.path.exists(fullpath):
                                                mb = os.path.getmtime(t_path)
                                                ma_str = str(ma)
                                                mb_str = str(mb)
                                                siz_src = str(os.path.getsize(fullpath))
                                                siz_dest = str(os.path.getsize(t_path))
                                                if mb >= ma and siz_src == siz_dest:
                                                    if self.output_verbosity is 0:
                                                        output_str = str('updated new: ' + t_path).strip()
                                                    elif self.output_verbosity is 1:
                                                        output_str = str('updated new: (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                                    self.tb_5.append(output_str)
                                                    cp1_count += 1
                                                elif mb < ma or siz_src != siz_dest:
                                                    if siz_src != siz_dest:
                                                        output_str = str('failed to copy new (failed bytes check): (' + siz_dest + '/' + siz_src + ' bytes) ' + t_path).strip()
                                                        self.tb_5.append(output_str)
                                                        cp1_fail_count += 1
                                                    elif mb < ma:
                                                        output_str = str('failed to copy new (failed timestamp check): (Source: ' + ma_str + ' Destination:' + mb_str + ') ' + t_path).strip()
                                                        self.tb_5.append(output_str)
                                                        cp1_fail_count += 1
                                            elif not os.path.exists(t_path):
                                                output_str = str('failed to update file (file does no exist in destination): ' + t_path).strip()
                                                self.tb_5.append(output_str)
                                                cp1_fail_count += 1

            # Output Summary
            cp0_count_str = str(cp0_count)
            cp0_fail_count_str = str(cp0_fail_count)
            cp1_count_str = str(cp1_count)
            cp1_fail_count_str = str(cp1_fail_count)

            output_sum =  str('copied new: (' + cp0_count_str + ') | failed to copy new: (' + cp0_fail_count_str + ') | updated: (' + cp1_count_str + ')  | failed to update: (' + cp1_fail_count_str + ')').strip()
            print('-- ThreadClass5: ' + output_sum)
            self.tb_5.append(output_sum)

            # Disengage
            btnx_main_var[5].setIcon(QIcon(self.img_btnx_led_0))
            stop_thr_button_var[5].setIcon(QIcon(self.img_stop_thread_false))
            stop_thr_button_var[5].setEnabled(False)
            thread_engaged_var[5] = False
            paths_readonly_button_var[5].setEnabled(True)

    def stop_thr(self):
        global btnx_main_var
        global confirm_op5_bool, confirm_op5_wait
        
        confirm_op5_bool = False
        confirm_op5_wait = True
        print('-- confirm_op5 declined: (confirm_op5_bool)', confirm_op5_bool)
        btnx_main_var[5].setIcon(QIcon(self.img_btnx_led_0))
        self.confirm_op5_tru.setEnabled(False)
        self.confirm_op5_tru.setIcon(QIcon(self.img_execute_false))
        stop_thr_button_var[5].setIcon(QIcon(self.img_stop_thread_false))
        stop_thr_button_var[5].setEnabled(False)
        thread_engaged_var[5] = False
        paths_readonly_button_var[5].setEnabled(True)

        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
