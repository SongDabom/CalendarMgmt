from import_list import *

def label_setting(self, qwidget, s_xPst, s_yPst, e_xPst, e_yPst, Align, Txt):
    qwidget.setGeometry(QRect(s_xPst, s_yPst, e_xPst, e_yPst))
    qwidget.setText(Txt)
    if  Align == 'L':
        qwidget.setAlignment(Qt.AlignLeft)
    elif Align == 'R':
        qwidget.setAlignment(Qt.AlignRight)
    else:
        qwidget.setAlignment(Qt.AlignCenter)

def fontSetting(self, tgt_widget, type, size, widget_index):
    font_type = {"4R": "에스코어 드림 4 Regular", "5M": "에스코어 드림 5 Medium",
                 "6B": "에스코어 드림 6 Bold", "8H": "에스코어 드림 8 Heavy"}
    font = QFont()
    font.setFamily(font_type[type])
    font.setPointSize(size)
    if widget_index == " ":
        tgt_widget.setFont(font)
    else:
        tgt_widget.setFont(int(widget_index), font)

def readOnly_setting(self, type, qobject, option):              # option: 0(True), 1(Talse)
    if option == 0:
        qobject.setStyleSheet("background: lightgray")
        if   type == 'lE' or type == 'dE' or type == 'tE':         # QLineEdit, QDateEdit, QTextEdit
            qobject.setReadOnly(True)
        elif type == 'cB':
            qobject.setEnabled(False)
    else:
        if type == 'lE' or type == 'dE' or type == 'tE':  # QLineEdit, QDateEdit, QTextEdit
            qobject.setReadOnly(False)
        elif type == 'cB':
            qobject.setEnabled(True)

def tool_button_setting(self, qwidget, tool_button_arr):
    qwidget.setToolTip(tool_button_arr[0])
    qwidget.setGeometry(QRect(tool_button_arr[1], tool_button_arr[2], tool_button_arr[3], tool_button_arr[4]))
    icon = QIcon()
    icon.addPixmap(QPixmap(tool_button_arr[5]), QIcon.Normal, QIcon.Off)
    qwidget.setCursor(QCursor(Qt.PointingHandCursor))  # Point Cursor가 손가락 Cursor로 변경
    qwidget.setIcon(icon)
    qwidget.setIconSize(QSize(tool_button_arr[6], tool_button_arr[7]))
    qwidget.setStyleSheet("border : 0")
    qwidget.clicked.connect(tool_button_arr[8])

def comboBox_setting(self, qwidget, s_xPst, s_yPst, e_xPst, e_yPst, cB_list, idx, evntNm):
    qwidget.setGeometry(QRect(s_xPst, s_yPst, e_xPst, e_yPst))
    qwidget.addItems(cB_list)
    qwidget.setCurrentIndex(idx)
    qwidget.currentIndexChanged[int].connect(evntNm)

def winFlame_setting(self, sizeTyp, sizeHorzLnth, sizeVertLnth, setColor, pstnAlign, hdrFlmLess, title, Icn, mxmSizBttnHnt, hlpBttnHnt, clsBttnHnt):
    if  sizeTyp == 'R':
        self.resize(sizeHorzLnth, sizeVertLnth)
    elif sizeTyp == 'F':
        self.setFixedSize(sizeHorzLnth, sizeVertLnth)       # 어떤 환경이던 Dialog 크기를

    if setColor == '' or setColor == ' ': pass
    else:
        optnTxt = 'background: ' + setColor
        self.setStyleSheet(optnTxt)                            # Windoq의 배경색을 설정

    if pstnAlign == 'C':
       qr = self.frameGeometry()
       qr.moveCenter(QDesktopWidget().availableGeometry().center())
       self.move(qr.topLeft())

    if hdrFlmLess == 'Y':
       self.setWindowFlags(Qt.FramelessWindowHint)             # Window 헤더부분 Flame을 제거함
       return

    self.setWindowTitle(title)                                 # Window Title 지정

    if Icn == '' or Icn == ' ': pass
    else:
        self.setWindowIcon(QIcon(Icn))                         # Window창의 Title옆의 Icon 모양 Setting

    if mxmSizBttnHnt == 'N':
       self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

    if hlpBttnHnt== 'N':
       self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Window창의 Question 버튼(?모양)를 Disable함

    if clsBttnHnt == 'N':
       self.setWindowFlag(Qt.WindowCloseButtonHint, False)  # Window창의 Close 버튼(x모양)를 Disable함

def tpOfLayout_setting(self, qwidget, Layo_Typ, s_xPst, s_yPst, e_xPst, e_yPst, itm_arr):
    qwidget.setGeometry(QRect(s_xPst, s_yPst, e_xPst, e_yPst))

    if   Layo_Typ == 'F':       # formLayout
         Layout = QFormLayout(qwidget)
    elif Layo_Typ == 'H':       # horizontalLayout
         Layout = QHBoxLayout(qwidget)
    elif Layo_Typ == 'V':       # verticallLayout
         Layout = QVBoxLayout(qwidget)
    elif Layo_Typ == 'G':       # gridLayout
         Layout = QGridLayout(qwidget)

    Layout.setContentsMargins(0, 0, 0, 0)

    for i in range(len(itm_arr)):
        if itm_arr[i][0] != 'CB' and itm_arr[i][0] != '':       # Check Box and ''
            if   itm_arr[i][0] == 'lb':                  # Label
                qobjet = QLabel(qwidget)
                qobjet.setText(itm_arr[i][1])
            elif itm_arr[i][0] == 'tB':                  # Tool Button
                itm_arr[i][1] = QToolButton(qwidget)
                qobjet = itm_arr[i][1]

            if Layo_Typ == 'F':  # formLayout
                Layout.setWidget(i, QFormLayout.LabelRole, qobjet)
            elif Layo_Typ == 'H':  # horizontalLayout
                Layout.addWidget(qobjet)
            # elif Layo_Typ == 'V':  # verticalLayout
                # Layout.addWidget(l_title)
            elif Layo_Typ == 'G':  # gridLayout
                Layout.addWidget(qobjet, i, 0, 1, 1)

        if   itm_arr[i][2] == "lE":                    # Line Edit
            itm_arr[i][3] = QLineEdit(qwidget)
            if itm_arr[i][4] == "R":
                itm_arr[i][3].setReadOnly(True)
                itm_arr[i][3].setStyleSheet("background: lightgray")
        elif itm_arr[i][2] == "tE":                    # Text Edit
            itm_arr[i][3] = QTextEdit(qwidget)
            if itm_arr[i][4] == "R":
                itm_arr[i][3].setReadOnly(True)
                itm_arr[i][3].setStyleSheet("background: lightgray")
        elif itm_arr[i][2] == "cB":                    # Combo Box
            itm_arr[i][3] = QComboBox(qwidget)
            if itm_arr[i][4] != "":
               itm_arr[i][3].addItems(itm_arr[i][4])
        elif itm_arr[i][2] == "dE":                    # Date Edit
            itm_arr[i][3] = QDateEdit(qwidget)
            itm_arr[i][3].setCalendarPopup(True)
        elif itm_arr[i][2] == "pB":                     # Push Button
            itm_arr[i][3] = QPushButton(qwidget)
            itm_arr[i][3].setText(itm_arr[i][4])
            itm_arr[i][3].pressed.connect(itm_arr[i][5])
        elif itm_arr[i][2] == "CB":                     # Check Box
            itm_arr[i][3] = QCheckBox(qwidget)
            itm_arr[i][3].setText(itm_arr[i][1])
            # itm_arr[i][3].setChecked(True)
            if itm_arr[i][4] != "":
                itm_arr[i][3].stateChanged.connect(itm_arr[i][4])

        if Layo_Typ == 'F':  # formLayout
            Layout.setWidget(i, QFormLayout.FieldRole, itm_arr[i][3])
        elif Layo_Typ == 'H':  # horizontalLayout
            Layout.addWidget(itm_arr[i][3])
        elif Layo_Typ == 'V':  # horizontalLayout
            Layout.addWidget(itm_arr[i][3])
        elif Layo_Typ == 'G':  # gridLayout
            Layout.addWidget(itm_arr[i][3], i, 1, 1, 1)

def TableWidget_setting(self, qwidget, s_xPst, s_yPst, e_xPst, e_yPst, colCnt, rowCnt, setEdit, setVisbl, evtSnglClck, evtDblClck):
    qwidget.setGeometry(QRect(s_xPst, s_yPst, e_xPst, e_yPst))
    qwidget.setColumnCount(colCnt)
    qwidget.setRowCount(rowCnt)
    if setEdit == 'N':
        qwidget.setEditTriggers(QAbstractItemView.NoEditTriggers)         # Cell Editing 기능
    if setVisbl == 'N':
        qwidget.verticalHeader().setVisible(False)                        # index 안보이는 기능
    if evtSnglClck == 'Y':
        qwidget.clicked.connect(self.tableWidget_clicked)                 # Click event 발생
    if evtDblClck == 'Y':
        qwidget.doubleClicked.connect(self.tableWidget_doubleClicked)     # Double Click event 발생

def TableWidget_hdr_setting(self, qwidget, type, setSecRsz, Back_Color, title_arr, hdrClck):
    bg_color = "::section {""background-color: " + Back_Color + "; }"
    if   type == 'H':
        tW_Title = qwidget.horizontalHeader()
        if hdrClck == 'Y':
           tW_Title.sectionClicked.connect(self.onColHeaderClicked)
    elif type == 'V':
        tW_Title = qwidget.verticalHeader()
        if hdrClck == 'Y':
           tW_Title.sectionClicked.connect(self.onRowHeaderClicked)

    if   setSecRsz == 'S':
        tW_Title.setSectionResizeMode(QHeaderView.Stretch)
    elif setSecRsz == 'R':
        tW_Title.setSectionResizeMode(QHeaderView.ResizeToContents)
    tW_Title.setStyleSheet(bg_color)

    for i in range(len(title_arr)):
        item = QTableWidgetItem()
        if   type == 'H':
            qwidget.setHorizontalHeaderItem(i, item)
            item = qwidget.horizontalHeaderItem(i)
        elif type == 'V':
            qwidget.setVerticalHeaderItem(i, item)
            item = qwidget.verticalHeaderItem(i)
        item.setText(title_arr[i])

def final_decision_button_box(self, qwidget, v, w, x, y, Ok_txt, Cancel_txt, Ok_evt, Canc_evt):
    qwidget.setGeometry(QRect(v, w, x, y))
    qwidget.setOrientation(Qt.Horizontal)
    if   Ok_txt == '':
         qwidget.setStandardButtons(QDialogButtonBox.Cancel)
         qwidget.button(QDialogButtonBox.Cancel).setText(Cancel_txt)  # Cancel -> 취소
         qwidget.rejected.connect(Canc_evt)
    elif Cancel_txt == '':
         qwidget.setStandardButtons(QDialogButtonBox.Ok)
         qwidget.button(QDialogButtonBox.Ok).setText(Ok_txt)  # Ok -> 등록, 저장
         qwidget.accepted.connect(Ok_evt)
    else:
         qwidget.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
         qwidget.button(QDialogButtonBox.Ok).setText(Ok_txt)  # Ok -> 등록, 저장
         qwidget.button(QDialogButtonBox.Cancel).setText(Cancel_txt)  # Cancel -> 취소
         qwidget.accepted.connect(Ok_evt)
         qwidget.rejected.connect(Canc_evt)

# Message Icon Option : QMessageBox.[NoIcon, Question, Information, Warning, Critical]
# 범용 Message Box(Single Buttons)
def message_box_1(self, MsgOption, title, MsgText, YesText):
    msgBox1 = QMessageBox()
    msgBox1.setIcon(MsgOption)
    msgBox1.setWindowTitle(title)
    msgBox1.setText(MsgText)
    msgBox1.setStandardButtons(QMessageBox.Yes)
    buttonY = msgBox1.button(QMessageBox.Yes)
    buttonY.setText(YesText)
    msgBox1.exec_()

# 범용 Message Box(2 Buttons)
def message_box_2(self, MsgOption, title, MsgText, YesText, NoText):
    global MsgBoxRtnSignal

    msgBox2 = QMessageBox()
    msgBox2.setIcon(MsgOption)
    msgBox2.setWindowTitle(title)
    msgBox2.setText(MsgText)
    msgBox2.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    buttonY = msgBox2.button(QMessageBox.Yes)
    buttonY.setText(YesText)
    buttonN = msgBox2.button(QMessageBox.No)
    buttonN.setText(NoText)
    msgBox2.exec_()

    if msgBox2.clickedButton() == buttonY:
        MsgBoxRtnSignal = 'Y'
    elif msgBox2.clickedButton() == buttonN:
        MsgBoxRtnSignal = 'N'
    return MsgBoxRtnSignal

def determine_Qdate(self, year, mon, day):
    if day > 0: day =  day - 1
    if mon < 10: mon_str = "0" + str(mon)
    else :       mon_str = str(mon)

    firstQDate = QDate.fromString(str(year) + mon_str + '01', "yyyyMMdd")
    RtnQDate = firstQDate.addDays(day)
    return RtnQDate

def determine_lstDay(self, year, mon):
    year_div, mon_mod = divmod(mon + 1, 12)
    if mon_mod == 0 :
        mon_mod = 12
        year_div = 0
    year = year + year_div
    if mon_mod < 10 :
        mon_str = "0" + str(mon_mod)
    else :
        mon_str = str(mon_mod)
    last_day = QDate.day(QDate.fromString(str(year) + mon_str, "yyyyMM").addDays(-1))
    return last_day

def get_from_srcTable(self, src_type, directory_path, fileName):
    df_list = []
    if src_type == 'DB':
       return
    else:
        if directory_path == '':
           final_path = fileName
        else:
           final_path = directory_path + '/' + fileName
        if os.path.isfile(final_path):
            if   src_type == 'xls':
                df = pd.read_excel(final_path, keep_default_na=False)
                # df = pd.read_excel(final_path)
                # df = pd.read_excel(final_path, convert_float=True)
            elif src_type == 'txt':
                df = pd.read_table(final_path, sep=' ')
            df_list = df.values.tolist()
            for i in range(len(df_list)):
                df_list[i][0] = str(df_list[i][0])

            # df_list에 'nan'으로 표시된 값을 ''로 대체
            for i in range(len(df_list)):
                for j in range(len(df_list[i])):
                    if pd.isna(df_list[i][j]) == True:
                        df_list[i][j] = ''
    return df_list

def save_to_trgtTable(self, target_type, target_list, column_header_title, directory_path, fileName):
    if target_type == 'DB':
       print("DB")
       return
    else:
        if directory_path == '':
           final_path = fileName
        else:
           final_path = directory_path + '/' + fileName
        if os.path.isfile(final_path):
            os.remove(final_path)

        df = pd.DataFrame(target_list, columns=column_header_title)
        if   target_type == 'xls':
            df.to_excel(final_path, index=False)
        elif target_type == 'txt':
            df.to_csv(final_path, index=False, sep=' ')


#    QComboBox.setEnabled(False)              #Combox를 Read Only 처럼 지정