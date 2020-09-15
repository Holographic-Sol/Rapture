import os
import sys
import time
import shutil
import datetime
import win32con
import win32api
import win32process
import distutils.dir_util
from win32api import GetSystemMetrics
from win32gui import GetWindowText, GetForegroundWindow
from PyQt5.QtCore import Qt, QThread, QSize, QTimer, QPoint, QCoreApplication, QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit, QDesktopWidget, QTextBrowser
from PyQt5.QtGui import QIcon, QFont, QPixmap, QCursor, QTextCursor
from PyQt5 import QtCore
from pynput.mouse import Listener


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
cfg_f = 'config_profile_0.txt'
img_path = './image/default/'
source_path_entered = ''
dest_path_entered = ''
path_var = ['', '', '', '', '', '']
dest_path_var = ['', '', '', '', '', '']
name_tile = ['', '', '', '', '', '']
debug_enabled = False
confirm_op0_wait = True
confirm_op1_wait = True
confirm_op2_wait = True
confirm_op3_wait = True
confirm_op4_wait = True
confirm_op5_wait = True
confirm_op0_bool = False
confirm_op1_bool = False
confirm_op2_bool = False
confirm_op3_bool = False
confirm_op4_bool = False
confirm_op5_bool = False
configuration_engaged = False
settings_input_response_dest_bool = None
settings_input_response_source_bool = None
compare_bool_var = [False, False, False, False, False, False]
thread_engaged_var = [False, False, False, False, False, False]
thread_initialized_var = [False, False, False, False, False, False]
valid_len_bool = False
valid_drive_bool = False
valid_char_bool = False
valid_non_win_res_nm_bool = False
out_of_bounds = True
source_selected = ()
dest_selected = ()
settings_active_int = 0
settings_active_int_prev = ()
compare_clicked = ()
sanitize_input_int = ()
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


class App(QMainWindow):
    #cursorMove = pyqtSignal(object)
    def __init__(self):
        super(App, self).__init__()
        global debug_enabled, img_path

        # Set Program Icon & Program Title
        self.setWindowIcon(QIcon('./icon.png'))
        self.title = '[SHIFT] Extreme Backup Solution'
        # Set Window Width And Height
        self.width = 630
        self.height = 310
        # Position Window On The Display
        scr_w = GetSystemMetrics(0)
        scr_h = GetSystemMetrics(1)
        self.left = (scr_w / 2) - (self.width / 2)
        self.top = ((scr_h / 2) - (self.height / 2))
        # Set Window Title Bar Frameless Windows Hint
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        # Set Font
        self.font_s4b = QFont("Segoe UI", 4, QFont.Bold)
        self.font_s5b = QFont("Segoe UI", 5, QFont.Bold)
        self.font_s6b = QFont("Segoe UI", 6, QFont.Bold)
        # Run Set Style Sheet Function & Run Set Images Function
        self.set_style_sheet_funk()
        self.set_images_funk()
        # Run initUI Function
        self.initUI()

    def initUI(self):
        global debug_enabled
        global path_var, dest_path_var, settings_active_int
        global confirm_op0_bool, confirm_op1_bool, confirm_op2_bool, confirm_op3_bool, confirm_op4_bool, confirm_op5_bool
        global confirm_op0_wait, confirm_op1_wait, confirm_op2_wait, confirm_op3_wait, confirm_op4_wait, confirm_op5_wait

        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.output_verbosity = 1
        self.btnx_main_var = []
        self.btnx_mode_btn_var = []
        self.stop_thread_btn_var = []
        self.paths_readonly_btn_var = []
        self.back_label_var = []
        self.settings_source_edit_var = []
        self.settings_dest_edit_var = []
        self.settings_title_var = []
        self.setting_title_B_var = []
        self.tb_var = []
        self.cnfg_prof_btn_var = []
        self.confirm_op_var = []

        # Title Bar: Geometry
        cnfg_prof_btn_h = 10
        cnfg_prof_btn_w = 40
        tot_prof_btn_w = (cnfg_prof_btn_w * 10) + (5 * 9)
        cnfg_prof_btn_ph = 4
        cnfg_prof_btn_pw = (self.width / 2) - (tot_prof_btn_w / 2)
        # Sector 1: Geometry Main Function
        back_label_buffer = 6
        back_label_ankor_w0 = 8
        back_label_ankor_w1 = 111
        back_label_ankor_w2 = 214
        back_label_ankor_w3 = 317
        back_label_ankor_w4 = 420
        back_label_ankor_w5 = 523
        back_label_ankor_h0 = 28
        back_label_ankor_h1 = 28
        back_label_ankor_h2 = 28
        back_label_ankor_h3 = 28
        back_label_ankor_h4 = 28
        back_label_ankor_h5 = 28
        self.back_label_w_0 = 99
        self.back_label_h_0 = 83
        self.back_label_w_1 = 99
        self.back_label_h_1 = 90
        btnx_buffer_0 = 3
        btnx_w = 54
        btnx_h = 54
        confirm_op_w = 30
        confirm_op_h = 10
        self.title_lable_w_0 = 87
        self.title_lable_h_0 = 15
        self.title_lable_w_1 = 87
        self.title_lable_h_1 = 16

        # Sector 2: Geometry Source & Destination
        user_paths_ankor_w = 107
        user_paths_ankor_h = (back_label_ankor_h0 + back_label_buffer + btnx_h + btnx_buffer_0 + 1 + self.title_lable_h_0 + 20)
        source_dest_buffer_w = 5
        source_dest_buffer_h = 5
        source_dest_w = (self.width - 152)
        source_dest_h = 15
        # Sector 3: Geometry Output
        self.tb_w = self.width - 10
        self.tb_pos_w = 5
        self.tb_pos_h = 185
        self.tb_h = (self.height - self.tb_pos_h - 5)

        # Title Bar: Logo
        self.title_logo_btn = QPushButton(self)
        self.title_logo_btn.move(0, 0)
        self.title_logo_btn.resize(20, 20)
        self.title_logo_btn.setIcon(QIcon("./icon.png"))
        self.title_logo_btn.setIconSize(QSize(12, 12))
        self.title_logo_btn.clicked.connect(self.title_logo_btn_funk)
        self.title_logo_btn.setStyleSheet(self.default_title_qpb_style)
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
        # Manual Refresh From Configuration File
        self.refresh_btn = QPushButton(self)
        self.refresh_btn.move(20, 0)
        self.refresh_btn.resize(20, 20)
        self.refresh_btn.setIcon(QIcon("./icon.png"))
        self.refresh_btn.setIconSize(QSize(12, 12))
        self.refresh_btn.clicked.connect(self.refresh_btn_funk)
        self.refresh_btn.setStyleSheet(self.default_title_qpb_style)
        self.refresh_btn.hide()
        # Tiltle Bar: Configuration Profile 0
        self.cnfg_prof_btn_0 = QPushButton(self)
        self.cnfg_prof_btn_0.move(cnfg_prof_btn_pw, cnfg_prof_btn_ph)
        self.cnfg_prof_btn_0.resize(cnfg_prof_btn_w, cnfg_prof_btn_h)
        self.cnfg_prof_btn_0.setFont(self.font_s5b)
        self.cnfg_prof_btn_0.setText('SHIFT 0')
        self.cnfg_prof_btn_0.setIconSize(QSize(12, 12))
        self.cnfg_prof_btn_0.clicked.connect(self.cnfg_prof_funk_0)
        self.cnfg_prof_btn_0.setStyleSheet(self.default_title_config_prof_qpbtn_style_1)
        self.cnfg_prof_btn_var.append(self.cnfg_prof_btn_0)
        # Tiltle Bar: Configuration Profile 1
        self.cnfg_prof_btn_1 = QPushButton(self)
        self.cnfg_prof_btn_1.move((cnfg_prof_btn_pw + cnfg_prof_btn_w + 5), cnfg_prof_btn_ph)
        self.cnfg_prof_btn_1.resize(cnfg_prof_btn_w, cnfg_prof_btn_h)
        self.cnfg_prof_btn_1.setFont(self.font_s5b)
        self.cnfg_prof_btn_1.setText('SHIFT 1')
        self.cnfg_prof_btn_1.setIconSize(QSize(12, 12))
        self.cnfg_prof_btn_1.clicked.connect(self.cnfg_prof_funk_1)
        self.cnfg_prof_btn_1.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_var.append(self.cnfg_prof_btn_1)
        # Tiltle Bar: Configuration Profile 2
        self.cnfg_prof_btn_2 = QPushButton(self)
        self.cnfg_prof_btn_2.move((cnfg_prof_btn_pw + (cnfg_prof_btn_w * 2) + 10), cnfg_prof_btn_ph)
        self.cnfg_prof_btn_2.resize(cnfg_prof_btn_w, cnfg_prof_btn_h)
        self.cnfg_prof_btn_2.setFont(self.font_s5b)
        self.cnfg_prof_btn_2.setText('SHIFT 2')
        self.cnfg_prof_btn_2.setIconSize(QSize(12, 12))
        self.cnfg_prof_btn_2.clicked.connect(self.cnfg_prof_funk_2)
        self.cnfg_prof_btn_2.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_var.append(self.cnfg_prof_btn_2)
        # Tiltle Bar: Configuration Profile 3
        self.cnfg_prof_btn_3 = QPushButton(self)
        self.cnfg_prof_btn_3.move((cnfg_prof_btn_pw + (cnfg_prof_btn_w * 3) + 15), cnfg_prof_btn_ph)
        self.cnfg_prof_btn_3.resize(cnfg_prof_btn_w, cnfg_prof_btn_h)
        self.cnfg_prof_btn_3.setFont(self.font_s5b)
        self.cnfg_prof_btn_3.setText('SHIFT 3')
        self.cnfg_prof_btn_3.setIconSize(QSize(12, 12))
        self.cnfg_prof_btn_3.clicked.connect(self.cnfg_prof_funk_3)
        self.cnfg_prof_btn_3.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_var.append(self.cnfg_prof_btn_3)
        # Tiltle Bar: Configuration Profile 4
        self.cnfg_prof_btn_4 = QPushButton(self)
        self.cnfg_prof_btn_4.move((cnfg_prof_btn_pw + (cnfg_prof_btn_w * 4) + 20), cnfg_prof_btn_ph)
        self.cnfg_prof_btn_4.resize(cnfg_prof_btn_w, cnfg_prof_btn_h)
        self.cnfg_prof_btn_4.setFont(self.font_s5b)
        self.cnfg_prof_btn_4.setText('SHIFT 4')
        self.cnfg_prof_btn_4.setIconSize(QSize(12, 12))
        self.cnfg_prof_btn_4.clicked.connect(self.cnfg_prof_funk_4)
        self.cnfg_prof_btn_4.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_var.append(self.cnfg_prof_btn_4)
        # Tiltle Bar: Configuration Profile 5
        self.cnfg_prof_btn_5 = QPushButton(self)
        self.cnfg_prof_btn_5.move((cnfg_prof_btn_pw + (cnfg_prof_btn_w * 5) + 25), cnfg_prof_btn_ph)
        self.cnfg_prof_btn_5.resize(cnfg_prof_btn_w, cnfg_prof_btn_h)
        self.cnfg_prof_btn_5.setFont(self.font_s5b)
        self.cnfg_prof_btn_5.setText('SHIFT 5')
        self.cnfg_prof_btn_5.setIconSize(QSize(12, 12))
        self.cnfg_prof_btn_5.clicked.connect(self.cnfg_prof_funk_5)
        self.cnfg_prof_btn_5.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_var.append(self.cnfg_prof_btn_5)
        # Tiltle Bar: Configuration Profile 6
        self.cnfg_prof_btn_6 = QPushButton(self)
        self.cnfg_prof_btn_6.move((cnfg_prof_btn_pw + (cnfg_prof_btn_w * 6) + 30), cnfg_prof_btn_ph)
        self.cnfg_prof_btn_6.resize(cnfg_prof_btn_w, cnfg_prof_btn_h)
        self.cnfg_prof_btn_6.setFont(self.font_s5b)
        self.cnfg_prof_btn_6.setText('SHIFT 6')
        self.cnfg_prof_btn_6.setIconSize(QSize(12, 12))
        self.cnfg_prof_btn_6.clicked.connect(self.cnfg_prof_funk_6)
        self.cnfg_prof_btn_6.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_var.append(self.cnfg_prof_btn_6)
        # Tiltle Bar: Configuration Profile 7
        self.cnfg_prof_btn_7 = QPushButton(self)
        self.cnfg_prof_btn_7.move((cnfg_prof_btn_pw + (cnfg_prof_btn_w * 7) + 35), cnfg_prof_btn_ph)
        self.cnfg_prof_btn_7.resize(cnfg_prof_btn_w, cnfg_prof_btn_h)
        self.cnfg_prof_btn_7.setFont(self.font_s5b)
        self.cnfg_prof_btn_7.setText('SHIFT 7')
        self.cnfg_prof_btn_7.setIconSize(QSize(12, 12))
        self.cnfg_prof_btn_7.clicked.connect(self.cnfg_prof_funk_7)
        self.cnfg_prof_btn_7.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_var.append(self.cnfg_prof_btn_7)
        # Tiltle Bar: Configuration Profile 8
        self.cnfg_prof_btn_8 = QPushButton(self)
        self.cnfg_prof_btn_8.move((cnfg_prof_btn_pw + (cnfg_prof_btn_w * 8) + 40), cnfg_prof_btn_ph)
        self.cnfg_prof_btn_8.resize(cnfg_prof_btn_w, cnfg_prof_btn_h)
        self.cnfg_prof_btn_8.setFont(self.font_s5b)
        self.cnfg_prof_btn_8.setText('SHIFT 8')
        self.cnfg_prof_btn_8.setIconSize(QSize(12, 12))
        self.cnfg_prof_btn_8.clicked.connect(self.cnfg_prof_funk_8)
        self.cnfg_prof_btn_8.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_var.append(self.cnfg_prof_btn_8)
        # Tiltle Bar: Configuration Profile 9
        self.cnfg_prof_btn_9 = QPushButton(self)
        self.cnfg_prof_btn_9.move((cnfg_prof_btn_pw + (cnfg_prof_btn_w * 9) + 45), cnfg_prof_btn_ph)
        self.cnfg_prof_btn_9.resize(cnfg_prof_btn_w, cnfg_prof_btn_h)
        self.cnfg_prof_btn_9.setFont(self.font_s5b)
        self.cnfg_prof_btn_9.setText('SHIFT 9')
        self.cnfg_prof_btn_9.setIconSize(QSize(12, 12))
        self.cnfg_prof_btn_9.clicked.connect(self.cnfg_prof_funk_9)
        self.cnfg_prof_btn_9.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_var.append(self.cnfg_prof_btn_9)
        # Sector 1: Background Colour
        self.back_label_main = QLabel(self)
        self.back_label_main.move(0, 20)
        self.back_label_main.resize(self.width, 98)
        self.back_label_main.setStyleSheet(self.default_bg_0_style)
        # Sector 1: Background Tiles
        i = 0
        while i < 6:
            back_label = 'back_label' + str(i)
            self.back_label = QLabel(self)
            self.back_label.resize(self.back_label_w_0, self.back_label_h_0)
            self.back_label.setStyleSheet(self.default_bg_tile_style)
            self.back_label_var.append(self.back_label)
            i += 1
        # Sector 1: Background Tiles Moved Into Positions, W & H
        self.back_label_var[0].move(back_label_ankor_w0, back_label_ankor_h0)
        self.back_label_var[1].move(back_label_ankor_w1, back_label_ankor_h1)
        self.back_label_var[2].move(back_label_ankor_w2, back_label_ankor_h2)
        self.back_label_var[3].move(back_label_ankor_w3, back_label_ankor_h3)
        self.back_label_var[4].move(back_label_ankor_w4, back_label_ankor_h4)
        self.back_label_var[5].move(back_label_ankor_w5, back_label_ankor_h5)

        # Sector 1: Objects Placed On Top Background Tiles
        i = 0
        while i < 6:
            # Sector 1: Main Function Button(s)
            btnx_name = 'btnx_main' + str(i)
            self.btnx_main = QPushButton(self)
            self.btnx_main.resize(btnx_w, btnx_h)
            self.btnx_main.setIcon(QIcon(self.img_btnx_led_0))
            self.btnx_main.setIconSize(QSize(54, 54))
            self.btnx_main.setStyleSheet(self.default_btnx_main_style)
            self.btnx_main_var.append(self.btnx_main)
            # Sector 1: Switch Main Function Mode Button(s)
            self.btnx_mode_button = 'btnx_mode_button' + str(i)
            self.btnx_mode_button = QPushButton(self)
            self.btnx_mode_button.resize(30, 26)
            self.btnx_mode_button.setIcon(QIcon(self.img_mode_0))
            self.btnx_mode_button.setIconSize(QSize(18, 18))
            self.btnx_mode_button.setStyleSheet(self.default_qpbtn_style)
            self.btnx_mode_btn_var.append(self.btnx_mode_button)
            # Sector 1: Stop Main Functions(s) Button(s)
            stop_thread_btn = 'stop_thread_btn' + str(i)
            self.stop_thread_btn = QPushButton(self)
            self.stop_thread_btn.resize(30, 10)
            self.stop_thread_btn.setIcon(QIcon(self.img_stop_thread_false))
            self.stop_thread_btn.setIconSize(QSize(15, 15))
            self.stop_thread_btn.setStyleSheet(self.default_qpbtn_style)
            self.stop_thread_btn_var.append(self.stop_thread_btn)
            self.stop_thread_btn.setEnabled(False)
            # Sector 2: Enable/Disable ReadOnly Path Settings
            paths_readonly_button = 'paths_readonly_button' + str(i)
            self.paths_readonly_button = QPushButton(self)
            self.paths_readonly_button.resize(15, 35)
            self.paths_readonly_button.move((user_paths_ankor_w + source_dest_w + 15), user_paths_ankor_h)
            self.paths_readonly_button.setIcon(QIcon(self.img_read_ony_true))
            self.paths_readonly_button.setIconSize(QSize(8, 8))
            self.paths_readonly_button.setStyleSheet(self.default_qpb_highlight)
            self.paths_readonly_btn_var.append(self.paths_readonly_button)
            self.paths_readonly_btn_var[i].hide()
            i += 1

        self.paths_readonly_btn_var[0].show()
        self.btnx_main_var[0].setStyleSheet(self.default_btnx_main_style_1)
        self.stop_thread_btn_var[0].setStyleSheet(self.default_qpb_highlight)
        self.btnx_main_0 = self.btnx_main_var[0]
        self.btnx_main_1 = self.btnx_main_var[1]
        self.btnx_main_2 = self.btnx_main_var[2]
        self.btnx_main_3 = self.btnx_main_var[3]
        self.btnx_main_4 = self.btnx_main_var[4]
        self.btnx_main_5 = self.btnx_main_var[5]
        self.btnx_mode_btn_0 = self.btnx_mode_btn_var[0]
        self.btnx_mode_btn_1 = self.btnx_mode_btn_var[1]
        self.btnx_mode_btn_2 = self.btnx_mode_btn_var[2]
        self.btnx_mode_btn_3 = self.btnx_mode_btn_var[3]
        self.btnx_mode_btn_4 = self.btnx_mode_btn_var[4]
        self.btnx_mode_btn_5 = self.btnx_mode_btn_var[5]
        self.stop_thread_btn_0 = self.stop_thread_btn_var[0]
        self.stop_thread_btn_1 = self.stop_thread_btn_var[1]
        self.stop_thread_btn_2 = self.stop_thread_btn_var[2]
        self.stop_thread_btn_3 = self.stop_thread_btn_var[3]
        self.stop_thread_btn_4 = self.stop_thread_btn_var[4]
        self.stop_thread_btn_5 = self.stop_thread_btn_var[5]
        self.paths_readonly_btn_0 = self.paths_readonly_btn_var[0]
        self.paths_readonly_btn_1 = self.paths_readonly_btn_var[1]
        self.paths_readonly_btn_2 = self.paths_readonly_btn_var[2]
        self.paths_readonly_btn_3 = self.paths_readonly_btn_var[3]
        self.paths_readonly_btn_4 = self.paths_readonly_btn_var[4]
        self.paths_readonly_btn_5 = self.paths_readonly_btn_var[5]
        # Sector 1: Loading 0
        self.loading_lbl_0 = QLabel(self)
        self.loading_lbl_0.move(back_label_ankor_w0 + back_label_buffer, (back_label_ankor_h0 + back_label_buffer + btnx_h + btnx_buffer_0 + self.title_lable_h_0 + 5))
        self.loading_lbl_0.resize(87, 8)
        self.loading_lbl_0.setStyleSheet(self.default_loading)
        self.loading_lbl_0.hide()
        # Sector 1: Loading 1
        self.loading_lbl_1 = QLabel(self)
        self.loading_lbl_1.move(back_label_ankor_w1 + back_label_buffer, (back_label_ankor_h1 + back_label_buffer + btnx_h + btnx_buffer_0 + self.title_lable_h_0 + 5))
        self.loading_lbl_1.resize(87, 8)
        self.loading_lbl_1.setStyleSheet(self.default_loading)
        self.loading_lbl_1.hide()
        # Sector 1: Loading 2
        self.loading_lbl_2 = QLabel(self)
        self.loading_lbl_2.move(back_label_ankor_w2 + back_label_buffer, (back_label_ankor_h2 + back_label_buffer + btnx_h + btnx_buffer_0 + self.title_lable_h_0 + 5))
        self.loading_lbl_2.resize(87, 8)
        self.loading_lbl_2.setStyleSheet(self.default_loading)
        self.loading_lbl_2.hide()
        # Sector 1: Loading 3
        self.loading_lbl_3 = QLabel(self)
        self.loading_lbl_3.move(back_label_ankor_w3 + back_label_buffer, (back_label_ankor_h3 + back_label_buffer + btnx_h + btnx_buffer_0 + self.title_lable_h_0 + 5))
        self.loading_lbl_3.resize(87, 8)
        self.loading_lbl_3.setStyleSheet(self.default_loading)
        self.loading_lbl_3.hide()
        # Sector 1: Loading 4
        self.loading_lbl_4 = QLabel(self)
        self.loading_lbl_4.move(back_label_ankor_w4 + back_label_buffer, (back_label_ankor_h4 + back_label_buffer + btnx_h + btnx_buffer_0 + self.title_lable_h_0 + 5))
        self.loading_lbl_4.resize(87, 8)
        self.loading_lbl_4.setStyleSheet(self.default_loading)
        self.loading_lbl_4.hide()
        # Sector 1: Loading 5
        self.loading_lbl_5 = QLabel(self)
        self.loading_lbl_5.move(back_label_ankor_w5 + back_label_buffer, (back_label_ankor_h5 + back_label_buffer + btnx_h + btnx_buffer_0 + self.title_lable_h_0 + 5))
        self.loading_lbl_5.resize(87, 8)
        self.loading_lbl_5.setStyleSheet(self.default_loading)
        self.loading_lbl_5.hide()
        # Sector 2: Settings Page Left
        self.scr_left = QPushButton(self)
        self.scr_left.resize(5, 35)
        self.scr_left.move(5, 126)
        self.scr_left.setIcon(QIcon(self.img_menu_left))
        self.scr_left.setIconSize(QSize(15, 35))
        self.scr_left.clicked.connect(self.scr_left_funk)
        self.scr_left.setStyleSheet(self.default_qpbtn_page_switch_style)
        # Sector 2: Settings Page Right
        self.scr_right = QPushButton(self)
        self.scr_right.resize(5, 35)
        self.scr_right.move((self.width - 10), 126)
        self.scr_right.setIcon(QIcon(self.img_menu_right))
        self.scr_right.setIconSize(QSize(15, 35))
        self.scr_right.clicked.connect(self.scr_right_funk)
        self.scr_right.setStyleSheet(self.default_qpbtn_page_switch_style)
        # Sector 2: A Label To Signify Source Path Configuration
        self.settings_source_label = QLabel(self)
        self.settings_source_label.move(15, user_paths_ankor_h)
        self.settings_source_label.resize(87, 15)
        self.settings_source_label.setFont(self.font_s6b)
        self.settings_source_label.setText('Source:')
        self.settings_source_label.setStyleSheet(self.default_qlbl_highlight)
        self.settings_source_label.setAlignment(Qt.AlignCenter) 
        # Sector 2: A Label To Signify Destination Path Configuration
        self.settings_dest_label = QLabel(self)
        self.settings_dest_label.move(15, user_paths_ankor_h + source_dest_h + source_dest_buffer_h)
        self.settings_dest_label.resize(self.title_lable_w_0, self.title_lable_h_0)
        self.settings_dest_label.setFont(self.font_s6b)
        self.settings_dest_label.setText('Destination:')
        self.settings_dest_label.setStyleSheet(self.default_qlbl_highlight)
        self.settings_dest_label.setAlignment(Qt.AlignCenter) 
        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 0
        self.setting_title0 = QPushButton(self)
        self.setting_title0.resize(self.title_lable_w_0, self.title_lable_h_0)
        self.setting_title0.move((back_label_ankor_w0 + back_label_buffer), (back_label_ankor_h0 + back_label_buffer + btnx_h + btnx_buffer_0))
        self.setting_title0.setFont(self.font_s6b)
        self.setting_title0.setText("")
        self.setting_title0.setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var.append(self.setting_title0)
        self.setting_title0.show()
        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 1
        self.setting_title1 = QPushButton(self)
        self.setting_title1.resize(self.title_lable_w_0, self.title_lable_h_0)
        self.setting_title1.move((back_label_ankor_w1 + back_label_buffer), (back_label_ankor_h1 + back_label_buffer + btnx_h + btnx_buffer_0))
        self.setting_title1.setFont(self.font_s6b)
        self.setting_title1.setText("")
        self.setting_title1.setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var.append(self.setting_title1)
        self.setting_title1.show()
        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 2
        self.setting_title2 = QPushButton(self)
        self.setting_title2.resize(self.title_lable_w_0, self.title_lable_h_0)
        self.setting_title2.move((back_label_ankor_w2 + back_label_buffer), (back_label_ankor_h2 + back_label_buffer + btnx_h + btnx_buffer_0))
        self.setting_title2.setFont(self.font_s6b)
        self.setting_title2.setText("")
        self.setting_title2.setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var.append(self.setting_title2)
        self.setting_title2.show()
        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 3
        self.setting_title3 = QPushButton(self)
        self.setting_title3.resize(self.title_lable_w_0, self.title_lable_h_0)
        self.setting_title3.move((back_label_ankor_w3 + back_label_buffer), (back_label_ankor_h3 + back_label_buffer + btnx_h + btnx_buffer_0))
        self.setting_title3.setFont(self.font_s6b)
        self.setting_title3.setText("")
        self.setting_title3.setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var.append(self.setting_title3)
        self.setting_title3.show()
        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 4
        self.setting_title4 = QPushButton(self)
        self.setting_title4.resize(self.title_lable_w_0, self.title_lable_h_0)
        self.setting_title4.move((back_label_ankor_w4 + back_label_buffer), (back_label_ankor_h4 + back_label_buffer + btnx_h + btnx_buffer_0))
        self.setting_title4.setFont(self.font_s6b)
        self.setting_title4.setText("")
        self.setting_title4.setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var.append(self.setting_title4)
        self.setting_title4.show()
        # Sector 2: Title Lable Signifies Which Path Is Displayed To Be Configured 5
        self.setting_title5 = QPushButton(self)
        self.setting_title5.resize(self.title_lable_w_0, self.title_lable_h_0)
        self.setting_title5.move((back_label_ankor_w5 + back_label_buffer), (back_label_ankor_h5 + back_label_buffer + btnx_h + btnx_buffer_0))
        self.setting_title5.setFont(self.font_s6b)
        self.setting_title5.setText("")
        self.setting_title5.setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var.append(self.setting_title5)
        self.setting_title5.show()
        # Sector 1: Title Label QLine Edits Which Title Is Displayed 0
        self.setting_title_B_0 = QLineEdit(self)
        self.setting_title_B_0.resize(self.title_lable_w_0, self.title_lable_h_0)
        self.setting_title_B_0.move((back_label_ankor_w0 + back_label_buffer), (back_label_ankor_h0 + back_label_buffer + btnx_h + btnx_buffer_0))
        self.setting_title_B_0.setFont(self.font_s6b)
        self.setting_title_B_0.setText('')
        self.setting_title_B_0.setReadOnly(False)
        self.setting_title_B_0.returnPressed.connect(self.setting_title_B_funk)
        self.setting_title_B_0.setStyleSheet(self.default_qle_highlight_1)
        self.setting_title_B_var.append(self.setting_title_B_0)
        self.setting_title_B_var[0].hide()
        # Sector 1: Title Label QLine Edits Which Title Is Displayed 0
        self.setting_title_B_1 = QLineEdit(self)
        self.setting_title_B_1.resize(self.title_lable_w_0, self.title_lable_h_0)
        self.setting_title_B_1.move((back_label_ankor_w1 + back_label_buffer), (back_label_ankor_h1 + back_label_buffer + btnx_h + btnx_buffer_0))
        self.setting_title_B_1.setFont(self.font_s6b)
        self.setting_title_B_1.setText('')
        self.setting_title_B_1.setReadOnly(False)
        self.setting_title_B_1.returnPressed.connect(self.setting_title_B_funk)
        self.setting_title_B_1.setStyleSheet(self.default_qle_highlight_1)
        self.setting_title_B_var.append(self.setting_title_B_1)
        self.setting_title_B_var[1].hide()
        # Sector 1: Title Label QLine Edits Which Title Is Displayed 0
        self.setting_title_B_2 = QLineEdit(self)
        self.setting_title_B_2.resize(self.title_lable_w_0, self.title_lable_h_0)
        self.setting_title_B_2.move((back_label_ankor_w2 + back_label_buffer), (back_label_ankor_h2 + back_label_buffer + btnx_h + btnx_buffer_0))
        self.setting_title_B_2.setFont(self.font_s6b)
        self.setting_title_B_2.setText('')
        self.setting_title_B_2.setReadOnly(False)
        self.setting_title_B_2.returnPressed.connect(self.setting_title_B_funk)
        self.setting_title_B_2.setStyleSheet(self.default_qle_highlight_1)
        self.setting_title_B_var.append(self.setting_title_B_2)
        self.setting_title_B_var[2].hide()
        # Sector 1: Title Label QLine Edits Which Title Is Displayed 0
        self.setting_title_B_3 = QLineEdit(self)
        self.setting_title_B_3.resize(self.title_lable_w_0, self.title_lable_h_0)
        self.setting_title_B_3.move((back_label_ankor_w3 + back_label_buffer), (back_label_ankor_h3 + back_label_buffer + btnx_h + btnx_buffer_0))
        self.setting_title_B_3.setFont(self.font_s6b)
        self.setting_title_B_3.setText('')
        self.setting_title_B_3.setReadOnly(False)
        self.setting_title_B_3.returnPressed.connect(self.setting_title_B_funk)
        self.setting_title_B_3.setStyleSheet(self.default_qle_highlight_1)
        self.setting_title_B_var.append(self.setting_title_B_3)
        self.setting_title_B_var[3].hide()
        # Sector 1: Title Label QLine Edits Which Title Is Displayed 0
        self.setting_title_B_4 = QLineEdit(self)
        self.setting_title_B_4.resize(self.title_lable_w_0, self.title_lable_h_0)
        self.setting_title_B_4.move((back_label_ankor_w4 + back_label_buffer), (back_label_ankor_h4 + back_label_buffer + btnx_h + btnx_buffer_0))
        self.setting_title_B_4.setFont(self.font_s6b)
        self.setting_title_B_4.setText('')
        self.setting_title_B_4.setReadOnly(False)
        self.setting_title_B_4.returnPressed.connect(self.setting_title_B_funk)
        self.setting_title_B_4.setStyleSheet(self.default_qle_highlight_1)
        self.setting_title_B_var.append(self.setting_title_B_4)
        self.setting_title_B_var[4].hide()
        # Sector 1: Title Label QLine Edits Which Title Is Displayed 0
        self.setting_title_B_5 = QLineEdit(self)
        self.setting_title_B_5.resize(self.title_lable_w_0, self.title_lable_h_0)
        self.setting_title_B_5.move((back_label_ankor_w5 + back_label_buffer), (back_label_ankor_h5 + back_label_buffer + btnx_h + btnx_buffer_0))
        self.setting_title_B_5.setFont(self.font_s6b)
        self.setting_title_B_5.setText('')
        self.setting_title_B_5.setReadOnly(False)
        self.setting_title_B_5.returnPressed.connect(self.setting_title_B_funk)
        self.setting_title_B_5.setStyleSheet(self.default_qle_highlight_1)
        self.setting_title_B_var.append(self.setting_title_B_5)
        self.setting_title_B_var[5].hide()
        # Sector 2: Source Path Configuration Edit 0
        self.settings_source0 = QLineEdit(self)
        self.settings_source0.move(user_paths_ankor_w, user_paths_ankor_h)
        self.settings_source0.resize(source_dest_w, source_dest_h)
        self.settings_source0.setFont(self.font_s6b)
        self.settings_source0.setText(path_var[0])
        self.settings_source0.setReadOnly(True)
        self.settings_source0.returnPressed.connect(self.settings_source_pre_funk0)
        self.settings_source0.setStyleSheet(self.default_qle_highlight_0)
        self.settings_source_edit_var.append(self.settings_source0)
        self.settings_source_edit_var[0].show()
        # Sector 2: Source Path Configuration Edit 1
        self.settings_source1 = QLineEdit(self)
        self.settings_source1.move(user_paths_ankor_w, user_paths_ankor_h)
        self.settings_source1.resize(source_dest_w, source_dest_h)
        self.settings_source1.setFont(self.font_s6b)
        self.settings_source1.setText(path_var[1])
        self.settings_source1.setReadOnly(True)
        self.settings_source1.returnPressed.connect(self.settings_source_pre_funk1)
        self.settings_source1.setStyleSheet(self.default_qle_style)
        self.settings_source_edit_var.append(self.settings_source1)
        self.settings_source_edit_var[1].hide()
        # Sector 2: Source Path Configuration Edit 2
        self.settings_source2 = QLineEdit(self)
        self.settings_source2.move(user_paths_ankor_w, user_paths_ankor_h)
        self.settings_source2.resize(source_dest_w, source_dest_h)
        self.settings_source2.setFont(self.font_s6b)
        self.settings_source2.setText(path_var[2])
        self.settings_source2.setReadOnly(True)
        self.settings_source2.returnPressed.connect(self.settings_source_pre_funk2)
        self.settings_source2.setStyleSheet(self.default_qle_style)
        self.settings_source_edit_var.append(self.settings_source2)
        self.settings_source_edit_var[2].hide()
        # Sector 2: Source Path Configuration Edit 3
        self.settings_source3 = QLineEdit(self)
        self.settings_source3.move(user_paths_ankor_w, user_paths_ankor_h)
        self.settings_source3.resize(source_dest_w, source_dest_h)
        self.settings_source3.setFont(self.font_s6b)
        self.settings_source3.setText(path_var[3])
        self.settings_source3.setReadOnly(True)
        self.settings_source3.returnPressed.connect(self.settings_source_pre_funk3)
        self.settings_source3.setStyleSheet(self.default_qle_style)
        self.settings_source_edit_var.append(self.settings_source3)
        self.settings_source_edit_var[3].hide()
        # Sector 2: Source Path Configuration Edit 4
        self.settings_source4 = QLineEdit(self)
        self.settings_source4.move(user_paths_ankor_w, user_paths_ankor_h)
        self.settings_source4.resize(source_dest_w, source_dest_h)
        self.settings_source4.setFont(self.font_s6b)
        self.settings_source4.setText(path_var[4])
        self.settings_source4.setReadOnly(True)
        self.settings_source4.returnPressed.connect(self.settings_source_pre_funk4)
        self.settings_source4.setStyleSheet(self.default_qle_style)
        self.settings_source_edit_var.append(self.settings_source4)
        self.settings_source_edit_var[4].hide()
        # Sector 2: Source Path Configuration Edit 5
        self.settings_source5 = QLineEdit(self)
        self.settings_source5.move(user_paths_ankor_w, user_paths_ankor_h)
        self.settings_source5.resize(source_dest_w, source_dest_h)
        self.settings_source5.setFont(self.font_s6b)
        self.settings_source5.setText(path_var[5])
        self.settings_source5.setReadOnly(True)
        self.settings_source5.returnPressed.connect(self.settings_source_pre_funk5)
        self.settings_source5.setStyleSheet(self.default_qle_style)
        self.settings_source_edit_var.append(self.settings_source5)
        self.settings_source_edit_var[5].hide()
        # Sector 2: Destination Path Configuration Edit 0  source_dest_buffer_h
        self.settings_dest0 = QLineEdit(self)
        self.settings_dest0.move(user_paths_ankor_w, user_paths_ankor_h + source_dest_h + source_dest_buffer_h)
        self.settings_dest0.resize(source_dest_w, 15)
        self.settings_dest0.setFont(self.font_s6b)
        self.settings_dest0.setText(dest_path_var[0])
        self.settings_dest0.setReadOnly(True)
        self.settings_dest0.returnPressed.connect(self.settings_dest_pre_funk0)
        self.settings_dest0.setStyleSheet(self.default_qle_highlight_0)
        self.settings_dest_edit_var.append(self.settings_dest0)
        self.settings_dest_edit_var[0].show()
        # Sector 2: Destination Path Configuration Edit 1
        self.settings_dest1 = QLineEdit(self)
        self.settings_dest1.move(user_paths_ankor_w, user_paths_ankor_h + source_dest_h + source_dest_buffer_h)
        self.settings_dest1.resize(source_dest_w, 15)
        self.settings_dest1.setFont(self.font_s6b)
        self.settings_dest1.setText(dest_path_var[1])
        self.settings_dest1.setReadOnly(True)
        self.settings_dest1.returnPressed.connect(self.settings_dest_pre_funk1)
        self.settings_dest1.setStyleSheet(self.default_qle_style)
        self.settings_dest_edit_var.append(self.settings_dest1)
        self.settings_dest_edit_var[1].hide()
        # Sector 2: Destination Path Configuration Edit 2
        self.settings_dest2 = QLineEdit(self)
        self.settings_dest2.move(user_paths_ankor_w, user_paths_ankor_h + source_dest_h + source_dest_buffer_h)
        self.settings_dest2.resize(source_dest_w, 15)
        self.settings_dest2.setFont(self.font_s6b)
        self.settings_dest2.setText(dest_path_var[2])
        self.settings_dest2.setReadOnly(True)
        self.settings_dest2.returnPressed.connect(self.settings_dest_pre_funk2)
        self.settings_dest2.setStyleSheet(self.default_qle_style)
        self.settings_dest_edit_var.append(self.settings_dest2)
        self.settings_dest_edit_var[2].hide()
        # Sector 2: Destination Path Configuration Edit 3
        self.settings_dest3 = QLineEdit(self)
        self.settings_dest3.move(user_paths_ankor_w, user_paths_ankor_h + source_dest_h + source_dest_buffer_h)
        self.settings_dest3.resize(source_dest_w, 15)
        self.settings_dest3.setFont(self.font_s6b)
        self.settings_dest3.setText(dest_path_var[3])
        self.settings_dest3.setReadOnly(True)
        self.settings_dest3.returnPressed.connect(self.settings_dest_pre_funk3)
        self.settings_dest3.setStyleSheet(self.default_qle_style)
        self.settings_dest_edit_var.append(self.settings_dest3)
        self.settings_dest_edit_var[3].hide()
        # Sector 2: Destination Path Configuration Edit 4
        self.settings_dest4 = QLineEdit(self)
        self.settings_dest4.move(user_paths_ankor_w, user_paths_ankor_h + source_dest_h + source_dest_buffer_h)
        self.settings_dest4.resize(source_dest_w, 15)
        self.settings_dest4.setFont(self.font_s6b)
        self.settings_dest4.setText(dest_path_var[4])
        self.settings_dest4.setReadOnly(True)
        self.settings_dest4.returnPressed.connect(self.settings_dest_pre_funk4)
        self.settings_dest4.setStyleSheet(self.default_qle_style)
        self.settings_dest_edit_var.append(self.settings_dest4)
        self.settings_dest_edit_var[4].hide()
        # Sector 2: Destination Path Configuration Edit 5
        self.settings_dest5 = QLineEdit(self)
        self.settings_dest5.move(user_paths_ankor_w, user_paths_ankor_h + source_dest_h + source_dest_buffer_h)
        self.settings_dest5.resize(source_dest_w, 15)
        self.settings_dest5.setFont(self.font_s6b)
        self.settings_dest5.setText(dest_path_var[5])
        self.settings_dest5.setReadOnly(True)
        self.settings_dest5.returnPressed.connect(self.settings_dest_pre_funk5)
        self.settings_dest5.setStyleSheet(self.default_qle_style)
        self.settings_dest_edit_var.append(self.settings_dest5)
        self.settings_dest_edit_var[5].hide()
        # Sector 2: File Path Validation LED Source
        self.settings_input_response_label_src = QLabel(self)
        self.settings_input_response_label_src.move((user_paths_ankor_w + source_dest_w + 5), user_paths_ankor_h)
        self.settings_input_response_label_src.resize(5, 15)
        self.settings_input_response_label_src.setStyleSheet(self.default_valid_path_led)
        # Sector 2: File Path Validation LED Destination
        self.settings_input_response_label_dst = QLabel(self)
        self.settings_input_response_label_dst.move((user_paths_ankor_w + source_dest_w + 5), user_paths_ankor_h + source_dest_h + source_dest_buffer_h)
        self.settings_input_response_label_dst.resize(5, 15)
        self.settings_input_response_label_dst.setStyleSheet(self.default_valid_path_led)
         # Sector 1: Main Function Confirmation 0
        self.confirm_op0_tru = QPushButton(self)
        self.confirm_op0_tru.resize(confirm_op_w, confirm_op_h)
        self.confirm_op0_tru.setIcon(QIcon(self.img_execute_false))
        self.confirm_op0_tru.setIconSize(QSize(45, 10))
        self.confirm_op0_tru.setStyleSheet(self.default_qpbtn_style)
        self.confirm_op0_tru.clicked.connect(self.confirm_op0_funk0)
        self.confirm_op0_tru.setEnabled(False)
        self.confirm_op0_tru.show()
        self.confirm_op_var.append(self.confirm_op0_tru)
        # Sector 1: Main Function Confirmation 1
        self.confirm_op1_tru = QPushButton(self)
        self.confirm_op1_tru.resize(confirm_op_w, confirm_op_h)
        self.confirm_op1_tru.setIcon(QIcon(self.img_execute_false))
        self.confirm_op1_tru.setIconSize(QSize(45, 10))
        self.confirm_op1_tru.setStyleSheet(self.default_qpbtn_style)
        self.confirm_op1_tru.clicked.connect(self.confirm_op1_funk0)
        self.confirm_op1_tru.setEnabled(False)
        self.confirm_op1_tru.show()
        self.confirm_op_var.append(self.confirm_op1_tru)
        # Sector 1: Main Function Confirmation 2
        self.confirm_op2_tru = QPushButton(self)
        self.confirm_op2_tru.resize(confirm_op_w, confirm_op_h)
        self.confirm_op2_tru.setIcon(QIcon(self.img_execute_false))
        self.confirm_op2_tru.setIconSize(QSize(45, 10))
        self.confirm_op2_tru.setStyleSheet(self.default_qpbtn_style)
        self.confirm_op2_tru.clicked.connect(self.confirm_op2_funk0)
        self.confirm_op2_tru.setEnabled(False)
        self.confirm_op2_tru.show()
        self.confirm_op_var.append(self.confirm_op2_tru)
        # Sector 1: Main Function Confirmation 3
        self.confirm_op3_tru = QPushButton(self)
        self.confirm_op3_tru.resize(confirm_op_w, confirm_op_h)
        self.confirm_op3_tru.setIcon(QIcon(self.img_execute_false))
        self.confirm_op3_tru.setIconSize(QSize(45, 10))
        self.confirm_op3_tru.setStyleSheet(self.default_qpbtn_style)
        self.confirm_op3_tru.clicked.connect(self.confirm_op3_funk0)
        self.confirm_op3_tru.setEnabled(False)
        self.confirm_op3_tru.show()
        self.confirm_op_var.append(self.confirm_op3_tru)
        # Sector 1: Main Function Confirmation 4
        self.confirm_op4_tru = QPushButton(self)
        self.confirm_op4_tru.resize(confirm_op_w, confirm_op_h)
        self.confirm_op4_tru.setIcon(QIcon(self.img_execute_false))
        self.confirm_op4_tru.setIconSize(QSize(45, 10))
        self.confirm_op4_tru.setStyleSheet(self.default_qpbtn_style)
        self.confirm_op4_tru.clicked.connect(self.confirm_op4_funk0)
        self.confirm_op4_tru.setEnabled(False)
        self.confirm_op4_tru.show()
        self.confirm_op_var.append(self.confirm_op4_tru)
        # Sector 1: Main Function Confirmation 5
        self.confirm_op5_tru = QPushButton(self)
        self.confirm_op5_tru.resize(confirm_op_w, confirm_op_h)
        self.confirm_op5_tru.setIcon(QIcon(self.img_execute_false))
        self.confirm_op5_tru.setIconSize(QSize(45, 10))
        self.confirm_op5_tru.setStyleSheet(self.default_qpbtn_style)
        self.confirm_op5_tru.clicked.connect(self.confirm_op5_funk0)
        self.confirm_op5_tru.setEnabled(False)
        self.confirm_op5_tru.show()
        self.confirm_op_var.append(self.confirm_op5_tru)
        # Sector 3: Output Text Browser Label 0
        self.tb_label_0 = QLabel(self)
        self.tb_label_0.move(5, (self.tb_pos_h - 14))
        self.tb_label_0.resize(124, 14)
        self.tb_label_0.setFont(self.font_s6b)
        self.tb_label_0.setStyleSheet(self.default_qlbl_highlight)
        self.tb_label_0.setAlignment(Qt.AlignCenter)
        self.tb_label_0.show()
        # Sector 3: Output Text Browser 0
        self.tb_0 = QTextBrowser(self)
        self.tb_0.move(self.tb_pos_w, self.tb_pos_h)
        self.tb_0.resize(self.tb_w, self.tb_h)
        self.tb_0.setFont(self.font_s6b)
        self.tb_0.setObjectName("tb_0")
        self.tb_0.setStyleSheet(self.default_qtbb_style)
        self.tb_0.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_0.horizontalScrollBar().setValue(0)
        self.tb_var.append(self.tb_0)
        self.tb_var[0].show()
        # Sector 3: Output Text Browser 1
        self.tb_1 = QTextBrowser(self)
        self.tb_1.move(self.tb_pos_w, self.tb_pos_h)
        self.tb_1.resize(self.tb_w, self.tb_h)
        self.tb_1.setFont(self.font_s6b)
        self.tb_1.setObjectName("tb_1")
        self.tb_1.setStyleSheet(self.default_qtbb_style)
        self.tb_1.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_1.horizontalScrollBar().setValue(0)
        self.tb_var.append(self.tb_1)
        self.tb_var[1].hide()
        # Sector 3: Output Text Browser 2
        self.tb_2 = QTextBrowser(self)
        self.tb_2.move(self.tb_pos_w, self.tb_pos_h)
        self.tb_2.resize(self.tb_w, self.tb_h)
        self.tb_2.setFont(self.font_s6b)
        self.tb_2.setObjectName("tb_2")
        self.tb_2.setStyleSheet(self.default_qtbb_style)
        self.tb_2.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_2.horizontalScrollBar().setValue(0)
        self.tb_var.append(self.tb_2)
        self.tb_var[2].hide()
        # Sector 3: Output Text Browser 3
        self.tb_3 = QTextBrowser(self)
        self.tb_3.move(self.tb_pos_w, self.tb_pos_h)
        self.tb_3.resize(self.tb_w, self.tb_h)
        self.tb_3.setFont(self.font_s6b)
        self.tb_3.setObjectName("tb_3")
        self.tb_3.setStyleSheet(self.default_qtbb_style)
        self.tb_3.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_3.horizontalScrollBar().setValue(0)
        self.tb_var.append(self.tb_3)
        self.tb_var[3].hide()
        # Sector 3: Output Text Browser 4
        self.tb_4 = QTextBrowser(self)
        self.tb_4.move(self.tb_pos_w, self.tb_pos_h)
        self.tb_4.resize(self.tb_w, self.tb_h)
        self.tb_4.setFont(self.font_s6b)
        self.tb_4.setObjectName("tb_4")
        self.tb_4.setStyleSheet(self.default_qtbb_style)
        self.tb_4.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_4.horizontalScrollBar().setValue(0)
        self.tb_var.append(self.tb_4)
        self.tb_var[4].hide()
        # Sector 3: Output Text Browser 5
        self.tb_5 = QTextBrowser(self)
        self.tb_5.move(self.tb_pos_w, self.tb_pos_h)
        self.tb_5.resize(self.tb_w, self.tb_h)
        self.tb_5.setFont(self.font_s6b)
        self.tb_5.setObjectName("tb_5")
        self.tb_5.setStyleSheet(self.default_qtbb_style)
        self.tb_5.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_5.horizontalScrollBar().setValue(0)
        self.tb_var.append(self.tb_5)
        self.tb_var[5].hide()
        # Sector 1: Attatch Main Function Buttons To Background Tiles Position
        self.btnx_main_0.move((back_label_ankor_w0 + back_label_buffer), (back_label_ankor_h0 + 5))
        self.btnx_main_1.move((back_label_ankor_w1 + back_label_buffer), (back_label_ankor_h1 + 5))
        self.btnx_main_2.move((back_label_ankor_w2 + back_label_buffer), (back_label_ankor_h2 + 5))
        self.btnx_main_3.move((back_label_ankor_w3 + back_label_buffer), (back_label_ankor_h3 + 5))
        self.btnx_main_4.move((back_label_ankor_w4 + back_label_buffer), (back_label_ankor_h4 + 5))
        self.btnx_main_5.move((back_label_ankor_w5 + back_label_buffer), (back_label_ankor_h5 + 5))
        # Sector 1: Attatch Drop Down Settings Buttons To Background Tiles Position
        self.confirm_op0_tru.move((back_label_ankor_w0 + 63), (back_label_ankor_h0 + 49))
        self.confirm_op1_tru.move((back_label_ankor_w1 + 63), (back_label_ankor_h1 + 49))
        self.confirm_op2_tru.move((back_label_ankor_w2 + 63), (back_label_ankor_h2 + 49))
        self.confirm_op3_tru.move((back_label_ankor_w3 + 63), (back_label_ankor_h3 + 49))
        self.confirm_op4_tru.move((back_label_ankor_w4 + 63), (back_label_ankor_h4 + 49))
        self.confirm_op5_tru.move((back_label_ankor_w5 + 63), (back_label_ankor_h5 + 49))
        # Sector 1: Attatch Main Function Mode Buttons To Background Tiles Position
        self.btnx_mode_btn_0.move((back_label_ankor_w0 + 63), (back_label_ankor_h0 + 19))
        self.btnx_mode_btn_1.move((back_label_ankor_w1 + 63), (back_label_ankor_h1 + 19))
        self.btnx_mode_btn_2.move((back_label_ankor_w2 + 63), (back_label_ankor_h2 + 19))
        self.btnx_mode_btn_3.move((back_label_ankor_w3 + 63), (back_label_ankor_h3 + 19))
        self.btnx_mode_btn_4.move((back_label_ankor_w4 + 63), (back_label_ankor_h4 + 19))
        self.btnx_mode_btn_5.move((back_label_ankor_w5 + 63), (back_label_ankor_h5 + 19))
        # Sector 1: Attatch Stop Main Function Buttons To Background Tiles Position
        self.stop_thread_btn_0.move((back_label_ankor_w0 + 63), (back_label_ankor_h0 + 5))
        self.stop_thread_btn_1.move((back_label_ankor_w1 + 63), (back_label_ankor_h1 + 5))
        self.stop_thread_btn_2.move((back_label_ankor_w2 + 63), (back_label_ankor_h2 + 5))
        self.stop_thread_btn_3.move((back_label_ankor_w3 + 63), (back_label_ankor_h3 + 5))
        self.stop_thread_btn_4.move((back_label_ankor_w4 + 63), (back_label_ankor_h4 + 5))
        self.stop_thread_btn_5.move((back_label_ankor_w5 + 63), (back_label_ankor_h5 + 5))
        # Sector 1: Plug Main Function Mode Buttons Into Functions
        self.btnx_mode_btn_0.clicked.connect(self.set_comp_bool_pre_funk0)
        self.btnx_mode_btn_1.clicked.connect(self.set_comp_bool_pre_funk1)
        self.btnx_mode_btn_2.clicked.connect(self.set_comp_bool_pre_funk2)
        self.btnx_mode_btn_3.clicked.connect(self.set_comp_bool_pre_funk3)
        self.btnx_mode_btn_4.clicked.connect(self.set_comp_bool_pre_funk4)
        self.btnx_mode_btn_5.clicked.connect(self.set_comp_bool_pre_funk5)
        # Sector 1: Plug Stop Main Function Buttons Into Functions
        self.stop_thread_btn_0.clicked.connect(self.stop_thr_funk0)
        self.stop_thread_btn_1.clicked.connect(self.stop_thr_funk1)
        self.stop_thread_btn_2.clicked.connect(self.stop_thr_funk2)
        self.stop_thread_btn_3.clicked.connect(self.stop_thr_funk3)
        self.stop_thread_btn_4.clicked.connect(self.stop_thr_funk4)
        self.stop_thread_btn_5.clicked.connect(self.stop_thr_funk5)
        # Sector 1: Plug Main Function Buttons Into Main Function Button Threads
        self.btnx_main_0.clicked.connect(self.thread_funk_0)
        self.btnx_main_1.clicked.connect(self.thread_funk_1)
        self.btnx_main_2.clicked.connect(self.thread_funk_2)
        self.btnx_main_3.clicked.connect(self.thread_funk_3)
        self.btnx_main_4.clicked.connect(self.thread_funk_4)
        self.btnx_main_5.clicked.connect(self.thread_funk_5)
        # Sector 1: Plug Main Function Buttons Into Drop Down Settings Functions
        self.btnx_main_0.clicked.connect(self.btnx_set_focus_pre_funk_0)
        self.btnx_main_1.clicked.connect(self.btnx_set_focus_pre_funk_1)
        self.btnx_main_2.clicked.connect(self.btnx_set_focus_pre_funk_2)
        self.btnx_main_3.clicked.connect(self.btnx_set_focus_pre_funk_3)
        self.btnx_main_4.clicked.connect(self.btnx_set_focus_pre_funk_4)
        self.btnx_main_5.clicked.connect(self.btnx_set_focus_pre_funk_5)
        # Sector 2: Plug Read Only Buttons Into Read Only Functions
        self.paths_readonly_btn_0.clicked.connect(self.paths_readonly_button_pre_funk_0)
        self.paths_readonly_btn_1.clicked.connect(self.paths_readonly_button_pre_funk_1)
        self.paths_readonly_btn_2.clicked.connect(self.paths_readonly_button_pre_funk_2)
        self.paths_readonly_btn_3.clicked.connect(self.paths_readonly_button_pre_funk_3)
        self.paths_readonly_btn_4.clicked.connect(self.paths_readonly_button_pre_funk_4)
        self.paths_readonly_btn_5.clicked.connect(self.paths_readonly_button_pre_funk_5)
        #Sector 2: Plug Settings Title Buttons Into Set Focus Pre-Functions
        self.setting_title0.clicked.connect(self.btnx_set_focus_pre_funk_0)
        self.setting_title1.clicked.connect(self.btnx_set_focus_pre_funk_1)
        self.setting_title2.clicked.connect(self.btnx_set_focus_pre_funk_2)
        self.setting_title3.clicked.connect(self.btnx_set_focus_pre_funk_3)
        self.setting_title4.clicked.connect(self.btnx_set_focus_pre_funk_4)
        self.setting_title5.clicked.connect(self.btnx_set_focus_pre_funk_5)
        # Thread: Adjusts App Geometry To Account For Display Re-Scaling
        scaling_thread = ScalingClass(self.setGeometry, self.width, self.height, self.pos)
        scaling_thread.start()
        # Thread: Main Function Thread - Read/Write Thread 0
        self.thread_0 = ThreadClass0(self.tb_0,
                                     self.confirm_op0_tru,
                                     self.img_btnx_led_0,
                                     self.img_btnx_led_1,
                                     self.img_btnx_led_2,
                                     self.img_execute_false,
                                     self.img_execute_true,
                                     self.img_stop_thread_false,
                                     self.img_stop_thread_true,
                                     self.output_verbosity,
                                     self.btnx_main_0,
                                     self.stop_thread_btn_0,
                                     self.paths_readonly_btn_0,
                                     self.cnfg_prof_btn_var,
                                     self.paths_readonly_btn_var,
                                     self.loading_lbl_0)
        # Thread: Main Function Thread - Read/Write Thread 1
        self.thread_1 = ThreadClass1(self.tb_1,
                                     self.confirm_op1_tru,
                                     self.img_btnx_led_0,
                                     self.img_btnx_led_1,
                                     self.img_btnx_led_2,
                                     self.img_execute_false,
                                     self.img_execute_true,
                                     self.img_stop_thread_false,
                                     self.img_stop_thread_true,
                                     self.output_verbosity,
                                     self.btnx_main_1,
                                     self.stop_thread_btn_1,
                                     self.paths_readonly_btn_1,
                                     self.cnfg_prof_btn_var,
                                     self.paths_readonly_btn_var,
                                     self.loading_lbl_1)
        # Thread: Main Function Thread - Read/Write Thread 2
        self.thread_2 = ThreadClass2(self.tb_2,
                                     self.confirm_op2_tru,
                                     self.img_btnx_led_0,
                                     self.img_btnx_led_1,
                                     self.img_btnx_led_2,
                                     self.img_execute_false,
                                     self.img_execute_true,
                                     self.img_stop_thread_false,
                                     self.img_stop_thread_true,
                                     self.output_verbosity,
                                     self.btnx_main_2,
                                     self.stop_thread_btn_2,
                                     self.paths_readonly_btn_2,
                                     self.cnfg_prof_btn_var,
                                     self.paths_readonly_btn_var,
                                     self.loading_lbl_2)
        # Thread: Main Function Thread - Read/Write Thread 3
        self.thread_3 = ThreadClass3(self.tb_3,
                                     self.confirm_op3_tru,
                                     self.img_btnx_led_0,
                                     self.img_btnx_led_1,
                                     self.img_btnx_led_2,
                                     self.img_execute_false,
                                     self.img_execute_true,
                                     self.img_stop_thread_false,
                                     self.img_stop_thread_true,
                                     self.output_verbosity,
                                     self.btnx_main_3,
                                     self.stop_thread_btn_3,
                                     self.paths_readonly_btn_3,
                                     self.cnfg_prof_btn_var,
                                     self.paths_readonly_btn_var,
                                     self.loading_lbl_3)
        # Thread: Main Function Thread - Read/Write Thread 4
        self.thread_4 = ThreadClass4(self.tb_4,
                                     self.confirm_op4_tru,
                                     self.img_btnx_led_0,
                                     self.img_btnx_led_1,
                                     self.img_btnx_led_2,
                                     self.img_execute_false,
                                     self.img_execute_true,
                                     self.img_stop_thread_false,
                                     self.img_stop_thread_true,
                                     self.output_verbosity,
                                     self.btnx_main_4,
                                     self.stop_thread_btn_4,
                                     self.paths_readonly_btn_4,
                                     self.cnfg_prof_btn_var,
                                     self.paths_readonly_btn_var,
                                     self.loading_lbl_4)
        # Thread: Main Function Thread - Read/Write Thread 5
        self.thread_5 = ThreadClass5(self.tb_5,
                                     self.confirm_op5_tru,
                                     self.img_btnx_led_0,
                                     self.img_btnx_led_1,
                                     self.img_btnx_led_2,
                                     self.img_execute_false,
                                     self.img_execute_true,
                                     self.img_stop_thread_false,
                                     self.img_stop_thread_true,
                                     self.output_verbosity,
                                     self.btnx_main_5,
                                     self.stop_thread_btn_5,
                                     self.paths_readonly_btn_5,
                                     self.cnfg_prof_btn_var,
                                     self.paths_readonly_btn_var,
                                     self.loading_lbl_5)
        # Thread: LEDs In Sector 2 Indicate Source & Destination Path Validity
        self.settings_input_response_thread = SettingsInputResponse(self.default_valid_path_led_green,
                                                               self.default_valid_path_led_red,
                                                               self.default_valid_path_led,
                                                               self.settings_input_response_label_src,
                                                               self.settings_input_response_label_dst)
        # Thread: Checks The Validity Of Directory Paths Set In Sector 2 As Source & Destination And Updates GUI Accordingly
        self.update_settings_window_thread = UpdateSettingsWindow(self.settings_source_edit_var,
                                                                  self.settings_dest_edit_var,
                                                                  self.settings_title_var,
                                                                  self.tb_label_0,
                                                                  self.thread_0,
                                                                  self.thread_1,
                                                                  self.thread_2,
                                                                  self.thread_3,
                                                                  self.thread_4,
                                                                  self.thread_5)
        self.update_settings_window_thread.start()
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
        try:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
            if debug_enabled is True:
                print(self.oldPos)
        except Exception as e:
            if debug_enabled is True:
                print('-- exception:', str(e).strip().encode('utf-8'))

    # Function: Sets StyleSheets And Window Pallette
    def set_style_sheet_funk(self):
        global debug_enabled
        if debug_enabled is True:
            if debug_enabled is True:
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
           border:2px solid rgb(15, 15, 15);}"""

        # Default Stylesheet: Loading
        self.default_loading = """QLabel {background-color: rgb(0, 0, 200);
           border-top:2px solid rgb(0, 0, 0);
           border-bottom:2px solid rgb(0, 0, 0);
           border-left:0px solid rgb(0, 0, 0);
           border-right:0px solid rgb(0, 0, 0);}"""

        # Default Stylesheet: Valid Source Path LED Green
        self.default_valid_path_led_green = """QLabel {background-color: rgb(0, 255, 0);
           border:2px solid rgb(35, 35, 35);}"""

        # Default Stylesheet: Valid Source Path LED Red
        self.default_valid_path_led_red = """QLabel {background-color: rgb(255, 0, 0);
           border:2px solid rgb(35, 35, 35);}"""

        # Default StyleSheet: Title Configuration Profiles QPushButtons
        self.default_title_config_prof_qpbtn_style = """QPushButton{background-color: rgb(0, 0, 0);
               color: grey;
               border:0px solid rgb(0, 0, 0);
               border-bottom:0px solid rgb(0, 0, 0)}"""

        # Default StyleSheet: Title Configuration Profiles QPushButtons
        self.default_title_config_prof_qpbtn_style_1 = """QPushButton{background-color: rgb(0, 0, 0);
               color: rgb(0, 255, 0);
               border:0px solid rgb(0, 0, 0);
               border-bottom:0px solid rgb(0, 0, 0)}"""

        # Default StyleSheet: QPushButtons Pressed
        self.default_qpbtn_prsd_style = """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 0, 0);}"""

        # Default QPushButtons Page Left & Right
        self.default_qpbtn_page_switch_style = """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 0, 0);}"""

        # Default QLineEdit
        self.default_qle_style = """QLineEdit {background-color: rgb(30, 30, 30);
            border:0px solid rgb(0, 0, 0);
            selection-color: white;
            selection-background-color: rgb(0, 100, 255);
            color: grey;}"""

        # Default QLabels
        self.default_qlbl_style = """QLabel {background-color: rgb(30, 30, 30);
           color: grey;
           border:0px solid rgb(35, 35, 35);}"""

        # Default QPushButtons
        self.default_qpbtn_style = """QPushButton{background-color: rgb(30, 30, 30);
               border:0px solid rgb(0, 0, 0);}"""

        # Default QPushButton Text
        self.default_qpbtn_style_txt_0 = """QPushButton {background-color: rgb(30, 30, 30);
           text-align: center;
           color: grey;
           border:0px solid rgb(35, 35, 35);}"""

        # Default Highlighted QPushButton Text Highlight
        self.default_qpbtn_style_txt_1 = """QPushButton {background-color: rgb(30, 30, 30);
           text-align: center;
           color: white;
           border:0px solid rgb(35, 35, 35);}"""

        # Default Highlighted QLineEdit 
        self.default_qle_highlight_0 = """QLineEdit {background-color: rgb(30, 30, 30);
            border-top:0px solid rgb(30, 30, 200);
            selection-color: white;
            selection-background-color: rgb(0, 100, 255);
            color: white;}"""

        # Default Highlighted QLineEdit 
        self.default_qle_highlight_1 = """QLineEdit {background-color: rgb(30, 30, 30);
            border-top:0px solid rgb(30, 30, 200);
            selection-color: white;
            selection-background-color: rgb(0, 100, 255);
            color: white;}"""

        # Default Highlighted: QLabels
        self.default_qlbl_highlight = """QLabel {background-color: rgb(30, 30, 30);
           color: white;
           border:0px solid rgb(35, 35, 35);}"""

        # Default Highlighted QPushButton
        self.default_qpb_highlight = """QPushButton {background-color: rgb(30, 30, 30);
           color: white;
           border:0px solid rgb(35, 35, 35);}"""

        # Default Stylesheet: btnx_main
        self.default_btnx_main_style = """QPushButton{background-color: rgb(0, 0, 0);
                   border:2px solid rgb(30, 30, 30);}"""
        # Default Stylesheet: btnx_main
        self.default_btnx_main_style_1 = """QPushButton{background-color: rgb(0, 0, 0);
                   border:2px solid rgb(30, 30, 30);}"""
        
        # Default StyleSheet: QTextBoxBrowsers
        self.default_qtbb_style = """QTextBrowser {background-color: black;
            border-top:2px solid rgb(30, 30, 30);
            border-bottom:2px solid rgb(30, 30, 30);
            border-left:2px solid rgb(30, 30, 30);
            border-right:2px solid rgb(30, 30, 30);
            selection-color: white;
            selection-background-color: rgb(0, 100, 255);
            color: grey;}"""

    # Function: Concatinates Static Image Values With Variable Image Path
    def set_images_funk(self):
        if debug_enabled is True:
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

    def title_logo_btn_funk(self):
        if debug_enabled is True:
            print('-- plugged in: title_logo_btn_funk')

    def refresh_btn_funk(self):
        if debug_enabled is True:
            print('-- plugged in: refresh button')
        self.all_readonly()
        self.update_settings_window_thread.start()

    def all_readonly(self):
        self.settings_source_edit_var[0].setReadOnly(True)
        self.settings_source_edit_var[1].setReadOnly(True)
        self.settings_source_edit_var[2].setReadOnly(True)
        self.settings_source_edit_var[3].setReadOnly(True)
        self.settings_source_edit_var[4].setReadOnly(True)
        self.settings_source_edit_var[5].setReadOnly(True)

        self.settings_dest_edit_var[0].setReadOnly(True)
        self.settings_dest_edit_var[1].setReadOnly(True)
        self.settings_dest_edit_var[2].setReadOnly(True)
        self.settings_dest_edit_var[3].setReadOnly(True)
        self.settings_dest_edit_var[4].setReadOnly(True)
        self.settings_dest_edit_var[5].setReadOnly(True)

        self.paths_readonly_btn_0.setIcon(QIcon(self.img_read_ony_true))
        self.paths_readonly_btn_1.setIcon(QIcon(self.img_read_ony_true))
        self.paths_readonly_btn_2.setIcon(QIcon(self.img_read_ony_true))
        self.paths_readonly_btn_3.setIcon(QIcon(self.img_read_ony_true))
        self.paths_readonly_btn_4.setIcon(QIcon(self.img_read_ony_true))
        self.paths_readonly_btn_5.setIcon(QIcon(self.img_read_ony_true))
        self.paths_readonly_btn_0.setIconSize(QSize(8, 8))
        self.paths_readonly_btn_1.setIconSize(QSize(8, 8))
        self.paths_readonly_btn_2.setIconSize(QSize(8, 8))
        self.paths_readonly_btn_3.setIconSize(QSize(8, 8))
        self.paths_readonly_btn_4.setIconSize(QSize(8, 8))
        self.paths_readonly_btn_5.setIconSize(QSize(8, 8))

        self.setting_title_B_var[0].hide()
        self.setting_title_B_var[1].hide()
        self.setting_title_B_var[2].hide()
        self.setting_title_B_var[3].hide()
        self.setting_title_B_var[4].hide()
        self.setting_title_B_var[5].hide()

        self.show_settings_title()

    # self.cnfg_prof_btn_2.setStyleSheet(self.default_title_config_prof_qpbtn_style)
    def cnfg_prof_btn_style_funk_0(self):
        self.cnfg_prof_btn_0.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_1.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_2.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_3.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_4.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_5.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_6.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_7.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_8.setStyleSheet(self.default_title_config_prof_qpbtn_style)
        self.cnfg_prof_btn_9.setStyleSheet(self.default_title_config_prof_qpbtn_style)

    def cnfg_prof_funk_0(self):  # self.update_settings_window_thread.start()
        global cfg_f,configuration_engaged
        if configuration_engaged is False:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

            self.cnfg_prof_btn_style_funk_0()
            self.cnfg_prof_btn_0.setStyleSheet(self.default_title_config_prof_qpbtn_style_1)
            cfg_f = './config_profile_0.txt'

            self.update_settings_window_thread.start()
        elif configuration_engaged is True:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

    def cnfg_prof_funk_1(self):
        global cfg_f,configuration_engaged
        if configuration_engaged is False:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

            self.cnfg_prof_btn_style_funk_0()
            self.cnfg_prof_btn_1.setStyleSheet(self.default_title_config_prof_qpbtn_style_1)
            cfg_f = './config_profile_1.txt'

            self.update_settings_window_thread.start()
        elif configuration_engaged is True:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

    def cnfg_prof_funk_2(self):
        global cfg_f,configuration_engaged
        if configuration_engaged is False:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

            self.cnfg_prof_btn_style_funk_0()
            self.cnfg_prof_btn_2.setStyleSheet(self.default_title_config_prof_qpbtn_style_1)
            cfg_f = './config_profile_2.txt'

            self.update_settings_window_thread.start()
        elif configuration_engaged is True:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

    def cnfg_prof_funk_3(self):
        global cfg_f,configuration_engaged
        if configuration_engaged is False:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

            self.cnfg_prof_btn_style_funk_0()
            self.cnfg_prof_btn_3.setStyleSheet(self.default_title_config_prof_qpbtn_style_1)
            cfg_f = './config_profile_3.txt'

            self.update_settings_window_thread.start()
        elif configuration_engaged is True:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

    def cnfg_prof_funk_4(self):
        global cfg_f,configuration_engaged
        if configuration_engaged is False:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

            self.cnfg_prof_btn_style_funk_0()
            self.cnfg_prof_btn_4.setStyleSheet(self.default_title_config_prof_qpbtn_style_1)
            cfg_f = './config_profile_4.txt'

            self.update_settings_window_thread.start()
        elif configuration_engaged is True:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

    def cnfg_prof_funk_5(self):
        global cfg_f,configuration_engaged
        if configuration_engaged is False:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

            self.cnfg_prof_btn_style_funk_0()
            self.cnfg_prof_btn_5.setStyleSheet(self.default_title_config_prof_qpbtn_style_1)
            cfg_f = './config_profile_5.txt'

            self.update_settings_window_thread.start()
        elif configuration_engaged is True:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

    def cnfg_prof_funk_6(self):
        global cfg_f,configuration_engaged
        if configuration_engaged is False:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

            self.cnfg_prof_btn_style_funk_0()
            self.cnfg_prof_btn_6.setStyleSheet(self.default_title_config_prof_qpbtn_style_1)
            cfg_f = './config_profile_6.txt'

            self.update_settings_window_thread.start()
        elif configuration_engaged is True:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

    def cnfg_prof_funk_7(self):
        global cfg_f,configuration_engaged
        if configuration_engaged is False:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

            self.cnfg_prof_btn_style_funk_0()
            self.cnfg_prof_btn_7.setStyleSheet(self.default_title_config_prof_qpbtn_style_1)
            cfg_f = './config_profile_7.txt'

            self.update_settings_window_thread.start()
        elif configuration_engaged is True:
            print('-- configuration_engaged:', configuration_engaged)

    def cnfg_prof_funk_8(self):
        global cfg_f,configuration_engaged
        if configuration_engaged is False:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

            self.cnfg_prof_btn_style_funk_0()
            self.cnfg_prof_btn_8.setStyleSheet(self.default_title_config_prof_qpbtn_style_1)
            cfg_f = './config_profile_8.txt'

            self.update_settings_window_thread.start()
        elif configuration_engaged is True:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

    def cnfg_prof_funk_9(self):
        global cfg_f,configuration_engaged
        if configuration_engaged is False:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

            self.cnfg_prof_btn_style_funk_0()
            self.cnfg_prof_btn_9.setStyleSheet(self.default_title_config_prof_qpbtn_style_1)
            cfg_f = './config_profile_9.txt'

            self.update_settings_window_thread.start()
        elif configuration_engaged is True:
            if debug_enabled is True:
                print('-- configuration_engaged:', configuration_engaged)

    # Sector 2: Set's Configuration Title(s)
    def setting_title_B_funk(self):
        global settings_active_int
        if debug_enabled is True:
            print('settings_active_int:', settings_active_int)
        if len(self.setting_title_B_var[settings_active_int].text()) <= 16:
            name_str = 'NAME ' + str(settings_active_int) + ': '
            name_tile[settings_active_int] = self.setting_title_B_var[settings_active_int].text().strip()
            self.settings_title_var[settings_active_int].setText(self.setting_title_B_var[settings_active_int].text().strip())
            self.tb_label_0.setText(name_tile[settings_active_int] + ' Output')
            if os.path.exists(cfg_f):
                path_item = []
                with open(cfg_f, 'r') as fo:
                    for line in fo:
                        line = line.strip()
                        if not line.startswith(name_str):
                            path_item.append(line)
                        elif line.startswith(name_str):
                            new_line = name_str + self.setting_title_B_var[settings_active_int].text().strip()
                            path_item.append(new_line)
                open(cfg_f, 'w').close()
                with open(cfg_f, 'a') as fo:
                    i = 0
                    for path_items in path_item:
                        fo.writelines(path_item[i] + '\n')
                        i += 1
                fo.close()
            self.setting_title_B_var[settings_active_int].hide()
            self.settings_title_var[settings_active_int].show()
            self.paths_readonly_button_funk()
    # Section 1 Funtion: Main Function Confirmation 0
    def confirm_op0_funk0(self):
        global confirm_op0_bool, confirm_op0_wait, debug_enabled
        if debug_enabled is True:
            print('-- plugged in: confirm_op0_funk0: accepted')
        confirm_op0_bool = True
        confirm_op0_wait = False
    # Section 1 Funtion: Main Function Confirmation 1
    def confirm_op1_funk0(self):
        global confirm_op1_bool, confirm_op1_wait, debug_enabled
        if debug_enabled is True:
            print('-- plugged in: confirm_op1_funk0: accepted')
        confirm_op1_bool = True
        confirm_op1_wait = False
    # Section 1 Funtion: Main Function Confirmation 2
    def confirm_op2_funk0(self):
        global confirm_op2_bool, confirm_op2_wait, debug_enabled
        if debug_enabled is True:
            print('-- plugged in: confirm_op2_funk0: accepted')
        confirm_op2_bool = True
        confirm_op2_wait = False
    # Section 1 Funtion: Main Function Confirmation 3
    def confirm_op3_funk0(self):
        global confirm_op3_bool, confirm_op3_wait, debug_enabled
        if debug_enabled is True:
            print('-- plugged in: confirm_op3_funk0: accepted')
        confirm_op3_bool = True
        confirm_op3_wait = False
    # Section 1 Funtion: Main Function Confirmation 4
    def confirm_op4_funk0(self):
        global confirm_op4_bool, confirm_op4_wait, debug_enabled
        if debug_enabled is True:
            print('-- plugged in: confirm_op4_funk0: accepted')
        confirm_op4_bool = True
        confirm_op4_wait = False
    # Section 1 Funtion: Main Function Confirmation 5
    def confirm_op5_funk0(self):
        global confirm_op5_bool, confirm_op5_wait, debug_enabled
        if debug_enabled is True:
            print('-- plugged in: confirm_op5_funk0: accepted')
        confirm_op5_bool = True
        confirm_op5_wait = False

    def paths_readonly_button_pre_funk_0(self):
        global settings_active_int
        settings_active_int = 0
        self.paths_readonly_button_funk()

    def paths_readonly_button_pre_funk_1(self):
        global settings_active_int
        settings_active_int = 1
        self.paths_readonly_button_funk()

    def paths_readonly_button_pre_funk_2(self):
        global settings_active_int
        settings_active_int = 2
        self.paths_readonly_button_funk()

    def paths_readonly_button_pre_funk_3(self):
        global settings_active_int
        settings_active_int = 3
        self.paths_readonly_button_funk()

    def paths_readonly_button_pre_funk_4(self):
        global settings_active_int
        settings_active_int = 4
        self.paths_readonly_button_funk()

    def paths_readonly_button_pre_funk_5(self):
        global settings_active_int
        settings_active_int = 5
        self.paths_readonly_button_funk()
    # Section 2 Funtion: Set Source & Destination ReadOnly Bool
    def paths_readonly_button_funk(self):
        global debug_enabled, settings_active_int
        if debug_enabled is True:
            print('-- plugged in: paths_readonly_button_funk')
            print('-- settings_active_int', settings_active_int)
        if self.settings_source_edit_var[settings_active_int].isReadOnly() is True:
            self.settings_source_edit_var[settings_active_int].setReadOnly(False)
            self.settings_dest_edit_var[settings_active_int].setReadOnly(False)
            self.paths_readonly_btn_var[settings_active_int].setIcon(QIcon(self.img_read_ony_false))
            self.paths_readonly_btn_var[settings_active_int].setIconSize(QSize(8, 21))
            self.settings_title_var[settings_active_int].hide()
            self.setting_title_B_var[settings_active_int].setText(name_tile[settings_active_int])
            self.setting_title_B_var[settings_active_int].show()
        elif self.settings_source_edit_var[settings_active_int].isReadOnly() is False:
            self.settings_source_edit_var[settings_active_int].setReadOnly(True)
            self.settings_dest_edit_var[settings_active_int].setReadOnly(True)
            self.paths_readonly_btn_var[settings_active_int].setIcon(QIcon(self.img_read_ony_true))
            self.paths_readonly_btn_var[settings_active_int].setIconSize(QSize(8, 8))
            self.settings_title_var[settings_active_int].show()
            self.setting_title_B_var[settings_active_int].hide()
    # Sector 2 Funtion: Moves To Next Settings Page Left
    def scr_left_funk(self):
        global debug_enabled, settings_active_int
        if settings_active_int is 0:
            settings_active_int = 5
            self.btnx_set_focus_funk()
        elif settings_active_int is 1:
            settings_active_int = 0
            self.btnx_set_focus_funk()
        elif settings_active_int is 2:
            settings_active_int = 1
            self.btnx_set_focus_funk()
        elif settings_active_int is 3:
            settings_active_int = 2
            self.btnx_set_focus_funk()
        elif settings_active_int is 4:
            settings_active_int = 3
            self.btnx_set_focus_funk()
        elif settings_active_int is 5:
            settings_active_int = 4
            self.btnx_set_focus_funk()
    # Sector 2 Funtion: Moves To Next Settings Page Right
    def scr_right_funk(self):
        global debug_enabled, settings_active_int
        if settings_active_int is 0:
            settings_active_int = 1
            self.btnx_set_focus_funk()
        elif settings_active_int is 1:
            settings_active_int = 2
            self.btnx_set_focus_funk()
        elif settings_active_int is 2:
            settings_active_int = 3
            self.btnx_set_focus_funk()
        elif settings_active_int is 3:
            settings_active_int = 4
            self.btnx_set_focus_funk()
        elif settings_active_int is 4:
            settings_active_int = 5
            self.btnx_set_focus_funk()
        elif settings_active_int is 5:
            settings_active_int = 0
            self.btnx_set_focus_funk()
    # Sector 2 Funtion: Provides settings_source_funk With Information From Source Path Edit 0
    def settings_source_pre_funk0(self):
        global debug_enabled, source_path_entered, source_selected
        source_selected = 0
        source_path_entered = self.settings_source_edit_var[0].text()
        self.settings_source_funk()
    # Sector 2 Funtion: Provides settings_source_funk With Information From Source Path Edit 1
    def settings_source_pre_funk1(self):
        global debug_enabled, source_path_entered, source_selected
        source_selected = 1
        source_path_entered = self.settings_source_edit_var[1].text()
        self.settings_source_funk()
    # Sector 2 Funtion: Provides settings_source_funk With Information From Source Path Edit 2
    def settings_source_pre_funk2(self):
        global debug_enabled, source_path_entered, source_selected
        source_selected = 2
        source_path_entered = self.settings_source_edit_var[2].text()
        self.settings_source_funk()
    # Sector 2 Funtion: Provides settings_source_funk With Information From Source Path Edit 3
    def settings_source_pre_funk3(self):
        global debug_enabled, source_path_entered, source_selected
        source_selected = 3
        source_path_entered = self.settings_source_edit_var[3].text()
        self.settings_source_funk()
    # Sector 2 Funtion: Provides settings_source_funk With Information From Source Path Edit 4
    def settings_source_pre_funk4(self):
        global debug_enabled, source_path_entered, source_selected
        source_selected = 4
        source_path_entered = self.settings_source_edit_var[4].text()
        self.settings_source_funk()
    # Sector 2 Funtion: Provides settings_source_funk With Information From Source Path Edit 5
    def settings_source_pre_funk5(self):
        global debug_enabled, source_path_entered, source_selected
        source_selected = 5
        source_path_entered = self.settings_source_edit_var[5].text()
        self.settings_source_funk()
    # Sector 2 Funtion: Provides settings_dest_funk With Information From Destination Path Edit 0
    def settings_dest_pre_funk0(self):
        global debug_enabled, dest_path_entered, dest_selected
        dest_selected = 0
        dest_path_entered = self.settings_dest_edit_var[0].text()
        self.settings_dest_funk()
    # Sector 2 Funtion: Provides settings_dest_funk With Information From Destination Path Edit 1
    def settings_dest_pre_funk1(self):
        global debug_enabled, dest_path_entered, dest_selected
        dest_selected = 1
        dest_path_entered = self.settings_dest_edit_var[1].text()
        self.settings_dest_funk()
    # Sector 2 Funtion: Provides settings_dest_funk With Information From Destination Path Edit 2
    def settings_dest_pre_funk2(self):
        global debug_enabled, dest_path_entered, dest_selected
        dest_selected = 2
        dest_path_entered = self.settings_dest_edit_var[2].text()
        self.settings_dest_funk()
    # Sector 2 Funtion: Provides settings_dest_funk With Information From Destination Path Edit 3
    def settings_dest_pre_funk3(self):
        global debug_enabled, dest_path_entered, dest_selected
        dest_selected = 3
        dest_path_entered = self.settings_dest_edit_var[3].text()
        self.settings_dest_funk()
    # Sector 2 Funtion: Provides settings_dest_funk With Information From Destination Path Edit 4
    def settings_dest_pre_funk4(self):
        global debug_enabled, dest_path_entered, dest_selected
        dest_selected = 4
        dest_path_entered = self.settings_dest_edit_var[4].text()
        self.settings_dest_funk()
    # Sector 2 Funtion: Provides settings_dest_funk With Information From Destination Path Edit 5
    def settings_dest_pre_funk5(self):
        global debug_enabled, dest_path_entered, dest_selected
        dest_selected = 5
        dest_path_entered = self.settings_dest_edit_var[5].text()
        self.settings_dest_funk()
    # Sector 2 Funtion: Hides Objects in Sector 2, Resizes Sector One Background Labels, Rotates Sector 1 Drop Down Settings Arrows
    def hide_settings_funk(self):
        global settings_active_int
        if debug_enabled is True:
            print('-- plugged in: hide_settings_funk')
        self.setting_title_B_var[0].hide()
        self.setting_title_B_var[1].hide()
        self.setting_title_B_var[2].hide()
        self.setting_title_B_var[3].hide()
        self.setting_title_B_var[4].hide()
        self.setting_title_B_var[5].hide()
        self.settings_source_edit_var[0].hide()
        self.settings_source_edit_var[1].hide()
        self.settings_source_edit_var[2].hide()
        self.settings_source_edit_var[3].hide()
        self.settings_source_edit_var[4].hide()
        self.settings_source_edit_var[5].hide()
        self.settings_dest_edit_var[0].hide()
        self.settings_dest_edit_var[1].hide()
        self.settings_dest_edit_var[2].hide()
        self.settings_dest_edit_var[3].hide()
        self.settings_dest_edit_var[4].hide()
        self.settings_dest_edit_var[5].hide()
        self.tb_0.hide()
        self.tb_1.hide()
        self.tb_2.hide()
        self.tb_3.hide()
        self.tb_4.hide()
        self.tb_5.hide()
        self.tb_label_0.hide()
        self.paths_readonly_btn_0.hide()
        self.paths_readonly_btn_1.hide()
        self.paths_readonly_btn_2.hide()
        self.paths_readonly_btn_3.hide()
        self.paths_readonly_btn_4.hide()
        self.paths_readonly_btn_5.hide()

    def btnx_set_focus_pre_funk_0(self):
        global debug_enabled, settings_active_int
        settings_active_int = 0
        self.btnx_set_focus_funk()

    def btnx_set_focus_pre_funk_1(self):
        global debug_enabled, settings_active_int
        settings_active_int = 1
        self.btnx_set_focus_funk()

    def btnx_set_focus_pre_funk_2(self):
        global debug_enabled, settings_active_int
        settings_active_int = 2
        self.btnx_set_focus_funk()

    def btnx_set_focus_pre_funk_3(self):
        global debug_enabled, settings_active_int
        settings_active_int = 3
        self.btnx_set_focus_funk()

    def btnx_set_focus_pre_funk_4(self):
        global debug_enabled, settings_active_int
        settings_active_int = 4
        self.btnx_set_focus_funk()

    def btnx_set_focus_pre_funk_5(self):
        global debug_enabled, settings_active_int
        settings_active_int = 5
        self.btnx_set_focus_funk()

    def settings_title_focus_false(self):
        self.settings_title_var[0].setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var[1].setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var[2].setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var[3].setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var[4].setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var[5].setStyleSheet(self.default_qpbtn_style_txt_0)

    def show_settings_title(self):
        self.settings_title_var[0].show()
        self.settings_title_var[1].show()
        self.settings_title_var[2].show()
        self.settings_title_var[3].show()
        self.settings_title_var[4].show()
        self.settings_title_var[5].show()

    def btnx_set_focus_funk(self):
        global debug_enabled, settings_active_int
        self.hide_settings_funk()
        self.show_settings_title()
        self.settings_title_focus_false()
        self.highlight_off_0()
        self.backlabel_resize_0()
        self.title_lable_resize()

        # Emphasize Importance
        self.btnx_main_var[settings_active_int].setStyleSheet(self.default_btnx_main_style_1)
        self.stop_thread_btn_var[settings_active_int].setStyleSheet(self.default_qpb_highlight)
        self.confirm_op_var[settings_active_int].setStyleSheet(self.default_qpb_highlight)
        self.settings_title_var[settings_active_int].setStyleSheet(self.default_qpbtn_style_txt_1)
        self.settings_source_edit_var[settings_active_int].setStyleSheet(self.default_qle_highlight_0)
        self.settings_dest_edit_var[settings_active_int].setStyleSheet(self.default_qle_highlight_0)
        self.settings_source_label.setStyleSheet(self.default_qlbl_highlight)
        self.settings_dest_label.setStyleSheet(self.default_qlbl_highlight)
        self.tb_label_0.setStyleSheet(self.default_qlbl_highlight)
        self.paths_readonly_btn_var[settings_active_int].setStyleSheet(self.default_qpb_highlight)

        self.settings_title_var[settings_active_int].resize(self.title_lable_w_0, self.title_lable_h_1)
        self.back_label_var[settings_active_int].resize(self.back_label_w_1, self.back_label_h_1)
        self.paths_readonly_btn_var[settings_active_int].setIconSize(QSize(8, 8))
        self.paths_readonly_btn_var[settings_active_int].setIcon(QIcon(self.img_read_ony_true))

        try:
            self.tb_label_0.setText(name_tile[settings_active_int] + ' Output')
        except Exception as e:
            if debug_enabled is True:
                print('-- exception:', str(e).strip().encode('utf-8'))

        self.tb_label_0.show()
        self.settings_source_edit_var[settings_active_int].show()
        self.settings_dest_edit_var[settings_active_int].show()
        self.tb_var[settings_active_int].show()
        self.paths_readonly_btn_var[settings_active_int].show()

        self.settings_source_edit_var[settings_active_int].setReadOnly(True)
        self.settings_dest_edit_var[settings_active_int].setReadOnly(True)
        self.paths_readonly_btn_var[settings_active_int].setEnabled(True)

        settings_active_int_prev = settings_active_int

    def highlight_off_0(self):
        self.btnx_main_var[0].setStyleSheet(self.default_btnx_main_style)
        self.btnx_main_var[1].setStyleSheet(self.default_btnx_main_style)
        self.btnx_main_var[2].setStyleSheet(self.default_btnx_main_style)
        self.btnx_main_var[3].setStyleSheet(self.default_btnx_main_style)
        self.btnx_main_var[4].setStyleSheet(self.default_btnx_main_style)
        self.btnx_main_var[5].setStyleSheet(self.default_btnx_main_style)

        self.stop_thread_btn_var[0].setStyleSheet(self.default_qpbtn_style)
        self.stop_thread_btn_var[1].setStyleSheet(self.default_qpbtn_style)
        self.stop_thread_btn_var[2].setStyleSheet(self.default_qpbtn_style)
        self.stop_thread_btn_var[3].setStyleSheet(self.default_qpbtn_style)
        self.stop_thread_btn_var[4].setStyleSheet(self.default_qpbtn_style)
        self.stop_thread_btn_var[5].setStyleSheet(self.default_qpbtn_style)

        self.confirm_op_var[0].setStyleSheet(self.default_qpbtn_style)
        self.confirm_op_var[1].setStyleSheet(self.default_qpbtn_style)
        self.confirm_op_var[2].setStyleSheet(self.default_qpbtn_style)
        self.confirm_op_var[3].setStyleSheet(self.default_qpbtn_style)
        self.confirm_op_var[4].setStyleSheet(self.default_qpbtn_style)
        self.confirm_op_var[5].setStyleSheet(self.default_qpbtn_style)

        self.settings_title_var[0].setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var[1].setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var[2].setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var[3].setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var[4].setStyleSheet(self.default_qpbtn_style_txt_0)
        self.settings_title_var[5].setStyleSheet(self.default_qpbtn_style_txt_0)

    def backlabel_resize_0(self):
        i = 0
        for thread_engaged_vars in thread_engaged_var:
            if not thread_engaged_var[i] is True:
                self.back_label_var[i].resize(self.back_label_w_0, self.back_label_h_0)
            i += 1
        #self.back_label_var[0].resize(self.back_label_w_0, self.back_label_h_0)
        #self.back_label_var[1].resize(self.back_label_w_0, self.back_label_h_0)
        #self.back_label_var[2].resize(self.back_label_w_0, self.back_label_h_0)
        #self.back_label_var[3].resize(self.back_label_w_0, self.back_label_h_0)
        #self.back_label_var[4].resize(self.back_label_w_0, self.back_label_h_0)
        #self.back_label_var[5].resize(self.back_label_w_0, self.back_label_h_0)

    def title_lable_resize(self):
        self.settings_title_var[0].resize(self.title_lable_w_0, self.title_lable_h_0)
        self.settings_title_var[1].resize(self.title_lable_w_0, self.title_lable_h_0)
        self.settings_title_var[2].resize(self.title_lable_w_0, self.title_lable_h_0)
        self.settings_title_var[3].resize(self.title_lable_w_0, self.title_lable_h_0)
        self.settings_title_var[4].resize(self.title_lable_w_0, self.title_lable_h_0)
        self.settings_title_var[5].resize(self.title_lable_w_0, self.title_lable_h_0)

    # Sector 1 Function: Starts Main Sector 1 Thread 0
    def thread_funk_0(self):
        self.thread_0.start()
    # Sector 1 Function: Starts Main Sector 1 Thread 1
    def thread_funk_1(self):
        self.thread_1.start()
    # Sector 1 Function: Starts Main Sector 1 Thread 2
    def thread_funk_2(self):
        self.thread_2.start()
    # Sector 1 Function: Starts Main Sector 1 Thread 3
    def thread_funk_3(self):
        self.thread_3.start()
    # Sector 1 Function: Starts Main Sector 1 Thread 4
    def thread_funk_4(self):
        self.thread_4.start()
    # Sector 1 Function: Starts Main Sector 1 Thread 5
    def thread_funk_5(self):
        self.thread_5.start()
    # Sector 1 Function: Provides Relative Information To set_comp_bool_funk From Section 1 Main Function Mode Switch Button 0
    def set_comp_bool_pre_funk0(self):
        global debug_enabled, compare_clicked
        compare_clicked = 0
        self.set_comp_bool_funk()
    # Sector 1 Function: Provides Relative Information To set_comp_bool_funk From Section 1 Main Function Mode Switch Button 1
    def set_comp_bool_pre_funk1(self):
        global debug_enabled, compare_clicked
        compare_clicked = 1
        self.set_comp_bool_funk()
    # Sector 1 Function: Provides Relative Information To set_comp_bool_funk From Section 1 Main Function Mode Switch Button 2
    def set_comp_bool_pre_funk2(self):
        global debug_enabled, compare_clicked
        compare_clicked = 2
        self.set_comp_bool_funk()
    # Sector 1 Function: Provides Relative Information To set_comp_bool_funk From Section 1 Main Function Mode Switch Button 3
    def set_comp_bool_pre_funk3(self):
        global debug_enabled, compare_clicked
        compare_clicked = 3
        self.set_comp_bool_funk()
    # Sector 1 Function: Provides Relative Information To set_comp_bool_funk From Section 1 Main Function Mode Switch Button 4
    def set_comp_bool_pre_funk4(self):
        global debug_enabled, compare_clicked
        compare_clicked = 4
        self.set_comp_bool_funk()
    # Sector 1 Function: Provides Relative Information To set_comp_bool_funk From Section 1 Main Function Mode Switch Button 5
    def set_comp_bool_pre_funk5(self):
        global debug_enabled, compare_clicked
        compare_clicked = 5
        self.set_comp_bool_funk()
    # Sector 1 Function: Uses Integer To Switch Main Function Mode Relative To Mode Button Clicked
    def set_comp_bool_funk(self):
        global debug_enabled, compare_bool_var, compare_clicked, thread_engaged_var
        if thread_engaged_var[compare_clicked] is False:
            if compare_bool_var[compare_clicked] is False:
                compare_bool_var[compare_clicked] = True
                self.btnx_mode_btn_var[compare_clicked].setIcon(QIcon(self.img_mode_1))
                self.btnx_mode_btn_var[compare_clicked].setStyleSheet(self.default_qpbtn_prsd_style)
            elif compare_bool_var[compare_clicked] is True:
                compare_bool_var[compare_clicked] = False
                self.btnx_mode_btn_var[compare_clicked].setIcon(QIcon(self.img_mode_0))
                self.btnx_mode_btn_var[compare_clicked].setStyleSheet(self.default_qpbtn_style)
        elif thread_engaged_var[compare_clicked] is True:
            if debug_enabled is True:
                print('-- thread engaged: setting mode unavailable')
    # Sector 1 Function: Stops Sector 1 Main Function Thread 0
    def stop_thr_funk0(self):
        global debug_enabled
        self.thread_0.stop_thr()
    # Sector 1 Function: Stops Sector 1 Main Function Thread 1
    def stop_thr_funk1(self):
        global debug_enabled
        self.thread_1.stop_thr()
    # Sector 1 Function: Stops Sector 1 Main Function Thread 2
    def stop_thr_funk2(self):
        global debug_enabled
        self.thread_2.stop_thr()
    # Sector 1 Function: Stops Sector 1 Main Function Thread 3
    def stop_thr_funk3(self):
        global debug_enabled
        self.thread_3.stop_thr()
    # Sector 1 Function: Stops Sector 1 Main Function Thread 4
    def stop_thr_funk4(self):
        global debug_enabled
        self.thread_4.stop_thr()
    # Sector 1 Function: Stops Sector 1 Main Function Thread 5
    def stop_thr_funk5(self):
        global debug_enabled
        self.thread_5.stop_thr()

    def sanitize_input_funk(self):
        global valid_len_bool, valid_drive_bool, valid_char_bool, valid_non_win_res_nm_bool, source_path_entered, dest_path_entered, sanitize_input_int
        valid_len_bool = False
        valid_drive_bool = False
        valid_char_bool = False
        valid_non_win_res_nm_bool = False
        if sanitize_input_int is 0:
            str_path = source_path_entered
        elif sanitize_input_int is 1:
            str_path = dest_path_entered
        str_len = len(str_path)
        if str_len < 255 and str_len >= 3:
            valid_len_bool = True
            char_var0 = str_path[0]
            char_var1 = str_path[1]
            char_var2 = str_path[2]
            char_var3 = str(char_var0 + char_var1 + char_var2)
            if os.path.exists(char_var3) and char_var0.isalpha() and char_var1 is ':' and char_var2 is '\\':
                valid_drive_bool = True
                valid_char = []
                invalid_char = ['<', '>', ':', '"', '/', '|', '?', '*', '.']
                i = 0
                for str_paths in str_path:
                    if not i is 1:
                        if str_path[i] in invalid_char:
                            valid_char.append(False)
                    i += 1
                if not False in valid_char:
                    valid_char_bool = True
                    valid_var = []
                    win_res_nm = ['CON', 'PRN', 'AUX', 'NUL',
                        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
                    i = 0
                    for win_res_nms in win_res_nm:
                        if str('\\' + win_res_nm[i] + '\\') in str_path:
                            valid_var.append(False)
                        elif str_path.endswith(win_res_nm[i]):
                            valid_var.append(False)
                        elif str(win_res_nm[i] + '.') in str_path:
                            valid_var.append(False)
                        i += 1
                    if not False in valid_var:
                        valid_non_win_res_nm_bool = True
        if debug_enabled is True:
            print('-- resutls:')
            print('-- string length:', valid_len_bool)
            print('-- drive letter:', valid_drive_bool)
            print('-- valid characters:', valid_char_bool)
            print('-- does not contain system reserved names:', valid_non_win_res_nm_bool)


    # Sector 2 Funtion: Writes Source Changes To Configuration File
    def settings_source_funk(self):
        global debug_enabled, source_path_entered, source_selected, config_src_var, path_var, settings_input_response_source_bool, cfg_f
        global valid_len_bool, valid_drive_bool, valid_char_bool, valid_non_win_res_nm_bool, sanitize_input_int
        settings_input_response_source_bool = False
        sanitize_input_int = 0
        self.sanitize_input_funk()
        if os.path.exists(source_path_entered) and valid_len_bool is True and valid_drive_bool is True and valid_char_bool is True and valid_non_win_res_nm_bool is True:
            if debug_enabled is True:
                print('-- input source path passed current sanitization checks')
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
                    fo.writelines(path_item[i] + '\n')
                    i += 1
            fo.close()
            path_var[source_selected] = source_path_entered
            settings_input_response_source_bool = True
            self.paths_readonly_button_funk()
        else:
            print('-- input source path failed current sanitization checks')
            self.settings_source_edit_var[source_selected].setText(path_var[source_selected])
            settings_input_response_source_bool = False
        self.settings_input_response_thread.start()

    # Sector 2 Funtion: Writes Destination Changes To Configuration File
    def settings_dest_funk(self):
        global debug_enabled, dest_path_entered, dest_selected, config_dst_var, dest_path_var, path_var, settings_input_response_dest_bool
        global valid_len_bool, valid_drive_bool, valid_char_bool, valid_non_win_res_nm_bool, sanitize_input_int
        settings_input_response_dest_bool = False
        sanitize_input_int = 1
        self.sanitize_input_funk()
        if valid_len_bool is True and valid_drive_bool is True and valid_non_win_res_nm_bool is True and valid_char_bool is True:
            if debug_enabled is True:
                print('-- input destination path passed current sanitization checks')
                print('-- creating destination:', dest_path_entered)
            distutils.dir_util.mkpath(dest_path_entered)
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
            settings_input_response_dest_bool = True
            self.paths_readonly_button_funk()
        else:
            if debug_enabled is True:
                print('-- input destination path failed current sanitization checks')
            self.settings_dest_edit_var[dest_selected].setText(dest_path_var[dest_selected])
            settings_input_response_dest_bool = False
        self.settings_input_response_thread.start()

# Scaling Class: Automatically Adjusts Form's Geometry Accounting For Changes In Display Scaling Settings
class ScalingClass(QThread):
    def __init__(self, setGeometry, width, height, pos):
        QThread.__init__(self)
        self.setGeometry = setGeometry
        self.width = width
        self.height = height
        self.pos = pos

    def run(self):
        global debug_enabled
        if debug_enabled is True:
            print('-- plugged in: ScalingClass')
        #while True:
        #    time.sleep(0.01)
            #self.setGeometry(self.pos().x(), self.pos().y(), self.width, self.height)

# Input Respons Class: LED's Dsilpay Valid/Invalid Paths Attempted At Being Set In Sector 2 Source & Destination Path Configuration
class SettingsInputResponse(QThread):
    def __init__(self, default_valid_path_led_green, default_valid_path_led_red, default_valid_path_led, settings_input_response_label_src, settings_input_response_label_dst):
        QThread.__init__(self)
        self.default_valid_path_led_green = default_valid_path_led_green
        self.default_valid_path_led_red = default_valid_path_led_red
        self.default_valid_path_led = default_valid_path_led
        self.settings_input_response_label_src = settings_input_response_label_src
        self.settings_input_response_label_dst = settings_input_response_label_dst

    def run(self):
        global debug_enabled, settings_input_response_source_bool, settings_input_response_dest_bool
        if settings_input_response_source_bool is True:
            self.settings_input_response_label_src.setStyleSheet(self.default_valid_path_led_green)
            settings_input_response_source_bool = None
            time.sleep(1)
            self.settings_input_response_label_src.setStyleSheet(self.default_valid_path_led)
        elif settings_input_response_source_bool is False:
            self.settings_input_response_label_src.setStyleSheet(self.default_valid_path_led_red)
            settings_input_response_source_bool = None
            time.sleep(1)
            self.settings_input_response_label_src.setStyleSheet(self.default_valid_path_led)
        elif settings_input_response_dest_bool is True:
            self.settings_input_response_label_dst.setStyleSheet(self.default_valid_path_led_green)
            settings_input_response_dest_bool = None
            time.sleep(1)
            self.settings_input_response_label_dst.setStyleSheet(self.default_valid_path_led)
        elif settings_input_response_dest_bool is False:
            self.settings_input_response_label_dst.setStyleSheet(self.default_valid_path_led_red)
            settings_input_response_dest_bool = None
            time.sleep(1)
            self.settings_input_response_label_dst.setStyleSheet(self.default_valid_path_led)

# Update Sector 2 Settings Window: Sources & Destination Paths Displayed Only When Last Valid Path Entered Still Actually Exists
class UpdateSettingsWindow(QThread):
    def __init__(self, settings_source_edit_var, settings_dest_edit_var, settings_title_var, tb_label_0, thread_0, thread_1, thread_2, thread_3, thread_4, thread_5):
        QThread.__init__(self)
        self.settings_source_edit_var = settings_source_edit_var
        self.settings_dest_edit_var = settings_dest_edit_var
        self.settings_title_var = settings_title_var
        self.tb_label_0 = tb_label_0
        self.thread_0 = thread_0
        self.thread_1 = thread_1
        self.thread_2 = thread_2
        self.thread_3 = thread_3
        self.thread_4 = thread_4
        self.thread_5 = thread_5
        self.local_thread_var = [self.thread_0, self.thread_1, self.thread_2, self.thread_3, self.thread_4, self.thread_5]

    # Run This Thread While Program Is Alive And Read Configuration File
    def run(self):
        global debug_enabled
        if debug_enabled is True:
            print('-- plugged in: UpdateSettingsWindow')
        self.get_conf_funk()
        while __name__ == '__main__':
            self.get_conf_funk()
            time.sleep(1)

    # While Source And Destination Path Configuration Edit ReadOnly, Check Configured Paths Existance And Set Boolean Accordingly
    def get_conf_funk(self):
        global debug_enabled, path_var, dest_path_var, name_tile, configuration_engaged, cfg_f, img_path, thread_engaged_var
        configuration_engaged = True
        # Only Update Displayed Source & Destination Paths If Source & Destination Paths Not Being Edited
        check_var = []
        i = 0
        for self.settings_source_edit_vars in self.settings_source_edit_var:
            if self.settings_source_edit_var[i].isReadOnly() is False:
                check_var.append(False)
            elif self.settings_source_edit_var[i].isReadOnly() is True:
                check_var.append(True)
            i += 1
        if not False in check_var:
            name_max_chars = 16
            name_tile = []
            path_var = []
            dest_path_var = []
            if os.path.exists(cfg_f):
                with open(cfg_f, 'r') as fo:
                    for line in fo:
                        line = line.strip()
                        if line.startswith('NAME 0: '):
                            line = line.replace('NAME 0: ', '')
                            if len(line) <= name_max_chars and len(name_tile) <= 6:
                                name_tile.append(line)
                            elif not len(line) <= name_max_chars or len(name_tile) >= 6:
                                name_tile.append('Configuration 0')
                        if line.startswith('NAME 1: '):
                            line = line.replace('NAME 1: ', '')
                            if len(line) <= name_max_chars and len(name_tile) <= 6:
                                name_tile.append(line)
                            elif not len(line) <= name_max_chars or len(name_tile) <= 6:
                                name_tile.append('Configuration 1')
                        if line.startswith('NAME 2: '):
                            line = line.replace('NAME 2: ', '')
                            if len(line) <= name_max_chars and len(name_tile) <= 6:
                                name_tile.append(line)
                            elif not len(line) <= name_max_chars or len(name_tile) <= 6:
                                name_tile.append('Configuration 2')
                        if line.startswith('NAME 3: '):
                            line = line.replace('NAME 3: ', '')
                            if len(line) <= name_max_chars and len(name_tile) <= 6:
                                name_tile.append(line)
                            elif not len(line) <= name_max_chars or len(name_tile) <= 6:
                                name_tile.append('Configuration 3')
                        if line.startswith('NAME 4: '):
                            line = line.replace('NAME 4: ', '')
                            if len(line) <= name_max_chars and len(name_tile) <= 6:
                                name_tile.append(line)
                            elif not len(line) <= name_max_chars or len(name_tile) <= 6:
                                name_tile.append('Configuration 4')
                        if line.startswith('NAME 5: '):
                            line = line.replace('NAME 5: ', '')
                            if len(line) <= name_max_chars and len(name_tile) <= 6:
                                name_tile.append(line)
                            elif not len(line) <= name_max_chars or len(name_tile) <= 6:
                                name_tile.append('Configuration 5')
                        if line.startswith('SOURCE 0: '):
                            line = line.replace('SOURCE 0: ', '')
                            if os.path.exists(line) and len(path_var) <= 6:
                                path_var.append(line)
                            elif not os.path.exists(line) and len(path_var) <= 6:
                                path_var.append('')
                        if line.startswith('SOURCE 1: '):
                            line = line.replace('SOURCE 1: ', '')
                            if os.path.exists(line) and len(path_var) <= 6:
                                path_var.append(line)
                            elif not os.path.exists(line) and len(path_var) <= 6:
                                path_var.append('')
                        if line.startswith('SOURCE 2: '):
                            line = line.replace('SOURCE 2: ', '')
                            if os.path.exists(line) and len(path_var) <= 6:
                                path_var.append(line)
                            elif not os.path.exists(line) and len(path_var) <= 6:
                                path_var.append('')
                        if line.startswith('SOURCE 3: '):
                            line = line.replace('SOURCE 3: ', '')
                            if os.path.exists(line) and len(path_var) <= 6:
                                path_var.append(line)
                            elif not os.path.exists(line) and len(path_var) <= 6:
                                path_var.append('')
                        if line.startswith('SOURCE 4: '):
                            line = line.replace('SOURCE 4: ', '')
                            if os.path.exists(line) and len(path_var) <= 6:
                                path_var.append(line)
                            elif not os.path.exists(line) and len(path_var) <= 6:
                                path_var.append('')
                        if line.startswith('SOURCE 5: '):
                            line = line.replace('SOURCE 5: ', '')
                            if os.path.exists(line) and len(path_var) <= 6:
                                path_var.append(line)
                            elif not os.path.exists(line) and len(path_var) <= 6:
                                path_var.append('')
                        if line.startswith('DESTINATION 0: '):
                            line = line.replace('DESTINATION 0: ', '')
                            if os.path.exists(line) and len(dest_path_var) <= 6:
                                dest_path_var.append(line)
                            elif not os.path.exists(line) and len(dest_path_var) <= 6:
                                dest_path_var.append('')
                        if line.startswith('DESTINATION 1: '):
                            line = line.replace('DESTINATION 1: ', '')
                            if os.path.exists(line) and len(dest_path_var) <= 6:
                                dest_path_var.append(line)
                            elif not os.path.exists(line) and len(dest_path_var) <= 6:
                                dest_path_var.append('')
                        if line.startswith('DESTINATION 2: '):
                            line = line.replace('DESTINATION 2: ', '')
                            if os.path.exists(line) and len(dest_path_var) <= 6:
                                dest_path_var.append(line)
                            elif not os.path.exists(line) and len(dest_path_var) <= 6:
                                dest_path_var.append('')
                        if line.startswith('DESTINATION 3: '):
                            line = line.replace('DESTINATION 3: ', '')
                            if os.path.exists(line) and len(dest_path_var) <= 6:
                                dest_path_var.append(line)
                            elif not os.path.exists(line) and len(dest_path_var) <= 6:
                                dest_path_var.append('')
                        if line.startswith('DESTINATION 4: '):
                            line = line.replace('DESTINATION 4: ', '')
                            if os.path.exists(line) and len(dest_path_var) <= 6:
                                dest_path_var.append(line)
                            elif not os.path.exists(line) and len(dest_path_var) <= 6:
                                dest_path_var.append('')
                        if line.startswith('DESTINATION 5: '):
                            line = line.replace('DESTINATION 5: ', '')
                            if os.path.exists(line) and len(dest_path_var) <= 6:
                                dest_path_var.append(line)
                            elif not os.path.exists(line) and len(dest_path_var) <= 6:
                                dest_path_var.append('')
                        if line.startswith('IMAGE PATH: '):
                            line = line.replace('IMAGE PATH: ', '')
                            if os.path.exists(line) and len(dest_path_var) <= 6:
                                img_path = line
                            elif not os.path.exists(line) and len(dest_path_var) <= 6:
                                img_path = '.\\image\\default\\'
                fo.close()
                i = 0
                for self.settings_source_edit_vars in self.settings_source_edit_var:
                    if path_var[i] != self.settings_source_edit_var[i].text() and thread_engaged_var[i] is False:
                        self.settings_source_edit_var[i].setText(path_var[i])
                    elif path_var[i] != self.settings_source_edit_var[i].text()  and thread_engaged_var[i] is True:
                        if thread_initialized_var[i] is True:
                            self.local_thread_var[i].stop_thr()
                    i += 1
                i = 0
                for self.settings_dest_edit_vars in self.settings_dest_edit_var:
                    if dest_path_var[i] != self.settings_dest_edit_var[i].text()  and thread_engaged_var[i] is False:
                        self.settings_dest_edit_var[i].setText(dest_path_var[i])
                    elif dest_path_var[i] != self.settings_dest_edit_var[i].text()  and thread_engaged_var[i] is True:
                        if thread_initialized_var[i] is True:
                            self.local_thread_var[i].stop_thr()
                    i += 1
                i = 0
                for self.settings_title_vars in self.settings_title_var:
                    if name_tile[i] != self.settings_title_var[i].text() and thread_engaged_var[i] is False:
                        self.settings_title_var[i].setText(name_tile[i])
                    elif name_tile[i] != self.settings_title_var[i].text() and thread_engaged_var[i] is True:
                        if thread_initialized_var[i] is True:
                            self.local_thread_var[i].stop_thr()
                    i += 1
                self.tb_label_0.setText(name_tile[settings_active_int] + ' Output')
            elif not os.path.exists(cfg_f):
                if debug_enabled is True:
                    print('-- creating new configuration file')
                open(cfg_f, 'w').close()
                with open(cfg_f, 'a') as fo:
                    fo.writelines('NAME 0: Configuration 0\n')
                    fo.writelines('NAME 1: Configuration 1\n')
                    fo.writelines('NAME 2: Configuration 2\n')
                    fo.writelines('NAME 3: Configuration 3\n')
                    fo.writelines('NAME 4: Configuration 4\n')
                    fo.writelines('NAME 5: Configuration 5\n')
                    i = 0
                    for config_src_vars in config_src_var:
                        fo.writelines(config_src_var[i] + ' x' + '\n')
                        i += 1
                    i = 0
                    for config_dst_vars in config_dst_var:
                        fo.writelines(config_dst_var[i] + ' x' + '\n')
                        i += 1
                    fo.writelines('IMAGE PATH: .\\image\\default\\')
                fo.close()
        configuration_engaged = False


class ThreadClass0(QThread):
    def __init__(self, tb_0, confirm_op0_tru, img_btnx_led_0, img_btnx_led_1, img_btnx_led_2, img_execute_false, img_execute_true, img_stop_thread_false, img_stop_thread_true,
                 output_verbosity, btnx_main_0, stop_thread_btn_0, paths_readonly_btn_0, cnfg_prof_btn_var, paths_readonly_btn_var, loading_lbl_0):
        QThread.__init__(self)
        self.cnfg_prof_btn_var = cnfg_prof_btn_var
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
        self.btnx_main_0 = btnx_main_0
        self.stop_thread_btn_0 = stop_thread_btn_0
        self.paths_readonly_btn_0 = paths_readonly_btn_0
        self.cp0_count = 0
        self.cp0_fail_count = 0
        self.cp1_count = 0
        self.cp1_fail_count = 0
        self.path_0 = ''
        self.path_1 = ''
        self.write_call = ()
        self.paths_readonly_btn_var = paths_readonly_btn_var
        self.local_path = ''
        self.dest = ''
        self.bytes_count = 0
        self.bytes_count_str = ''
        self.bytes_count_1 = 0
        self.bytes_count_1_str = ''
        self.progress = ()
        self.progress_str = ''
        self.siz_src = ''
        self.f_count = 0
        self.f_count_1 = 0
        self.f_count_str = 0
        self.f_count_1_str = 0
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_0 = loading_lbl_0

    def write_funk(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var
        try:
            shutil.copy2(self.path_0, self.path_1)
        except Exception as e:
            if debug_enabled is True:
                print('-- exception:', str(e).strip().encode('utf-8'))
            try:
                os.makedirs(os.path.dirname(self.path_1))
                shutil.copy2(self.path_0, self.path_1)
            except Exception as e:
                if debug_enabled is True:
                    print('-- exception:', str(e).strip().encode('utf-8'))
                output_str = str('error: ' + self.path_1).strip()
                try:
                    self.tb_0.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))

    def check_write(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var
        if os.path.exists(self.path_1) and os.path.exists(self.path_0):
            siz_src = str(os.path.getsize(self.path_0))
            siz_dest = str(os.path.getsize(self.path_1))
            if siz_src == siz_dest:
                if self.write_call is 0:
                    self.cp0_count += 1
                    output_str = str('copied new: (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                elif self.write_call is 1:
                    self.cp1_count += 1
                    output_str = str('updated new: (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                try:
                    self.tb_0.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))
            elif siz_src != siz_dest:
                if self.write_call is 0:
                    self.cp0_fail_count += 1
                    output_str = str('failed to copy new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                elif self.write_call is 1:
                    self.cp1_fail_count += 1
                    output_str = str('failed to update new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                try:
                    self.tb_0.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))
        elif not os.path.exists(self.path_1):
            self.cp0_fail_count += 1
            if self.write_call is 0:
                self.cp0_fail_count += 1
                output_str = str('failed to copy new (file does no exist in destination): ' + self.path_1).strip()
            if self.write_call is 1:
                self.cp1_fail_count += 1
                output_str = str('failed to update file (file does no exist in destination): ' + self.path_1).strip()
            try:
                self.tb_0.append(output_str)
            except Exception as e:
                if debug_enabled is True:
                    print('-- exception:', str(e).strip().encode('utf-8'))
        # EDIT
        if debug_enabled is True:
            self.progress_output()

    def run(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var
        # If Source & Destination Configuration Is Disengaged Then Continue
        if configuration_engaged is False:
            thread_engaged_var[0] = True
            thread_initialized_var[0] = True
            # Set Paths In Stone Before Continuing. Asigns Source & Destination Variables To New Variables That Cannot Be Changed Once Function Exectutes
            self.local_path = path_var[0]
            self.dest = dest_path_var[0]
            compare_bool = compare_bool_var[0]
            self.cnfg_prof_btn_var[0].setEnabled(False)
            self.cnfg_prof_btn_var[1].setEnabled(False)
            self.cnfg_prof_btn_var[2].setEnabled(False)
            self.cnfg_prof_btn_var[3].setEnabled(False)
            self.cnfg_prof_btn_var[4].setEnabled(False)
            self.cnfg_prof_btn_var[5].setEnabled(False)
            self.cnfg_prof_btn_var[6].setEnabled(False)
            self.cnfg_prof_btn_var[7].setEnabled(False)
            self.cnfg_prof_btn_var[8].setEnabled(False)
            self.cnfg_prof_btn_var[9].setEnabled(False)
            self.paths_readonly_btn_var[0].setEnabled(False)
            self.btnx_main_0.setIcon(QIcon(self.img_btnx_led_1))
            self.confirm_op0_tru.setIcon(QIcon(self.img_execute_true))
            self.confirm_op0_tru.setEnabled(True)
            self.stop_thread_btn_0.setEnabled(True)
            self.stop_thread_btn_0.setIcon(QIcon(self.img_stop_thread_true))
            while confirm_op0_wait is True:
                time.sleep(0.3)
            thread_initialized_var[0] = False
            confirm_op0_wait = True
            self.confirm_op0_tru.setIcon(QIcon(self.img_execute_false))
            self.confirm_op0_tru.setEnabled(False)
            if confirm_op0_bool is True:
                if debug_enabled is True:
                    print('-- ThreadClass0: confirm_op0_bool: accepted')
                self.btnx_main_0.setIcon(QIcon(self.img_btnx_led_2))
                change_var = False
                if os.path.exists(self.local_path) and os.path.exists(self.dest):
                    for dirname, subdirlist, filelist in os.walk(self.local_path):
                        for fname in filelist:
                            self.path_0 = os.path.join(dirname, fname)
                            self.path_1 = self.path_0.replace(self.local_path, '')
                            self.path_1 = self.dest + self.path_1
                            if not os.path.exists(self.path_1):
                                self.path_0_item.append(self.path_0)
                                self.path_1_item.append(self.path_1)
                                self.siz_src = str(os.path.getsize(self.path_0))
                                siz_src_int = int(self.siz_src)
                                self.bytes_count = self.bytes_count + siz_src_int
                                self.f_count += 1
                                self.f_count_str = str(self.f_count)
                            elif os.path.exists(self.path_1) and os.path.exists(self.path_0) and compare_bool is True:
                                ma = os.path.getmtime(self.path_0)
                                mb = os.path.getmtime(self.path_1)
                                if mb < ma:
                                    self.path_0_item.append(self.path_0)
                                    self.path_1_item.append(self.path_1)
                                    self.siz_src = str(os.path.getsize(self.path_0))
                                    siz_src_int = int(self.siz_src)
                                    self.bytes_count = self.bytes_count + siz_src_int
                                    self.f_count += 1
                                    self.f_count_str = str(self.f_count)
                    self.bytes_count_str = str(self.bytes_count)
                    self.loading_lbl_0.resize(0, 7)
                    self.loading_lbl_0.show()
                    print('progress:', self.progress)
                    i = 0
                    for self.path_0_items in self.path_0_item:
                        self.path_0 = self.path_0_item[i]
                        self.path_1 = self.path_1_item[i]
                        if not os.path.exists(self.path_1):
                            self.siz_src = str(os.path.getsize(self.path_0))
                            siz_src_int = int(self.siz_src)
                            self.bytes_count_1 = self.bytes_count_1 + siz_src_int
                            self.bytes_count_1_str = str(self.bytes_count_1)
                            self.progress = (100 * float(self.bytes_count_1) / float(self.bytes_count))
                            self.progress_str = str(self.progress) + '%'
                            self.f_count_1 += 1
                            self.f_count_1_str = str(self.f_count_1)
                            change_var = True
                            self.write_funk()
                            self.write_call = 0
                            self.check_write()
                            self.progress_int = (int(self.progress) - 9)
                            self.loading_lbl_0.resize(self.progress_int, 8)
                        elif os.path.exists(self.path_1) and os.path.exists(self.path_0) and compare_bool is True:
                            ma = os.path.getmtime(self.path_0)
                            mb = os.path.getmtime(self.path_1)
                            if mb < ma:
                                self.siz_src = str(os.path.getsize(self.path_0))
                                siz_src_int = int(self.siz_src)
                                self.bytes_count_1 = self.bytes_count_1 + siz_src_int
                                self.bytes_count_1_str = str(self.bytes_count_1)
                                self.progress = (100 * float(self.bytes_count_1) / float(self.bytes_count))
                                self.progress_str = str(self.progress) + '%'
                                self.f_count_1 += 1
                                self.f_count_1_str = str(self.f_count_1)
                                change_var = True
                                self.write_funk()
                                self.write_call = 1
                                self.check_write()
                                self.progress_int = (int(self.progress) - 9)
                                self.loading_lbl_0.resize(self.progress_int, 8)

                        i += 1
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_0.resize(0, 7)
        self.loading_lbl_0.hide()
        self.summary()
        self.disengage()

    def progress_output(self):
        var_0 = str(self.f_count_1_str + '/' + self.f_count_str)
        var_1 = str(self.convert_bytes(self.bytes_count_1))
        var_2 = str(self.convert_bytes(self.bytes_count))
        var_3 = str(self.progress_str)
        var_4 = var_1 + '/' + var_2
        var_5 = var_4 + '  ' + var_3
        var_6 = var_0 + '  ' + var_5
        print(var_6)

    def convert_bytes(self, num):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return ("%3.1f %s" % (num, x))
            num /= 1024.0

    def summary(self):
        cp0_count_str = str(self.cp0_count)
        cp0_fail_count_str = str(self.cp0_fail_count)
        cp1_count_str = str(self.cp1_count)
        cp1_fail_count_str = str(self.cp1_fail_count)
        output_sum =  str('copied new: (' + cp0_count_str + ') | failed to copy new: (' + cp0_fail_count_str + ') | updated: (' + cp1_count_str + ')  | failed to update: (' + cp1_fail_count_str + ')').strip()
        if debug_enabled is True:
            print('-- ThreadClass3: ' + output_sum)
        self.tb_0.append(output_sum)
        self.tb_0.moveCursor(QTextCursor.End)
        self.tb_0.ensureCursorVisible()
        self.cp0_count = 0
        self.cp0_fail_count = 0
        self.cp1_count = 0
        self.cp1_fail_count = 0
        self.current_f = ''
        self.path_0 = ''
        self.path_1 = ''
        self.write_call = ()

    def disengage(self):
        self.btnx_main_0.setIcon(QIcon(self.img_btnx_led_0))
        self.stop_thread_btn_0.setIcon(QIcon(self.img_stop_thread_false))
        self.confirm_op0_tru.setIcon(QIcon(self.img_execute_false))
        self.stop_thread_btn_0.setEnabled(False)
        self.paths_readonly_btn_0.setEnabled(True)
        self.confirm_op0_tru.setEnabled(False)
        self.cnfg_prof_btn_var[0].setEnabled(True)
        self.cnfg_prof_btn_var[1].setEnabled(True)
        self.cnfg_prof_btn_var[2].setEnabled(True)
        self.cnfg_prof_btn_var[3].setEnabled(True)
        self.cnfg_prof_btn_var[4].setEnabled(True)
        self.cnfg_prof_btn_var[5].setEnabled(True)
        self.cnfg_prof_btn_var[6].setEnabled(True)
        self.cnfg_prof_btn_var[7].setEnabled(True)
        self.cnfg_prof_btn_var[8].setEnabled(True)
        self.cnfg_prof_btn_var[9].setEnabled(True)
        self.paths_readonly_btn_var[0].setEnabled(True)
        thread_engaged_var[0] = False
        confirm_op0_bool = False
        confirm_op0_wait = True
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_0.resize(0, 7)
        self.loading_lbl_0.hide()

    def stop_thr(self):
        global debug_enabled, confirm_op0_bool, confirm_op0_wait
        if not self.path_1 is '':
            output_str = 'terminated during: ' + self.path_1
            self.tb_0.append(output_str)
        if confirm_op0_bool is True:
            self.summary()
        self.disengage()
        if debug_enabled is True:
            print('-- confirm_op0 declined: (confirm_op0_bool)', confirm_op0_bool)
        self.terminate()


class ThreadClass1(QThread):
    def __init__(self, tb_1, confirm_op1_tru, img_btnx_led_0, img_btnx_led_1, img_btnx_led_2, img_execute_false, img_execute_true, img_stop_thread_false, img_stop_thread_true,
                 output_verbosity, btnx_main_1, stop_thread_btn_1, paths_readonly_btn_1, cnfg_prof_btn_var, paths_readonly_btn_var, loading_lbl_1):
        QThread.__init__(self)
        self.cnfg_prof_btn_var = cnfg_prof_btn_var
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
        self.btnx_main_1 = btnx_main_1
        self.stop_thread_btn_1 = stop_thread_btn_1
        self.paths_readonly_btn_1 = paths_readonly_btn_1
        self.cp0_count = 0
        self.cp0_fail_count = 0
        self.cp1_count = 0
        self.cp1_fail_count = 0
        self.path_0 = ''
        self.path_1 = ''
        self.write_call = ()
        self.paths_readonly_btn_var = paths_readonly_btn_var
        self.dest = ''
        self.bytes_count = 0
        self.bytes_count_str = ''
        self.bytes_count_1 = 0
        self.bytes_count_1_str = ''
        self.progress_str = ''
        self.progress  = ()
        self.siz_src = ''
        self.f_count = 0
        self.f_count_1 = 0
        self.f_count_str = 0
        self.f_count_1_str = 0
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_1 = loading_lbl_1

    def write_funk(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var
        try:
            shutil.copy2(self.path_0, self.path_1)
        except Exception as e:
            if debug_enabled is True:
                print('-- exception:', str(e).strip().encode('utf-8'))
            try:
                os.makedirs(os.path.dirname(self.path_1))
                shutil.copy2(self.path_0, self.path_1)
            except Exception as e:
                if debug_enabled is True:
                    print('-- exception:', str(e).strip().encode('utf-8'))
                output_str = str('error: ' + self.path_1).strip()
                try:
                    self.tb_1.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))

    def check_write(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var
        if os.path.exists(self.path_1) and os.path.exists(self.path_0):
            siz_src = str(os.path.getsize(self.path_0))
            siz_dest = str(os.path.getsize(self.path_1))
            if siz_src == siz_dest:
                if self.write_call is 0:
                    self.cp0_count += 1
                    output_str = str('copied new: (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                elif self.write_call is 1:
                    self.cp1_count += 1
                    output_str = str('updated new: (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                try:
                    self.tb_1.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))
            elif siz_src != siz_dest:
                if self.write_call is 0:
                    self.cp0_fail_count += 1
                    output_str = str('failed to copy new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                elif self.write_call is 1:
                    self.cp1_fail_count += 1
                    output_str = str('failed to update new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                try:
                    self.tb_1.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))
        elif not os.path.exists(self.path_1):
            self.cp0_fail_count += 1
            if self.write_call is 0:
                self.cp0_fail_count += 1
                output_str = str('failed to copy new (file does no exist in destination): ' + self.path_1).strip()
            if self.write_call is 1:
                self.cp1_fail_count += 1
                output_str = str('failed to update file (file does no exist in destination): ' + self.path_1).strip()
            try:
                self.tb_1.append(output_str)
            except Exception as e:
                if debug_enabled is True:
                    print('-- exception:', str(e).strip().encode('utf-8'))
        if debug_enabled is True:
            self.progress_output()

    def run(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op1_wait, confirm_op1_bool, thread_engaged_var
        if configuration_engaged is False:
            thread_engaged_var[1] = True
            thread_initialized_var[1] = True
            local_path = path_var[1]
            self.dest = dest_path_var[1]
            compare_bool = compare_bool_var[1]
            self.cnfg_prof_btn_var[0].setEnabled(False)
            self.cnfg_prof_btn_var[1].setEnabled(False)
            self.cnfg_prof_btn_var[2].setEnabled(False)
            self.cnfg_prof_btn_var[3].setEnabled(False)
            self.cnfg_prof_btn_var[4].setEnabled(False)
            self.cnfg_prof_btn_var[5].setEnabled(False)
            self.cnfg_prof_btn_var[6].setEnabled(False)
            self.cnfg_prof_btn_var[7].setEnabled(False)
            self.cnfg_prof_btn_var[8].setEnabled(False)
            self.cnfg_prof_btn_var[9].setEnabled(False)
            self.paths_readonly_btn_var[1].setEnabled(False)
            self.btnx_main_1.setIcon(QIcon(self.img_btnx_led_1))
            self.confirm_op1_tru.setIcon(QIcon(self.img_execute_true))
            self.confirm_op1_tru.setEnabled(True)
            self.stop_thread_btn_1.setEnabled(True)
            self.stop_thread_btn_1.setIcon(QIcon(self.img_stop_thread_true))
            while confirm_op1_wait is True:
                time.sleep(0.3)
            thread_initialized_var[1] = False
            confirm_op1_wait = True
            self.confirm_op1_tru.setIcon(QIcon(self.img_execute_false))
            self.confirm_op1_tru.setEnabled(False)
            if confirm_op1_bool is True:
                if debug_enabled is True:
                    print('-- ThreadClass1: confirm_op1_bool: accepted')
                self.btnx_main_1.setIcon(QIcon(self.img_btnx_led_2))
                change_var = False
                if os.path.exists(local_path) and os.path.exists(self.dest):
                    for dirname, subdirlist, filelist in os.walk(local_path):
                        for fname in filelist:
                            self.path_0 = os.path.join(dirname, fname)
                            self.path_1 = self.path_0.replace(local_path, '')
                            self.path_1 = self.dest + self.path_1
                            # Mode 0: Write Missing Files Only
                            if not os.path.exists(self.path_1):
                                self.path_0_item.append(self.path_0)
                                self.path_1_item.append(self.path_1)
                                self.siz_src = str(os.path.getsize(self.path_0))
                                siz_src_int = int(self.siz_src)
                                self.bytes_count = self.bytes_count + siz_src_int
                                self.f_count += 1
                                self.f_count_str = str(self.f_count)
                            # Mode 1: Write Missing & Update Outdated Files
                            elif os.path.exists(self.path_1) and os.path.exists(self.path_0) and compare_bool is True:
                                ma = os.path.getmtime(self.path_0)
                                mb = os.path.getmtime(self.path_1)
                                if mb < ma:
                                    self.path_0_item.append(self.path_0)
                                    self.path_1_item.append(self.path_1)
                                    self.siz_src = str(os.path.getsize(self.path_0))
                                    siz_src_int = int(self.siz_src)
                                    self.bytes_count = self.bytes_count + siz_src_int
                                    self.f_count += 1
                                    self.f_count_str = str(self.f_count)
                    self.bytes_count_str = str(self.bytes_count)
                    self.loading_lbl_1.resize(0, 7)
                    self.loading_lbl_1.show()
                    print('progress:', self.progress)
                    i = 0
                    for self.path_0_items in self.path_0_item:
                        self.path_0 = self.path_0_item[i]
                        self.path_1 = self.path_1_item[i]
                        if not os.path.exists(self.path_1):
                            self.siz_src = str(os.path.getsize(self.path_0))
                            siz_src_int = int(self.siz_src)
                            self.bytes_count_1 = self.bytes_count_1 + siz_src_int
                            self.bytes_count_1_str = str(self.bytes_count_1)
                            self.progress = (100 * float(self.bytes_count_1) / float(self.bytes_count))
                            self.progress_str = str(self.progress) + '%'
                            self.f_count_1 += 1
                            self.f_count_1_str = str(self.f_count_1)
                            change_var = True
                            self.write_funk()
                            self.write_call = 0
                            self.check_write()
                            self.progress_int = (int(self.progress) - 9)
                            self.loading_lbl_1.resize(self.progress_int, 8)
                        elif os.path.exists(self.path_1) and os.path.exists(self.path_0) and compare_bool is True:
                            ma = os.path.getmtime(self.path_0)
                            mb = os.path.getmtime(self.path_1)
                            if mb < ma:
                                self.siz_src = str(os.path.getsize(self.path_0))
                                siz_src_int = int(self.siz_src)
                                self.bytes_count_1 = self.bytes_count_1 + siz_src_int
                                self.bytes_count_1_str = str(self.bytes_count_1)
                                self.progress = (100 * float(self.bytes_count_1) / float(self.bytes_count))
                                self.progress_str = str(self.progress) + '%'
                                self.f_count_1 += 1
                                self.f_count_1_str = str(self.f_count_1)
                                change_var = True
                                self.write_funk()
                                self.write_call = 1
                                self.check_write()
                                self.progress_int = (int(self.progress) - 9)
                                self.loading_lbl_1.resize(self.progress_int, 8)

                        i += 1
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_1.resize(0, 7)
        self.loading_lbl_1.hide()
        self.summary()
        self.disengage()

    def progress_output(self):
        var_0 = str(self.f_count_1_str + '/' + self.f_count_str)
        var_1 = str(self.convert_bytes(self.bytes_count_1))
        var_2 = str(self.convert_bytes(self.bytes_count))
        var_3 = str(self.progress_str)
        var_4 = var_1 + '/' + var_2
        var_5 = var_4 + '  ' + var_3
        var_6 = var_0 + '  ' + var_5
        print(var_6)

    def convert_bytes(self, num):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return ("%3.1f %s" % (num, x))
            num /= 1024.0

    def summary(self):
        cp0_count_str = str(self.cp0_count)
        cp0_fail_count_str = str(self.cp0_fail_count)
        cp1_count_str = str(self.cp1_count)
        cp1_fail_count_str = str(self.cp1_fail_count)
        output_sum =  str('copied new: (' + cp0_count_str + ') | failed to copy new: (' + cp0_fail_count_str + ') | updated: (' + cp1_count_str + ')  | failed to update: (' + cp1_fail_count_str + ')').strip()
        if debug_enabled is True:
            print('-- ThreadClass3: ' + output_sum)
        self.tb_1.append(output_sum)
        self.tb_1.moveCursor(QTextCursor.End)
        self.tb_1.ensureCursorVisible()
        self.cp0_count = 0
        self.cp0_fail_count = 0
        self.cp1_count = 0
        self.cp1_fail_count = 0
        self.current_f = ''
        self.path_0 = ''
        self.path_1 = ''
        self.write_call = ()

    def disengage(self):
        self.btnx_main_1.setIcon(QIcon(self.img_btnx_led_0))
        self.stop_thread_btn_1.setIcon(QIcon(self.img_stop_thread_false))
        self.confirm_op1_tru.setIcon(QIcon(self.img_execute_false))
        self.stop_thread_btn_1.setEnabled(False)
        self.paths_readonly_btn_1.setEnabled(True)
        self.confirm_op1_tru.setEnabled(False)
        self.cnfg_prof_btn_var[0].setEnabled(True)
        self.cnfg_prof_btn_var[1].setEnabled(True)
        self.cnfg_prof_btn_var[2].setEnabled(True)
        self.cnfg_prof_btn_var[3].setEnabled(True)
        self.cnfg_prof_btn_var[4].setEnabled(True)
        self.cnfg_prof_btn_var[5].setEnabled(True)
        self.cnfg_prof_btn_var[6].setEnabled(True)
        self.cnfg_prof_btn_var[7].setEnabled(True)
        self.cnfg_prof_btn_var[8].setEnabled(True)
        self.cnfg_prof_btn_var[9].setEnabled(True)
        self.paths_readonly_btn_var[1].setEnabled(True)
        thread_engaged_var[1] = False
        confirm_op1_bool = False
        confirm_op1_wait = True
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_1.resize(0, 7)
        self.loading_lbl_1.hide()

    def stop_thr(self):
        global debug_enabled, confirm_op1_bool, confirm_op1_wait
        if not self.path_1 is '':
            output_str = 'terminated during: ' + self.path_1
            self.tb_1.append(output_str)
        if confirm_op1_bool is True:
            self.summary()
        self.disengage()
        if debug_enabled is True:
            print('-- confirm_op1 declined: (confirm_op1_bool)', confirm_op1_bool)
        self.terminate()


class ThreadClass2(QThread):
    def __init__(self, tb_2, confirm_op2_tru, img_btnx_led_0, img_btnx_led_1, img_btnx_led_2, img_execute_false, img_execute_true, img_stop_thread_false, img_stop_thread_true,
                 output_verbosity, btnx_main_2, stop_thread_btn_2, paths_readonly_btn_2, cnfg_prof_btn_var, paths_readonly_btn_var, loading_lbl_2):
        QThread.__init__(self)
        self.cnfg_prof_btn_var = cnfg_prof_btn_var
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
        self.btnx_main_2 = btnx_main_2
        self.stop_thread_btn_2 = stop_thread_btn_2
        self.paths_readonly_btn_2 = paths_readonly_btn_2
        self.cp0_count = 0
        self.cp0_fail_count = 0
        self.cp1_count = 0
        self.cp1_fail_count = 0
        self.path_0 = ''
        self.path_1 = ''
        self.write_call = ()
        self.paths_readonly_btn_var = paths_readonly_btn_var
        self.dest = ''
        self.bytes_count = 0
        self.bytes_count_str = ''
        self.bytes_count_1 = 0
        self.bytes_count_1_str = ''
        self.progress_str = ''
        self.progress  = ()
        self.siz_src = ''
        self.f_count = 0
        self.f_count_1 = 0
        self.f_count_str = 0
        self.f_count_1_str = 0
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_2 = loading_lbl_2

    def write_funk(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var
        try:
            shutil.copy2(self.path_0, self.path_1)
        except Exception as e:
            if debug_enabled is True:
                print('-- exception:', str(e).strip().encode('utf-8'))
            try:
                os.makedirs(os.path.dirname(self.path_1))
                shutil.copy2(self.path_0, self.path_1)
            except Exception as e:
                if debug_enabled is True:
                    print('-- exception:', str(e).strip().encode('utf-8'))
                output_str = str('error: ' + self.path_1).strip()
                try:
                    self.tb_2.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))

    def check_write(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var
        if os.path.exists(self.path_1) and os.path.exists(self.path_0):
            siz_src = str(os.path.getsize(self.path_0))
            siz_dest = str(os.path.getsize(self.path_1))
            if siz_src == siz_dest:
                if self.write_call is 0:
                    self.cp0_count += 1
                    output_str = str('copied new: (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                elif self.write_call is 1:
                    self.cp1_count += 1
                    output_str = str('updated new: (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                try:
                    self.tb_2.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))
            elif siz_src != siz_dest:
                if self.write_call is 0:
                    self.cp0_fail_count += 1
                    output_str = str('failed to copy new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                elif self.write_call is 1:
                    self.cp1_fail_count += 1
                    output_str = str('failed to update new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                try:
                    self.tb_2.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))
        elif not os.path.exists(self.path_1):
            self.cp0_fail_count += 1
            if self.write_call is 0:
                self.cp0_fail_count += 1
                output_str = str('failed to copy new (file does no exist in destination): ' + self.path_1).strip()
            if self.write_call is 1:
                self.cp1_fail_count += 1
                output_str = str('failed to update file (file does no exist in destination): ' + self.path_1).strip()
            try:
                self.tb_2.append(output_str)
            except Exception as e:
                if debug_enabled is True:
                    print('-- exception:', str(e).strip().encode('utf-8'))
        if debug_enabled is True:
            self.progress_output()

    def run(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op2_wait, confirm_op2_bool, thread_engaged_var
        if configuration_engaged is False:
            thread_engaged_var[2] = True
            thread_initialized_var[2] = True
            local_path = path_var[2]
            self.dest = dest_path_var[2]
            compare_bool = compare_bool_var[2]
            self.cnfg_prof_btn_var[0].setEnabled(False)
            self.cnfg_prof_btn_var[1].setEnabled(False)
            self.cnfg_prof_btn_var[2].setEnabled(False)
            self.cnfg_prof_btn_var[3].setEnabled(False)
            self.cnfg_prof_btn_var[4].setEnabled(False)
            self.cnfg_prof_btn_var[5].setEnabled(False)
            self.cnfg_prof_btn_var[6].setEnabled(False)
            self.cnfg_prof_btn_var[7].setEnabled(False)
            self.cnfg_prof_btn_var[8].setEnabled(False)
            self.cnfg_prof_btn_var[9].setEnabled(False)
            self.paths_readonly_btn_var[2].setEnabled(False)
            self.btnx_main_2.setIcon(QIcon(self.img_btnx_led_1))
            self.confirm_op2_tru.setIcon(QIcon(self.img_execute_true))
            self.confirm_op2_tru.setEnabled(True)
            self.stop_thread_btn_2.setEnabled(True)
            self.stop_thread_btn_2.setIcon(QIcon(self.img_stop_thread_true))
            while confirm_op2_wait is True:
                time.sleep(0.3)
            thread_initialized_var[2] = False
            confirm_op2_wait = True
            self.confirm_op2_tru.setIcon(QIcon(self.img_execute_false))
            self.confirm_op2_tru.setEnabled(False)
            if confirm_op2_bool is True:
                if debug_enabled is True:
                    print('-- ThreadClass2: confirm_op2_bool: accepted')
                self.btnx_main_2.setIcon(QIcon(self.img_btnx_led_2))
                change_var = False
                if os.path.exists(local_path) and os.path.exists(self.dest):
                    for dirname, subdirlist, filelist in os.walk(local_path):
                        for fname in filelist:
                            self.path_0 = os.path.join(dirname, fname)
                            self.path_1 = self.path_0.replace(local_path, '')
                            self.path_1 = self.dest + self.path_1
                            # Mode 0: Write Missing Files Only
                            if not os.path.exists(self.path_1):
                                self.path_0_item.append(self.path_0)
                                self.path_1_item.append(self.path_1)
                                self.siz_src = str(os.path.getsize(self.path_0))
                                siz_src_int = int(self.siz_src)
                                self.bytes_count = self.bytes_count + siz_src_int
                                self.f_count += 1
                                self.f_count_str = str(self.f_count)
                            # Mode 1: Write Missing & Update Outdated Files
                            elif os.path.exists(self.path_1) and os.path.exists(self.path_0) and compare_bool is True:
                                ma = os.path.getmtime(self.path_0)
                                mb = os.path.getmtime(self.path_1)
                                if mb < ma:
                                    self.path_0_item.append(self.path_0)
                                    self.path_1_item.append(self.path_1)
                                    self.siz_src = str(os.path.getsize(self.path_0))
                                    siz_src_int = int(self.siz_src)
                                    self.bytes_count = self.bytes_count + siz_src_int
                                    self.f_count += 1
                                    self.f_count_str = str(self.f_count)
                    self.bytes_count_str = str(self.bytes_count)
                    self.loading_lbl_2.resize(0, 7)
                    self.loading_lbl_2.show()
                    print('progress:', self.progress)
                    i = 0
                    for self.path_0_items in self.path_0_item:
                        self.path_0 = self.path_0_item[i]
                        self.path_1 = self.path_1_item[i]
                        if not os.path.exists(self.path_1):
                            self.siz_src = str(os.path.getsize(self.path_0))
                            siz_src_int = int(self.siz_src)
                            self.bytes_count_1 = self.bytes_count_1 + siz_src_int
                            self.bytes_count_1_str = str(self.bytes_count_1)
                            self.progress = (100 * float(self.bytes_count_1) / float(self.bytes_count))
                            self.progress_str = str(self.progress) + '%'
                            self.f_count_1 += 1
                            self.f_count_1_str = str(self.f_count_1)
                            change_var = True
                            self.write_funk()
                            self.write_call = 0
                            self.check_write()
                            self.progress_int = (int(self.progress) - 9)
                            self.loading_lbl_2.resize(self.progress_int, 8)
                        elif os.path.exists(self.path_1) and os.path.exists(self.path_0) and compare_bool is True:
                            ma = os.path.getmtime(self.path_0)
                            mb = os.path.getmtime(self.path_1)
                            if mb < ma:
                                self.siz_src = str(os.path.getsize(self.path_0))
                                siz_src_int = int(self.siz_src)
                                self.bytes_count_1 = self.bytes_count_1 + siz_src_int
                                self.bytes_count_1_str = str(self.bytes_count_1)
                                self.progress = (100 * float(self.bytes_count_1) / float(self.bytes_count))
                                self.progress_str = str(self.progress) + '%'
                                self.f_count_1 += 1
                                self.f_count_1_str = str(self.f_count_1)
                                change_var = True
                                self.write_funk()
                                self.write_call = 1
                                self.check_write()
                                self.progress_int = (int(self.progress) - 9)
                                self.loading_lbl_2.resize(self.progress_int, 8)

                        i += 1
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_2.resize(0, 7)
        self.loading_lbl_2.hide()
        self.summary()
        self.disengage()

    def progress_output(self):
        var_0 = str(self.f_count_1_str + '/' + self.f_count_str)
        var_1 = str(self.convert_bytes(self.bytes_count_1))
        var_2 = str(self.convert_bytes(self.bytes_count))
        var_3 = str(self.progress_str)
        var_4 = var_1 + '/' + var_2
        var_5 = var_4 + '  ' + var_3
        var_6 = var_0 + '  ' + var_5
        print(var_6)

    def convert_bytes(self, num):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return ("%3.1f %s" % (num, x))
            num /= 1024.0

    def summary(self):
        cp0_count_str = str(self.cp0_count)
        cp0_fail_count_str = str(self.cp0_fail_count)
        cp1_count_str = str(self.cp1_count)
        cp1_fail_count_str = str(self.cp1_fail_count)
        output_sum =  str('copied new: (' + cp0_count_str + ') | failed to copy new: (' + cp0_fail_count_str + ') | updated: (' + cp1_count_str + ')  | failed to update: (' + cp1_fail_count_str + ')').strip()
        if debug_enabled is True:
            print('-- ThreadClass3: ' + output_sum)
        self.tb_2.append(output_sum)
        self.tb_2.moveCursor(QTextCursor.End)
        self.tb_2.ensureCursorVisible()
        self.cp0_count = 0
        self.cp0_fail_count = 0
        self.cp1_count = 0
        self.cp1_fail_count = 0
        self.current_f = ''
        self.path_0 = ''
        self.path_1 = ''
        self.write_call = ()

    def disengage(self):
        self.btnx_main_2.setIcon(QIcon(self.img_btnx_led_0))
        self.stop_thread_btn_2.setIcon(QIcon(self.img_stop_thread_false))
        self.confirm_op2_tru.setIcon(QIcon(self.img_execute_false))
        self.stop_thread_btn_2.setEnabled(False)
        self.paths_readonly_btn_2.setEnabled(True)
        self.confirm_op2_tru.setEnabled(False)
        self.cnfg_prof_btn_var[0].setEnabled(True)
        self.cnfg_prof_btn_var[1].setEnabled(True)
        self.cnfg_prof_btn_var[2].setEnabled(True)
        self.cnfg_prof_btn_var[3].setEnabled(True)
        self.cnfg_prof_btn_var[4].setEnabled(True)
        self.cnfg_prof_btn_var[5].setEnabled(True)
        self.cnfg_prof_btn_var[6].setEnabled(True)
        self.cnfg_prof_btn_var[7].setEnabled(True)
        self.cnfg_prof_btn_var[8].setEnabled(True)
        self.cnfg_prof_btn_var[9].setEnabled(True)
        self.paths_readonly_btn_var[0].setEnabled(True)
        thread_engaged_var[2] = False
        confirm_op2_bool = False
        confirm_op2_wait = True
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_2.resize(0, 7)
        self.loading_lbl_2.hide()

    def stop_thr(self):
        global debug_enabled, confirm_op2_bool, confirm_op2_wait
        if not self.path_1 is '':
            output_str = 'terminated during: ' + self.path_1
            self.tb_2.append(output_str)
        if confirm_op2_bool is True:
            self.summary()
        self.disengage()
        if debug_enabled is True:
            print('-- confirm_op2 declined: (confirm_op2_bool)', confirm_op2_bool)
        self.terminate()


class ThreadClass3(QThread):
    def __init__(self, tb_3, confirm_op3_tru, img_btnx_led_0, img_btnx_led_1, img_btnx_led_2, img_execute_false, img_execute_true, img_stop_thread_false, img_stop_thread_true,
                 output_verbosity, btnx_main_3, stop_thread_btn_3, paths_readonly_btn_3, cnfg_prof_btn_var, paths_readonly_btn_var, loading_lbl_3):
        QThread.__init__(self)
        self.cnfg_prof_btn_var = cnfg_prof_btn_var
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
        self.btnx_main_3 = btnx_main_3
        self.stop_thread_btn_3 = stop_thread_btn_3
        self.paths_readonly_btn_3 = paths_readonly_btn_3
        self.cp0_count = 0
        self.cp0_fail_count = 0
        self.cp1_count = 0
        self.cp1_fail_count = 0
        self.path_0 = ''
        self.path_1 = ''
        self.write_call = ()
        self.paths_readonly_btn_var = paths_readonly_btn_var
        self.dest = ''
        self.bytes_count = 0
        self.bytes_count_str = ''
        self.bytes_count_1 = 0
        self.bytes_count_1_str = ''
        self.progress_str = ''
        self.progress  = ()
        self.siz_src = ''
        self.f_count = 0
        self.f_count_1 = 0
        self.f_count_str = 0
        self.f_count_1_str = 0
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_3 = loading_lbl_3

    def write_funk(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var
        try:
            shutil.copy2(self.path_0, self.path_1)
        except Exception as e:
            if debug_enabled is True:
                print('-- exception:', str(e).strip().encode('utf-8'))
            try:
                os.makedirs(os.path.dirname(self.path_1))
                shutil.copy2(self.path_0, self.path_1)
            except Exception as e:
                if debug_enabled is True:
                    print('-- exception:', str(e).strip().encode('utf-8'))
                output_str = str('error: ' + self.path_1).strip()
                try:
                    self.tb_3.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))

    def check_write(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var
        if os.path.exists(self.path_1) and os.path.exists(self.path_0):
            siz_src = str(os.path.getsize(self.path_0))
            siz_dest = str(os.path.getsize(self.path_1))
            if siz_src == siz_dest:
                if self.write_call is 0:
                    self.cp0_count += 1
                    output_str = str('copied new: (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                elif self.write_call is 1:
                    self.cp1_count += 1
                    output_str = str('updated new: (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                try:
                    self.tb_3.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))
            elif siz_src != siz_dest:
                if self.write_call is 0:
                    self.cp0_fail_count += 1
                    output_str = str('failed to copy new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                elif self.write_call is 1:
                    self.cp1_fail_count += 1
                    output_str = str('failed to update new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                try:
                    self.tb_3.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))
        elif not os.path.exists(self.path_1):
            self.cp0_fail_count += 1
            if self.write_call is 0:
                self.cp0_fail_count += 1
                output_str = str('failed to copy new (file does no exist in destination): ' + self.path_1).strip()
            if self.write_call is 1:
                self.cp1_fail_count += 1
                output_str = str('failed to update file (file does no exist in destination): ' + self.path_1).strip()
            try:
                self.tb_3.append(output_str)
            except Exception as e:
                if debug_enabled is True:
                    print('-- exception:', str(e).strip().encode('utf-8'))
        if debug_enabled is True:
            self.progress_output()

    def run(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op3_wait, confirm_op3_bool, thread_engaged_var
        if configuration_engaged is False:
            thread_engaged_var[3] = True
            thread_initialized_var[3] = True
            local_path = path_var[3]
            self.dest = dest_path_var[3]
            compare_bool = compare_bool_var[3]
            self.cnfg_prof_btn_var[0].setEnabled(False)
            self.cnfg_prof_btn_var[1].setEnabled(False)
            self.cnfg_prof_btn_var[2].setEnabled(False)
            self.cnfg_prof_btn_var[3].setEnabled(False)
            self.cnfg_prof_btn_var[4].setEnabled(False)
            self.cnfg_prof_btn_var[5].setEnabled(False)
            self.cnfg_prof_btn_var[6].setEnabled(False)
            self.cnfg_prof_btn_var[7].setEnabled(False)
            self.cnfg_prof_btn_var[8].setEnabled(False)
            self.cnfg_prof_btn_var[9].setEnabled(False)
            self.paths_readonly_btn_var[3].setEnabled(False)
            self.btnx_main_3.setIcon(QIcon(self.img_btnx_led_1))
            self.confirm_op3_tru.setIcon(QIcon(self.img_execute_true))
            self.confirm_op3_tru.setEnabled(True)
            self.stop_thread_btn_3.setEnabled(True)
            self.stop_thread_btn_3.setIcon(QIcon(self.img_stop_thread_true))
            while confirm_op3_wait is True:
                time.sleep(0.3)
            thread_initialized_var[3] = False
            confirm_op3_wait = True
            self.confirm_op3_tru.setIcon(QIcon(self.img_execute_false))
            self.confirm_op3_tru.setEnabled(False)
            if confirm_op3_bool is True:
                if debug_enabled is True:
                    print('-- ThreadClass3: confirm_op3_bool: accepted')
                self.btnx_main_3.setIcon(QIcon(self.img_btnx_led_2))
                change_var = False
                if os.path.exists(local_path) and os.path.exists(self.dest):
                    for dirname, subdirlist, filelist in os.walk(local_path):
                        for fname in filelist:
                            self.path_0 = os.path.join(dirname, fname)
                            self.path_1 = self.path_0.replace(local_path, '')
                            self.path_1 = self.dest + self.path_1
                            # Mode 0: Write Missing Files Only
                            if not os.path.exists(self.path_1):
                                self.path_0_item.append(self.path_0)
                                self.path_1_item.append(self.path_1)
                                self.siz_src = str(os.path.getsize(self.path_0))
                                siz_src_int = int(self.siz_src)
                                self.bytes_count = self.bytes_count + siz_src_int
                                self.f_count += 1
                                self.f_count_str = str(self.f_count)
                            # Mode 1: Write Missing & Update Outdated Files
                            elif os.path.exists(self.path_1) and os.path.exists(self.path_0) and compare_bool is True:
                                ma = os.path.getmtime(self.path_0)
                                mb = os.path.getmtime(self.path_1)
                                if mb < ma:
                                    self.path_0_item.append(self.path_0)
                                    self.path_1_item.append(self.path_1)
                                    self.siz_src = str(os.path.getsize(self.path_0))
                                    siz_src_int = int(self.siz_src)
                                    self.bytes_count = self.bytes_count + siz_src_int
                                    self.f_count += 1
                                    self.f_count_str = str(self.f_count)
                    self.bytes_count_str = str(self.bytes_count)
                    self.loading_lbl_3.resize(0, 7)
                    self.loading_lbl_3.show()
                    print('progress:', self.progress)
                    i = 0
                    for self.path_0_items in self.path_0_item:
                        self.path_0 = self.path_0_item[i]
                        self.path_1 = self.path_1_item[i]
                        if not os.path.exists(self.path_1):
                            self.siz_src = str(os.path.getsize(self.path_0))
                            siz_src_int = int(self.siz_src)
                            self.bytes_count_1 = self.bytes_count_1 + siz_src_int
                            self.bytes_count_1_str = str(self.bytes_count_1)
                            self.progress = (100 * float(self.bytes_count_1) / float(self.bytes_count))
                            self.progress_str = str(self.progress) + '%'
                            self.f_count_1 += 1
                            self.f_count_1_str = str(self.f_count_1)
                            change_var = True
                            self.write_funk()
                            self.write_call = 0
                            self.check_write()
                            self.progress_int = (int(self.progress) - 9)
                            self.loading_lbl_3.resize(self.progress_int, 8)
                        elif os.path.exists(self.path_1) and os.path.exists(self.path_0) and compare_bool is True:
                            ma = os.path.getmtime(self.path_0)
                            mb = os.path.getmtime(self.path_1)
                            if mb < ma:
                                self.siz_src = str(os.path.getsize(self.path_0))
                                siz_src_int = int(self.siz_src)
                                self.bytes_count_1 = self.bytes_count_1 + siz_src_int
                                self.bytes_count_1_str = str(self.bytes_count_1)
                                self.progress = (100 * float(self.bytes_count_1) / float(self.bytes_count))
                                self.progress_str = str(self.progress) + '%'
                                self.f_count_1 += 1
                                self.f_count_1_str = str(self.f_count_1)
                                change_var = True
                                self.write_funk()
                                self.write_call = 1
                                self.check_write()
                                self.progress_int = (int(self.progress) - 9)
                                self.loading_lbl_3.resize(self.progress_int, 8)

                        i += 1
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_3.resize(0, 7)
        self.loading_lbl_3.hide()
        self.summary()
        self.disengage()

    def progress_output(self):
        var_0 = str(self.f_count_1_str + '/' + self.f_count_str)
        var_1 = str(self.convert_bytes(self.bytes_count_1))
        var_2 = str(self.convert_bytes(self.bytes_count))
        var_3 = str(self.progress_str)
        var_4 = var_1 + '/' + var_2
        var_5 = var_4 + '  ' + var_3
        var_6 = var_0 + '  ' + var_5
        print(var_6)

    def convert_bytes(self, num):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return ("%3.1f %s" % (num, x))
            num /= 1024.0

    def summary(self):
        cp0_count_str = str(self.cp0_count)
        cp0_fail_count_str = str(self.cp0_fail_count)
        cp1_count_str = str(self.cp1_count)
        cp1_fail_count_str = str(self.cp1_fail_count)
        output_sum =  str('copied new: (' + cp0_count_str + ') | failed to copy new: (' + cp0_fail_count_str + ') | updated: (' + cp1_count_str + ')  | failed to update: (' + cp1_fail_count_str + ')').strip()
        if debug_enabled is True:
            print('-- ThreadClass3: ' + output_sum)
        self.tb_3.append(output_sum)
        self.tb_3.moveCursor(QTextCursor.End)
        self.tb_3.ensureCursorVisible()
        self.cp0_count = 0
        self.cp0_fail_count = 0
        self.cp1_count = 0
        self.cp1_fail_count = 0
        self.current_f = ''
        self.path_0 = ''
        self.path_1 = ''
        self.write_call = ()

    def disengage(self):
        self.btnx_main_3.setIcon(QIcon(self.img_btnx_led_0))
        self.stop_thread_btn_3.setIcon(QIcon(self.img_stop_thread_false))
        self.confirm_op3_tru.setIcon(QIcon(self.img_execute_false))
        self.stop_thread_btn_3.setEnabled(False)
        self.paths_readonly_btn_3.setEnabled(True)
        self.confirm_op3_tru.setEnabled(False)
        self.cnfg_prof_btn_var[0].setEnabled(True)
        self.cnfg_prof_btn_var[1].setEnabled(True)
        self.cnfg_prof_btn_var[2].setEnabled(True)
        self.cnfg_prof_btn_var[3].setEnabled(True)
        self.cnfg_prof_btn_var[4].setEnabled(True)
        self.cnfg_prof_btn_var[5].setEnabled(True)
        self.cnfg_prof_btn_var[6].setEnabled(True)
        self.cnfg_prof_btn_var[7].setEnabled(True)
        self.cnfg_prof_btn_var[8].setEnabled(True)
        self.cnfg_prof_btn_var[9].setEnabled(True)
        self.paths_readonly_btn_var[3].setEnabled(True)
        thread_engaged_var[3] = False
        confirm_op3_bool = False
        confirm_op3_wait = True
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_3.resize(0, 7)
        self.loading_lbl_3.hide()

    def stop_thr(self):
        global debug_enabled, confirm_op3_bool, confirm_op3_wait
        if not self.path_1 is '':
            output_str = 'terminated during: ' + self.path_1
            self.tb_3.append(output_str)
        if confirm_op3_bool is True:
            self.summary()
        self.disengage()
        if debug_enabled is True:
            print('-- confirm_op3 declined: (confirm_op3_bool)', confirm_op3_bool)
        self.terminate()


class ThreadClass4(QThread):
    def __init__(self, tb_4, confirm_op4_tru, img_btnx_led_0, img_btnx_led_1, img_btnx_led_2, img_execute_false, img_execute_true, img_stop_thread_false, img_stop_thread_true,
                 output_verbosity, btnx_main_4, stop_thread_btn_4, paths_readonly_btn_4, cnfg_prof_btn_var, paths_readonly_btn_var, loading_lbl_4):
        QThread.__init__(self)
        self.cnfg_prof_btn_var = cnfg_prof_btn_var
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
        self.btnx_main_4 = btnx_main_4
        self.stop_thread_btn_4 = stop_thread_btn_4
        self.paths_readonly_btn_4 = paths_readonly_btn_4
        self.cp0_count = 0
        self.cp0_fail_count = 0
        self.cp1_count = 0
        self.cp1_fail_count = 0
        self.path_0 = ''
        self.path_1 = ''
        self.write_call = ()
        self.paths_readonly_btn_var = paths_readonly_btn_var
        self.dest = ''
        self.bytes_count = 0
        self.bytes_count_str = ''
        self.bytes_count_1 = 0
        self.bytes_count_1_str = ''
        self.progress_str = ''
        self.progress  = ()
        self.siz_src = ''
        self.f_count = 0
        self.f_count_1 = 0
        self.f_count_str = 0
        self.f_count_1_str = 0
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_4 = loading_lbl_4

    def write_funk(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var
        try:
            shutil.copy2(self.path_0, self.path_1)
        except Exception as e:
            if debug_enabled is True:
                print('-- exception:', str(e).strip().encode('utf-8'))
            try:
                os.makedirs(os.path.dirname(self.path_1))
                shutil.copy2(self.path_0, self.path_1)
            except Exception as e:
                if debug_enabled is True:
                    print('-- exception:', str(e).strip().encode('utf-8'))
                output_str = str('error: ' + self.path_1).strip()
                try:
                    self.tb_4.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))

    def check_write(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var
        if os.path.exists(self.path_1) and os.path.exists(self.path_0):
            siz_src = str(os.path.getsize(self.path_0))
            siz_dest = str(os.path.getsize(self.path_1))
            if siz_src == siz_dest:
                if self.write_call is 0:
                    self.cp0_count += 1
                    output_str = str('copied new: (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                elif self.write_call is 1:
                    self.cp1_count += 1
                    output_str = str('updated new: (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                try:
                    self.tb_4.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))
            elif siz_src != siz_dest:
                if self.write_call is 0:
                    self.cp0_fail_count += 1
                    output_str = str('failed to copy new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                elif self.write_call is 1:
                    self.cp1_fail_count += 1
                    output_str = str('failed to update new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                try:
                    self.tb_4.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))
        elif not os.path.exists(self.path_1):
            self.cp0_fail_count += 1
            if self.write_call is 0:
                self.cp0_fail_count += 1
                output_str = str('failed to copy new (file does no exist in destination): ' + self.path_1).strip()
            if self.write_call is 1:
                self.cp1_fail_count += 1
                output_str = str('failed to update file (file does no exist in destination): ' + self.path_1).strip()
            try:
                self.tb_4.append(output_str)
            except Exception as e:
                if debug_enabled is True:
                    print('-- exception:', str(e).strip().encode('utf-8'))
        if debug_enabled is True:
            self.progress_output()

    def run(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op4_wait, confirm_op4_bool, thread_engaged_var
        if configuration_engaged is False:
            thread_engaged_var[4] = True
            thread_initialized_var[4] = True
            local_path = path_var[4]
            self.dest = dest_path_var[4]
            compare_bool = compare_bool_var[4]
            self.cnfg_prof_btn_var[0].setEnabled(False)
            self.cnfg_prof_btn_var[1].setEnabled(False)
            self.cnfg_prof_btn_var[2].setEnabled(False)
            self.cnfg_prof_btn_var[3].setEnabled(False)
            self.cnfg_prof_btn_var[4].setEnabled(False)
            self.cnfg_prof_btn_var[5].setEnabled(False)
            self.cnfg_prof_btn_var[6].setEnabled(False)
            self.cnfg_prof_btn_var[7].setEnabled(False)
            self.cnfg_prof_btn_var[8].setEnabled(False)
            self.cnfg_prof_btn_var[9].setEnabled(False)
            self.paths_readonly_btn_var[4].setEnabled(False)
            self.btnx_main_4.setIcon(QIcon(self.img_btnx_led_1))
            self.confirm_op4_tru.setIcon(QIcon(self.img_execute_true))
            self.confirm_op4_tru.setEnabled(True)
            self.stop_thread_btn_4.setEnabled(True)
            self.stop_thread_btn_4.setIcon(QIcon(self.img_stop_thread_true))
            while confirm_op4_wait is True:
                time.sleep(0.3)
            thread_initialized_var[4] = False
            confirm_op4_wait = True
            self.confirm_op4_tru.setIcon(QIcon(self.img_execute_false))
            self.confirm_op4_tru.setEnabled(False)
            if confirm_op4_bool is True:
                if debug_enabled is True:
                    print('-- ThreadClass4: confirm_op4_bool: accepted')
                self.btnx_main_4.setIcon(QIcon(self.img_btnx_led_2))
                change_var = False
                if os.path.exists(local_path) and os.path.exists(self.dest):
                    for dirname, subdirlist, filelist in os.walk(local_path):
                        for fname in filelist:
                            self.path_0 = os.path.join(dirname, fname)
                            self.path_1 = self.path_0.replace(local_path, '')
                            self.path_1 = self.dest + self.path_1
                            # Mode 0: Write Missing Files Only
                            if not os.path.exists(self.path_1):
                                self.path_0_item.append(self.path_0)
                                self.path_1_item.append(self.path_1)
                                self.siz_src = str(os.path.getsize(self.path_0))
                                siz_src_int = int(self.siz_src)
                                self.bytes_count = self.bytes_count + siz_src_int
                                self.f_count += 1
                                self.f_count_str = str(self.f_count)
                            # Mode 1: Write Missing & Update Outdated Files
                            elif os.path.exists(self.path_1) and os.path.exists(self.path_0) and compare_bool is True:
                                ma = os.path.getmtime(self.path_0)
                                mb = os.path.getmtime(self.path_1)
                                if mb < ma:
                                    self.path_0_item.append(self.path_0)
                                    self.path_1_item.append(self.path_1)
                                    self.siz_src = str(os.path.getsize(self.path_0))
                                    siz_src_int = int(self.siz_src)
                                    self.bytes_count = self.bytes_count + siz_src_int
                                    self.f_count += 1
                                    self.f_count_str = str(self.f_count)
                    self.bytes_count_str = str(self.bytes_count)
                    self.loading_lbl_4.resize(0, 7)
                    self.loading_lbl_4.show()
                    print('progress:', self.progress)
                    i = 0
                    for self.path_0_items in self.path_0_item:
                        self.path_0 = self.path_0_item[i]
                        self.path_1 = self.path_1_item[i]
                        if not os.path.exists(self.path_1):
                            self.siz_src = str(os.path.getsize(self.path_0))
                            siz_src_int = int(self.siz_src)
                            self.bytes_count_1 = self.bytes_count_1 + siz_src_int
                            self.bytes_count_1_str = str(self.bytes_count_1)
                            self.progress = (100 * float(self.bytes_count_1) / float(self.bytes_count))
                            self.progress_str = str(self.progress) + '%'
                            self.f_count_1 += 1
                            self.f_count_1_str = str(self.f_count_1)
                            change_var = True
                            self.write_funk()
                            self.write_call = 0
                            self.check_write()
                            self.progress_int = (int(self.progress) - 9)
                            self.loading_lbl_4.resize(self.progress_int, 8)
                        elif os.path.exists(self.path_1) and os.path.exists(self.path_0) and compare_bool is True:
                            ma = os.path.getmtime(self.path_0)
                            mb = os.path.getmtime(self.path_1)
                            if mb < ma:
                                self.siz_src = str(os.path.getsize(self.path_0))
                                siz_src_int = int(self.siz_src)
                                self.bytes_count_1 = self.bytes_count_1 + siz_src_int
                                self.bytes_count_1_str = str(self.bytes_count_1)
                                self.progress = (100 * float(self.bytes_count_1) / float(self.bytes_count))
                                self.progress_str = str(self.progress) + '%'
                                self.f_count_1 += 1
                                self.f_count_1_str = str(self.f_count_1)
                                change_var = True
                                self.write_funk()
                                self.write_call = 1
                                self.check_write()
                                self.progress_int = (int(self.progress) - 9)
                                self.loading_lbl_4.resize(self.progress_int, 8)

                        i += 1
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_4.resize(0, 7)
        self.loading_lbl_4.hide()
        self.summary()
        self.disengage()

    def progress_output(self):
        var_0 = str(self.f_count_1_str + '/' + self.f_count_str)
        var_1 = str(self.convert_bytes(self.bytes_count_1))
        var_2 = str(self.convert_bytes(self.bytes_count))
        var_3 = str(self.progress_str)
        var_4 = var_1 + '/' + var_2
        var_5 = var_4 + '  ' + var_3
        var_6 = var_0 + '  ' + var_5
        print(var_6)

    def convert_bytes(self, num):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return ("%3.1f %s" % (num, x))
            num /= 1024.0

    def summary(self):
        cp0_count_str = str(self.cp0_count)
        cp0_fail_count_str = str(self.cp0_fail_count)
        cp1_count_str = str(self.cp1_count)
        cp1_fail_count_str = str(self.cp1_fail_count)
        output_sum =  str('copied new: (' + cp0_count_str + ') | failed to copy new: (' + cp0_fail_count_str + ') | updated: (' + cp1_count_str + ')  | failed to update: (' + cp1_fail_count_str + ')').strip()
        if debug_enabled is True:
            print('-- ThreadClass3: ' + output_sum)
        self.tb_4.append(output_sum)
        self.tb_4.moveCursor(QTextCursor.End)
        self.tb_4.ensureCursorVisible()
        self.cp0_count = 0
        self.cp0_fail_count = 0
        self.cp1_count = 0
        self.cp1_fail_count = 0
        self.current_f = ''
        self.path_0 = ''
        self.path_1 = ''
        self.write_call = ()

    def disengage(self):
        self.btnx_main_4.setIcon(QIcon(self.img_btnx_led_0))
        self.stop_thread_btn_4.setIcon(QIcon(self.img_stop_thread_false))
        self.confirm_op4_tru.setIcon(QIcon(self.img_execute_false))
        self.stop_thread_btn_4.setEnabled(False)
        self.paths_readonly_btn_4.setEnabled(True)
        self.confirm_op4_tru.setEnabled(False)
        self.cnfg_prof_btn_var[0].setEnabled(True)
        self.cnfg_prof_btn_var[1].setEnabled(True)
        self.cnfg_prof_btn_var[2].setEnabled(True)
        self.cnfg_prof_btn_var[3].setEnabled(True)
        self.cnfg_prof_btn_var[4].setEnabled(True)
        self.cnfg_prof_btn_var[5].setEnabled(True)
        self.cnfg_prof_btn_var[6].setEnabled(True)
        self.cnfg_prof_btn_var[7].setEnabled(True)
        self.cnfg_prof_btn_var[8].setEnabled(True)
        self.cnfg_prof_btn_var[9].setEnabled(True)
        self.paths_readonly_btn_var[4].setEnabled(True)
        thread_engaged_var[4] = False
        confirm_op4_bool = False
        confirm_op4_wait = True
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_4.resize(0, 7)
        self.loading_lbl_4.hide()

    def stop_thr(self):
        global debug_enabled, confirm_op4_bool, confirm_op4_wait
        if not self.path_1 is '':
            output_str = 'terminated during: ' + self.path_1
            self.tb_4.append(output_str)
        if confirm_op4_bool is True:
            self.summary()
        self.disengage()
        if debug_enabled is True:
            print('-- confirm_op4 declined: (confirm_op4_bool)', confirm_op4_bool)
        self.terminate()


class ThreadClass5(QThread):
    def __init__(self, tb_5, confirm_op5_tru, img_btnx_led_0, img_btnx_led_1, img_btnx_led_2, img_execute_false, img_execute_true, img_stop_thread_false, img_stop_thread_true,
                 output_verbosity, btnx_main_5, stop_thread_btn_5, paths_readonly_btn_5, cnfg_prof_btn_var, paths_readonly_btn_var, loading_lbl_5):
        QThread.__init__(self)
        self.cnfg_prof_btn_var = cnfg_prof_btn_var
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
        self.btnx_main_5 = btnx_main_5
        self.stop_thread_btn_5 = stop_thread_btn_5
        self.paths_readonly_btn_5 = paths_readonly_btn_5
        self.cp0_count = 0
        self.cp0_fail_count = 0
        self.cp1_count = 0
        self.cp1_fail_count = 0
        self.path_0 = ''
        self.path_1 = ''
        self.write_call = ()
        self.paths_readonly_btn_var = paths_readonly_btn_var
        self.dest = ''
        self.bytes_count = 0
        self.bytes_count_str = ''
        self.bytes_count_1 = 0
        self.bytes_count_1_str = ''
        self.progress_str = ''
        self.progress  = ()
        self.siz_src = ''
        self.f_count = 0
        self.f_count_1 = 0
        self.f_count_str = 0
        self.f_count_1_str = 0
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_5 = loading_lbl_5

    def write_funk(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var
        try:
            shutil.copy2(self.path_0, self.path_1)
        except Exception as e:
            if debug_enabled is True:
                print('-- exception:', str(e).strip().encode('utf-8'))
            try:
                os.makedirs(os.path.dirname(self.path_1))
                shutil.copy2(self.path_0, self.path_1)
            except Exception as e:
                if debug_enabled is True:
                    print('-- exception:', str(e).strip().encode('utf-8'))
                output_str = str('error: ' + self.path_1).strip()
                try:
                    self.tb_5.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))

    def check_write(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op0_wait, confirm_op0_bool, thread_engaged_var
        if os.path.exists(self.path_1) and os.path.exists(self.path_0):
            siz_src = str(os.path.getsize(self.path_0))
            siz_dest = str(os.path.getsize(self.path_1))
            if siz_src == siz_dest:
                if self.write_call is 0:
                    self.cp0_count += 1
                    output_str = str('copied new: (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                elif self.write_call is 1:
                    self.cp1_count += 1
                    output_str = str('updated new: (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                try:
                    self.tb_5.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))
            elif siz_src != siz_dest:
                if self.write_call is 0:
                    self.cp0_fail_count += 1
                    output_str = str('failed to copy new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                elif self.write_call is 1:
                    self.cp1_fail_count += 1
                    output_str = str('failed to update new (failed bytes check, possible false negative as file exists): (' + siz_dest + '/' + siz_src + ' bytes) ' + self.path_1).strip()
                try:
                    self.tb_5.append(output_str)
                except Exception as e:
                    if debug_enabled is True:
                        print('-- exception:', str(e).strip().encode('utf-8'))
        elif not os.path.exists(self.path_1):
            self.cp0_fail_count += 1
            if self.write_call is 0:
                self.cp0_fail_count += 1
                output_str = str('failed to copy new (file does no exist in destination): ' + self.path_1).strip()
            if self.write_call is 1:
                self.cp1_fail_count += 1
                output_str = str('failed to update file (file does no exist in destination): ' + self.path_1).strip()
            try:
                self.tb_5.append(output_str)
            except Exception as e:
                if debug_enabled is True:
                    print('-- exception:', str(e).strip().encode('utf-8'))
        if debug_enabled is True:
            self.progress_output()

    def run(self):
        global debug_enabled, path_var, dest_path_var, configuration_engaged, confirm_op5_wait, confirm_op5_bool, thread_engaged_var
        if configuration_engaged is False:
            thread_engaged_var[5] = True
            thread_initialized_var[5] = True
            local_path = path_var[5]
            self.dest = dest_path_var[5]
            compare_bool = compare_bool_var[5]
            self.cnfg_prof_btn_var[0].setEnabled(False)
            self.cnfg_prof_btn_var[1].setEnabled(False)
            self.cnfg_prof_btn_var[2].setEnabled(False)
            self.cnfg_prof_btn_var[3].setEnabled(False)
            self.cnfg_prof_btn_var[4].setEnabled(False)
            self.cnfg_prof_btn_var[5].setEnabled(False)
            self.cnfg_prof_btn_var[6].setEnabled(False)
            self.cnfg_prof_btn_var[7].setEnabled(False)
            self.cnfg_prof_btn_var[8].setEnabled(False)
            self.cnfg_prof_btn_var[9].setEnabled(False)
            self.paths_readonly_btn_var[5].setEnabled(False)
            self.btnx_main_5.setIcon(QIcon(self.img_btnx_led_1))
            self.confirm_op5_tru.setIcon(QIcon(self.img_execute_true))
            self.confirm_op5_tru.setEnabled(True)
            self.stop_thread_btn_5.setEnabled(True)
            self.stop_thread_btn_5.setIcon(QIcon(self.img_stop_thread_true))
            while confirm_op5_wait is True:
                time.sleep(0.3)
            thread_initialized_var[5] = False
            confirm_op5_wait = True
            self.confirm_op5_tru.setIcon(QIcon(self.img_execute_false))
            self.confirm_op5_tru.setEnabled(False)
            if confirm_op5_bool is True:
                if debug_enabled is True:
                    print('-- ThreadClass5: confirm_op5_bool: accepted')
                self.btnx_main_5.setIcon(QIcon(self.img_btnx_led_2))
                change_var = False
                if os.path.exists(local_path) and os.path.exists(self.dest):
                    for dirname, subdirlist, filelist in os.walk(local_path):
                        for fname in filelist:
                            self.path_0 = os.path.join(dirname, fname)
                            self.path_1 = self.path_0.replace(local_path, '')
                            self.path_1 = self.dest + self.path_1
                            # Mode 0: Write Missing Files Only
                            if not os.path.exists(self.path_1):
                                self.path_0_item.append(self.path_0)
                                self.path_1_item.append(self.path_1)
                                self.siz_src = str(os.path.getsize(self.path_0))
                                siz_src_int = int(self.siz_src)
                                self.bytes_count = self.bytes_count + siz_src_int
                                self.f_count += 1
                                self.f_count_str = str(self.f_count)
                            # Mode 1: Write Missing & Update Outdated Files
                            elif os.path.exists(self.path_1) and os.path.exists(self.path_0) and compare_bool is True:
                                ma = os.path.getmtime(self.path_0)
                                mb = os.path.getmtime(self.path_1)
                                if mb < ma:
                                    self.path_0_item.append(self.path_0)
                                    self.path_1_item.append(self.path_1)
                                    self.siz_src = str(os.path.getsize(self.path_0))
                                    siz_src_int = int(self.siz_src)
                                    self.bytes_count = self.bytes_count + siz_src_int
                                    self.f_count += 1
                                    self.f_count_str = str(self.f_count)
                    self.bytes_count_str = str(self.bytes_count)
                    self.loading_lbl_5.resize(0, 7)
                    self.loading_lbl_5.show()
                    print('progress:', self.progress)
                    i = 0
                    for self.path_0_items in self.path_0_item:
                        self.path_0 = self.path_0_item[i]
                        self.path_1 = self.path_1_item[i]
                        if not os.path.exists(self.path_1):
                            self.siz_src = str(os.path.getsize(self.path_0))
                            siz_src_int = int(self.siz_src)
                            self.bytes_count_1 = self.bytes_count_1 + siz_src_int
                            self.bytes_count_1_str = str(self.bytes_count_1)
                            self.progress = (100 * float(self.bytes_count_1) / float(self.bytes_count))
                            self.progress_str = str(self.progress) + '%'
                            self.f_count_1 += 1
                            self.f_count_1_str = str(self.f_count_1)
                            change_var = True
                            self.write_funk()
                            self.write_call = 0
                            self.check_write()
                            self.progress_int = (int(self.progress) - 9)
                            self.loading_lbl_5.resize(self.progress_int, 8)
                        elif os.path.exists(self.path_1) and os.path.exists(self.path_0) and compare_bool is True:
                            ma = os.path.getmtime(self.path_0)
                            mb = os.path.getmtime(self.path_1)
                            if mb < ma:
                                self.siz_src = str(os.path.getsize(self.path_0))
                                siz_src_int = int(self.siz_src)
                                self.bytes_count_1 = self.bytes_count_1 + siz_src_int
                                self.bytes_count_1_str = str(self.bytes_count_1)
                                self.progress = (100 * float(self.bytes_count_1) / float(self.bytes_count))
                                self.progress_str = str(self.progress) + '%'
                                self.f_count_1 += 1
                                self.f_count_1_str = str(self.f_count_1)
                                change_var = True
                                self.write_funk()
                                self.write_call = 1
                                self.check_write()
                                self.progress_int = (int(self.progress) - 9)
                                self.loading_lbl_5.resize(self.progress_int, 8)

                        i += 1
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_5.resize(0, 7)
        self.loading_lbl_5.hide()
        self.summary()
        self.disengage()

    def progress_output(self):
        var_0 = str(self.f_count_1_str + '/' + self.f_count_str)
        var_1 = str(self.convert_bytes(self.bytes_count_1))
        var_2 = str(self.convert_bytes(self.bytes_count))
        var_3 = str(self.progress_str)
        var_4 = var_1 + '/' + var_2
        var_5 = var_4 + '  ' + var_3
        var_6 = var_0 + '  ' + var_5
        print(var_6)

    def convert_bytes(self, num):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return ("%3.1f %s" % (num, x))
            num /= 1024.0

    def summary(self):
        cp0_count_str = str(self.cp0_count)
        cp0_fail_count_str = str(self.cp0_fail_count)
        cp1_count_str = str(self.cp1_count)
        cp1_fail_count_str = str(self.cp1_fail_count)
        output_sum =  str('copied new: (' + cp0_count_str + ') | failed to copy new: (' + cp0_fail_count_str + ') | updated: (' + cp1_count_str + ')  | failed to update: (' + cp1_fail_count_str + ')').strip()
        if debug_enabled is True:
            print('-- ThreadClass3: ' + output_sum)
        self.tb_5.append(output_sum)
        self.tb_5.moveCursor(QTextCursor.End)
        self.tb_5.ensureCursorVisible()
        self.cp0_count = 0
        self.cp0_fail_count = 0
        self.cp1_count = 0
        self.cp1_fail_count = 0
        self.current_f = ''
        self.path_0 = ''
        self.path_1 = ''
        self.write_call = ()

    def disengage(self):
        self.btnx_main_5.setIcon(QIcon(self.img_btnx_led_0))
        self.stop_thread_btn_5.setIcon(QIcon(self.img_stop_thread_false))
        self.confirm_op5_tru.setIcon(QIcon(self.img_execute_false))
        self.stop_thread_btn_5.setEnabled(False)
        self.paths_readonly_btn_5.setEnabled(True)
        self.confirm_op5_tru.setEnabled(False)
        self.cnfg_prof_btn_var[0].setEnabled(True)
        self.cnfg_prof_btn_var[1].setEnabled(True)
        self.cnfg_prof_btn_var[2].setEnabled(True)
        self.cnfg_prof_btn_var[3].setEnabled(True)
        self.cnfg_prof_btn_var[4].setEnabled(True)
        self.cnfg_prof_btn_var[5].setEnabled(True)
        self.cnfg_prof_btn_var[6].setEnabled(True)
        self.cnfg_prof_btn_var[7].setEnabled(True)
        self.cnfg_prof_btn_var[8].setEnabled(True)
        self.cnfg_prof_btn_var[9].setEnabled(True)
        self.paths_readonly_btn_var[5].setEnabled(True)
        thread_engaged_var[5] = False
        confirm_op5_bool = False
        confirm_op5_wait = True
        self.path_0_item = []
        self.path_1_item = []
        self.loading_lbl_5.resize(0, 7)
        self.loading_lbl_5.hide()

    def stop_thr(self):
        global debug_enabled, confirm_op5_bool, confirm_op5_wait
        if not self.path_1 is '':
            output_str = 'terminated during: ' + self.path_1
            self.tb_5.append(output_str)
        if confirm_op5_bool is True:
            self.summary()
        self.disengage()
        if debug_enabled is True:
            print('-- confirm_op5 declined: (confirm_op5_bool)', confirm_op5_bool)
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
