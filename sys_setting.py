from import_list import *
from mainwindow import  *
import glb_funcs
import glb_vars

class Ui_sysConfigSetting(QDialog):
    def __init__(self):
        super().__init__()
        self.getInitData()
        self.setupUi()

    def getInitData(self):
        global g_doc_readOly
        g_doc_readOly = ''
        
        if glb_vars.sysSetting_info_arr[1] != '':
            g_doc_readOly = 'R'

        glb_vars.DB_activIdx = glb_vars.sysSetting_info_arr[0]

    def setupUi(self):
        glb_funcs.winFlame_setting(self, 'R', 500, 450, '', 'C', '', "환경설정", '', 'N', 'N', 'N')

        global g_sys_itmDef_arr
        strgTp_arr = ['PC (Excel file)', 'PC (Text file)', 'DB Server']
        g_sys_itmDef_arr = [["lb", "데이타 저장방식", "cB", "self.cB_DB_StrgTp", strgTp_arr], ["lb", "시작문서번호", "lE", "self.lE_docNo", g_doc_readOly],
                            ["lb", "문서접두코드", "lE", "self.lE_docCrtr", "R"]]
        self.gLytWidget_1 = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.gLytWidget_1, 'G', 30, 30, 440, 130, g_sys_itmDef_arr)
        g_sys_itmDef_arr[0][3].setCurrentIndex(glb_vars.DB_activIdx)

        if g_doc_readOly == 'R':
            g_sys_itmDef_arr[0][3].setEnabled(False)
        g_sys_itmDef_arr[0][3].currentIndexChanged[int].connect(self.chgScrLyt)

        g_sys_itmDef_arr[1][3].setText(str(glb_vars.sysSetting_info_arr[1]))
        g_sys_itmDef_arr[2][3].setText(glb_vars.sysSetting_info_arr[2])

        global g_sys_itmDef_1_arr
        g_sys_itmDef_1_arr = [["lb", "", "pB", "self.pB_strgPstn", "저장 위치 >> ", self.pB_control1]]
        sys_itmDef_2_arr = [["lb", "", "pB", "self.pB_user", "사용자 ID >> ", self.pB_control2], ["lb", "", "pB", "self.pB_passWrd", "비밀 번호 >> ", self.pB_control3],
                            ["lb", "", "pB", "self.pB_strgPstn", "DB 명 >> ", self.pB_control4], ["lb", "", "pB", "self.pB_strgPstn", "Char Set >> ", self.pB_control5]]

        if glb_vars.DB_activIdx == 2:
            for i in range(len(sys_itmDef_2_arr)):
                g_sys_itmDef_1_arr.append(sys_itmDef_2_arr[i])

        self.vLytWidget  = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.vLytWidget, 'V', 30, 200, 440, 130, g_sys_itmDef_1_arr)

        if glb_vars.sysSetting_info_arr[3] != '':
            g_sys_itmDef_1_arr[0][3].setText(glb_vars.sysSetting_info_arr[3])
        if glb_vars.sysSetting_info_arr[4] != '':
            g_sys_itmDef_1_arr[1][3].setText(glb_vars.sysSetting_info_arr[4])
        if glb_vars.sysSetting_info_arr[5] != '':
            g_sys_itmDef_1_arr[2][3].setText(glb_vars.sysSetting_info_arr[5])
        if glb_vars.sysSetting_info_arr[6] != '':
            g_sys_itmDef_1_arr[3][3].setText(glb_vars.sysSetting_info_arr[6])
        if glb_vars.sysSetting_info_arr[7] != '':
            g_sys_itmDef_1_arr[4][3].setText(glb_vars.sysSetting_info_arr[7])

        self.buttonBox = QDialogButtonBox(self)
        glb_funcs.final_decision_button_box(self, self.buttonBox,30, 400, 400, 30, "저장", "취소", self.accept, self.reject)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def chgScrLyt(self, i):
        glb_vars.DB_activIdx = i
        self.close()
        self.__init__()
        self.show()
        
    def pB_control1(self):
        if glb_vars.DB_activIdx == 0:
            # FileOpen = QFileDialog.getOpenFileName(self, 'Open file', './')
            directoryNm = QFileDialog.getExistingDirectory()
            if directoryNm != '':
               g_sys_itmDef_1_arr[0][3].setText('저장위치>> ' + directoryNm)
        else:
            self.pB_control_return(g_sys_itmDef_1_arr[0][3], 'DB Sever IP 주소 >> ')

    def pB_control2(self):
        self.pB_control_return(g_sys_itmDef_1_arr[1][3], '사용자 ID >> ')

    def pB_control3(self):
        self.pB_control_return(g_sys_itmDef_1_arr[2][3], '비밀 번호 >> ')

    def pB_control4(self):
        self.pB_control_return(g_sys_itmDef_1_arr[3][3], 'DB 명 >> ')

    def pB_control5(self):
        self.pB_control_return(g_sys_itmDef_1_arr[4][3], 'CharSet >> ')

    def pB_control_return(self, Qobject, input_title):
        text, ok = QInputDialog.getText(self, 'Input Dialog', input_title)
        if ok:
            Qobject.setText(input_title + str(text))
        else:
            return


    def retranslateUi(self):
        _translate = QCoreApplication.translate

    def accept(self):
        glb_funcs.message_box_2(self, QMessageBox.Question, "확인", "입력 값을 저장하시겠습니까?", "예", "아니오")
        if glb_funcs.MsgBoxRtnSignal != 'Y':
            return
        final_docNo = g_sys_itmDef_arr[1][3].text().replace(" ", "")
        if final_docNo == "" and final_docNo == 0:
            glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "최종 문서번호에 시작문서 번호를 입력하시오", "확인")
            return

        try:
            int(g_sys_itmDef_arr[1][3].text())
        except ValueError:
            glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "최종 문서번호에 숫자를 입력하시오", "확인")
            return
        if glb_vars.DB_activIdx == 0 or glb_vars.DB_activIdx == 1:
            if g_sys_itmDef_1_arr[0][3].text().split(">> ")[1] == "":
                glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "저장위치를 등록하시오", "확인")
                return
        else:
            if g_sys_itmDef_1_arr[1][3].text().split(">> ")[1] == "":
                glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "서버의 사용자 ID를 등록하시오", "확인")
                return
            if g_sys_itmDef_1_arr[2][3].text().split(">> ")[1] == "":
                glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "서버의 비밀번호", "확인")
                return
            if g_sys_itmDef_1_arr[3][3].text().split(">> ")[1] == "":
                glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "서버의 DB명을 등록하시오", "확인")
                return
            if g_sys_itmDef_1_arr[4][3].text().split(">> ")[1] == "":
                glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "서버의 Char Set code을  등록하시오", "확인")
                return

        finalClns_list = []
        sysSet_itm_info = [glb_vars.DB_activIdx, final_docNo, g_sys_itmDef_arr[2][3].text(), g_sys_itmDef_1_arr[0][3].text()]
        if glb_vars.DB_activIdx == 2:
            sysSet_itm_info.append(g_sys_itmDef_1_arr[1][2].text())  # 사용자 ID
            sysSet_itm_info.append(g_sys_itmDef_1_arr[2][2].text())  # 비밀번호
            sysSet_itm_info.append(g_sys_itmDef_1_arr[3][2].text())  # DB 명
            sysSet_itm_info.append(g_sys_itmDef_1_arr[4][2].text())  # Char Set
        else:
            sysSet_itm_info.append("")
            sysSet_itm_info.append("")
            sysSet_itm_info.append("")
            sysSet_itm_info.append("")

        sysSet_itm_info.append(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))  # 생성일

        finalClns_list.append(sysSet_itm_info)
        glb_funcs.save_to_trgtTable(self, 'txt', finalClns_list, glb_vars.sysSet_hdr_title, '', 'sys_setting.txt')
        glb_funcs.message_box_1(self, QMessageBox.Information, "성공", "저장되었습니다", "확인")
        glb_vars.data_changed_signal = 'Y'

        if glb_vars.strgPostion == '' and os.path.isfile('member_master.xlsx'):
            target = g_sys_itmDef_1_arr[0][3].text().split(">> ")[1] + '/' + 'member_master.xlsx'
            shutil.move('member_master.xlsx', target)
        self.close()


    # os.path.isdir(path)                       # 경로 존재 여부 체크
    # os.path.exists(directory명_name:          # Directory 존재 여부 체크
    # os.makedirs(path)                         # 신규 Directory 생성
    # os.chdir(path)                             # 작업경로 바꾸기
    # os.path.isfile(file_name):              # file 존재여부 체크
    # os.rename(old_path_name, new_path_name)    # 경로이름 바꾸기
    # os.getcwd()                                # 현재 작업경로 확인
    # os.listdir(path)                           # 작업중인 파일리스트 확인
    # os.path.join(base_dir, 'os')               # 기존경로와 새로운 폴더를 합쳐서 하위 경로 생성


