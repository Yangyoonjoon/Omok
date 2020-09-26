from PyQt5.QtGui import QBrush, QPen, QColor, QPainter
from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox

class Game(QObject):

    # 클래스 변수
    update_signal = pyqtSignal()
    gameover_signal = pyqtSignal(int)

    def __init__(self, w):
        super().__init__()
        self.parent = w
        self.rect = w.rect()

        # 바둑판 사각형
        self.outrect = QRectF(self.rect)
        gap = 10
        self.outrect.adjust(gap,gap,-gap,-gap)

        # 바둑돌 놓는 사각형
        self.inrect = QRectF(self.outrect)
        gap = 20
        self.inrect.adjust(gap,gap,-gap,-gap)

        self.line = 19
        self.size = self.inrect.width()/(self.line-1)

        # 바둑돌
        self.wdol = []
        self.bdol = []
        self.bTrun = True

        # 바둑돌 중간 교차점
        x = self.inrect.left()
        y = self.inrect.top()
        self.cpt = [[QPointF(x+(self.size*c), y+(self.size*r)) for c in range(self.line)] for r in range(self.line)]
        #print(self.cpt)

        # 바둑판 상태 저장 0:돌없음, 1:흑돌, 2:백돌
        self.state = [[0 for c in range(self.line)] for r in range(self.line)]
        #print(self.state)


        # 시그널, 슬롯
        self.update_signal.connect(self.parent.update)
        self.gameover_signal.connect(self.parent.gameOver)


    def draw(self, qp):
        b = QBrush(QColor(175,150,75))
        qp.setBrush(b)
        qp.drawRect(self.outrect)

        x = self.inrect.left()
        y = self.inrect.top()

        x1 = self.inrect.right()
        y1 = self.inrect.top()

        x2 = self.inrect.left()
        y2 = self.inrect.bottom()

        # 바둑판 줄 그리기
        for i in range(self.line):
            qp.drawLine(x, y+(self.size*i), x1, y1+(self.size*i))
            qp.drawLine(x+(self.size*i), y, x2+(self.size*i), y2)

        # 흑돌 그리기
        b = QBrush(Qt.black)
        qp.setBrush(b)
        for dol in self.bdol:
            x = dol.x()-self.size/2
            y = dol.y()-self.size/2
            rect = QRectF(x,y,self.size,self.size)
            qp.drawEllipse(rect)

        # 백돌 그리기
        b = QBrush(Qt.white)
        qp.setBrush(b)
        for dol in self.wdol:
            x = dol.x()-self.size/2
            y = dol.y()-self.size/2
            rect = QRectF(x,y,self.size,self.size)
            qp.drawEllipse(rect)

    def mouseDown(self, x, y):
        # 바둑판 안에 두었는지?
        #T = self.inrect.top()
        #B = self.inrect.bottom()
        #L = self.inrect.left()
        #R = self.inrect.right()
        #if (x>L and x<R) and (y>T and y<B):
        if self.inrect.contains(QPointF(x,y)):
            row, col = self.getCP(x, y)
            print('row:', row, 'col:', col)

            # 돌이 없으면
            if self.state[row][col] == 0:
                if self.bTrun:
                    self.state[row][col] = 1
                    self.bdol.append(self.cpt[row][col])
                else:
                    self.state[row][col] = 2
                    self.wdol.append(self.cpt[row][col])

                self.bTrun = not self.bTrun
                self.update_signal.emit()

                # 판정 0:진행중, 1:흑돌승, 2:백돌승, 3:무승부
                result = self.panjung()
                if result != 0:
                    self.gameover_signal.emit(result)

            else:
                QMessageBox.warning(self.parent, '오류', '이미 돌이 있습니다', QMessageBox.Ok)
        else:
            QMessageBox.warning(self.parent, '오류', '바둑판 안에 돌을 놓으세요', QMessageBox.Ok)


    def getCP(self, x, y):
        s = self.size
        for r in range(self.line):
            for c in range(self.line):
                pt = self.cpt[r][c]
                _x = pt.x()
                _y = pt.y()
                rect = QRectF(_x-s/2, _y-s/2, s, s)
                if rect.contains(QPointF(x,y)):
                    return r, c


    def panjung(self):
        # 판정 0:진행중, 1:흑돌승, 2:백돌승, 3:무승부

        cnt = 0
        for r in range(self.line):
            for c in range(self.line):
                # 무승부
                if self.state[r][c] != 0:
                    cnt += 1

                # 흑돌 가로 판정
                if c<=14:
                    if (self.state[r][c] == 1
                        and self.state[r][c+1] == 1
                        and self.state[r][c+2] == 1
                        and self.state[r][c+3] == 1
                        and self.state[r][c+4] == 1):
                        return 1
                # 흑돌 세로 판정
                if r<=14:
                    if (self.state[r][c] == 1
                        and self.state[r+1][c] == 1
                        and self.state[r+2][c] == 1
                        and self.state[r+3][c] == 1
                        and self.state[r+4][c] == 1):
                        return 1
                # 흑돌 대각(좌우) 판정
                if r<=14 and c<=14:
                    if (self.state[r][c] == 1
                        and self.state[r+1][c+1] == 1
                        and self.state[r+2][c+2] == 1
                        and self.state[r+3][c+3] == 1
                        and self.state[r+4][c+4] == 1):
                        return 1
                # 흑돌 대각(우좌) 판정
                if r<=14 and c>=4:
                    if (self.state[r][c] == 1
                        and self.state[r+1][c-1] == 1
                        and self.state[r+2][c-2] == 1
                        and self.state[r+3][c-3] == 1
                        and self.state[r+4][c-4] == 1):
                        return 1
                # 백돌 가로 판정
                if c<=14:
                    if (self.state[r][c] == 2
                        and self.state[r][c+1] == 2
                        and self.state[r][c+2] == 2
                        and self.state[r][c+3] == 2
                        and self.state[r][c+4] == 2):
                        return 2
                # 백돌 세로 판정
                if r<=14:
                    if (self.state[r][c] == 2
                        and self.state[r+1][c] == 2
                        and self.state[r+2][c] == 2
                        and self.state[r+3][c] == 2
                        and self.state[r+4][c] == 2):
                        return 2
                # 백돌 대각(좌우) 판정
                if r<=14 and c<=14:
                    if (self.state[r][c] == 2
                        and self.state[r+1][c+1] == 2
                        and self.state[r+2][c+2] == 2
                        and self.state[r+3][c+3] == 2
                        and self.state[r+4][c+4] == 2):
                        return 2
                # 백돌 대각(우좌) 판정
                if r<=14 and c>=4:
                    if (self.state[r][c] == 2
                        and self.state[r+1][c-1] == 2
                        and self.state[r+2][c-2] == 2
                        and self.state[r+3][c-3] == 2
                        and self.state[r+4][c-4] == 2):
                        return 2

        if cnt == self.line*self.line:
            return 3

        return 0