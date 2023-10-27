import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QScrollArea
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QFileInfo
import time
import crop

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

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.image_list = []
        self.current_image_index = 0

        self.init_ui()

    def init_ui(self):
        self.setGeometry(400, 200, 500, 500)
        self.setWindowTitle("Small Object Augmentation")
        self.setFixedSize(1200, 750)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(palette)

        layout = QHBoxLayout(self)

        self.preview_label = QLabel('Image Preview', self)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("color: white; border: 1px solid white;")
        layout.addWidget(self.preview_label, 2)

        left_layout = QVBoxLayout()

        self.folder_button = QPushButton('Select Folder', self)
        self.folder_button.setStyleSheet("background-color: white; color: black;")
        self.folder_button.clicked.connect(self.show_dialog)
        left_layout.addWidget(self.folder_button)


        # 스크롤 코드
        self.scroll_area = QScrollArea()
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setStyleSheet("color: white;")
        left_layout.addWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_content)

        button_layout = QHBoxLayout()
        self.prev_button = QPushButton('Previous', self)
        self.prev_button.setStyleSheet("background-color: white; color: black;")
        self.prev_button.clicked.connect(self.prev_image)
        button_layout.addWidget(self.prev_button)

        self.next_button = QPushButton('Next', self)
        self.next_button.setStyleSheet("background-color: white; color: black;")
        self.next_button.clicked.connect(self.next_image)
        button_layout.addWidget(self.next_button)

        left_layout.addLayout(button_layout)
        layout.addLayout(left_layout, 1)

        self.setLayout(layout)
        self.show()

    def show_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.image_list = [os.path.join(folder, file_name) for file_name in os.listdir(folder)
                            if file_name.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.current_image_index = 0
            self.display_image()

    def update_object(self, image_path):
        current_folder = os.getcwd()
        object_list = crop.save_cropped_images(current_folder, image_path)
        for filename in object_list:
            pixmap = QPixmap(filename).scaled(200, 200, Qt.KeepAspectRatio)
            label = DraggableLabel(pixmap, self.scroll_content)
            self.scroll_layout.addWidget(label)

    def display_image(self):
        if self.image_list:
            image_path = self.image_list[self.current_image_index]
            self.update_object(image_path)
            pixmap = QPixmap(image_path)
            self.preview_label.setPixmap(pixmap.scaled(self.preview_label.size(), Qt.KeepAspectRatio))

    def next_image(self):
        if self.image_list:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
            self.display_image()

    def prev_image(self):
        if self.image_list:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_list)
            self.display_image()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())