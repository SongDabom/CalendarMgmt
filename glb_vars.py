# from import_list import *

# def init():
    # global infoTrsf_arr, fixer_list, k0010_list,  k0020_list #hlpDsk_list, sel_hlpDsk_list,
    # global loginID, loginID_name, loginID_info, generalUsr, hlpDskUsr, hlpDskFixer, frst_login_time, activYear, activMon, activDay, DB_activIdx
    # global strgPostion, helpDeskEdtSts, sel_docNo, sel_docNo_wrt_info
    # global data_changed_signal, search_winTitle
    #
    # infoTrsf_arr = []
    # # hlpDsk_list = []
    # # sel_hlpDsk_list = []
    #
    # loginID = loginID_name = loginID_info = generalUsr = hlpDskUsr = hlpDskFixer = strgPostion = data_changed_signal = search_winTitle = ""
    # helpDeskEdtSts = ""
    # frst_login_time = ""
    # sel_docNo_wrt_info = ""
    #
    # activYear = activMon = activDay = 0
    # DB_activIdx = 0
    # sel_docNo = 0

    ## Header Title
     # global login_hdr_title, sysSet_hdr_title, mbr_master_hdr_title
login_hdr_title = ["ID", "ID 정보", '일반사용', 'HelpDesk등록', 'HelpDesk조치', "생성일자"]
sysSet_hdr_title = ['저장유형', '최종문서번호', '최종문서생성인', '저장위치', '사용자ID', '비밀번호', 'DB ID', 'Char Set', '생성일자']
mbr_master_hdr_title = ['ID', '비밀번호', '이름', '개인연락처', '업무연락처', '주소', '회사명', '부서명', '직책', '일반사용', 'HelpDesk등록', 'HelpDesk조치', '생성인', '생성일', '변경인', '변경일']
hlpDsk_hdr_title = ['문서번호', '발생일', '조치일', '조치책임자', '단지코드', '고객명', '연락처', '문의유형', '중요도', '처리상태', '제목', '문의내용', '조치내용', '비고', '생성인', '생성일', '변경인', '변경일']
codeSet_hdr_title = ["대표코드", "코드", "내용"]

# cB_priort_arr = ["상", "중", "하"]  # 중요도
# cB_prcsSts_arr = ["접수", "대기", "처리중", "처리완료"]  # 처리상태
