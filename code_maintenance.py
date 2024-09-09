from import_list import *
from mainwindow import  *
from member_mgmt import *

import glb_funcs
import glb_vars

class Ui_CodeMaintenance(QDialog):
    def __init__(self):
        super().__init__()
        self.getInitData()
        self.setupUi()

    def getInitData(self):
        self.TW_info_list = []
        self.sel_row = -1
        self.sel_code = ''
        self.sel_codeTxt = ''

        self.scr_parentCd_opt = self.scr_childCd_opt = self.scr_parentCdTxt_opt = self.scr_childCdTxt_opt =0

        if glb_vars.highest_parent_code == '':          # 최상위 코드 등록시(최상위 코드가 존재할지 않을 때)
            self.scr_parentCd_opt = self.scr_parentCdTxt_opt = 1     # 대표코드를 입력할 수 있도록 ReadOnly option 해제
        else:                                           # 일반코드 등록시 혹은 최상위코드에 대한 대표코드 등록시
            self.sel_code = glb_vars.clkd_code
            self.sel_codeTxt = glb_vars.clkd_codeTxt
            self.scr_childCd_opt = self.scr_childCdTxt_opt = 1       # 일반코드 혹은 최상위코드에 대한 대표코드를 입력할 수 있도록 ReadOnly Option 해제

    def setupUi(self):
        glb_funcs.winFlame_setting(self, 'R', 500, 400, '', 'C', '', "코드관리", '', 'N', 'N', 'N')

        self.itmDef_1_arr = [["lb", "대표코드", "lE", "self.lE_parentCd", ""], ["lb", "코드", "lE", "self.lE_childCd", ""]]
        self.gridLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.gridLayoutWidget, 'G', 30, 25, 110, 60, self.itmDef_1_arr)
        self.itmDef_1_arr[0][3].setText(self.sel_code)

        glb_funcs.readOnly_setting(self, 'lE', self.itmDef_1_arr[0][3], self.scr_parentCd_opt)
        glb_funcs.readOnly_setting(self, 'lE', self.itmDef_1_arr[1][3], self.scr_childCd_opt)

        self.itmDef_2_arr = [["", "", "lE", "self.lE_parentCdTxt", ""], ["", "", "lE", "self.lE_childCdTxt", ""]]
        self.gridLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.gridLayoutWidget, 'G', 145, 25, 280, 60, self.itmDef_2_arr)
        self.itmDef_2_arr[0][3].setText(self.sel_codeTxt)
        glb_funcs.readOnly_setting(self, 'lE', self.itmDef_2_arr[0][3], self.scr_parentCdTxt_opt)
        glb_funcs.readOnly_setting(self, 'lE', self.itmDef_2_arr[1][3], self.scr_childCdTxt_opt)

        tool_button_arr = [["추가", 430, 55, 30, 30, "img/add-file.png", 30, 30, self.addInfo],
                           ["삭제", 35, 340, 30, 30, "img/delete.png", 30, 30, self.delInfo]]
        for i in range(len(tool_button_arr)):
            self.toolButton = QToolButton(self)
            glb_funcs.tool_button_setting(self, self.toolButton, tool_button_arr[i])

        self.lb_Title = QLabel(self)
        glb_funcs.label_setting(self, self.lb_Title, 30, 100, 200, 20, 'L', '<작업대상 리스트>')

        tW_grpCd_arr = ["코드", "코드 Text"]
        self.tableWidget = QTableWidget(self)
        glb_funcs.TableWidget_setting(self, self.tableWidget, 30, 120, 440, 210, len(tW_grpCd_arr), 0, 'N', 'N', 'N', 'N')
        glb_funcs.TableWidget_hdr_setting(self, self.tableWidget, 'H', 'R', 'lightblue', tW_grpCd_arr, '')

        self.setup_tW_info()

        self.buttonBox = QDialogButtonBox(self)
        glb_funcs.final_decision_button_box(self, self.buttonBox,200, 350, 240, 30, "저장", "나가기", self.accept, self.reject)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate

    def setup_tW_info(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)                     # table Widget를 재 수행할 때 row grid line이 삭제되지 않고 남아있는 것을 방지함 
        for i in range(len(self.TW_info_list)):
            # self.tableWidget.removeRow(i)                   # 위 self.tableWidget.setRowCount(0)로 인해 의미없어짐
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            for j in range(len(self.TW_info_list[i])):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)         # 각 Cell의 위치 지정
                item.setText(str(self.TW_info_list[i][j]))
                item.setTextAlignment(Qt.AlignLeft)

    def addInfo(self):
        self.sel_row = -1                           # 기존에 Table Widget 내에 선택되어 있을 지도 모를 항목의 Row Index를 초기화 시킴
        temp_TW_info_arr = []
        if glb_vars.highest_parent_code == '':              # 최상위 코드가 존재하지 않음, 최상위코드를 등록함
            print(self.TW_info_list, len(self.TW_info_list))
            if len(self.TW_info_list) > 0:
                glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "최상위 코드는 2개 이상 등록 불가합니다.", "확인")
                self.itmDef_1_arr[0][3].setText(self.TW_info_list[0][0])        # 대표코드 이전으로 원복
                self.itmDef_2_arr[0][3].setText(self.TW_info_list[0][1])        # 대표코드 내용 이전으로 원복
                return
            self.itmDef_1_arr[0][3].setText(self.itmDef_1_arr[0][3].text().replace(' ', ''))  # 문자열에서 공백을 모두 제거함
            self.itmDef_2_arr[0][3].setText(self.itmDef_2_arr[0][3].text().strip())  # 문자열에서 좌우 공백을 제거함
            if self.itmDef_1_arr[0][3].text() == '' or self.itmDef_2_arr[0][3].text() == '':
                glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "코드 혹은 코드내용을 모두 입력하시오.", "확인")
                return
            if not self.itmDef_1_arr[0][3].text()[0].encode().isalpha():
                glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "코드의 첫 문자는 알파벳 대문자로 시작하시오.", "확인")
                return
            if not self.itmDef_1_arr[0][3].text()[0].isupper():
                glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "코드의 첫 문자가 알파벳 대문자가 아닙니다.", "확인")
                return
            temp_TW_info_arr.append(self.itmDef_1_arr[0][3].text())
            temp_TW_info_arr.append(self.itmDef_2_arr[0][3].text())
        else:                                                # 최상위 코드가 존재함으로 대표코드나 일반코드를 등록함
            self.itmDef_1_arr[1][3].setText(self.itmDef_1_arr[1][3].text().replace(' ', ''))  # 문자열에서 공백을 모두 제거함
            self.itmDef_2_arr[1][3].setText(self.itmDef_2_arr[1][3].text().strip())  # 문자열에서 좌우 공백을 제거함

            if self.itmDef_1_arr[1][3].text() == '' or self.itmDef_2_arr[1][3].text() == '':
                glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "코드 혹은 코드내용을 모두 입력하시오", "확인")
                return
            if self.itmDef_1_arr[0][3].text() == glb_vars.highest_parent_code:  # 화면의 대포코드가 최상위 대표코드일때
                if not self.itmDef_1_arr[1][3].text()[0].encode().isalpha():
                   glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "대표코드의 첫 문자는 알파벳으로 시작하시오", "확인")
                   return
                if self.itmDef_1_arr[1][3].text() < self.itmDef_1_arr[0][3].text():
                   glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "대표코드는 최상위 대표코드의 문자열 순서보다 앞에 올 수 없습니다", "확인")
                   return
                if not self.itmDef_1_arr[1][3].text()[0].isupper():
                    glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "대표코드의 첫 문자는 알파벳 대문자입니다.", "확인")
                    return

            temp_TW_info_arr.append(self.itmDef_1_arr[1][3].text())
            temp_TW_info_arr.append(self.itmDef_2_arr[1][3].text())

        if self.itmDef_1_arr[0][3].text() == self.itmDef_1_arr[1][3].text():
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "대표코드와 동일한 코드는 등록할 수 없습니다", "확인")
            return

        ## 코드 중복 점검
        upd_OK = 'Y'
        for i in range(len(self.TW_info_list)):
            if self.TW_info_list[i][0] == temp_TW_info_arr[0]:
                upd_OK = 'N'
                break
        if upd_OK == 'N':
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "이미 동일한 코드가 등록되어 있습니다", "확인")
            return
        self.TW_info_list.append(temp_TW_info_arr)
        list.sort(self.TW_info_list, key=lambda k: k[0])

        self.itmDef_1_arr[1][3].setText('')   # Table Widget에 Update 후 필드 초기화
        self.itmDef_2_arr[1][3].setText('')   # Table Widget에 Update 후  필드 초기화

        self.setup_tW_info()

    def delInfo(self):
        self.sel_row = self.tableWidget.currentIndex().row()
        # self.sel_col = self.tableWidget.currentIndex().column()
        if self.sel_row == -1:
            glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "삭제할 대상을 정확히 지정하시오.", "확인")
            return
        self.TW_info_list.__delitem__(self.sel_row)
        self.setup_tW_info()

    def accept(self):
        if self.TW_info_list == []:
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "먼저 작업대상 리스트에 코드를 추가하시오.", "확인")
            return

        glb_funcs.message_box_2(self, QMessageBox.Question, "작업내용 저장", "작업 내용을 저장하시겠습니까?", "예", "아니오")
        if glb_funcs.MsgBoxRtnSignal != 'Y':
            return

        self.df_codeSet_list = glb_funcs.get_from_srcTable(self, 'xls', glb_vars.strgPostion,'masterCode_set.xlsx')  # 코드집
        if glb_vars.highest_parent_code == '':              # 최상위 대표코드가 등록되지 않는 경우 대표코드를 코드와 동일하게 둠
            self.df_codeSet_list.append([self.itmDef_1_arr[0][3].text(), self.TW_info_list[0][0], self.TW_info_list[0][1]])
        else:
           for i in range(len(self.TW_info_list)):
               for j in range(len(self.df_codeSet_list)):
                   if self.df_codeSet_list[j][0] == self.itmDef_1_arr[0][3].text() and self.df_codeSet_list[j][1] == self.TW_info_list[i][0]:
                       glb_funcs.message_box_1(self, QMessageBox.Critical, "오류", "작업대상 리스트 중 코드(" +  self.TW_info_list[i][0] + ")가 이미 존재합니다.", "확인")
                       return
               self.df_codeSet_list.append([self.itmDef_1_arr[0][3].text(), self.TW_info_list[i][0], self.TW_info_list[i][1]])

        list.sort(self.df_codeSet_list, key=lambda k: (k[0], k[1]))
        # codeSet_hdr_title = ["대표코드", "코드", "내용"]
        glb_funcs.save_to_trgtTable(self, 'xls', self.df_codeSet_list, glb_vars.codeSet_hdr_title, glb_vars.strgPostion, 'masterCode_set.xlsx')
        glb_funcs.message_box_1(self, QMessageBox.Information, "저장완료", "작업대상 리스트의 코드(들)를 저장했습니다.", "확인")
        glb_vars.data_changed_signal = 'Y'
        self.close()

#### PC 파일 처리 방법
    # os.path.isdir(path)                        # 경로 존재 여부 체크
    # os.path.exists(directory명_name:           # Directory 존재 여부 체크
    # os.makedirs(path)                          # 신규 Directory 생성
    # os.chdir(path)                             # 작업경로 바꾸기
    # os.path.isfile(file_name):                 # file 존재여부 체크
    # os.rename(old_path_name, new_path_name)    # 경로이름 바꾸기
    # os.getcwd()                                # 현재 작업경로 확인
    # os.listdir(path)                           # 작업중인 파일리스트 확인
    # os.path.join(base_dir, 'os')               # 기존경로와 새로운 폴더를 합쳐서 하위 경로 생성


