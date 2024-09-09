from import_list import *
from helpdesk import *

import glb_funcs
import glb_vars

class Ui_Srch_N_Get_Cd_Nm(QDialog):
    def __init__(self):
        super().__init__()
        self.getInitData()
        self.setupUi()

    def getInitData(self):
        self.TW_info_list = []
        self.grpCd = self.grpCdNm = ''

    def setupUi(self):
        glb_funcs.winFlame_setting(self, 'R', 500, 450, '', 'C', '', glb_vars.search_winTitle, '', 'N', 'N', 'N')

        self.itmDef_1_arr = [["lb", "검색 코드", "lE", "self.lE_grpCd", ""]]
        self.gridLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.gridLayoutWidget, 'H', 40, 30, 130, 30, self.itmDef_1_arr)

        self.itmDef_2_arr = [["lb", "검색 Text", "lE", "self.lE_grpCdNm", ""]]
        self.gridLayoutWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.gridLayoutWidget, 'H', 190, 30, 220, 30, self.itmDef_2_arr)

        tool_button_arr = ["검색 실행", 420, 30, 30, 30, "img/preview.png", 30, 30, self.search]
        self.toolButton = QToolButton(self)
        glb_funcs.tool_button_setting(self, self.toolButton, tool_button_arr)

        self.itmDef_3_arr = [["CB", "전체 List 출력방지", "CB", "self.CB_dspOpt", ""]]
        self.horzLytWidget = QWidget(self)
        glb_funcs.tpOfLayout_setting(self, self.horzLytWidget, 'H', 330, 70, 150, 15, self.itmDef_3_arr)

        tW_grpCd_arr = ["코드", "코드 Text"]
        self.tableWidget = QTableWidget(self)
        glb_funcs.TableWidget_setting(self, self.tableWidget, 40, 90, 420, 300, len(tW_grpCd_arr), 0, 'N', 'N', 'N', 'Y')
        glb_funcs.TableWidget_hdr_setting(self, self.tableWidget, 'H', 'R', 'lightblue', tW_grpCd_arr, '')

        self.setup_tW_info()

        self.buttonBox = QDialogButtonBox(self)
        glb_funcs.final_decision_button_box(self, self.buttonBox, 220, 400, 240, 30, "", "취소", "", self.close_scr)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        # self.winTitle  = Ui_HelpDesk().winTitle

    def setup_tW_info(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        for i in range(len(self.TW_info_list)):
            # self.tableWidget.removeRow(i)              # 위 self.tableWidget.setRowCount(0)로 인해 의미없어짐
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            for j in range(len(self.TW_info_list[i])):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)         # 각 Cell의 위치 지정
                item.setText(str(self.TW_info_list[i][j]))
                item.setTextAlignment(Qt.AlignLeft)

    def tableWidget_doubleClicked(self):
        row = self.tableWidget.currentIndex().row()
        col = self.tableWidget.currentIndex().column()

        self.grpCd   = str(self.TW_info_list[row][0])
        self.grpCdNm = str(self.TW_info_list[row][1])

        self.close()

    def search(self):
        self.grpCd_input   = self.itmDef_1_arr[0][3].text().strip()
        self.grpCdNm_input = self.itmDef_2_arr[0][3].text().strip()

        self.TW_info_list = []
        if self.grpCd_input == '':
            if self.grpCdNm_input == '':
                if self.itmDef_3_arr[0][3].checkState() != 0:
                    glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "검색값을 입력하시오", "확인")
                    return
                else:
                    self.TW_info_list = self.code_grp_list
            else:
                for i in range(len(self.code_grp_list)):
                  if self.code_grp_list[i][1].find(self.grpCdNm_input) != -1:
                      self.TW_info_list.append(self.code_grp_list[i])
        else:
            if self.grpCdNm_input == '':
                for i in range(len(self.code_grp_list)):
                    if self.code_grp_list[i][0].find(self.grpCd_input) != -1:
                        self.TW_info_list.append(self.code_grp_list[i])
            else:
                for i in range(len(self.code_grp_list)):
                  if self.code_grp_list[i][0].find(self.grpCd_input) != -1 and self.code_grp_list[i][1].find(self.grpCdNm_input) != -1:
                      self.TW_info_list.append(self.code_grp_list[i])

        if self.TW_info_list == []:
            glb_funcs.message_box_1(self, QMessageBox.Warning, "경고", "검색대상이 선택되지 않았습니다", "확인")
            return

        self.setup_tW_info()

    def close_scr(self):
        glb_funcs.message_box_2(self, QMessageBox.Question, "작업중지", "작업을 중지하시겠습니까?", "예", "아니오")
        if glb_funcs.MsgBoxRtnSignal == 'Y':
           self.close()
        else: pass

