import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QScrollArea
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QBuffer

import crop
from DragLabel import DraggableLabel
from Paste_image import paste_obj

# main APP
class App(QWidget):

    def __init__(self):
        super().__init__()

        self.image_list = []
        self.object_list = []
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

# 버튼 정의
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
            label_position = event.pos()

            label_width = self.preview_label.width()
            label_height = self.preview_label.height()

            pixmap_width = self.preview_label.pixmap().width()
            pixmap_height = self.preview_label.pixmap().height()

            image_x = max(0, min(label_position.x() * pixmap_width / label_width, pixmap_width - 1))
            image_y = max(0, min(label_position.y() * pixmap_height / label_height, pixmap_height - 1))

            print("Dropped at (image coordinates):", image_x, image_y)

# 이미지 붙여넣기
            image_path = self.image_list[self.current_image_index]
            object_path = r"object/cropped_0.png"
            paste_obj(image_path, object_path, image_x, image_y)

# 객체를 초기화 시켜주는 코드 
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

# 이미지 폴더를 선택하는 함수
    def show_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.image_list = [os.path.join(folder, file_name) for file_name in os.listdir(folder)
                            if file_name.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.current_image_index = 0
            self.display_image()

#객체 업데이트
    def update_object(self, image_path):
        self.object_list = []
        current_folder = os.getcwd()
        self.object_list = crop.save_cropped_images(current_folder, image_path)
        self.clear_layout(self.scroll_layout)
        for filename in self.object_list:
            pixmap = QPixmap(filename)
            label = DraggableLabel(pixmap, filename, self.scroll_content)
            self.scroll_layout.addWidget(label)

#이미지를 보여주는 함수
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