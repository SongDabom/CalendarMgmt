from helpdesk import *
from member_mgmt import *
from helpdesklist import *
from code_maintenance import *

from login import *
from sys_setting import *

import glb_funcs
import glb_vars

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # glb_vars.init()
        self.getInitData()
        self.setupUi()

    ## Main 화면 초기화 정보 추출
    def getInitData(self):
        self.get_sysSetting_info()                           # system 환경설정 정보
        self.get_logIn_info()                                # 로그인 정보 및 로그인 상태 여부
        self.prepare_init_screen_info()

    ## Main화면 및 후속화면을 가동하기 위한 시스템환경설정정보를 가져옴
    def get_sysSetting_info(self):
        glb_vars.sysSetting_info_arr = []
        glb_vars.strgPostion = ''
        sysSett_list =  glb_funcs.get_from_srcTable(self, 'txt', '', 'sys_setting.txt')
        if sysSett_list != []:
            glb_vars.sysSetting_info_arr  = sysSett_list[0]
            glb_vars.strgPostion = glb_vars.sysSetting_info_arr[3].split(">> ")[1]
        else:
            for i in range(9):
                if i == 0: value = 0
                else:      value = ''
                glb_vars.sysSetting_info_arr.append(value)

    ## 로그인에 대한 기초정보 설정
    def get_logIn_info(self):
        ID_list = glb_funcs.get_from_srcTable(self, 'txt', '', 'tempID.txt')
        glb_vars.loginID = glb_vars.loginID_info = glb_vars.generalUsr = glb_vars.hlpDskUsr = glb_vars.hlpDskFixer = glb_vars.frst_login_time = ""
        glb_vars.loginID_modify_opt = ''
        if ID_list != []:
            glb_vars.loginID = ID_list[0][0]
            glb_vars.loginID_info = ID_list[0][1]
            glb_vars.generalUsr = ID_list[0][2]
            glb_vars.hlpDskUsr = ID_list[0][3]
            glb_vars.hlpDskFixer = ID_list[0][4]
            glb_vars.frst_login_time = ID_list[0][5]

        if glb_vars.loginID == "":
            self.toolTipTxt = "Log In"
            # self.sPst_x = 1460
            self.defaultIcon = "img/login.png"
            self.logMsg = '로그인이 필요합니다'
            # self.width  = 350
        else:
            self.toolTipTxt = "Log Out"
            # self.sPst_x  = 1520
            self.defaultIcon = "img/logout.png"
            self.logMsg = '" 님 환영합니다'
            # self.width = 400

    ## Main 화면에 대한 광영변수 지정 및 기초 정보 지정
    def prepare_init_screen_info(self):
        glb_vars.sel_hlpDsk_list = []
        self.sel_day_Postion_list = []                   # HelpDesk List에 출력되는 일자를 관리하기 위해
        glb_vars.infoTrsf_arr = []
        # self.click_row = self.click_col = -1             # Mouse가 Cell을 Click할 때 출력되는 좌표
        # self.selected_total_cells = ''
        glb_vars.data_changed_signal = ''

        todayQDt = QDate.currentDate()
        self.activYear = QDate.year(todayQDt)
        self.activMon = QDate.month(todayQDt)
        strtYear = self.activYear - 2

        self.strtQdate = glb_funcs.determine_Qdate(self, self.activYear, self.activMon, 1)    # 해당월 시작일을 QDate 형태로 변환
        self.sDay = self.strtQdate.dayOfWeek()                                                # 현재월 시작일의 요일을 구하기 위해

        self.lstDay = glb_funcs.determine_lstDay(self, self.activYear, self.activMon)         # 해당월의 마지막 일자 계산함

        if self.sDay == 7: self.sDay = 0           # 0을 지정하지 않으면 두번째 행부터 출력됨
        self.passedDays = -1 * self.sDay           # 시작일의 요일에 따라 그 주의 앞부분에 채워질 Cell의 칸 수

        self.TW_calendar_strtQDt = self.strtQdate.addDays(self.passedDays)                   # tW_Calendar의 첫번째 Cell에 위치할 첫번째 일자
        self.TW_calendar_lastQDt = self.TW_calendar_strtQDt.addDays(41)                      # tW_Calendar의 맨마지막 Cell에 위치할 마지막 일자

        activYrMon = str(self.activYear) + "년 " + str(self.activMon) + "월"
        k = 0
        self.cB_yrMon_arr = []
        self.cB_year_arr = []
        self.cB_month_arr = []
        for i in range(12) :
            self.cB_month_arr.append(str(i+1))
        for i in range(5) :                                             # 과거2년 + 당해년 + 미래2년
            self.cB_year_arr.append(str(strtYear + i))
            for j in range(12) :                                        # 12개월
                cB_Entry = str(strtYear + i)+ "년 " + str(j + 1) + "월"
                if cB_Entry == activYrMon :
                   self.activIdx = k
                self.cB_yrMon_arr.append(cB_Entry)
                k += 1


        if glb_vars.strgPostion != '':
           glb_vars.hlpDsk_list = glb_funcs.get_from_srcTable(self, 'xls', glb_vars.strgPostion, 'helpDeskList.xlsx')

    ## 초기화면의 Layout을 설정함
    def setupUi(self):
        glb_funcs.winFlame_setting(self, 'R', 1600, 1000, '', 'C', '', "Dash Bord",   '', 'N', 'N', 'N')

        self.centralwidget = QWidget()

        ## Main Title
        self.lb_Title = QLabel(self.centralwidget)
        glb_funcs.label_setting(self, self.lb_Title, 0, 30, 1600, 40, 'C', 'Help Desk')
        glb_funcs.fontSetting(self, self.lb_Title, '8H', 28, " ")  # "에스코어 드림 8 Heavy", PointSize(28)

        ## 로그인이 되었을 경우와 로그아웃이 되었을 경우에 대한 정보 제공
        self.lb_Title = QLabel(self.centralwidget)
        glb_funcs.label_setting(self, self.lb_Title, 1100, 30, 350, 20, 'R', '"' + glb_vars.loginID_info + self.logMsg)

        ## Tool Button에 대한 정의
        tool_button_arr = [["최신정보 갱신", 40, 20, 30, 30, "img/refresh.png", 30, 30, self.refreshInfo],
                           ["환경설정", 1520, 60, 30, 30, "img/OIP.png", 30, 30, self.configSetting],
                           [self.toolTipTxt, 1460, 20, 30, 30, self.defaultIcon, 30, 30, self.logInCtnr],
                           ["나가기", 1520, 20, 30, 30, "img/exit.png", 30, 30, self.exitScreen],
                           ["로그인 ID 정보수정", 1400, 45, 20, 20, "img/modi_user.png", 20, 20, self.modifyID]]

        if glb_vars.loginID == "":
            tool_button_arr.__delitem__(4)

        for i in range(len(tool_button_arr)):
            self.toolButton = QToolButton(self.centralwidget)
            glb_funcs.tool_button_setting(self, self.toolButton, tool_button_arr[i])

        self.setCentralWidget(self.centralwidget)

        ## Tab Widget을 생성하기 위한 정의
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QRect(10, 100, 1580, 890))
        self.tabWidget.setCurrentIndex(0)

        # Tab 정의
        self.dashBrdTab = QWidget()
        self.tabWidget.addTab(self.dashBrdTab, 'Dash Board')

        ## Dash Board Tab의 오른쪽 상단에 있는 다중일자 일괄조회 버튼
        tool_button_arr = [["일괄 조회", 1310, 30, 30, 30, "img/preview_eye.png", 40, 40, self.multiPreview]]
        for i in range(len(tool_button_arr)):
            self.multiPreviewButton = QToolButton(self.dashBrdTab)
            glb_funcs.tool_button_setting(self, self.multiPreviewButton, tool_button_arr[i])

        ## Calendar의 월별 일자 구성을 제어하는 Combo Box 정의
        self.cB_yrMon = QComboBox(self.dashBrdTab)
        self.cB_year = QComboBox(self.dashBrdTab)
        self.cB_month = QComboBox(self.dashBrdTab)
        glb_funcs.comboBox_setting(self, self.cB_yrMon, 1390, 30, 160, 25, self.cB_yrMon_arr, self.activIdx, self.setCaldr)
        glb_funcs.comboBox_setting(self, self.cB_year, 950, 30, 150, 25, self.cB_year_arr, self.activYear, self.setCaldr)
        glb_funcs.comboBox_setting(self, self.cB_month, 1150, 30, 100, 25, self.cB_month_arr, self.activMon, self.setCaldr)
        ## Calendar용 Table Widget에 대한 정의
        self.tW_Calendar = QTableWidget(self.dashBrdTab)
        glb_funcs.TableWidget_setting(self, self.tW_Calendar, 20, 70, 1530, 760, 7, 6, 'N', 'Y', 'Y', 'Y')

        # self.leftCornerTWdgt_pB = QPushButton(self.dashBrdTab)
        # self.leftCornerTWdgt_pB.setGeometry(QRect(20, 70, 40, 25))
        # self.leftCornerTWdgt_pB.setStyleSheet('background-color: lightgrey')
        # self.leftCornerTWdgt_pB.setCheckable(True)
        # self.leftCornerTWdgt_pB.clicked.connect(self.sel_all_cells)

        ## Table Widget Column Header에 대한 정의
        self.tW_horizTitl_arr = ["일", "월", "화", "수", "목", "금", "토"]
        glb_funcs.TableWidget_hdr_setting(self, self.tW_Calendar, 'H', 'S', 'lightblue', self.tW_horizTitl_arr, 'N')

        ## Table Widget Row Header에 대한 정의
        tW_vertcTitl_Arr = []
        for i in range(6) :
            tW_vertcTitl_Arr.append(str(i + 1) + "주차")
        glb_funcs.TableWidget_hdr_setting(self, self.tW_Calendar, 'V', 'S', 'lightgreen', tW_vertcTitl_Arr, 'N')

        self.redesign_tW_info()
        self.tabWidget.currentChanged.connect(self.get_tab_id)   #  Tab이 선택되었을 때 발생되는 Event

        self.add_masterInfoTab()

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    ## Calendar용 Table Widget 바로 위 오른 쪽 상단의 년월을 선택하는 ComboBox에서 선택 년월이 바뀔 때 실행되는 루틴
    def setCaldr(self, idx) :
        self.activYear = int(self.cB_yrMon_arr[idx].split("년")[0])                         # ComboBox에서 선택된 년월 정보
        self.activMon =  int(self.cB_yrMon_arr[idx].split("년")[1].split("월")[0])

        self.strtQdate = glb_funcs.determine_Qdate(self, self.activYear, self.activMon, 1)  # 시작일의 QDate type과 요일을 구하기 위해
        self.sDay = self.strtQdate.dayOfWeek()

        self.lstDay = glb_funcs.determine_lstDay(self, self.activYear, self.activMon)       # 선택월의 마지막 일자

        if self.sDay == 7: self.sDay = 0     # 0을 지정하지 않으면 두번째 행부터 출력됨
        self.passedDays = -1 * self.sDay     # 시작일의 요일에 따라 그 주의 앞부분에 채워질 Cell의 칸 수

        self.TW_calendar_strtQDt = self.strtQdate.addDays(self.passedDays)  # tW_Calendar의 첫번째 Cell에 위치할 첫번째 일자
        self.TW_calendar_lastQDt = self.TW_calendar_strtQDt.addDays(41)     # tW_Calendar의 맨마지막 Cell에 위치할 마지막 일자

        self.redesign_tW_info()

    ## 최종 Calendar 출력을 위한 TableWidget의 각 해당 Cell에 정보를 가공하여 출력
    def redesign_tW_info(self) :               # sDay: 선택월의 시작일자의 요일, lstDay: 선택월의 마지막일자
        self.tW_Calendar.clearContents()

        self.get_hlpDskInfo_list()                            # Table Widget에 출력될 정보를 정비함
        self.frstToLst_day_Postion_list = []                  # 각 달력일자의 일주일 기준에 대한 위치 좌표 관리

        for i in range(0, 42) :
            dayPos_arr = []
            r_num, c_num = divmod(i, 7)
            day = i + self.passedDays                         # self.passedDays는 음수 값임, 그래서 시작일부터 좌측으로 몇 칸(몇 일)이 지난달에 속해있는지 구분함
            if day >= 0: day = day + 1

            TW_cellQdate = glb_funcs.determine_Qdate(self, self.activYear, self.activMon, day)
            day = QDate.day(TW_cellQdate)
            month = QDate.month(TW_cellQdate)

            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            self.tW_Calendar.setItem(r_num, c_num, item)         # 각 Cell의 위치 지정
            dayPos_arr.append(r_num)
            dayPos_arr.append(c_num)
            dayPos_arr.append(day)
            dayPos_arr.append(TW_cellQdate)
            self.frstToLst_day_Postion_list.append(dayPos_arr)
            k = 0
            for j in range(len(glb_vars.sel_hlpDsk_list)):

                if QDate.fromString(glb_vars.sel_hlpDsk_list[j][1], "yyyy-MM-dd") < TW_cellQdate: continue
                if QDate.fromString(glb_vars.sel_hlpDsk_list[j][1], "yyyy-MM-dd") > TW_cellQdate: break
                k += 1

            if self.activMon != month:
                self.tW_Calendar.item(r_num, c_num).setBackground(QColor(240, 230, 230))  # 특정 Cell의 배경색깔 지정
            if(TW_cellQdate == QDate.currentDate()):
                self.tW_Calendar.item(r_num, c_num).setBackground(QColor(153,255,153))
            item.setText(str(day) + ' : ' + str(k) + '건')

    ## Table Widget에 출력될 정보를 정비함
    def get_hlpDskInfo_list(self):
        if glb_vars.strgPostion == '':             # System setting에서 파일 저장위치가 지정되었는지 체크
            return
        list.sort(glb_vars.hlpDsk_list, key=lambda k: k[1])           # 발생일 별 정렬
        for i in range(len(glb_vars.hlpDsk_list)):
            eventDate = QDate.fromString(glb_vars.hlpDsk_list[i][1], 'yyyy-MM-dd')
            if eventDate < self.TW_calendar_strtQDt:
                continue
            if eventDate > self.TW_calendar_lastQDt:
                break

            glb_vars.hlpDsk_list[i][1] = QDate.toString(eventDate, "yyyy-MM-dd")
            # glb_vars.hlpDsk_list[i][2] = QDate.fromString(glb_vars.hlpDsk_list[i][2], 'yyyy-MM-dd')
            glb_vars.sel_hlpDsk_list.append(glb_vars.hlpDsk_list[i])

        list.sort(glb_vars.hlpDsk_list, key=lambda k: k[0])           # 전표번호 별 정렬

    def retranslateUi(self):
        _translate = QCoreApplication.translate

    ## 로그인 여부에 따라 화면 우측상단의 동일 위치의 Tool Button을 변경하고 로그인과 로그아웃을 실행여부에 따라 실행방식을 정해줌
    def logInCtnr(self):
        if self.toolTipTxt == "Log In":
           glb_vars.data_changed_signal = ''
           glb_vars.loginID_modify_opt = ''
           win = Ui_Login()
           win.exec_()
           if glb_vars.data_changed_signal != '':
             self.refreshInfo()
        elif self.toolTipTxt == "Log Out":
            if os.path.isfile('tempID.txt'):
               os.remove('tempID.txt')                  # 기존 임시 ID 저장 파일 삭제
            self.refreshInfo()

    ## 로그인 ID 정보를 변경
    def modifyID(self):
        glb_vars.data_changed_signal = ''
        glb_vars.loginID_modify_opt = 'Y'
        win = Ui_Login()
        win.exec_()
        if glb_vars.data_changed_signal == 'Y':
            self.refreshInfo()

    # def onColHeaderClicked(self, col):
    #     self.click_row = -1              # Mouse가 Column Header를 Click 할 때 row No는 알지 못 하므로 Clear
    #     self.click_col = col
    #     self.selected_total_cells = ''
    #     self.sel_day_Postion_list = []                   # 지정된 Column에 대한 일자 정보 관리
    #     for i in range(len(self.frstToLst_day_Postion_list)):
    #         if self.frstToLst_day_Postion_list[i][1]  == self.click_col:
    #             self.sel_day_Postion_list.append(self.frstToLst_day_Postion_list[i])
    #
    #     glb_vars.infoTrsf_arr = []
    #     glb_vars.infoTrsf_arr.append(str(glb_vars.activYear) + "년 " + str(glb_vars.activMon) + "월 ")
    #     glb_vars.infoTrsf_arr.append(self.tW_horizTitl_arr[col] + "요일")
    #
    # def onRowHeaderClicked(self, row):
    #     self.click_row = row
    #     self.click_col = -1              # Mouse가 Row Header를 Click 할 때 Column No는 알지 못 하므로 Clear
    #     self.selected_total_cells = ''
    #     self.sel_day_Postion_list = []                   # 지정된 row에 대한 일자 정보 관리
    #     for i in range(len(self.frstToLst_day_Postion_list)):
    #         if self.frstToLst_day_Postion_list[i][0] == self.click_row:
    #             self.sel_day_Postion_list.append(self.frstToLst_day_Postion_list[i])
    #
    #     glb_vars.infoTrsf_arr = []
    #     glb_vars.infoTrsf_arr.append(str(glb_vars.activYear) + "년 " + str(glb_vars.activMon) + "월 ")
    #     glb_vars.infoTrsf_arr.append(str(row) + " 주차")

    # ## Table Widgwt의 왼쪽 상단 Corner Button을 눌렀을 때 Table Widget의 모든 Cell을 선택하도록 실행하기 위한 Push Button 기능
    # def sel_all_cells(self):
    #     if self.leftCornerTWdgt_pB.isChecked():    # Push Button이 눌러졌을 때
    #         self.tW_Calendar.selectAll()           # 모든 Cell을 선택함
    #         self.leftCornerTWdgt_pB.setStyleSheet('background-color: lightpink')  # Button 색깔을 연분홍색으로 바꿈
    #         self.selected_total_cells = 'X'
    #
    #         glb_vars.infoTrsf_arr =  []            # 다음 화면( HelpDesk list)의 Table Widget 바로 위의 가장 왼쪽에 출력될 날짜 선택 정보를 관리함
    #         glb_vars.infoTrsf_arr.append(str(glb_vars.activYear) + "년 " + str(glb_vars.activMon) + "월 ")
    #         glb_vars.infoTrsf_arr.append('')
    #     else:
    #         self.tW_Calendar.clearSelection()      # 선택된 모든 Cell을 원상태로 돌려놓음
    #         self.leftCornerTWdgt_pB.setStyleSheet('background-color: lightgrey')
    #         self.selected_total_cells = ''

    ## 모든 Cell 혹은 주별/주차별 Cell, 특정 Cell을 선택히고 다음 화면으로 전환되기 전 전달하기 위한 사전 정보를 수집하는 Routine
    def multiPreview(self):
        if self.check_Access_Enable() == 'N': return

        self.get_cell_information()
        if glb_vars.sel_QDate_grp_arr == []:
            glb_funcs.message_box_1(self, QMessageBox.Critical, '정보', '해당 날짜를 정확히 선택하시오!', '확인')
            return

        glb_vars.infoTrsf_arr = []  # 다음화면(HelpDesk List)의 TableWidget 바로 위 왼쪽에 출력되는 년/월 정보 관리용
        glb_vars.infoTrsf_arr.append(str(self.activYear) + "년 " + str(self.activMon) + "월 ")
        glb_vars.infoTrsf_arr.append(self.month_next_label)

        glb_vars.data_changed_signal = ''  # 지정 여부에 따라 화면전체 초기화 여부를 결정함

        win = Ui_HelpDeskList()
        win.exec_()

        glb_vars.sel_QDate_grp_arr = []
        if glb_vars.data_changed_signal != '':
            self.refreshInfo()

    ## TableWidget화면에서 Cell를 어떻게 선택지정했는지에 따라 화면 상단 좌측에 년/월 정보를 선택하여 출력함
    def get_cell_information(self):
        glb_vars.sel_QDate_grp_arr = []
        row_day_arr = []
        column_day_arr = []
        for cell in self.tW_Calendar.selectedItems():
            for i in range(len(self.frstToLst_day_Postion_list)):
                if self.frstToLst_day_Postion_list[i][0] == cell.row() and self.frstToLst_day_Postion_list[i][1] == cell.column():
                    glb_vars.sel_QDate_grp_arr.append(self.frstToLst_day_Postion_list[i][3])
                    break

            if cell.row() not in row_day_arr:
                row_day_arr.append(cell.row())
            if cell.column() not in column_day_arr:
                column_day_arr.append(cell.column())

        self.month_next_label = ''  # Blank일 경우 년/월 정보만 출력함
        if len(row_day_arr) == 1 and len(self.sel_day_Postion_list) == 7:  # 열을 선택했을 경우(요일별 출력)
            self.month_next_label = str(row_day_arr[0] + 1) + "주차"
        if len(column_day_arr) == 1 and len(self.sel_day_Postion_list) == 7:  # 열을 선택했을 경우(요일별 출력)
            self.month_next_label = str(self.tW_horizTitl_arr[column_day_arr[0]]) + "요일"

    ## 화면을 가동하기 위한 기본 환경설정 정보를 설정(입력)하기 위함
    def configSetting(self):
        if glb_vars.loginID != 'admin':
            glb_funcs.message_box_1(self, QMessageBox.Information, '정보', '먼저 admin 계정으로 로그인이 필요합니다', '확인')
            return
        else:
            df_mbr_list = glb_funcs.get_from_srcTable(self, 'xls', glb_vars.strgPostion, 'member_master.xlsx')
            if df_mbr_list != []:
                text, ok = QInputDialog.getText(self, 'Input Dialog',
                                                "System Access Password")  # Single LineEdit을  관리하는 Dialog 화면을 출력하여 정보를 입력할 수 있게 함
                if ok:
                    check_ok = ''
                    password = text.encode('utf-8')  ## text를 bytes string으로 변환 필요
                    for i in range(len(df_mbr_list)):
                        if df_mbr_list[i][0] == 'admin' and bcrypt.checkpw(password, df_mbr_list[i][1].encode('utf-8')):  # 이미 DB상에 암호화된 비밀번호와 입력된 비밀번호를 비교
                            check_ok = 'X'
                            break
                    if check_ok == 'X':
                        glb_vars.data_changed_signal = ''
                        win = Ui_sysConfigSetting()
                        win.exec_()
                        if glb_vars.data_changed_signal != '':
                            self.refreshInfo()
                    else:
                        glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "Password 오류", "확인")
                        return
                else:
                    return
            else:
                glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "System 환경 설정 필요", "확인")
                return
            
    def tableWidget_clicked(self):
        click_row = self.tW_Calendar.currentIndex().row()
        click_col = self.tW_Calendar.currentIndex().column()

    ## 후속화면(HelpDesk list)에 접근하기 위한 기본사항을 체크
    def check_Access_Enable(self):
        ok_check = 'Y'
        if glb_vars.sysSetting_info_arr[1] == '' or glb_vars.sysSetting_info_arr[3] == '':
            glb_funcs.message_box_1(self, QMessageBox.Warning, '오류', '환경 설정이 완료되지 않았습니다', '확인')
            ok_check = 'N'
            return ok_check

        if glb_vars.loginID == '' :
            glb_funcs.message_box_1(self, QMessageBox.Warning, '오류',  '먼저 일반계정으로 로그인이 필요합니다', '확인')
            ok_check = 'N'
            return ok_check

        if glb_vars.generalUsr != 'X':
            glb_funcs.message_box_1(self, QMessageBox.Information, '정보', '조회 권한이 없습니다', '확인')
            ok_check = 'N'
            return ok_check

    ## 특정 Cell을 double click했을 때 다음화면으로 전환되기 전에 전달되어야 하는 정보를 수집 정비하는 루틴
    def tableWidget_doubleClicked(self):
        if self.check_Access_Enable() == 'N': return

        row = self.tW_Calendar.currentIndex().row()
        col = self.tW_Calendar.currentIndex().column()

        glb_vars.sel_QDate_grp_arr = []
        for i in range(len(self.frstToLst_day_Postion_list)):
          if self.frstToLst_day_Postion_list[i][0] == row  and self.frstToLst_day_Postion_list[i][1] == col:
              year = QDate.year(self.frstToLst_day_Postion_list[i][3])
              month = QDate.month(self.frstToLst_day_Postion_list[i][3])
              day = QDate.day(self.frstToLst_day_Postion_list[i][3])
              glb_vars.sel_QDate_grp_arr.append(self.frstToLst_day_Postion_list[i][3])
              break

        glb_vars.infoTrsf_arr = []
        glb_vars.infoTrsf_arr.append(str(year) + "년 " + str(month) + "월 " + str(day) + "일")
        glb_vars.infoTrsf_arr.append(self.tW_horizTitl_arr[col] + "요일")

        ## 후속화면(HelpDesk List) 열기
        win = Ui_HelpDeskList()
        win.exec_()

        glb_vars.sel_QDate_grp_arr = []               # 기존 선택일자 정보 초기화
        if glb_vars.data_changed_signal != '':        # 후속화면(HelpDesk List)에서 변경사항이 있었다면
           self.refreshInfo()

    ## TreeWidget 틀 설정및 출력에 관한 루틴
    def add_masterInfoTab(self):
        self.add_masterInfoTab_init()
        self.setUp_treeWidget()

    ## TreeWiget에 대한 광영변수 지정
    def add_masterInfoTab_init(self):
        self.code_set_frstKey_arr = []  # 최상위 코드와 대표코드 집합
        glb_vars.highest_parent_code = ''  # 최상위 코드(대표코드 상위의 코드)
        glb_vars.clkd_parent_code = ''  # Click된 코드의 상위 코드
        glb_vars.clkd_parent_codeTxt = ''  # Click된 코드의 상위 코드 Text
        glb_vars.clkd_code = ''  # Click된 코드
        glb_vars.clkd_codeTxt = ''  # Click된 코드 Text
        self.child_exixtence = ''  # 하위코드 존재('Y')

    ## TreeWidget의 기본적인 틀을 정의함
    def setUp_treeWidget(self):
        self.masterInfoTab = QWidget()
        self.tabWidget.addTab(self.masterInfoTab, "기준정보")

        self.itmDef_1_arr = [["lb", "검색 코드", "lE", "self.lE_grpCd", ""]]
        self.gridLayoutWidget = QWidget(self.masterInfoTab)
        glb_funcs.tpOfLayout_setting(self, self.gridLayoutWidget, 'H', 140, 20, 130, 30, self.itmDef_1_arr)

        self.itmDef_2_arr = [["lb", "검색 Text", "lE", "self.lE_grpCdNm", ""]]
        self.gridLayoutWidget = QWidget(self.masterInfoTab)
        glb_funcs.tpOfLayout_setting(self, self.gridLayoutWidget, 'H', 280, 20, 220, 30, self.itmDef_2_arr)

        ## 기준정보 Tab의 오른쪽 상단에 있는 기준정보 생성 버튼
        tool_button_arr = [["검색 실행", 510, 20, 30, 30, "img/preview.png", 30, 30, self.search_items],
                           ["기준정보 생성", 670, 20, 30, 30, "img/add-file.png", 40, 40, self.addMaster],
                           ["기준정보 삭제", 710, 20, 30, 30, "img/delete.png", 40, 40, self.delMaster]]
        for i in range(len(tool_button_arr)):
            self.addMasterInfoButton = QToolButton(self.masterInfoTab)
            glb_funcs.tool_button_setting(self, self.addMasterInfoButton, tool_button_arr[i])

        self.assemble_treeWidget_structure()

    ## PC file에서 추출된 코드집에서 계층구조 형태로 출력되게 조작하는 루틴
    def assemble_treeWidget_structure(self):
        self.treeWidget = QTreeWidget(self.masterInfoTab)
        self.treeWidget.setGeometry(QRect(20, 60, 750, 790))

        ## treeWidget의 Title 지정
        tree_header = ['코드', ' 내용']
        for i in range(len(tree_header)):
            self.treeWidget.headerItem().setText(i, tree_header[i])

        self.prepare_basic_info_for_treeWidget()
        self.realize_treeWidget_structure()  # 계층구조로 실 데이타를 정비하기

        self.treeWidget.itemClicked.connect(self.handleTreeItemClicked)
        self.treeWidget.itemDoubleClicked.connect(self.handleTreeItemDoubleClicked)

    ## PC file에서 추출된 코드집에서 TreeWidget의 기준이 되는 최상위 대표코드와 대표코드를 정비하는 루틴
    def prepare_basic_info_for_treeWidget(self):
        self.df_codeSet_list = glb_funcs.get_from_srcTable(self, 'xls', glb_vars.strgPostion, 'masterCode_set.xlsx')  # 코드집
        if self.df_codeSet_list == []: return  # 코드집이 존재하지 않음

        ## 최상위 대표코드를 찾는 로직
        glb_vars.highest_parent_code = ''
        for i in range(len(self.df_codeSet_list)):
            if self.df_codeSet_list[i][0] == self.df_codeSet_list[i][1]:
                glb_vars.highest_parent_code = self.df_codeSet_list[i][0]
                break
        if glb_vars.highest_parent_code == '':
            glb_funcs.message_box_1(self, QMessageBox.Warning, '오류', '코드체계가 무너져서 관리자에게 문의하시오', '확인')
            return

        ## 최상위 대표코드의 child 대표코드를 추출하는 로직
        ## 성능을 개선하기 위해 최상위 대표코드의 child 대표코드를 추출하다가 끝날 경우 빠져나오도록 함
        self.code_set_frstKey_arr = []
        for i in range(len(self.df_codeSet_list)):
            if self.df_codeSet_list[i][0] == glb_vars.highest_parent_code:
                self.code_set_frstKey_arr.append(self.df_codeSet_list[i][1])
            else:
                if self.code_set_frstKey_arr != []: break

        ## 최상위 대표코드를 맨 앞자리에 위치하도록 하기 위해 추출된 대포코드중 최상위 대표코드를 삭제한 후 다시 0번째로 삽입함(최상위 대표코드 자신도 Child 대표코드로 등록되어 있음)
        for i in range(len(self.code_set_frstKey_arr)):
            if self.code_set_frstKey_arr[i] == glb_vars.highest_parent_code:
                self.code_set_frstKey_arr.__delitem__(i)
                break
        self.code_set_frstKey_arr.insert(0, glb_vars.highest_parent_code)  # 최상위 대표코드를 화면출력시 맨앞에 위치하도록 하기 위해

        self.cleansed_df_codeSet_list = copy.deepcopy(self.df_codeSet_list)

    ## PC File에서 추출된 코드집을 계층구조로 정비하여 출력하는 루틴
    def realize_treeWidget_structure(self):
        self.treeWidget.clear()  # 이 명령어가 없으면 Tree 구조를 갱신할 때마다 각 Entry 처리에 대한 Index 문제가 발생함

        ## 계층구조 구현
        for i in range(len(self.code_set_frstKey_arr)):
            item_0 = QTreeWidgetItem(self.treeWidget)  # 대표코드 지정
            for j in range(len(self.cleansed_df_codeSet_list)):
                if self.df_codeSet_list[j][1] == self.code_set_frstKey_arr[i]:
                    for k in range(len(self.cleansed_df_codeSet_list[j])):
                        if k == 0: continue  # PC file에서 추출된 코드집의 첫번째 자리는 대표코드이고 여기서는 최상위 대표코드가 되므로 이에 대한 출력을 제한하기 위해
                        glb_funcs.fontSetting(self, item_0, '5M', 10, k - 1)  # "에스코어 드림 5 medium", PointSize(10)
                        self.treeWidget.topLevelItem(i).setText(k - 1, str(self.cleansed_df_codeSet_list[j][k]))  # 첫번째 레벨 정보 출력하기 (대표코드, 내용)
                    break
            n = 0
            for j in range(len(self.cleansed_df_codeSet_list)):
                if self.cleansed_df_codeSet_list[j][0] == self.code_set_frstKey_arr[i]:
                    if self.cleansed_df_codeSet_list[j][0] == self.cleansed_df_codeSet_list[j][1]: continue
                    item_1 = QTreeWidgetItem(item_0)  # 대표코드에 Child 코드 지정
                    for k in range(len(self.df_codeSet_list[j])):
                        if k == 0: continue  # PC file에서 추출된 코드집의 첫번째 자리는 대표코드이고 여기서는 대표코드가 되므로 이에 대한 출력을 제한하기 위해
                        glb_funcs.fontSetting(self, item_0, '4R', 10, k - 1)  # "에스코어 드림 4 Regular", PointSize(10)
                        self.treeWidget.topLevelItem(i).child(n).setText(k - 1, str(self.cleansed_df_codeSet_list[j][k]))  # 두번째 레벨 정보 출력하기(일반코드, 내용)
                    n += 1

    ## TreeWidget에 있는 특정 대표코드에 대한 일반코드를 추가하는 루틴
    def addMaster(self):
        if glb_vars.highest_parent_code != '':
            if glb_vars.clkd_code == '':  # 화면상에 어떤 코드도 지정하지 않은 경우
                glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "생성하려는 코드의 대표코드를 Click하여 지정하시오", "확인")
                return
            if glb_vars.clkd_parent_code != '':  # 화면상에 일반코드를 지정한 경우(한 단계위의 대표코드를 지정해야 함
                glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "생성하려는 코드의 상위코드를 Click 하시오", "확인")
                return

        glb_vars.data_changed_signal = ''
        win = Ui_CodeMaintenance()
        win.exec_()
        self.treeWidget.clearSelection()
        glb_vars.clkd_code = glb_vars.clkd_parent_code =''
        if glb_vars.data_changed_signal != '':
            self.prepare_basic_info_for_treeWidget()
            self.realize_treeWidget_structure()  # 계층구조로 실 데이타를 정비하기

    ## TreeWidget에 선택지정된 항목에 대해 삭제가능여부 체크와 삭제처리하는 루틴
    def delMaster(self):
        if glb_vars.clkd_code == '':  # 화면상에 어떤 코드도 지정하지 않은 경우
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "삭제하려는 코드를 Click하여 지정하시오.", "확인")
            return
        if self.child_exixtence == 'Y':
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "하위코드가 있는 코드는 삭제 불가합니다.", "확인")
            self.child_exixtence == ''
            return
        if glb_vars.clkd_parent_code == '':
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "대표코드를 삭제하려면 최상위 대표코드 내에서 삭제를 진행하시오.", "확인")
            return
        if glb_vars.clkd_parent_code == glb_vars.highest_parent_code:
            for i in range(len(self.df_codeSet_list)):
                if self.df_codeSet_list[i][0] == glb_vars.clkd_code:
                    glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "삭제하려는 대표코드에는 하위 코드가 존재합니다.", "확인")
                    return

        self.df_codeSet_list = glb_funcs.get_from_srcTable(self, 'xls', glb_vars.strgPostion, 'masterCode_set.xlsx')  # 코드집
        for i in range(len(self.df_codeSet_list)):
            if self.df_codeSet_list[i][0] == glb_vars.clkd_parent_code and self.df_codeSet_list[i][
                1] == glb_vars.clkd_code:
                self.df_codeSet_list.__delitem__(i)
                break

        # codeSet_hdr_title = ["대표코드", "코드", "내용"]
        glb_funcs.save_to_trgtTable(self, 'xls', self.df_codeSet_list, glb_vars.codeSet_hdr_title,
                                    glb_vars.strgPostion, 'masterCode_set.xlsx')
        glb_funcs.message_box_1(self, QMessageBox.Information, "저장완료", "지정된 코드를 삭제 처리했습니다.", "확인")

        self.prepare_basic_info_for_treeWidget()
        self.realize_treeWidget_structure()  # 계층구조로 실 데이타를 정비하기

    ## 기준정보 Tab에서 검색조건에 의해 TreeWiget의 출력될 정보들을 재 가공하는 루틴
    def search_items(self):
        if glb_vars.clkd_code == '' or self.child_exixtence != 'Y':  # 화면상에 어떤 코드도 지정하지 않은 경우 혹은 일반하위코드를 지정한 경우
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "검색하려는 코드의 대표코드를 Click하여 지정하시오.", "확인")
            return

        self.Cd_input = self.itmDef_1_arr[0][3].text().strip()
        self.CdNm_input = self.itmDef_2_arr[0][3].text().strip()

        self.cleansed_df_codeSet_list = []
        if self.Cd_input == '':
            if self.CdNm_input == '':
                if glb_vars.highest_parent_code == glb_vars.clkd_code:  # 최상위 대표코드를 클릭하고 모두 검색을 수행할 경우
                    self.cleansed_df_codeSet_list = copy.deepcopy(self.df_codeSet_list)
                else:
                    for i in range(len(self.df_codeSet_list)):
                        if self.df_codeSet_list[i][0] == glb_vars.highest_parent_code or self.df_codeSet_list[i][
                            0] == glb_vars.clkd_code:
                            self.cleansed_df_codeSet_list.append(self.df_codeSet_list[i])
            else:
                for i in range(len(self.df_codeSet_list)):  # 기본적으로 최상위 대표코드와 대표코드는 화면에 출력되어야 함
                    if self.df_codeSet_list[i][0] == glb_vars.highest_parent_code or \
                            (self.df_codeSet_list[i][0] == glb_vars.clkd_code and str(
                                self.df_codeSet_list[i][2]).find(self.CdNm_input) != -1):
                        self.cleansed_df_codeSet_list.append(self.df_codeSet_list[i])
        else:
            if self.CdNm_input == '':
                for i in range(len(self.df_codeSet_list)):
                    if self.df_codeSet_list[i][0] == glb_vars.highest_parent_code or \
                            (self.df_codeSet_list[i][0] == glb_vars.clkd_code and str(
                                self.df_codeSet_list[i][1]).find(self.Cd_input) != -1):
                        self.cleansed_df_codeSet_list.append(self.df_codeSet_list[i])
            else:
                for i in range(len(self.df_codeSet_list)):
                    if self.df_codeSet_list[i][0] == glb_vars.highest_parent_code or (
                            self.df_codeSet_list[i][0] == glb_vars.clkd_code and \
                            self.df_codeSet_list[i][0].find(self.Cd_input) != -1 and str(
                        self.df_codeSet_list[i][1]).find(self.CdNm_input) != -1):
                        self.cleansed_df_codeSet_list.append(self.df_codeSet_list[i])

        if self.cleansed_df_codeSet_list == []:
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "검색대상이 선택되지 않았습니다", "확인")
            return

        self.realize_treeWidget_structure()

    def get_tab_id(self, idx):
        if self.check_Access_Enable() == 'N':
            self.tabWidget.setCurrentIndex(0)

    ## TreeWidget에서 특정 item을 Click했을 때 추출되는 기본 정보
    def handleTreeItemClicked(self, it, col):
        glb_vars.clkd_code = it.text(0)
        glb_vars.clkd_codeTxt = it.text(1)

        if it.parent() == None:
            glb_vars.clkd_parent_code = ''
        else:
           glb_vars.clkd_parent_code = it.parent().text(0)

        if it.child(0) == None:
            self.child_exixtence = ''
        else:
            self.child_exixtence = 'Y'

    def handleTreeItemDoubleClicked(self, it, col):
        print(glb_vars.clkd_code, glb_vars.clkd_parent_code)

    def refreshInfo(self):
        self.close()
        self.__init__()
        self.show()

    def exitScreen(self, event):
        if os.path.isfile('tempID.txt'):
            os.remove('tempID.txt')  # 기존 임시 ID 저장 파일 삭제
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    app.exec_()

## Window 상단 Close Icon에 대한 Event 연결 방법
#     QMetaObject.connectSlotsByName(self)
#     app.aboutToQuit.connect(self.closeEvent)
#
# def closeEvent(self, event):
#     event.accept()