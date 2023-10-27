from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QDrag
from PyQt5.QtCore import QByteArray, QBuffer, Qt, QMimeData


# <DraggableLabel 클래스>
class DraggableLabel(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setPixmap(pixmap)
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 드래그 시작
            drag = QDrag(self)
            mime_data = QMimeData()

            # 이미지를 QByteArray로 변환하여 mime_data에 저장
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QBuffer.WriteOnly)
            self.pixmap().save(buffer, "PNG")
            mime_data.setData("application/x-dnditemdata", byte_array)

            drag.setMimeData(mime_data)
            drag.setPixmap(self.pixmap().scaled(100, 100, Qt.KeepAspectRatio))
            drag.setHotSpot(event.pos())
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

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

            # 원본 이미지에 드롭된 이미지를 추가
            self.setPixmap(pixmap)
            event.acceptProposedAction()