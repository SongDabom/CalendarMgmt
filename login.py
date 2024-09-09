from import_list import *
from mainwindow import  *
from member_mgmt import *

import glb_funcs
import glb_vars

class Ui_Login(QDialog):
    def __init__(self):
        super().__init__()
        self.getInitData()
        self.setupUi()

    def getInitData(self):
        print(glb_vars.loginID)

    def setupUi(self):
        glb_funcs.winFlame_setting(self, 'R', 300, 170, '', 'C', '', "Log In", '', 'N', 'N', 'N')

        if glb_vars.loginID_modify_opt == '':
            tool_button_arr = ["사용자 추가", 260, 15, 20, 20, "img/add_person", 20, 20, self.add_ID]
            self.toolButton = QToolButton(self)
            glb_funcs.tool_button_setting(self, self.toolButton, tool_button_arr)

        self.itmDef_arr = [["lb", "ID", "lE", "self.lE_loginID", ""], ["lb", "Password", "lE", "self.lE_loginPwd", ""]]
        self.gridLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.gridLayoutWidget, 'G', 30, 40, 220, 60, self.itmDef_arr)
        self.itmDef_arr[1][3].setEchoMode(QLineEdit.Password)           # 비밀번호 입력시 마스킹 처리

        self.buttonBox = QDialogButtonBox(self)
        glb_funcs.final_decision_button_box(self, self.buttonBox,30, 120, 240, 30, "확인", "취소", self.accept, self.reject)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate

    def add_ID(self):
        glb_vars.loginID_modify_opt = ''
        win = Ui_Member()
        win.exec_()

    def accept(self):
        if glb_vars.loginID_modify_opt == 'Y':             # member ID 수정
            if glb_vars.loginID != self.itmDef_arr[0][3].text():  # 현재 로그인 ID 와 입력 로그인 ID 비교
                glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "현재 로그인 ID와 다른 로그인 정보를 수정할 수 없습니다", "확인")
                return

        df_mbr_list = glb_funcs.get_from_srcTable(self, 'xls', glb_vars.strgPostion, 'member_master.xlsx')
        if df_mbr_list == []:
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "먼저 admin ID를 생성해 시스템 환경 설정을 완료하시오", "확인")
            return

        password = self.itmDef_arr[1][3].text()
        password = password.encode('utf-8')        ## password를 bytes string으로 변환 필요

        access_ok = 'N'
        glb_vars.df_mbr_arr = []
        for i in range(len(df_mbr_list)):
            if df_mbr_list[i][0] == self.itmDef_arr[0][3].text() and \
                    bcrypt.checkpw(password, df_mbr_list[i][1].encode('utf-8')):         # 이미 DB상에 암호화된 비밀번호와 입력된 비밀번호를 비교
                if glb_vars.loginID_modify_opt == 'Y':       # member ID 수정
                    glb_vars.df_mbr_arr.append(df_mbr_list[i])
                    win = Ui_Member()
                    win.exec_()
                    if glb_vars.data_changed_signal == '':  # 다음화면에서 어떤 변경도 발생하지 않았다면
                        self.close()
                    ## 다음화면(Ui_Member())에서 어떤 변경이 발생하였다면 아래 Else 구문이하의 변경을 그 화면에서 해
                else:
                    glb_vars.loginID_name = df_mbr_list[i][2]
                    glb_vars.loginID_info = str(glb_vars.loginID_name) + ' ' + str(df_mbr_list[i][8]) + ' //' + str(df_mbr_list[i][7])  # 이름 직책 // 부서
                    glb_vars.generalUsr = df_mbr_list[i][9]
                    glb_vars.hlpDskUsr = df_mbr_list[i][10]
                    glb_vars.hlpDskFixer = df_mbr_list[i][11]
                access_ok = 'Y'
                break

        if access_ok == 'Y':
            ID_list = [[self.itmDef_arr[0][3].text(), glb_vars.loginID_info, glb_vars.generalUsr, glb_vars.hlpDskUsr,
                        glb_vars.hlpDskFixer, datetime.today().strftime('%Y-%m-%d %H:%M:%S')]]

            glb_funcs.save_to_trgtTable(self, 'txt', ID_list, glb_vars.login_hdr_title, '', 'tempID.txt')

            if glb_vars.loginID_modify_opt != 'Y':    # member ID 수정 아님
                glb_funcs.message_box_1(self, QMessageBox.Information, "성공", "Log In 되었습니다", "확인")
                glb_vars.data_changed_signal = 'Y'
            self.close()
        else:
            glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "ID/Password 오류", "확인")
            return


#### PC 파일 처리 방법
    # os.path.isdir(path)                       # 경로 존재 여부 체크
    # os.path.exists(directory명_name:          # Directory 존재 여부 체크
    # os.makedirs(path)                         # 신규 Directory 생성
    # os.chdir(path)                             # 작업경로 바꾸기
    # os.path.isfile(file_name):              # file 존재여부 체크
    # os.rename(old_path_name, new_path_name)    # 경로이름 바꾸기
    # os.getcwd()                                # 현재 작업경로 확인
    # os.listdir(path)                           # 작업중인 파일리스트 확인
    # os.path.join(base_dir, 'os')               # 기존경로와 새로운 폴더를 합쳐서 하위 경로 생성


