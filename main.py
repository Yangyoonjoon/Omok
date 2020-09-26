from PyQt5.QtWidgets import QWidget, QApplication
import sys
from game import *


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('오목')
        self.setFixedSize(600,600)

        self.game = Game(self)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.game.draw(qp)
        qp.end()

    def mousePressEvent(self, e):
        self.game.mouseDown(e.x(), e.y())

    def gameOver(self, result):
        if result == 1:
            winner = '흑돌승'
        elif result == 2:
            winner = '백돌승'
        else:
            winner = '무승부'
        answer = QMessageBox.question(self, winner, '한판더 하시겠습니까?', QMessageBox.Yes | QMessageBox.No)

        if answer == QMessageBox.Yes:
            del(self.game)
            self.game = Game(self)
            self.update()
        else:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
