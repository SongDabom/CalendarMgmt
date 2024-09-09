from import_list import *

from matplotlib import font_manager, rc

import glb_funcs
import glb_vars

class Ui_Graph(QDialog):
  def __init__(self):
      super().__init__()
      self.setupUi()

  def setupUi(self):
      self.setWindowTitle('처리상태')
      self.setGeometry(300, 100, 600, 400)

      layout = QVBoxLayout()

      ## Font를 아래와 같이 지정하지 않으면 한글출력시 깨짐
      font_path = "Fonts/NGULIM.TTF"
      font = font_manager.FontProperties(fname=font_path).get_name()
      rc('font', family=font)

      self.fig = plt.figure(figsize=[5, 5])          # Pie 그래프의 사이즈
      self.convas = FigureCanvas(self.fig)

      if glb_vars.graph_type == '파이':
          self.draw_pie_graph()
      elif glb_vars.graph_type == '막대':
          self.draw_bar_graph()
      elif glb_vars.graph_type == '꺽은선':
          self.draw_line_graph()
      else: self.close()

      layout.addWidget(self.convas)

      ## 전체 건 수 출력
      self.lb_title = QLabel(self)
      layout.addWidget(self.lb_title)
      glb_funcs.label_setting(self, self.lb_title, 0, 270, 300, 30, 'C', '총 ' + str(glb_vars.arr_sum) + ' 건')

      self.setLayout(layout)
      self.convas.show()

  def draw_pie_graph(self):
      ## Pie 그래프 그리기
      color_group = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'red', 'yellow', 'purple', 'lightgrey', 'lightpink']    # 각 Pie별 나타낼 수 있는 최대 배경 색깔

      colors = []
      labels = []
      ratio = []
      explode = []
      for i in range(len(glb_vars.graph_info_list)): # glb_vars.graph_info_list = [[특정 Pie 조각에 대한 Title, 특정 Pie 조각에 대한 절대깞, 전체 Pie에 대한 비율], ...]
          colors.append(color_group[i])
          labels.append(glb_vars.graph_info_list[i][0] + "(" + str(glb_vars.graph_info_list[i][1]) + " 건)")
          ratio. append(glb_vars.graph_info_list[i][2])
          explode.append(0.1)

      plt.pie(ratio, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)

  def draw_bar_graph(self):
      ax = plt.subplot()

      x_axis = []
      x_axis_title = []
      y_axis = []
      for i in range(len(glb_vars.graph_info_list)):
          x_axis.append(i)
          x_axis_title.append(glb_vars.graph_info_list[i][0])
          y_axis.append(glb_vars.graph_info_list[i][1])

      ax.set_xticks(x_axis)
      ax.set_xticklabels(x_axis_title, rotation=15)

      plt.bar(range(len(x_axis)), y_axis)

  def draw_line_graph(self):
      ax = plt.subplot()

      x_axis = []
      x_axis_title = []
      y_axis = []
      for i in range(len(glb_vars.graph_info_list)):
          x_axis.append(i)
          x_axis_title.append(glb_vars.graph_info_list[i][0])
          y_axis.append(glb_vars.graph_info_list[i][1])

      ax.set_xticks(x_axis)
      ax.set_xticklabels(x_axis_title, rotation=15)

      plt.plot(range(len(x_axis)), y_axis)