def paste_image(img_path, )


def dropEvent(self, event):
    if event.mimeData().hasText():
        filename = event.mimeData().text()
        print("선택된 객체의 파일 이름:", filename)

        label_position = event.pos()
        label_width = self.preview_label.width()
        label_height = self.preview_label.height()
        pixmap_width = self.preview_label.pixmap().width()
        pixmap_height = self.preview_label.pixmap().height()
        image_x = label_position.x() * pixmap_width / label_width
        image_y = label_position.y() * pixmap_height / label_height
        print("Dropped at (image coordinates):", image_x, image_y)
