import os
import sys
import time
from PyQt5.QtTest import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from SRParse import SRParse
from Timer import Timer

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.addTab(self.processTabUI(), "Parser")
        tabs.addTab(self.tableTabUI(), "Table")

        self.animation_speed_min = 500
        self.animation_speed_max = 3000
        self.animation_speed = int((self.animation_speed_max+self.animation_speed_min)/2)

        # 1 Top Layout
        top_layout = QHBoxLayout()

        # 1.1 Input Layout
        input_layout = QHBoxLayout()
        input_label = QLabel("Input")
        self.input_txt = QLineEdit()

        input_button = QPushButton("Parse")
        input_button.clicked.connect(self.on_click_input)
        step_button = QPushButton("Step")
        step_button.clicked.connect(self.on_click_step)

        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_txt)
        input_layout.addWidget(input_button)
        input_layout.addWidget(step_button)

        # 1.2 Time Layout
        time_layout = QHBoxLayout()
        self.time_txt = QLineEdit("00:00:00")
        self.time_txt.setReadOnly(True)
        self.time_txt.setGeometry(10, 10, 10, 10)


        mySlider = QSlider(Qt.Horizontal, self)
        mySlider.setGeometry(30, 40, 200, 30)
        mySlider.setRange(self.animation_speed_min, self.animation_speed_max)
        mySlider.setValue(self.animation_speed)
        mySlider.valueChanged[int].connect(self.changeSliderValue)

        time_layout.addStretch()
        time_layout.addWidget(QLabel("Speed"))
        time_layout.addWidget(mySlider)
        time_layout.addStretch()
        time_layout.addWidget(QLabel("Time"))
        time_layout.addWidget(self.time_txt)

        top_layout.addLayout(input_layout)
        top_layout.addLayout(time_layout)

        layout.addLayout(top_layout)
        layout.addWidget(tabs)

        self.setLayout(layout)
        self.setGeometry(700, 700, 990, 500)
        self.setWindowTitle('Shift Reduce Parser - Chris Vasquez - v2.0a')
        self.show()


    def tableTabUI(self):

        self.x_axis = {
            'id': 0,
            '+': 1,
            '*': 2,
            '(': 3,
            ')': 4,
            '$': 5,
            'E': 6,
            'T': 7,
            'F': 8
        }

        self.step_counter = 1
        self.rule_counter = 0
        self.coord_counter = 0
        self.previous_input = ""
        self.full_parse_flag = True


        tableTab = QWidget()
        self.table = QTableWidget()
        self.table.setRowCount(12)
        self.table.setColumnCount(9)
        header_font = QFont('Times', 14)
        header_font.setBold(True)

        self.table.setHorizontalHeaderLabels(["id", "+", "*", "(", ")", "$", "E", "T", "F"])
        self.table.setVerticalHeaderLabels(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','10','11'])
        self.table.verticalHeader().setFont(header_font)
        self.table.horizontalHeader().setFont(header_font)


        for i in range(0,12):
            self.table.setRowHeight(i,67)

        self.table.setItem(0,0, QTableWidgetItem("S5"))
        self.table.setItem(0,1, QTableWidgetItem(""))
        self.table.setItem(0,2, QTableWidgetItem(""))
        self.table.setItem(0,3, QTableWidgetItem("S4"))
        self.table.setItem(0,4, QTableWidgetItem(""))
        self.table.setItem(0,5, QTableWidgetItem(""))
        self.table.setItem(0,6, QTableWidgetItem("1"))
        self.table.setItem(0,7, QTableWidgetItem("2"))
        self.table.setItem(0,8, QTableWidgetItem("3"))

        self.table.setItem(1,0, QTableWidgetItem(""))
        self.table.setItem(1,1, QTableWidgetItem("S6"))
        self.table.setItem(1,2, QTableWidgetItem(""))
        self.table.setItem(1,3, QTableWidgetItem(""))
        self.table.setItem(1,4, QTableWidgetItem(""))
        self.table.setItem(1,5, QTableWidgetItem("accept"))
        self.table.setItem(1,6, QTableWidgetItem(""))
        self.table.setItem(1,7, QTableWidgetItem(""))
        self.table.setItem(1,8, QTableWidgetItem(""))

        self.table.setItem(2,0, QTableWidgetItem(""))
        self.table.setItem(2,1, QTableWidgetItem("R2"))
        self.table.setItem(2,2, QTableWidgetItem("S7"))
        self.table.setItem(2,3, QTableWidgetItem(""))
        self.table.setItem(2,4, QTableWidgetItem("R2"))
        self.table.setItem(2,5, QTableWidgetItem("R2"))
        self.table.setItem(2,6, QTableWidgetItem(""))
        self.table.setItem(2,7, QTableWidgetItem(""))
        self.table.setItem(2,8, QTableWidgetItem(""))

        self.table.setItem(3,0, QTableWidgetItem(""))
        self.table.setItem(3,1, QTableWidgetItem("R4"))
        self.table.setItem(3,2, QTableWidgetItem("R4"))
        self.table.setItem(3,3, QTableWidgetItem(""))
        self.table.setItem(3,4, QTableWidgetItem("R4"))
        self.table.setItem(3,5, QTableWidgetItem("R4"))
        self.table.setItem(3,6, QTableWidgetItem(""))
        self.table.setItem(3,7, QTableWidgetItem(""))
        self.table.setItem(3,8, QTableWidgetItem(""))

        self.table.setItem(4,0, QTableWidgetItem("S5"))
        self.table.setItem(4,1, QTableWidgetItem(""))
        self.table.setItem(4,2, QTableWidgetItem(""))
        self.table.setItem(4,3, QTableWidgetItem("S4"))
        self.table.setItem(4,4, QTableWidgetItem(""))
        self.table.setItem(4,5, QTableWidgetItem(""))
        self.table.setItem(4,6, QTableWidgetItem("8"))
        self.table.setItem(4,7, QTableWidgetItem("2"))
        self.table.setItem(4,8, QTableWidgetItem("3"))

        self.table.setItem(5,0, QTableWidgetItem(""))
        self.table.setItem(5,1, QTableWidgetItem("R6"))
        self.table.setItem(5,2, QTableWidgetItem("R6"))
        self.table.setItem(5,3, QTableWidgetItem(""))
        self.table.setItem(5,4, QTableWidgetItem("R6"))
        self.table.setItem(5,5, QTableWidgetItem("R6"))
        self.table.setItem(5,6, QTableWidgetItem(""))
        self.table.setItem(5,7, QTableWidgetItem(""))
        self.table.setItem(5,8, QTableWidgetItem(""))

        self.table.setItem(6,0, QTableWidgetItem("S5"))
        self.table.setItem(6,1, QTableWidgetItem(""))
        self.table.setItem(6,2, QTableWidgetItem(""))
        self.table.setItem(6,3, QTableWidgetItem("S4"))
        self.table.setItem(6,4, QTableWidgetItem(""))
        self.table.setItem(6,5, QTableWidgetItem(""))
        self.table.setItem(6,6, QTableWidgetItem(""))
        self.table.setItem(6,7, QTableWidgetItem("9"))
        self.table.setItem(6,8, QTableWidgetItem("3"))

        self.table.setItem(7,0, QTableWidgetItem("S5"))
        self.table.setItem(7,1, QTableWidgetItem(""))
        self.table.setItem(7,2, QTableWidgetItem(""))
        self.table.setItem(7,3, QTableWidgetItem("S4"))
        self.table.setItem(7,4, QTableWidgetItem(""))
        self.table.setItem(7,5, QTableWidgetItem(""))
        self.table.setItem(7,6, QTableWidgetItem(""))
        self.table.setItem(7,7, QTableWidgetItem(""))
        self.table.setItem(7,8, QTableWidgetItem("10"))

        self.table.setItem(8,0, QTableWidgetItem(""))
        self.table.setItem(8,1, QTableWidgetItem("S6"))
        self.table.setItem(8,2, QTableWidgetItem(""))
        self.table.setItem(8,3, QTableWidgetItem(""))
        self.table.setItem(8,4, QTableWidgetItem("S11"))
        self.table.setItem(8,5, QTableWidgetItem(""))
        self.table.setItem(8,6, QTableWidgetItem(""))
        self.table.setItem(8,7, QTableWidgetItem(""))
        self.table.setItem(8,8, QTableWidgetItem(""))

        self.table.setItem(9,0, QTableWidgetItem(""))
        self.table.setItem(9,1, QTableWidgetItem("R1"))
        self.table.setItem(9,2, QTableWidgetItem("S7"))
        self.table.setItem(9,3, QTableWidgetItem(""))
        self.table.setItem(9,4, QTableWidgetItem("R1"))
        self.table.setItem(9,5, QTableWidgetItem("R1"))
        self.table.setItem(9,6, QTableWidgetItem(""))
        self.table.setItem(9,7, QTableWidgetItem(""))
        self.table.setItem(9,8, QTableWidgetItem(""))

        self.table.setItem(10,0, QTableWidgetItem(""))
        self.table.setItem(10,1, QTableWidgetItem("R3"))
        self.table.setItem(10,2, QTableWidgetItem("R3"))
        self.table.setItem(10,3, QTableWidgetItem(""))
        self.table.setItem(10,4, QTableWidgetItem("R3"))
        self.table.setItem(10,5, QTableWidgetItem("R3"))
        self.table.setItem(10,6, QTableWidgetItem(""))
        self.table.setItem(10,7, QTableWidgetItem(""))
        self.table.setItem(10,8, QTableWidgetItem(""))

        self.table.setItem(11,0, QTableWidgetItem(""))
        self.table.setItem(11,1, QTableWidgetItem("R5"))
        self.table.setItem(11,2, QTableWidgetItem("R5"))
        self.table.setItem(11,3, QTableWidgetItem(""))
        self.table.setItem(11,4, QTableWidgetItem("R5"))
        self.table.setItem(11,5, QTableWidgetItem("R5"))
        self.table.setItem(11,6, QTableWidgetItem(""))
        self.table.setItem(11,7, QTableWidgetItem(""))
        self.table.setItem(11,8, QTableWidgetItem(""))

        for x in range(0, 12):
            for y in range(0,9):
                self.table.item(x,y).setTextAlignment(4|128)
                self.table.item(x,y).setFont(QFont('Times', 14))

        self.table.resizeRowsToContents()

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        tableTab.setLayout(layout)
        layout.setStretch(0, 1)
        return tableTab

    def processTabUI(self):
        processTab = QWidget()

        # Main GUI Layout
        main_layout = QVBoxLayout()


        # 2 Middle Layout
        middle_layout = QVBoxLayout()

        # Frame for Middle Layout
        frame = QGroupBox("Parser Process")
        frame.setLayout(middle_layout)

        # 2.1 Lower Middle Layout
        lower_middle_layout = QHBoxLayout()

        # 2.2.1 Derivation Steps
        derivation_steps_layout = QVBoxLayout()
        derivation_steps_layout.addWidget(QLabel('Derivation Steps'))
        self.derv_txt = QTextEdit("")
        self.derv_txt.setReadOnly(True)
        self.derv_txt.setFont(QFont("Times", 12))
        self.derv_txt.setStyleSheet('background-color: #f1f0ef;')
        derivation_steps_layout.addWidget(self.derv_txt)

        # 2.2.2 Production Rules
        production_rule_layout = QVBoxLayout()
        production_rule_layout.addWidget(QLabel('Production Rules'))
        self.prod_rule_txt = QTextEdit("")
        self.prod_rule_txt.setReadOnly(True)
        self.prod_rule_txt.setFont(QFont("Times", 12))
        self.prod_rule_txt.setStyleSheet('background-color: #f1f0ef;')
        production_rule_layout.addWidget(self.prod_rule_txt)

        # 2.2.3 Action
        action_layout = QVBoxLayout()
        action_layout.addWidget(QLabel('Action'))
        self.action_txt = QTextEdit("")
        self.action_txt.setReadOnly(True)
        self.action_txt.setFont(QFont("Times", 12))
        self.action_txt.setStyleSheet('background-color: #f1f0ef;')
        action_layout.addWidget(self.action_txt)

        # 2.2.4 Stack
        stack_layout = QVBoxLayout()
        stack_layout.addWidget(QLabel('Stack'))
        self.stack_txt = QTextEdit("")
        self.stack_txt.setReadOnly(True)
        self.stack_txt.setFont(QFont("Times", 12))
        self.stack_txt.setStyleSheet('background-color: #f1f0ef;')
        stack_layout.addWidget(self.stack_txt)

        # 3 Bottom Layout
        bottom_layout = QHBoxLayout()

        # 3.1 Production Rules

        PR_layout = QVBoxLayout()
        PR_layout.addWidget(QLabel('Production Rules'))
        self.PR_txt = QTextEdit()
        self.PR_txt.setPlainText("E -> E + T\nE -> T\nT -> T * F\nT -> F\nF -> (E)\nF -> id")
        self.PR_txt.setFont(QFont("Times", 15))
        self.PR_txt.setReadOnly(True)
        self.PR_txt.setStyleSheet('background-color: #f1f0ef;')
        PR_layout.addWidget(self.PR_txt)

        # 3.2 Terminal Results

        terminal_layout = QVBoxLayout()
        self.term_label = QLabel("")
        terminal_layout.addWidget(self.term_label)
        self.term_txt = QTextEdit("")
        self.term_txt.setReadOnly(True)
        self.term_txt.setFont(QFont("Times", 12))
        self.term_txt.setStyleSheet('background-color: #f1f0ef;')
        terminal_layout.addWidget(self.term_txt)

        # Nesting Layouts

        lower_middle_layout.addLayout(derivation_steps_layout)
        lower_middle_layout.addLayout(production_rule_layout)
        lower_middle_layout.addLayout(action_layout)
        lower_middle_layout.addLayout(stack_layout)

        middle_layout.addLayout(lower_middle_layout)

        bottom_layout.addLayout(PR_layout)
        bottom_layout.addLayout(terminal_layout)

        main_layout.addWidget(frame)
        main_layout.addLayout(bottom_layout)
        processTab.setLayout(main_layout)

        return processTab

    def changeSliderValue(self, value):
        self.animation_speed = value

    @pyqtSlot()

    def on_click_input(self):
        input_value = self.input_txt.text()
        self.full_parse_flag = True

        self.step_counter = 1
        self.rule_counter = 0
        self.coord_counter = 0

        for x in range(0, 12):
            for y in range(0, 9):
                self.table.item(x, y).setBackground(QColor(255,255,255))

        my_timer = Timer()

        my_timer.start()
        stack, actions, expressions, prod_rules, term_output, coords, status_code= SRParse(input_value)
        my_timer.stop()

        if status_code == 0:

            exp_results = ""
            action_results = ""
            stack_results = ""
            prod_rules_results = ""
            term_results = ""

            for i in expressions:
                exp_results += i + "\n"

            for j in actions:
                action_results += j + "\n"

            for k in stack:
                stack_results += k + "\n"

            for l in prod_rules:
                prod_rules_results += l + "\n"

            exp_results = exp_results.rstrip("\n")
            action_results = action_results.rstrip("\n")
            stack_results = stack_results.rstrip("\n")
            prod_rules_results = prod_rules_results.rstrip("\n")

            self.derv_txt.setText(exp_results)
            self.action_txt.setText(action_results)
            self.stack_txt.setText(stack_results)
            self.prod_rule_txt.setText(prod_rules_results)
            self.time_txt.setText(my_timer.getTime())

            self.term_label.setText("Successfully Parsed Input in " + str(len(stack)) + " steps")
            self.term_label.setStyleSheet("color: green")

            for m in term_output:
                term_results += m + "\n"

            term_results = term_results.rstrip("\n")

            self.term_txt.setText(term_results)

            # Table Highlight last
            while self.coord_counter < len(coords):

                # Peterson Lock to avoid multithreading issues
                if self.full_parse_flag:
                    # Table Highlight
                    my_x = self.x_axis[(coords[self.coord_counter])[1]]
                    my_y = (coords[self.coord_counter])[0]

                    self.table.item(int(my_y), my_x).setBackground(QColor(126, 225, 106))
                    self.coord_counter += 1



                    if (actions[self.step_counter - 1])[0] == "R":
                        my_x = self.x_axis[(coords[self.coord_counter])[1]]
                        my_y = (coords[self.coord_counter])[0]
                        self.table.item(int(my_y), my_x).setBackground(QColor(220, 114, 114))
                        self.coord_counter += 1

                    QTest.qWait((self.animation_speed_max+self.animation_speed_min)-self.animation_speed)

                    if self.full_parse_flag:
                        for x in range(0, 12):
                            for y in range(0, 9):
                                self.table.item(x, y).setBackground(QColor(255, 255, 255))
                    else:
                        break
                else:
                    break


                self.step_counter += 1



            if self.coord_counter == len(coords):
                my_x = self.x_axis[(coords[len(coords) - 1])[1]]
                my_y = (coords[len(coords) - 1])[0]

                self.table.item(int(my_y), my_x).setBackground(QColor(126, 225, 106))



        elif status_code == 1:
            self.term_label.setText("ERROR: Action Not Found Within Table!")
            self.term_label.setStyleSheet("color: red")

        elif status_code == 2:
            self.term_label.setText("ERROR: Program Encountered Empty Cell in Table!")
            self.term_label.setStyleSheet("color: red")

        elif status_code == 3:
            self.term_label.setText("ERROR: Unknown or Missing Character Within Input String!")
            self.term_label.setStyleSheet("color: red")

        elif status_code == 4:
            self.term_label.setText("ERROR: No Input Detected!")
            self.term_label.setStyleSheet("color: red")


    def on_click_step(self):
        input_value = self.input_txt.text()

        for x in range(0, 12):
            for y in range(0, 9):
                self.table.item(x, y).setBackground(QColor(255,255,255))

        if input_value != self.previous_input or self.full_parse_flag is True:
            self.derv_txt.setText("")
            self.action_txt.setText("")
            self.stack_txt.setText("")
            self.prod_rule_txt.setText("")
            self.time_txt.setText("00:00:00")
            self.term_txt.setText("")
            self.term_label.setText("")
            self.step_counter = 1
            self.rule_counter = 0
            self.coord_counter = 0
            self.full_parse_flag = False

        self.previous_input = input_value

        my_timer = Timer()

        my_timer.start()
        stack, actions, expressions, prod_rules, term_output, coords, status_code = SRParse(input_value)
        my_timer.stop()


        if status_code == 0:

            exp_results = ""
            action_results = ""
            stack_results = ""
            prod_rules_results = ""
            term_results = ""

            for i in range(0, self.step_counter):
                exp_results += expressions[i] + "\n"

            for j in range(0, self.step_counter):
                action_results += actions[j] + "\n"

            for k in range(0, self.step_counter):
                stack_results += stack[k] + "\n"

            if (actions[self.step_counter-1])[0] == "R":
                self.rule_counter += 1

            for l in range(0, self.rule_counter):
                prod_rules_results += prod_rules[l] + "\n"

            exp_results = exp_results.rstrip("\n")
            action_results = action_results.rstrip("\n")
            stack_results = stack_results.rstrip("\n")
            prod_rules_results = prod_rules_results.rstrip("\n")

            self.derv_txt.setText(exp_results)
            self.action_txt.setText(action_results)
            self.stack_txt.setText(stack_results)
            self.prod_rule_txt.setText(prod_rules_results)

            if self.step_counter == len(stack):
                self.time_txt.setText(my_timer.getTime())

            if self.step_counter != len(stack):
                self.term_label.setText("Step " + str(self.step_counter))
                self.term_label.setStyleSheet("color: black")
            else:
                self.term_label.setText("Successfully Parsed Input in " + str(len(stack)) + " steps")
                self.term_label.setStyleSheet("color: green")

            for m in range(0, self.step_counter):
                term_results += term_output[m] + "\n"

            term_results = term_results.rstrip("\n")

            self.term_txt.setText(term_results)

            if self.coord_counter < len(coords):
                # Table Highlight
                my_x = self.x_axis[(coords[self.coord_counter])[1]]
                my_y = (coords[self.coord_counter])[0]

                self.table.item(int(my_y), my_x).setBackground(QColor(126, 225, 106))
                self.coord_counter += 1

                if (actions[self.step_counter - 1])[0] == "R":
                    my_x = self.x_axis[(coords[self.coord_counter])[1]]
                    my_y = (coords[self.coord_counter])[0]
                    self.table.item(int(my_y), my_x).setBackground(QColor(220, 114, 114))
                    self.coord_counter += 1

            elif self.coord_counter == len(coords):
                my_x = self.x_axis[(coords[len(coords) - 1])[1]]
                my_y = (coords[len(coords) - 1])[0]

                self.table.item(int(my_y), my_x).setBackground(QColor(126, 225, 106))


            if self.step_counter < len(stack):
                self.step_counter += 1

        elif status_code == 1:
            self.term_label.setText("ERROR: Action Not Found Within Table!")
            self.term_label.setStyleSheet("color: red")

        elif status_code == 2:
            self.term_label.setText("ERROR: Program Encountered Empty Cell in Table!")
            self.term_label.setStyleSheet("color: red")

        elif status_code == 3:
            self.term_label.setText("ERROR: Unknown or Missing Character Within Input String!")
            self.term_label.setStyleSheet("color: red")

        elif status_code == 4:
            self.term_label.setText("ERROR: No Input Detected!")
            self.term_label.setStyleSheet("color: red")



def main():

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()