import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt ,QCoreApplication
import numpy as np
from time import sleep
import requests
import json
import pandas as pd
from datetime import datetime, timedelta

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def maple_API(key):
    # url, API key 입력
    url = 'https://public.api.nexon.com/openapi/maplestory/v1/cube-use-results'

    # 시작일,종료일 설정
    start = "2022-11-25" # 최초 데이터 시작일
    last = (datetime.today() - timedelta(days=1)).strftime(format="%Y-%m-%d")

    start_date = datetime.strptime(start, "%Y-%m-%d")
    last_date = datetime.strptime(last, "%Y-%m-%d")

    # 종료일 까지 반복
    total_cnt = 0
    total_history = []
    while start_date <= last_date:
        dates = start_date.strftime("%Y-%m-%d")
        headers = {
            'authorization' : key
        }
        params = {
            'count' : 1000,
            'date' : dates,
            'cursor' : ''
        }
        res = requests.get(url,headers=headers, params=params)
        data = res.json()
        if "count" in data:
            total_cnt += data['count']

        if len(data['cube_histories']) > 0:
            total_history.append(data['cube_histories'])

        start_date += timedelta(days=1)

    final_output = []
    for history in total_history:
        character_name = []
        create_date = []
        cube_type = []
        miracle_time_flag = []
        item_equip_part = []
        item_level = []
        target_item = []
        potential_option_grade = []
        additional_potential_option_grade = []
        before_potential_options = []
        before_additional_potential_options = []
        after_potential_options = []
        after_additional_potential_options = []
        for i in history:
            character_name.append(i['character_name'])
            create_date.append(i['create_date'])
            cube_type.append(i['cube_type'])
            miracle_time_flag.append(i['miracle_time_flag'])
            item_equip_part.append(i['item_equip_part'])
            item_level.append(i['item_level'])
            target_item.append(i['target_item'])
            potential_option_grade.append(i['potential_option_grade'])
            additional_potential_option_grade.append(i['additional_potential_option_grade'])
            before_potential_options.append(i['before_potential_options'])
            before_additional_potential_options.append(i['before_additional_potential_options'])
            after_potential_options.append(i['after_potential_options'])
            after_additional_potential_options.append(i['after_additional_potential_options'])

        output = pd.DataFrame({
            'character_name'  : character_name,
            'create_date' : create_date,
            'cube_type' : cube_type,
            'miracle_time_flag' : miracle_time_flag,
            'item_equip_part' : item_equip_part,
            'item_level' : item_level,
            'target_item' : target_item,
            'potential_option_grade' : potential_option_grade,
            'additional_potential_option_grade' : additional_potential_option_grade,
            'before_potential_options' : before_potential_options,
            'before_additional_potential_options' : before_additional_potential_options,
            'after_potential_options' : after_potential_options,
            'after_additional_potential_options' : after_additional_potential_options
        })
        final_output.append(output)
    final_output = pd.concat(final_output)
    
    s_cu = (final_output['cube_type']=='수상한 큐브').sum()
    j_cu = (final_output['cube_type']=='장인의 큐브').sum()
    m_cu = (final_output['cube_type']=='명장의 큐브').sum()
    r_cu = (final_output['cube_type']=='레드 큐브').sum()
    b_cu = (final_output['cube_type']=='블랙 큐브').sum()
    se_cu = (final_output['cube_type']=='수상한 에디셔널 큐브').sum()
    e_cu = (final_output['cube_type']=='에디셔널 큐브').sum()
    cube_info = [s_cu,j_cu,m_cu,r_cu,b_cu,se_cu,e_cu]
    final_output.to_csv('Maple_API_Cube_utf-8.csv', index=False)
    final_output.to_csv('Maple_API_Cube_euc-kr.csv', index=False,encoding='euc-kr')
    return total_cnt, cube_info

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        title = QLabel('큐브결과생성기',self)
        font = title.font()
        font.setPointSize(50)
        font.setFamily('Times New Roman')
        font.setBold(True)
        
        title.move(210, 25)

#         lbl_img = QLabel(self)
#         new_source = resource_path("sample_img.png")
#         pixmap = QPixmap(new_source)
#         lbl_img.setPixmap(QPixmap(pixmap))
#         lbl_img.move(60, 290)

        self.le = QLabel('',self)
        self.le.move(130, 55)
        self.le.resize(300,30)
        
        self.le2 = QLabel('',self)
        self.le2.move(130, 70)
        self.le2.resize(300,30)
        
        self.le3= QLabel('',self)
        self.le3.move(130, 85)
        self.le3.resize(300,30)
                
        self.le4 = QLabel('',self)
        self.le4.move(130, 100)
        self.le4.resize(300,30)

        self.le5 = QLabel('',self)
        self.le5.move(130, 115)
        self.le5.resize(300,30)
        
        self.le6 = QLabel('',self)
        self.le6.move(130, 130)
        self.le6.resize(300,30)
        
        self.le7 = QLabel('',self)
        self.le7.move(130, 145)
        self.le7.resize(300,30)
        
        self.le8 = QLabel('',self)
        self.le8.move(130, 160)
        self.le8.resize(300,30)
        
        self.le9 = QLabel('',self)
        self.le9.move(130, 180)
        self.le9.resize(300,30)
        
        self.btn = QPushButton('추출', self)
        self.btn.move(210, 230)
        self.btn.clicked.connect(self.showDialog)
        
        self.btn = QPushButton('Quit', self)
        self.btn.move(370, 350)
        self.btn.clicked.connect(QCoreApplication.instance().quit)

        self.setWindowTitle('큐브결과생성기')
        self.setGeometry(300, 300, 500, 400)
        self.show()
        


    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'API Key를 입력해주세요')

        if ok:
            try:
                total_cnt, cube_info = maple_API(text)
            except:
                total_cnt = 0
                cube_info =[0,0,0,0,0,0,0]
                self.le9.setText(f'올바른 API Key를 입력해주세요')
                
            self.le.setText(f'지금까지 사용한 총 큐브 개수 : {total_cnt}')
            
            self.le2.setText(f'지금까지 사용한 수상한 큐브 개수 : {cube_info[0]}')
            self.le3.setText(f'지금까지 사용한 장인의 큐브 개수 : {cube_info[1]}')
            self.le4.setText(f'지금까지 사용한 명장의 큐브 개수 : {cube_info[2]}')
            self.le5.setText(f'지금까지 사용한 레드 큐브 개수 : {cube_info[3]}')
            self.le6.setText(f'지금까지 사용한 블랙 큐브 개수 : {cube_info[4]}')
            self.le7.setText(f'지금까지 사용한 수에큐 개수 : {cube_info[5]}')
            self.le8.setText(f'지금까지 사용한 에디셔널 큐브 개수 : {cube_info[6]}')
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())