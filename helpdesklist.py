from import_list import *
from helpdesk import *
from draw_graph import *

import glb_funcs
import glb_vars

class Ui_HelpDeskList(QDialog):
    def __init__(self):
        super().__init__()
        self.getInitData()
        self.setupUi()

    def getInitData(self):
        self.preparation_for_comboboxs()
        self.lb_prcsts = ''              # Main title 바로 밑에 출력될 처리상태 정보
        glb_vars.fixer_list = []         # PC file에 있는 memeber_master에서 조치책임자 역할이 있는 담당자 집계용

        df_mbr_list = glb_funcs.get_from_srcTable(self, 'xls', glb_vars.strgPostion, 'member_master.xlsx')      # 전체 회원정보를 PC file에서 읽어옴
        for i in range(len(df_mbr_list)):
            if df_mbr_list[i][11] == 'X':          # HelpDesk 조치 책임자
                glb_vars.fixer_list.append([df_mbr_list[i][0], df_mbr_list[i][2], df_mbr_list[i][7], df_mbr_list[i][8]]) # ID, 이름, 부서명, 직책

        self.TW_info_list = []                     # Table Widget에 해당 리스트를 출력할 임시 저장소

        list.sort(glb_vars.sel_hlpDsk_list, key=lambda k: (k[1], k[0]))  # 전표번호 별 정렬
        self.orgnl_TW_info_list = []               # 바로 PC file에서 읽어 온 정보를 해당 조건에 필터링하여 화면에 출력하는 것이 아니고 나중 ComboBox의 선택조건에 대응하기 위해 임시 저장함
        # self.lb_prcsts_tot_cnt = self.lb_prcsts_req_cnt = self.lb_prcsts_wait_cnt = self.lb_prcsts_prcng_cnt = self.lb_prcsts_prcd_cnt = self.lb_prcsts_cls_cnt = 0
        self.prcSts_cnt_arr = []
        for j in range(len(glb_vars.k0040_list)):
            self.prcSts_cnt_arr.append(0)

        for i in range(len(glb_vars.sel_hlpDsk_list)):
            if glb_vars.sel_hlpDsk_list[i][1] in glb_vars.sel_QDate_grp_arr:
                crtDate = QDate.toString(glb_vars.sel_hlpDsk_list[i][1], 'yyyy-MM-dd')
                fixDate = QDate.toString(glb_vars.sel_hlpDsk_list[i][2], 'yyyy-MM-dd')
                crtName = crtInfo = fixName = grpCdNm = inqTpNm = priortNm = prcsStsNm = ''

                for j in range(len(df_mbr_list)):
                    if df_mbr_list[j][0] == glb_vars.sel_hlpDsk_list[i][14]:
                        crtName = df_mbr_list[j][2]
                        crtInfo = crtName + ' ' + str(df_mbr_list[j][8]) + ' //' + str(df_mbr_list[j][7])
                        break
                for j in range(len(df_mbr_list)):
                    if df_mbr_list[j][0] == glb_vars.sel_hlpDsk_list[i][3]:                # 조치책임자
                        fixName = df_mbr_list[j][2]
                        break
                for j in range(len(glb_vars.k0010_list)):
                    if glb_vars.k0010_list[j][0] == str(glb_vars.sel_hlpDsk_list[i][4]):    # 단지코드
                        grpCdNm = glb_vars.k0010_list[j][1]
                        break
                for j in range(len(glb_vars.k0020_list)):
                    if glb_vars.k0020_list[j][0] == glb_vars.sel_hlpDsk_list[i][7]:         # 문의유형
                        inqTpNm = glb_vars.k0020_list[j][1]
                        break
                for j in range(len(glb_vars.k0030_list)):
                    if glb_vars.k0030_list[j][0] == glb_vars.sel_hlpDsk_list[i][8]:         # 중요도
                        priortNm = glb_vars.k0030_list[j][1]
                        break
                for j in range(len(glb_vars.k0040_list)):
                    if glb_vars.k0040_list[j][0] == glb_vars.sel_hlpDsk_list[i][9]:         # 처리상태
                        prcsStsNm = glb_vars.k0040_list[j][1]
                        break

                # tW_hdr_arr = ["문서 번호", "발생일", "등록인", "조치일", "조치책임자", "문의유형", "제목", "중요도", "상태", " 단지 ", "고객", "연락처", "생성일", "변경일"]
                self.orgnl_TW_info_list.append([glb_vars.sel_hlpDsk_list[i][0], crtDate, crtName, fixDate, fixName, inqTpNm, glb_vars.sel_hlpDsk_list[i][10],
                                                priortNm, prcsStsNm, grpCdNm, glb_vars.sel_hlpDsk_list[i][5], glb_vars.sel_hlpDsk_list[i][6],
                                                glb_vars.sel_hlpDsk_list[i][15], glb_vars.sel_hlpDsk_list[i][17],
                                                crtInfo, glb_vars.sel_hlpDsk_list[i][3]])

                self.processing_status_count(glb_vars.sel_hlpDsk_list[i][9])

        self.TW_info_list = copy.deepcopy(self.orgnl_TW_info_list)

        self.lb_prcSts = '처리상태 전체 : ' + str(len(self.orgnl_TW_info_list)) + '건,  '
        for i in range(len(glb_vars.k0040_list)):
            self.lb_prcSts = self.lb_prcSts + glb_vars.k0040_list[i][1] + ' : ' + str(self.prcSts_cnt_arr[i]) +  '건,  '

        self.cB_sel_wrtDt_arr = []                 # 발생일 ComboBox용 임시 저장소
        for i in range(len(glb_vars.sel_QDate_grp_arr)):
            self.cB_sel_wrtDt_arr.append(QDate.toString(glb_vars.sel_QDate_grp_arr[i], 'yyyy-MM-dd'))

    def processing_status_count(self, prcStsCd):          # 처리상태의 각 상태별 갯수 구하기
        for j in range(len(glb_vars.k0040_list)):
            if glb_vars.k0040_list[j][0] == prcStsCd:
                self.prcSts_cnt_arr[j] += 1

    def preparation_for_comboboxs(self):
        ## 조치 책임자 ComboBox
        glb_vars.fixer_list = []
        df_mbr_list = glb_funcs.get_from_srcTable(self, 'xls', glb_vars.strgPostion, 'member_master.xlsx')
        for i in range(len(df_mbr_list)):
            if df_mbr_list[i][11] == 'X':  # HelpDesk 조치 책임자
                glb_vars.fixer_list.append(
                    [df_mbr_list[i][0], df_mbr_list[i][2], df_mbr_list[i][7], df_mbr_list[i][8]])  # ID, 이름, 부서명, 직책

        df_codeSet_list = glb_funcs.get_from_srcTable(self, 'xls', glb_vars.strgPostion, 'masterCode_set.xlsx')   # 코드집
        ## 단지 코드 ComboBox
        glb_vars.k0010_list = []
        for i in range(len(df_codeSet_list)):
            if df_codeSet_list[i][0] == 'K0010':        # 단지코드
              glb_vars.k0010_list.append([str(df_codeSet_list[i][1]), str(df_codeSet_list[i][2])])

        ## 문의유형 코드 ComboBox
        glb_vars.k0020_list = []
        for i in range(len(df_codeSet_list)):
            if df_codeSet_list[i][0] == 'K0020':  # 문의유형
                glb_vars.k0020_list.append([str(df_codeSet_list[i][1]), str(df_codeSet_list[i][2])])

        ## 중요도 코드 ComboBox
        glb_vars.k0030_list = []
        for i in range(len(df_codeSet_list)):
            if df_codeSet_list[i][0] == 'K0030':  # 중요도
                glb_vars.k0030_list.append([str(df_codeSet_list[i][1]), str(df_codeSet_list[i][2])])

        glb_vars.cB_priort_arr = []
        for i in range(len(glb_vars.k0030_list)):
            glb_vars.cB_priort_arr.append(glb_vars.k0030_list[i][1])

        ## 처리상태 코드 ComboBox
        glb_vars.k0040_list = []
        for i in range(len(df_codeSet_list)):
            if df_codeSet_list[i][0] == 'K0040':  # 처리상태
                glb_vars.k0040_list.append([str(df_codeSet_list[i][1]), str(df_codeSet_list[i][2])])

        glb_vars.cB_prcsSts_arr = []
        for i in range(len(glb_vars.k0040_list)):
            glb_vars.cB_prcsSts_arr.append(glb_vars.k0040_list[i][1])

    def setupUi(self):
        glb_funcs.winFlame_setting(self, 'R', 1200, 950, '', 'C', '', "Help Desk List", '', 'N', 'N', 'N')
        ## 화면 Main Title
        self.lb_title = QLabel(self)
        glb_funcs.label_setting(self, self.lb_title, 0, 20, 1200, 80, 'C', 'HelpDesk 상세 현황')
        glb_funcs.fontSetting(self, self.lb_title, '6B', 20, " ")  # "에스코어 드림 6 Bold", PointSize(20)

        ## 화면 Main Title 바로 아래 처리상태 단계별로 해당 건수를 출력함
        self.lb_title = QLabel(self)  # 화면 Title
        glb_funcs.label_setting(self, self.lb_title, 0, 80, 1200, 30, 'C', self.lb_prcSts)
        glb_funcs.fontSetting(self, self.lb_title, '5M', 9, " ")   # "에스코어 드림 5 Medium", PointSize(9)

        ##Grid 상단 오른쪽 날짜/ 요일 정보
        self.lb_title = QLabel(self)
        glb_funcs.label_setting(self, self.lb_title, 60, 180, 200, 30, 'L', glb_vars.infoTrsf_arr[0] + " " + glb_vars.infoTrsf_arr[1])

        tool_button_arr = [["최신정보 갱신", 40, 20, 30, 30, "img/refresh.png", 30, 30, self.refreshInfo],
                           ["차트 그리기", 900, 80, 30, 30, "img/circular_chart.png", 30, 30, self.drawChart],
                           ["조치내용등록", 990, 165, 30, 30, "img/solved.png", 30, 30, self.fixInfo],
                           ["추가", 1050, 165, 30, 30, "img/add-file.png", 30, 30, self.addInfo],
                           ["삭제", 1100, 165, 30, 30, "img/delete.png", 30, 30, self.delInfo]]
        for i in range(len(tool_button_arr)):
            self.toolButton = QToolButton(self)
            glb_funcs.tool_button_setting(self, self.toolButton, tool_button_arr[i])

        ## 발생일
        if len(self.cB_sel_wrtDt_arr) > 1:               # 이전 화면에서 날짜를 두개이상 선택함
           self.cB_sel_wrtDt_arr.insert(0, "전체선택")
        self.itmDef_c_arr = [["lb", "발생일", "cB", "self.cB_wrtDt", self.cB_sel_wrtDt_arr]]
        self.formLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.formLayoutWidget, 'F', 430, 170, 160, 40, self.itmDef_c_arr)
        self.itmDef_c_arr[0][3].currentIndexChanged.connect(self.reselect_TW)

        ## 중요도
        self.cB_sel_priort_arr = copy.deepcopy(glb_vars.cB_priort_arr)
        self.cB_sel_priort_arr.insert(0, "전체선택")
        self.itmDef_a_arr = [["lb", "중요도", "cB", "self.cB_priority", self.cB_sel_priort_arr]]
        self.formLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.formLayoutWidget, 'F', 650, 170, 120, 40, self.itmDef_a_arr)
        self.itmDef_a_arr[0][3].currentIndexChanged.connect(self.reselect_TW)

        ## 처리상태
        self.cB_sel_prcsSts_arr = copy.deepcopy(glb_vars.cB_prcsSts_arr)
        self.cB_sel_prcsSts_arr.insert(0, "전체선택")
        self.itmDef_b_arr = [["lb", "처리상태", "cB", "self.cB_prcsSts", self.cB_sel_prcsSts_arr]]
        self.formLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.formLayoutWidget, 'F', 800, 170, 140, 40, self.itmDef_b_arr)
        self.itmDef_b_arr[0][3].currentIndexChanged.connect(self.reselect_TW)

        tW_hdr_arr = ["문서 번호", " 발생일  ", "등록인", " 조치일 ", "조치책임자", "문 의 유 형", "    제                     목    ", "중요도", "상태", " 단  지 ", " 고    객 ", "연 락 처", "  생성일  ", "  변경일  "]

        self.tableWidget = QTableWidget(self)
        glb_funcs.TableWidget_setting(self, self.tableWidget, 50, 200, 1100, 650, len(tW_hdr_arr), 0, 'N', 'N', 'N', 'Y')
        self.tableWidget.setSortingEnabled(True)

        glb_funcs.TableWidget_hdr_setting(self, self.tableWidget, 'H', 'R', 'lightblue', tW_hdr_arr, '')

        self.buttonBox = QDialogButtonBox(self)
        glb_funcs.final_decision_button_box(self, self.buttonBox, 1000, 890, 150, 30, "", "나가기", "", self.reject)

        self.setup_tW_info()
        # self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate

    def setup_tW_info(self):                     # Table Widget에 정보를 출력하는 루틴
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)              # table Widget를 재 수행할 때 row grid line이 삭제되지 않고 남아있는 것을 방지함
        for i in range(len(self.TW_info_list)):
            # self.tableWidget.removeRow(i)          # 위 self.tableWidget.setRowCount(0)로 인해 의미없어짐
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            for j in range(len(self.TW_info_list[i])):
                if j == 14: break
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)         # 각 Cell의 위치 지정
                if j == 0:
                    self.tableWidget.item(i, j).setBackground(QColor(249, 251, 254))  # 특정 Cell의 배경색깔 지정
                item.setText(str(self.TW_info_list[i][j]))

    def reselect_TW(self):                       # TableWidget 바로위 검색 필터에서 지정한 Key로 다시 화면에 출력될 리스트를 필터하는 루틴
        self.TW_info_list = copy.deepcopy(self.orgnl_TW_info_list)

        ## 중요도
        temp_TW_info_list = []
        if self.itmDef_a_arr[0][3].currentIndex() == 0:
            temp_TW_info_list = self.TW_info_list
        else:
            for i in range(len(self.TW_info_list)):
                if self.TW_info_list[i][7] == self.itmDef_a_arr[0][3].currentText():
                    temp_TW_info_list.append(self.TW_info_list[i])
        self.TW_info_list = temp_TW_info_list

        ## 처리상태
        temp_TW_info_list = []
        if self.itmDef_b_arr[0][3].currentIndex() == 0:
            temp_TW_info_list = self.TW_info_list
        else:
            for i in range(len(self.TW_info_list)):
                if self.TW_info_list[i][8] == self.itmDef_b_arr[0][3].currentText():
                    temp_TW_info_list.append(self.TW_info_list[i])
        self.TW_info_list = temp_TW_info_list

        ## 선택일자
        temp_TW_info_list = []
        if self.itmDef_c_arr[0][3].currentIndex() == 0:
            temp_TW_info_list = self.TW_info_list
        else:
            idx = self.itmDef_c_arr[0][3].currentIndex()
            for i in range(len(self.TW_info_list)):
                if QDate.fromString(self.TW_info_list[i][1], 'yyyy-MM-dd') == QDate.fromString(self.itmDef_c_arr[0][3].currentText(), 'yyyy-MM-dd'):
                    temp_TW_info_list.append(self.TW_info_list[i])

        self.TW_info_list = temp_TW_info_list

        self.setup_tW_info()

    ## Table Widget내의 특정 Cell을 더블클릭했을때 처리되는 내용
    def tableWidget_doubleClicked(self):
        row = self.tableWidget.currentIndex().row()
        col = self.tableWidget.currentIndex().column()

        glb_vars.helpDeskEdtSts = "D"              # 조회

        glb_vars.sel_docNo = int(self.TW_info_list[row][0])
        glb_vars.sel_docNo_wrt_info = self.TW_info_list[row][12]
        glb_vars.data_changed_signal = ''
        win = Ui_HelpDesk()
        win.exec_()
        if glb_vars.data_changed_signal != '':
            self.refreshInfo()

    ## 추가 버튼
    def addInfo(self):
        if glb_vars.hlpDskUsr != '':
            glb_vars.helpDeskEdtSts = "C"          # 신규 생성
            glb_vars.data_changed_signal = ''

            win = Ui_HelpDesk()
            win.exec_()
            if glb_vars.data_changed_signal != '':
                self.refreshInfo()
        else:
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "신규 등록 권한이 없습니다", "확인")
            return

    def drawChart(self):
        glb_vars.arr_sum = sum(self.prcSts_cnt_arr)
        if glb_vars.arr_sum == 0:
            glb_funcs.message_box_1(self, QMessageBox.Information, "정보", "그래프를 그릴 대상이 없습니다", "확인")
            return

        items = ['파이', '막대', '꺽은선']
        glb_vars.graph_type = ''
        item_data, ok = QInputDialog.getItem(self, 'Input Dialog', "그래프 종류 선택하기", items)  # ComboBox용 Dialog 화면을 출력하여 정보를 선택할 수 있게 함
        if ok:
           glb_vars.graph_type = item_data
        else:
            return
        print(glb_vars.graph_type)
        glb_vars.graph_info_list = []
        for i in range(len(glb_vars.k0040_list)):
            glb_vars.graph_info_list.append([glb_vars.k0040_list[i][1], self.prcSts_cnt_arr[i], self.prcSts_cnt_arr[i] / glb_vars.arr_sum])
        win = Ui_Graph()
        win.exec_()

    def refreshInfo(self):                   # 최신정보 갱신 버튼
        self.close()
        self.__init__()
        # self.show()
        self.exec_()

    ## 조치내용 등록 버튼
    def fixInfo(self):
        if glb_vars.hlpDskFixer == '':
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "현 로그인 ID 대해 조치 등록 권한이 없습니다", "확인")
            return

        row = self.tableWidget.currentIndex().row()
        col = self.tableWidget.currentIndex().column()

        if row < 0:
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "작업할 대상을 지정하시오", "확인")
            return
        glb_vars.helpDeskEdtSts = "F"  # 조치
        glb_vars.sel_docNo = int(self.TW_info_list[row][0])
        glb_vars.sel_docNo_wrt_info = self.TW_info_list[row][12]

        if self.TW_info_list[row][15] != glb_vars.loginID:
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "해당건의 조치책임자가 아닙니다", "확인")
            return

        glb_vars.data_changed_signal = ''
        win = Ui_HelpDesk()
        win.exec_()
        if glb_vars.data_changed_signal != '':
            self.setup_tW_info()

    ## 삭제버튼ㄲ
    def delInfo(self):
        row = self.tableWidget.currentIndex().row()
        col = self.tableWidget.currentIndex().column()
        if col != 0:
            glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "삭제할 문서번호를 정확히 지정하시오", "확인")
            return
        msgCd = 0
        del_idx = -1
        Msg_Set = { 1: "상태가 '접수'가 아니면 삭제불가 합니다", 2: "초지내용에 작성중인 내용이 있습니다", 3: " 현재 로그인 ID가 작성자와 다릅니다" }
        for i in range(len(glb_vars.sel_hlpDsk_list)):
            if str(glb_vars.sel_hlpDsk_list[i][0]) == str(self.TW_info_list[row][0]):
               if   glb_vars.sel_hlpDsk_list[i][9] != '접수' :               msgCd = 1
               elif glb_vars.sel_hlpDsk_list[i][12].strip() != '':          msgCd = 2
               elif glb_vars.sel_hlpDsk_list[i][14]!= glb_vars.loginID:     msgCd = 3
               del_idx = i       # 삭제 대상
               break

        if msgCd != 0:
            glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", Msg_Set[msgCd], "확인")
            return

        if del_idx != -1:                    # index가 -1은 어떤 것도 선택 혹은 지정되지 않았다는 의미임
            glb_funcs.message_box_2(self, QMessageBox.Question, "저장", "선택 번호에 대한 삭제를 진행하시겠습니까?", "예", "아니오")
            if glb_funcs.MsgBoxRtnSignal == 'N':
                return

        glb_vars.hlpDsk_list = glb_funcs.get_from_srcTable(self, 'xls', glb_vars.strgPostion, 'helpDeskList.xlsx')
        k = -1
        for i in range(len(glb_vars.hlpDsk_list)):
            if str(glb_vars.hlpDsk_list[i][0]) == str(self.TW_info_list[row][0]):
                k = i
                break
        if k == -1:
            glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "삭제할 문서번호가 DB 저장소에 존재하지 않습니다", "확인")
            return
        glb_vars.hlpDsk_list.__delitem__(k)

        glb_funcs.save_to_trgtTable(self, 'xls', glb_vars.hlpDsk_list, glb_vars.hlpDsk_hdr_title, glb_vars.strgPostion, 'helpDeskList.xlsx')
        glb_vars.data_changed_signal = 'Y'  # 이전 Dialog 화면에 화면 Refresh를 하도록 전달
        glb_funcs.message_box_1(self, QMessageBox.Information, "정보", "삭제처리 되었습니다.", "확인")
        glb_vars.sel_hlpDsk_list.__delitem__(del_idx)

        self.setup_tW_info()

  ## TableWidget에 리스트 출력시 Sorting에 대한 기능
    #1. 먼저 Sorting 기능을 활성화 하기 위해서는 반드시 앞서 "self.tableWidget.setSortingEnabled(True)"가 지정되어야 함
    #2. self.tableWidget.sortByColumn(col_no, option)을 지정하면 TableWidget에 리스트 출력시 지정된 특정 Column을 기준으로 Sorting되어 출력됨
    #   (col_no는 헤더의 Column 순서번호, option은 [Qt.AscendingOrder, Qt.AscendingOrder]중 하나 선택됨
    #3. 특정 헤더의 Column(A Column)을 눌렀을 때 눌러진 해당 Column이 아닌 다른 Column(B Column)이 지정된 방식으로만 Sorting 되도록 하기위해서는
    #   self.tableWidget.horizontalHeader().sortIndicatorChanged.connect(self.handleSortIndicatorChanged)
    #   def handleSortIndicatorChanged(self, index, order):         # --> index: 눌러진 Column(A Column), order: 0(Ascending), 1(Descending)
    #       if index == col_no_a:                                     # --> col_no_a = (눌러진 Column(A Column))
    #          self.tableWidget.horizontalHeader().setSortIndicator(col_no_b, Qt.AscendingOrder)  # --> col_no_b(Sorting 대상 Column)