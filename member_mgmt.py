from import_list import *
import glb_funcs
import glb_vars

class Ui_Member(QDialog):
    def __init__(self):
        super().__init__()
        self.getInitData()
        self.setupUi()

    def getInitData(self):
        self.title_opt = self.chgr = self.chgDt = ''
        self.generalUsr = self.hlpDskUsr = self.hlpDskSolver = True
        if glb_vars.loginID_modify_opt == 'Y':  # member ID 정보 수정
            self.title_opt = '변경'
            self.ID = glb_vars.df_mbr_arr[0][0]  # ID
            self.pwd = glb_vars.df_mbr_arr[0][1]  # Password
            self.name = glb_vars.df_mbr_arr[0][2]  # 이름
            self.cellPhone = glb_vars.df_mbr_arr[0][3]  # 개인 전화
            self.bizPhone = glb_vars.df_mbr_arr[0][4]  # 부서 전화
            self.addr = glb_vars.df_mbr_arr[0][5]  # 주소
            self.comNm = glb_vars.df_mbr_arr[0][6]  # 회사명
            self.deptNm = glb_vars.df_mbr_arr[0][7]  # 부서명
            self.bizPosition = glb_vars.df_mbr_arr[0][8]  # 직책
            self.crtr = glb_vars.df_mbr_arr[0][12]  # 생성인
            self.crtDt = glb_vars.df_mbr_arr[0][13]  # 생성일
            if glb_vars.df_mbr_arr[0][9] == '':    # 일반사용자
                self.generalUsr = False
            if glb_vars.df_mbr_arr[0][10] == '':   # Help Desk 등록자
                self.hlpDskUsr = False
            if glb_vars.df_mbr_arr[0][11] == '':   # 조치 책임자
                self.hlpDskSolver = False
        else:
            self.title_opt = '등록'

    def setupUi(self):
        glb_funcs.winFlame_setting(self, 'R', 500, 630, '', 'C', '', "회원정보", '', 'N', 'N', 'N')

        self.lb_title = QLabel(self)
        glb_funcs.label_setting(self, self.lb_title, 0, 20, 500, 40, 'C', '회원정보 ' + self.title_opt)
        glb_funcs.fontSetting(self, self.lb_title, '6B', 20, " ")  # "에스코어 드림 6 Bold", PointSize(20)

        self.itmDef_1_arr = [["CB", "일반사용", "CB", "self.CB_usrTp1", ""], ["CB", "HelpDesk 등록", "CB", "self.CB_usrTp2", ""],
                          ["CB", "HelpDesk 조치 책임", "CB", "self.CB_usrTp3", ""]]
        self.horzLytWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.horzLytWidget, 'H', 30, 80, 450, 30, self.itmDef_1_arr)
        self.itmDef_1_arr[0][3].setChecked(self.generalUsr)
        self.itmDef_1_arr[1][3].setChecked(self.hlpDskUsr)
        self.itmDef_1_arr[2][3].setChecked(self.hlpDskSolver)

        self.lb_Title = QLabel(self)
        glb_funcs.label_setting(self, self.lb_Title, 30, 120, 450, 15, 'R', '(*)표시 항목은 필수 입력대상입니다)')
        self.lb_Title.setStyleSheet("Color : red")

        self.itmDef_2_arr = [["lb", "회원 ID (*)", "lE", "self.lE_loginID", ""], ["lb", "비밀번호 (*)", "lE", "self.lE_loginPWD1", ""], ["lb", "비밀번호 확인 (*)", "lE", "self.lE_loginPWD2", ""],
                          ["lb", "이름 (*)", "lE", "self.lE_name", ""], ["lb", "개인 연락처 (*)", "lE", "self.lE_cellPhn", ""], ["lb", "업무 연락처", "lE", "self.lE_offcPhn", ""],
                          ["lb", "주소", "lE", "self.lE_addr", ""], ["lb", "회사명", "lE", "self.lE_compNm", ""], ["lb", "부서명", "lE", "self.lE_deptNm", ""],
                          ["lb", "직책", "lE", "self.lE_offcPstn", ""]]

        self.gridLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.gridLayoutWidget, 'G', 30, 130, 450, 400, self.itmDef_2_arr)
        if glb_vars.loginID_modify_opt == 'Y':  # member ID 정보 수정
            self.itmDef_2_arr[0][3].setText(glb_vars.loginID)
            self.itmDef_2_arr[0][3].setReadOnly(True)
            self.itmDef_2_arr[0][3].setStyleSheet("background: lightgray")
            self.itmDef_2_arr[1][3].setText(self.pwd)
            self.itmDef_2_arr[2][3].setText(self.pwd)
            self.itmDef_2_arr[3][3].setText(self.name)
            self.itmDef_2_arr[4][3].setText(self.cellPhone)
            self.itmDef_2_arr[5][3].setText(self.bizPhone)
            self.itmDef_2_arr[6][3].setText(self.addr)
            self.itmDef_2_arr[7][3].setText(self.comNm)
            self.itmDef_2_arr[8][3].setText(self.deptNm)
            self.itmDef_2_arr[9][3].setText(self.bizPosition)
        else:
            self.itmDef_2_arr[0][3].setPlaceholderText("공백을 입력하지 마시오")
            self.itmDef_2_arr[4][3].setPlaceholderText("999-9999-9999 형식으로 입력하시오")
            self.itmDef_2_arr[5][3].setPlaceholderText("지역번호-999-9999 형식으로 입력하시오")

        self.itmDef_2_arr[1][3].setEchoMode(QLineEdit.Password)        # 비밀번호 입력/출력시 마스킹 처리
        self.itmDef_2_arr[2][3].setEchoMode(QLineEdit.Password)        # 비밀번호 입력/출력시 마스킹 처리

        self.buttonBox = QDialogButtonBox(self)
        glb_funcs.final_decision_button_box(self, self.buttonBox, 160, 580, 300, 30, "저장", "취소", self.accept, self.reject)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate

    def accept(self):
        generalUsr = hlpDskUsr = hlpDskSolver = ''
        if self.itmDef_1_arr[0][3].checkState() != 0: generalUsr = "X"                       # QRadioButton.isChecked()
        if self.itmDef_1_arr[1][3].checkState() != 0: hlpDskUsr = "X"
        if self.itmDef_1_arr[2][3].checkState() != 0: hlpDskSolver = "X"

        member_ID = self.itmDef_2_arr[0][3].text().strip()
        if member_ID == '' or self.itmDef_2_arr[1][3].text().strip() == '' or \
            self.itmDef_2_arr[3][3].text().strip() == '' or self.itmDef_2_arr[4][3].text().strip() == '':
           glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "필수 입력란에 등록되지 않은 정보가 있습니다", "확인")
           return
        elif self.itmDef_2_arr[1][3].text() != self.itmDef_2_arr[2][3].text():
            glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "비밀번호가 서로 동일하지 않습니다", "확인")
            return

        df_mbr_list = glb_funcs.get_from_srcTable(self, 'xls', glb_vars.strgPostion, 'member_master.xlsx')
        for i in range(len(df_mbr_list)):
            if df_mbr_list[i][0] == member_ID:
                if glb_vars.loginID_modify_opt == 'Y':    # ID 정보 변경"
                    df_mbr_list.__delitem__(i)
                    break
                glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "이미 등록되어 있는 ID 입니다", "확인")
                return

        if glb_vars.loginID_modify_opt == 'Y':  # ID 정보 변경"
            encryptedPwd = self.itmDef_2_arr[1][3].text()         # 비밀번호
            self.chgr = glb_vars.loginID  # 변경인
            self.chgDt = datetime.today().strftime('%Y-%m-%d %H:%M:%S')  # 변경일
            glb_vars.loginID_name = self.itmDef_2_arr[3][3].text()
            glb_vars.loginID_info = str(glb_vars.loginID_name) + ' ' + str(self.itmDef_2_arr[9][3].text()) + ' //' + str(self.itmDef_2_arr[8][3].text())  # 이름 직책 // 부서
            glb_vars.generalUsr = generalUsr
            glb_vars.hlpDskUsr = hlpDskUsr
            glb_vars.hlpDskFixer = hlpDskSolver

        else:
            ## 비밀번호 암호화
            password = str(self.itmDef_2_arr[1][3].text())
            password = password.encode('utf-8')
            passwordHash = bcrypt.hashpw(password, bcrypt.gensalt())
            encryptedPwd = passwordHash.decode()

            self.crtr = glb_vars.loginID  # 생성인
            self.crtDt = datetime.today().strftime('%Y-%m-%d %H:%M:%S')  # 생성일

        master_data_arr =[member_ID, encryptedPwd, self.itmDef_2_arr[3][3].text(),
                           self.itmDef_2_arr[4][3].text(), self.itmDef_2_arr[5][3].text(), self.itmDef_2_arr[6][3].text(),
                           self.itmDef_2_arr[7][3].text(), self.itmDef_2_arr[8][3].text(), self.itmDef_2_arr[9][3].text(),
                           generalUsr, hlpDskUsr, hlpDskSolver, self.crtr, self.crtDt, self.chgr, self.chgDt]

        # mbr_master_hdr_title = ['ID', '비밀번호', '이름', '개인연락처', '업무연락처', '주소', '회사명', '부서명', '직책', '일반사용', 'HelpDesk등록', 'HelpDesk조치', '생성인', '생성일', '변경인', '변경일']

        df_mbr_list.append(master_data_arr)
        list.sort(df_mbr_list, key=lambda k: (k[0]))
        # f = open(glb_vars.strgPostion + '/member_master.xlsx', "w")
        # print(f.mode)
        glb_funcs.save_to_trgtTable(self, 'xls', df_mbr_list, glb_vars.mbr_master_hdr_title, glb_vars.strgPostion, 'member_master.xlsx')
        glb_funcs.message_box_1(self, QMessageBox.Information, "성공", self.title_opt + " 되었습니다", "확인")
        glb_vars.data_changed_signal = 'Y'
        self.close()
