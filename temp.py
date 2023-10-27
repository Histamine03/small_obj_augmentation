import sys
from PyQt5.QtCore import Qt, QMimeData, QSize, QPoint
from PyQt5.QtGui import QPixmap, QDrag
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QScrollArea, QVBoxLayout, QWidget
import os

class DraggableLabel(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setPixmap(pixmap)
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            drag.setMimeData(mime_data)
            drag.setPixmap(self.pixmap().scaled(100, 100, Qt.KeepAspectRatio))
            drag.setHotSpot(event.pos())
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()

    def dropEvent(self, event):
        position = event.pos()
        self.setPixmap(self.pixmap())

class ImageGallery(QMainWindow):
    def __init__(self, image_folder):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.scroll_area = QScrollArea(self.central_widget)
        self.layout.addWidget(self.scroll_area)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.load_images(image_folder)

    def load_images(self, image_folder):
        for filename in os.listdir(image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                img_path = os.path.join(image_folder, filename)
                pixmap = QPixmap(img_path).scaled(200, 200, Qt.KeepAspectRatio)
                label = DraggableLabel(pixmap, self.scroll_content)
                self.scroll_layout.addWidget(label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageGallery(r"C:\Users\양태훈\city_data")
    window.show()
    sys.exit(app.exec_())


