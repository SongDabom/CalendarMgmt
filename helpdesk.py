# from import_list import *
# from helpdesklist import  *
from search_N_get_Cd_Nm import *

import glb_funcs
import glb_vars

class Ui_HelpDesk(QDialog):
    def __init__(self):
        super().__init__()
        self.getInitData()
        self.setupUi()

    def getInitData(self):
        self.sel_hlpDsk_info_arr = []
        self.fixer_list = []
        self.fixerID = self.fixerNm = self.grpCd = self.grpCdTxt = self.inqTp = self.inqTpTxt = ''
        self.cB_priort_activIdx = self.cB_prcsSts_activIdx = 0

        # 기본적으로 화면내 모든 입력 필드를 ReadOnly로 지정함
        self.scr_wrtDt_opt = self.scr_fixDt_opt = self.scr_custNm_opt = self.scr_custPhno_opt = 1
        self.scr_cB_priort_opt = self.scr_cB_prcsSts_opt = self.scr_title_opt = self.scr_inquery_opt = self.scr_response_opt = self.scr_remark_opt = 1

        for i in range(len(glb_vars.fixer_list)):
            self.fixer_list.append([glb_vars.fixer_list[i][0], glb_vars.fixer_list[i][1] + ' ' + glb_vars.fixer_list[i][3] + '//' + glb_vars.fixer_list[i][2]])

        if   glb_vars.helpDeskEdtSts == "C":         # 신규등록
            self.wrtDt  = QDate.currentDate()                 # 발생일 = 이전 화면 list 선택일
            self.fixDt  = self.wrtDt.addDays(14)            # 조치일: 발생일로 부터 14일 후
            if self.fixDt <= QDate.currentDate():           # 조치일이 현재일 보다 작은 경우 현재일 부터 14일 지정
                self.fixDt = self.fixDt.addDays(14)
            self.wrtrInfo = glb_vars.loginID_info           # 작성자 정보 : 신규등록시 현 로그인 ID
            self.scr_response_opt = 0
            for i in range(19):
                self.sel_hlpDsk_info_arr.append("")
        else:                                        # 변경, 조치, 조회
            for i in range(len(glb_vars.sel_hlpDsk_list)):
                if str(glb_vars.sel_hlpDsk_list[i][0]) == str(glb_vars.sel_docNo):
                    self.sel_hlpDsk_info_arr = glb_vars.sel_hlpDsk_list[i]
                    print(self.sel_hlpDsk_info_arr)
                    for j in range(len(self.fixer_list)):
                        if self.fixer_list[j][0] == self.sel_hlpDsk_info_arr[3]:      # 조치책임자
                            self.fixerID = self.fixer_list[j][0]
                            self.fixerNm = self.fixer_list[j][1]
                            break
                    for j in range(len(glb_vars.k0010_list)):
                        if glb_vars.k0010_list[j][0] == str(self.sel_hlpDsk_info_arr[4]):   # 단지코드
                            self.grpCd   = glb_vars.k0010_list[j][0]
                            self.grpCdTxt = glb_vars.k0010_list[j][1]
                            break
                    for j in range(len(glb_vars.k0020_list)):
                        if glb_vars.k0020_list[j][0] == self.sel_hlpDsk_info_arr[7]:   # 문의유형
                            self.inqTp    = glb_vars.k0020_list[j][0]
                            self.inqTpTxt = glb_vars.k0020_list[j][1]
                            break
                    for j in range(len(glb_vars.k0030_list)):
                        if glb_vars.k0030_list[j][0] == self.sel_hlpDsk_info_arr[8]:       # 중요도
                            self.cB_priort_activIdx = j           # 중요도의 Default 지정 Index
                            break
                    for j in range(len(glb_vars.k0040_list)):
                        if glb_vars.k0040_list[j][0] == self.sel_hlpDsk_info_arr[9]:       # 처리상태
                            self.cB_prcsSts_activIdx = j           # 처리상태의 Default 지정 Index
                            break
                    break
            self.wrtDt = self.sel_hlpDsk_info_arr[1]             # 작성일
            self.fixDt = self.sel_hlpDsk_info_arr[2]             # 조치일
            self.wrtrInfo = glb_vars.sel_docNo_wrt_info          # 작성자 정보

            ## 화면상 각 입력필드에 대한 입력 혹은 ReadOnly 지정 ( "0" 이면 ReadOnly)
            if   glb_vars.helpDeskEdtSts == "D":         # 조회
                self.scr_wrtDt_opt = self.scr_fixDt_opt = self.scr_custNm_opt = self.scr_custPhno_opt = 0
                self.scr_cB_priort_opt = self.scr_cB_prcsSts_opt = self.scr_title_opt = self.scr_inquery_opt = self.scr_response_opt = self.scr_remark_opt = 0
            elif glb_vars.helpDeskEdtSts == "M":         # 수정
                self.scr_response_opt = 0
            elif glb_vars.helpDeskEdtSts == "F":         # 조치
                self.scr_wrtDt_opt = self.scr_custNm_opt = self.scr_custPhno_opt = 0
                self.scr_cB_priort_opt = self.scr_cB_prcsSts_opt = self.scr_title_opt = self.scr_inquery_opt = 0

    def setupUi(self):
        glb_funcs.winFlame_setting(self, 'R', 1010, 950, '', 'C', '', "Help Desk", '', 'N', 'N', 'N')

        ## Title
        self.lb_title = QLabel(self)
        glb_funcs.label_setting(self, self.lb_title, 0, 30, 1010, 80, 'C', 'HelpDesk 업무 일지')
        glb_funcs.fontSetting(self, self.lb_title, '6B', 20, " ")  # "에스코어 드림 6 Bold", PointSize(20)

        if glb_vars.helpDeskEdtSts != "C":                         # 신규등록
            self.lb_docNo = QLabel(self)
            glb_funcs.label_setting(self, self.lb_docNo, 50, 80, 200, 40, 'L', '문서 번호 :' + str(self.sel_hlpDsk_info_arr[0]))
            glb_funcs.fontSetting(self, self.lb_docNo, '5M', 10, " ")  # "에스코어 드림 5 Medium", PointSize(10)

        self.l_currTm = QLabel(self)
        glb_funcs.label_setting(self, self.l_currTm, 800, 80, 150, 20, 'C', datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

        ## 작성자
        itmDef_1_arr = [["lb", "작   성   자", "lE", "self.lE_writer", ""]]
        self.grdLytWidget_1 = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.grdLytWidget_1, 'G', 50, 130, 500, 40, itmDef_1_arr)
        itmDef_1_arr[0][3].setText(self.wrtrInfo)
        glb_funcs.readOnly_setting(self, 'lE', itmDef_1_arr[0][3], 0)

        ## 작성일, 조치일
        self.itmDef_2_arr = [["lb", "               발생일", "dE", "self.dE_wrtDt", ""], ["lb", "               조치일", "dE", "self.de_fixDt", ""]]
        self.grdLytWidget_2 = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.grdLytWidget_2, 'G', 750, 130, 200, 70, self.itmDef_2_arr)
        self.itmDef_2_arr[0][3].setDate(self.wrtDt)
        glb_funcs.readOnly_setting(self, 'dE', self.itmDef_2_arr[0][3], self.scr_wrtDt_opt)
        self.itmDef_2_arr[1][3].setDate(self.fixDt)
        glb_funcs.readOnly_setting(self, 'dE', self.itmDef_2_arr[1][3], self.scr_fixDt_opt)

        ##조치책임자
        self.itmDef_a_arr = [["lb", "조치책임자", "lE", "self.lE_fxrCd", "R"]]
        self.horizLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.horizLayoutWidget, 'H', 50, 170, 150, 40, self.itmDef_a_arr)
        self.itmDef_a_arr[0][3].setText(self.fixerID)

        ##  조치책임자 탐색 Icon, 초치책임자명
        self.itmDef_b_arr = [["tB", "self.tB_fxrCd", "lE", "self.lE_fxrCdTxt", "R"]]
        self.horizLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.horizLayoutWidget, 'H', 200, 170, 350, 40, self.itmDef_b_arr)
        icon = QIcon()
        icon.addPixmap(QPixmap('img/magnifying-glass.png'), QIcon.Normal, QIcon.Off)
        self.itmDef_b_arr[0][1].setIcon(icon)
        self.itmDef_b_arr[0][1].clicked.connect(self.seach_grpCode_3)
        self.itmDef_b_arr[0][3].setText(self.fixerNm)

        ## 단지코드
        self.itmDef_3_arr = [["lb", "단지   코드", "lE", "self.lE_grpCd", "R"]]
        self.horizLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.horizLayoutWidget, 'H', 50, 210, 150, 40, self.itmDef_3_arr)
        self.itmDef_3_arr[0][3].setText(self.grpCd)

        ## 단지코드 탐색 Icon, 단지코드명
        self.itmDef_4_arr = [["tB", "self.tB_grpCd", "lE", "self.lE_grpCdTxt", "R"]]
        self.horizLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.horizLayoutWidget, 'H', 200, 210, 350, 40, self.itmDef_4_arr)
        icon = QIcon()
        icon.addPixmap(QPixmap('img/magnifying-glass.png'), QIcon.Normal, QIcon.Off)
        self.itmDef_4_arr[0][1].setIcon(icon)
        self.itmDef_4_arr[0][1].clicked.connect(self.seach_grpCode_1)
        self.itmDef_4_arr[0][3].setText(self.grpCdTxt)

        ## 고객명, 연락처
        self.itmDef_5_arr = [["lb", "   고객명", "lE", "self.lE_custNm", ""], ["lb", "  연락처","lE", "self.lE_custPhno", ""]]
        self.horizontalLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.horizontalLayoutWidget, 'H', 590, 216, 360, 30, self.itmDef_5_arr)
        self.itmDef_5_arr[0][3].setText(self.sel_hlpDsk_info_arr[5])
        glb_funcs.readOnly_setting(self, 'lE', self.itmDef_5_arr[0][3], self.scr_custNm_opt)
        self.itmDef_5_arr[1][3].setText(self.sel_hlpDsk_info_arr[6])
        glb_funcs.readOnly_setting(self, 'lE', self.itmDef_5_arr[1][3], self.scr_custPhno_opt)

        ## 문의유형
        self.itmDef_6_arr = [["lb", "문의   유형", "lE", "self.lE_inqTp", "R"]]
        self.horizLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.horizLayoutWidget, 'H', 50, 250, 150, 40, self.itmDef_6_arr)
        self.itmDef_6_arr[0][3].setText(self.inqTp)

        ## 문의유형 탐색 Icon, 문의유형명
        self.itmDef_7_arr = [["tB", "self.tB_inqTp", "lE", "self.lE_inqTpTxt", "R"]]
        self.horizLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.horizLayoutWidget, 'H', 200, 250, 350, 40, self.itmDef_7_arr)
        icon = QIcon()
        icon.addPixmap(QPixmap('img/magnifying-glass.png'), QIcon.Normal, QIcon.Off)
        self.itmDef_7_arr[0][1].setIcon(icon)
        self.itmDef_7_arr[0][1].clicked.connect(self.seach_grpCode_2)
        self.itmDef_7_arr[0][3].setText(self.inqTpTxt)

        ## 중요도
        self.itmDef_8_arr = [["lb", "중요도", "cB", "self.cB_priority", glb_vars.cB_priort_arr]]
        self.formLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.formLayoutWidget, 'F', 610, 260, 120, 40, self.itmDef_8_arr)
        self.itmDef_8_arr[0][3].setCurrentIndex(self.cB_priort_activIdx)
        if glb_vars.helpDeskEdtSts == "D":  # 조회
            self.itmDef_8_arr[0][3].setEnabled(False)                 # Combox를 Read Only 처럼 지정

        ## 처리상태
        self.itmDef_9_arr = [["lb", "처리상태", "cB", "self.cB_prcsSts", glb_vars.cB_prcsSts_arr]]
        self.formLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.formLayoutWidget, 'F', 760, 260, 190, 40, self.itmDef_9_arr)
        self.itmDef_9_arr[0][3].setCurrentIndex(self.cB_prcsSts_activIdx)
        if glb_vars.helpDeskEdtSts == "D":                            # 조회
            self.itmDef_9_arr[0][3].setEnabled(False)                 # ComboBox를 Read Only 처럼 지정

        ### 제목, 문의내용, 조치내용, 비고
        self.grd_itmDef_arr = [["lb", "제       목", "lE", "self.lE_title", ""], ["lb", "문의 내용", "tE", "self.tE_inquery", ""],
                          ["lb", "조치 내용", "tE", "self.self.tE_response", ""], ["lb", "비       고", "tE", "self.tE_remark", ""]]

        self.gridLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.gridLayoutWidget, 'G', 50, 320, 900, 530, self.grd_itmDef_arr)
        self.grd_itmDef_arr[0][3].setText(self.sel_hlpDsk_info_arr[10])                            # 제목
        glb_funcs.readOnly_setting(self, 'lE', self.grd_itmDef_arr[0][3], self.scr_title_opt)
        self.grd_itmDef_arr[1][3].setText(self.sel_hlpDsk_info_arr[11])                            # 문의내용
        glb_funcs.readOnly_setting(self, 'tE', self.grd_itmDef_arr[1][3], self.scr_inquery_opt)
        self.grd_itmDef_arr[2][3].setText(self.sel_hlpDsk_info_arr[12])                            # 조치내용
        glb_funcs.readOnly_setting(self, 'tE', self.grd_itmDef_arr[2][3], self.scr_response_opt)
        self.grd_itmDef_arr[3][3].setText(self.sel_hlpDsk_info_arr[13])                            # 비고
        glb_funcs.readOnly_setting(self, 'tE', self.grd_itmDef_arr[3][3], self.scr_remark_opt)

        ## 처리버튼(저장, 취소)
        self.buttonBox = QDialogButtonBox(self)
        if glb_vars.helpDeskEdtSts == "D":  # 조회
            tool_button_arr = ["내용수정", 100, 880, 30, 30, "img/edit.png", 30, 30, self.modifyInfo]
            for i in range(len(tool_button_arr)):
                self.toolButton = QToolButton(self)
                glb_funcs.tool_button_setting(self, self.toolButton, tool_button_arr)

            glb_funcs.final_decision_button_box(self, self.buttonBox, 800, 890, 150, 30, "", "나가기", "", self.reject)
        else:
            glb_funcs.final_decision_button_box(self, self.buttonBox, 800, 890, 150, 30, "저장", "취소", self.accept, self.reject)

        self.retranslateUi()
        # QMetaObject.connectSlotsByName(self)

    def seach_grpCode_1(self):     # 단지코드 검색용 Function
        if glb_vars.helpDeskEdtSts == "D" or glb_vars.helpDeskEdtSts == "F":  # 조회, 조치
            return
        glb_vars.search_winTitle = "단지  코드 검색"
        win = Ui_Srch_N_Get_Cd_Nm()
        win.grpCd   = self.itmDef_3_arr[0][3].text()
        win.grpCdNm = self.itmDef_4_arr[0][3].text()
        win.code_grp_list = glb_vars.k0010_list
        win.exec_()
        self.itmDef_3_arr[0][3].setText(win.grpCd)
        self.itmDef_4_arr[0][3].setText(win.grpCdNm)

    def seach_grpCode_2(self):     # 문의유형 검색용 Function
        if glb_vars.helpDeskEdtSts == "D" or glb_vars.helpDeskEdtSts == "F":  # 조회, 조치
            return
        glb_vars.search_winTitle = "문의  유형 검색"
        win = Ui_Srch_N_Get_Cd_Nm()
        win.grpCd   = self.itmDef_6_arr[0][3].text()
        win.grpCdNm = self.itmDef_7_arr[0][3].text()
        win.code_grp_list = glb_vars.k0020_list
        win.exec_()
        self.itmDef_6_arr[0][3].setText(win.grpCd)
        self.itmDef_7_arr[0][3].setText(win.grpCdNm)

    def seach_grpCode_3(self):      # 처리책임자 검색용 Function
        if glb_vars.helpDeskEdtSts == "D" or glb_vars.helpDeskEdtSts == "F":  # 조회, 조치
            return
        glb_vars.search_winTitle = "조치책임자 검색"
        win = Ui_Srch_N_Get_Cd_Nm()
        win.grpCd   = self.itmDef_a_arr[0][3].text()
        win.grpCdNm = self.itmDef_b_arr[0][3].text()
        win.code_grp_list = self.fixer_list
        win.exec_()
        self.itmDef_a_arr[0][3].setText(win.grpCd)
        self.itmDef_b_arr[0][3].setText(win.grpCdNm)

    def retranslateUi(self):
        _translate = QCoreApplication.translate

    def accept(self):
        msgCd = 0
        if   self.itmDef_a_arr[0][3].text() == '': msgCd = 1             # 조치책임자
        elif self.itmDef_3_arr[0][3].text() == '': msgCd = 2             # 단지코드
        elif self.itmDef_5_arr[0][3].text() == '': msgCd = 3             # 고객명
        elif self.itmDef_5_arr[1][3].text() == '': msgCd = 4             # 고객연락처
        elif self.itmDef_6_arr[0][3].text() == '': msgCd = 5             # 문의유형
        elif self.grd_itmDef_arr[0][3].text() == '': msgCd = 6             # 제목
        elif self.grd_itmDef_arr[1][3].toPlainText() == '': msgCd = 7             # 문의내용

        if glb_vars.helpDeskEdtSts == "F":   #  조치
            if self.grd_itmDef_arr[2][3].toPlainText() == '': msgCd = 8           # 조치내용

        Msg_Set = { 1: "조치책임자", 2: "단지코드", 3: "고객명", 4: "고객연락처", 5: "문의유형", 6: "제목", 7: "문의내용", 8: "조치내용" }

        if msgCd != 0:
            glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", Msg_Set[msgCd] + " 정보가 입력되지 않았습니다.", "확인")
            return

        if self.itmDef_2_arr[0][3].date() > self.itmDef_2_arr[1][3].date():     # 작성일 > 조치일
            glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "작성일은 조치일을 초과할 수 없습니다.", "확인")
            return

        glb_funcs.message_box_2(self, QMessageBox.Question, "저장", "작업을 저장하시겠습니까?", "예", "아니오")
        if glb_funcs.MsgBoxRtnSignal == 'N':
            return

        priority = prcsSts = ''
        if glb_vars.k0030_list != []:           # 기준정보 Tab에서 해당 코드 Set(중요도)이 등록되지 않았을 경우
            priority = glb_vars.k0030_list[self.itmDef_8_arr[0][3].currentIndex()][0]
        if glb_vars.k0040_list != []:           # 기준정보 Tab에서 해당 코드 Set(처리상태)이 등록되지 않았을 경우
            prcsSts  = glb_vars.k0040_list[self.itmDef_9_arr[0][3].currentIndex()][0]

        glb_vars.hlpDsk_list = glb_funcs.get_from_srcTable(self, 'xls', glb_vars.strgPostion, 'helpDeskList.xlsx')
        if   glb_vars.helpDeskEdtSts == "C":  # 신규등록
            if glb_vars.hlpDsk_list == []:                         # helpDeskList.xlsx field이 존재하기 않음(최조 생성상태)
                DocNo = int(glb_vars.sysSetting_info_arr[1]) + 1
            else:
                DocNo = int(glb_vars.hlpDsk_list[-1][0]) + 1       # helpDeskList.xlsx에서 최종문서번호를 찿아 1을 더해 신규문서번호 확정
            crtID = glb_vars.loginID
            crtDate = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            chgID = ''
            chgDate = ''
        else:                                  # 변경, 조치 (조회는 처음부터 이 Method를 거치지 않음)
            DocNo = glb_vars.sel_docNo
            crtID = self.sel_hlpDsk_info_arr[14]
            crtDate = self.sel_hlpDsk_info_arr[15]
            chgID = glb_vars.loginID
            if glb_vars.helpDeskEdtSts == "F":   #  조치
                chgID = self.itmDef_a_arr[0][3].text()
            chgDate = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

            ## glb_vars.hlpDsk_list에서 변경대상을 삭제하고 변경할 대상을 추가하여 정렬한 후 다시 PC File로 저장함
            k = -1                                    # 0 으로 하면 실제 첫번째 변경건이 있을 수 있기 때문임
            for i in range(len(glb_vars.hlpDsk_list)):
                print("hD_list = ", glb_vars.hlpDsk_list[i][0], "화면 =", glb_vars.sel_docNo)
                if str(glb_vars.hlpDsk_list[i][0]) == str(glb_vars.sel_docNo):
                    k = i
                    break
            if k == -1:
                glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "해당건의 문서번호가 존재하지 않습니다. 점검 필요", "확인")
                return
            glb_vars.hlpDsk_list.__delitem__(k)

            ## glb_vars.sel_hlpDsk_list에서 변경대상을 삭제하고 변경할 대상을 추가(이전 Dialog화면에 바로 반영되게 하기 위해)
            k = -1  # 0 으로 하면 실제 첫번째 변경건이 있을 수 있기 때문임
            for i in range(len(glb_vars.sel_hlpDsk_list)):
                if str(glb_vars.sel_hlpDsk_list[i][0]) == str(glb_vars.sel_docNo):
                    k = i
                    break
            glb_vars.sel_hlpDsk_list.__delitem__(k)

        ## 화면의 저장대상 정비하기
        #glb_vars.hlpDsk_hdr_title = ['문서번호', '작성일', '조치일', '조치책임자', '단지코드', '고객명', '연락처', '문의유형', '중요도', '처리상태', '제목', '문의내용', '조치내용', '비고', '생성인', '생성일', '변경인', '변경일']
        hlpDsk_info_append_list = []
        hlpDsk_info_append_list.append([str(DocNo), QDate.toString(self.itmDef_2_arr[0][3].date(), "yyyy-MM-dd"), QDate.toString(self.itmDef_2_arr[0][3].date(), "yyyy-MM-dd"),
                                        self.itmDef_a_arr[0][3].text(), str(self.itmDef_3_arr[0][3].text()), str(self.itmDef_5_arr[0][3].text()), str(self.itmDef_5_arr[1][3].text()),
                                        self.itmDef_6_arr[0][3].text(), priority, prcsSts, self.grd_itmDef_arr[0][3].text(), self.grd_itmDef_arr[1][3].toPlainText(),
                                        self.grd_itmDef_arr[2][3].toPlainText(), self.grd_itmDef_arr[3][3].toPlainText(), crtID, crtDate, chgID, chgDate])

        glb_vars.hlpDsk_list.append(hlpDsk_info_append_list[0])                # 저장대상 기존 정보와 합치기
        list.sort(glb_vars.hlpDsk_list, key=lambda k: k[0])                    # 문서번호로 정렬
        glb_funcs.save_to_trgtTable(self, 'xls', glb_vars.hlpDsk_list, glb_vars.hlpDsk_hdr_title, glb_vars.strgPostion, 'helpDeskList.xlsx')

        glb_vars.data_changed_signal = 'Y'                                     # 이전 Dialog 화면에 화면 Refresh를 하도록 전달
        glb_funcs.message_box_1(self, QMessageBox.Information, "정보", "저장되었습니다.", "확인")

        hlpDsk_info_append_list[0][1] = QDate.fromString(hlpDsk_info_append_list[0][1], 'yyyy-MM-dd')          # 이전 화면(helpDesk List)의 등록일자
        hlpDsk_info_append_list[0][2] = QDate.fromString(hlpDsk_info_append_list[0][2], 'yyyy-MM-dd')          # 이전 화면(helpDesk List)의 조치일자
        glb_vars.sel_hlpDsk_list.append(hlpDsk_info_append_list[0])             # 이전 Dialog 화면(helpDesk List)의 출력에 관여된 List type에 반영
        self.close()

    def modifyInfo(self):
        if self.sel_hlpDsk_info_arr[14] != glb_vars.loginID:
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "해당건의 등록자가 아닙니다", "확인")
            return
        glb_vars.helpDeskEdtSts = "M"
        self.close()
        self.__init__()
        self.exec_()

    # def accept(self):