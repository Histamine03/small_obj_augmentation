import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QSplashScreen
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        label = QLabel("Main Window", self.central_widget)
        self.layout.addWidget(label)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 스플래시 스크린 설정
    pixmap = QPixmap("path/to/your/splash_image.jpg")
    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
    splash.show()

    # 메인 윈도우 설정
    main_win = MainWindow()

    # 스플래시 스크린을 일정 시간 동안 보여준 후 메인 윈도우를 띄움
    timer = QTimer()
    timer.singleShot(5000, splash.close)  # 5초 후 스플래시 스크린 종료
    timer.singleShot(5000, main_win.show)  # 5초 후 메인 윈도우 보여주기

    sys.exit(app.exec_())
