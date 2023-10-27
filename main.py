import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QScrollArea
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QBuffer

import crop
from DragLabel import DraggableLabel


# main APP
class App(QWidget):

    def __init__(self):
        super().__init__()

        self.image_list = []
        self.current_image_index = 0

        self.init_ui()
        self.setAcceptDrops(True)

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


        self.scroll_area.setWidgetResizable(True) 
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

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

        # 드랍 코드 
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-dnditemdata"):
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-dnditemdata"):
            # 드롭된 이미지를 QByteArray에서 QPixmap으로 변환
            byte_array = event.mimeData().data("application/x-dnditemdata")
            buffer = QBuffer(byte_array)
            buffer.open(QBuffer.ReadOnly)
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.data(), "PNG")

            # 드롭 위치에 라벨을 생성하고 이미지를 설정
            label = QLabel(self)
            label.setPixmap(pixmap)
            label.move(event.pos())
            label.show()

            event.acceptProposedAction()


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
            pixmap = QPixmap(filename)
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