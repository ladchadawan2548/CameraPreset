try:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
except:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

ROOT_RESOURCE_DIR = 'C:/Users/ladch/OneDrive/maya/2024/scripts/CameraPreset/picture'

class CameraPresetDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('❄️ NCT WISH 💚')
        self.resize(450,350)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.setStyleSheet('''
            QDialog {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0#94BBE9 stop:0.5 #F9F4A2, stop:1 #AEEECD);
            }
            QLineEdit, QComboBox, QPushButton {
                border-radius: 8px;
                font-size: 14px;
                font-family: DIN Medium;
            }
        '''
        )

        self.headerLabel = QtWidgets.QLabel('🎬 CAMERA PRESET TOOL 🎥')
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headerLabel.setStyleSheet('font-size: 16px; font-weight: bold; color: #004f6e;')
        self.mainLayout.addWidget(self.headerLabel)

        self.imageLabel = QtWidgets.QLabel()
        self.imagePixmap = QtGui.QPixmap(f"{ROOT_RESOURCE_DIR}/05.png")
        scaled_pixmap = self.imagePixmap.scaled(
            QtCore.QSize(300,300),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )

        self.imageLabel.setPixmap(scaled_pixmap)
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.imageLabel)


        self.presetLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.presetLayout)
        self.presetDropdown = QtWidgets.QComboBox()
        self.default_presets = {
            "Cinematic 35mm": ("35", "2.35:1", "1920 x 817"),
            "Medium Shot 50mm": ("50", "16:9", "1920 x 1080"),
            "Close-up 85mm": ("85", "16:9", "1920 x 1080"),
            "Product Showcase": ("70", "1:1", "1080 x 1080"),
            "Turntable Preview": ("35", "16:9", "1920 x 1080"),
            "Social Portrait": ("35", "9:16", "1080 x 1920"),
            "Social Square": ("50", "1:1", "1080 x 1080"),
            "Isometric": ("Orthographic", "N/A", "N/A", {"rotateX": 35.264, "rotateY": 45, "rotateZ": 0, "orthoWidth": 50})
        }
        self.presetDropdown.addItems(self.default_presets.keys())

        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.apply_btn.setStyleSheet(
            '''
                QPushButton {
                    background-color: #78D4F0;
                    color: white;
                    border-radius: 10px;
                    font-size: 16px;
                    font-family: DIN Medium;
                    font-weight: Medium;
                }
                QPushButton:hover {
                    background-color: #EDE887;
                }
                QPushButton:pressed {
                    background-color: #D084FA;
                }
            '''
        )
        self.save_btn = QtWidgets.QPushButton("Save Preset")
        self.save_btn.setStyleSheet(
            '''
                QPushButton {
                    background-color: #7DF595;
                    color: white;
                    border-radius: 10px;
                    font-size: 16px;
                    font-family: DIN Medium;
                    font-weight: Medium;
                }
                QPushButton:hover {
                    background-color: #EDE887;
                }
                QPushButton:pressed {
                    background-color: #D084FA;
                }
            '''
        )       
        self.delete_btn = QtWidgets.QPushButton("Delete Preset")
        self.delete_btn.setStyleSheet(
            '''
                QPushButton {
                    background-color: #F57DD3;
                    color: white;
                    border-radius: 10px;
                    font-size: 16px;
                    font-family: DIN Medium;
                    font-weight: Medium;
                }
                QPushButton:hover {
                    background-color: #EDE887;
                }
                QPushButton:pressed {
                    background-color: #D084FA;
                }
            '''
        )

        self.presetLayout.addWidget(self.presetDropdown)
        self.presetLayout.addWidget(self.apply_btn)
        self.presetLayout.addWidget(self.save_btn)
        self.presetLayout.addWidget(self.delete_btn)

        self.focalLineEdit = QtWidgets.QLineEdit(" 35")
        self.aspectDropdown = QtWidgets.QComboBox()
        self.aspectDropdown.addItems(["16:9", " 1:1", " 9:16", " 2.35:1"])
        self.resLineEdit = QtWidgets.QLineEdit(" 1920 x 1080")

        form = QtWidgets.QFormLayout()
        form.addRow("Focal Length (mm):", self.focalLineEdit)
        form.addRow("Aspect Ratio:", self.aspectDropdown)
        form.addRow("Resolution:", self.resLineEdit)
        self.mainLayout.addLayout(form)

        self.createCamCheck = QtWidgets.QCheckBox("Create New Camera")
        self.createCamCheck.setStyleSheet(
            '''
                QCheckBox {
                    color: #87E89A;
                    font-size: 16px;
                    font-family: "DIN Medium";
                    font-weight: Medium;
                }

                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                }

                QCheckBox::indicator:checked {
                    background-color: #9BD6FA;
                    border: 2px solid #224599;
                }

                QCheckBox::indicator:unchecked {
                    background-color: #8DCBFA;
                    border: 2px solid #B0B0B0;
                }
            '''
        )
        self.resetButton = QtWidgets.QPushButton("🔄 Reset")
        self.resetButton.setStyleSheet(
            '''
                QPushButton {
                    background-color: #8DCBFA;
                    color: white;
                    border-radius: 10px;
                    font-size: 16px;
                    font-family: DIN Medium;
                    font-weight: Medium;
                }
                QPushButton:hover {
                    background-color: #EDE887;
                }
                QPushButton:pressed {
                    background-color: #D084FA;
                }
            '''
        )
        optLayout = QtWidgets.QHBoxLayout()
        optLayout.addWidget(self.createCamCheck)
        optLayout.addWidget(self.resetButton)
        self.mainLayout.addLayout(optLayout)

        self.applyButton = QtWidgets.QPushButton("🪼 APPLY PRESET ✨")
        self.applyButton.setStyleSheet(
            '''
                QPushButton {
                    background-color: #87E89A;
                    color: white;
                    border-radius: 10px;
                    font-size: 16px;
                    font-family: DIN Medium;
                    font-weight: Medium;
                }
                QPushButton:hover {
                    background-color: #8DCBFA;
                }
                QPushButton:pressed {
                    background-color: #D084FA;
                }
            '''
        )
        self.cancelButton = QtWidgets.QPushButton("⛔ CANCEL🥓")
        self.cancelButton.setStyleSheet(
            '''
                QPushButton {
                    background-color: #FA7DC6;
                    color: white;
                    border-radius: 10px;
                    font-size: 16px;
                    font-family: DIN Medium;
                    font-weight: Medium;
                }
                QPushButton:hover {
                    background-color: #CD95F0;
                }
                QPushButton:pressed {
                    background-color: #FFBC85;
                }
            '''
        )
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.addWidget(self.applyButton)
        btnLayout.addWidget(self.cancelButton)
        self.mainLayout.addLayout(btnLayout)

        # ---------- Connections ----------
        self.applyButton.clicked.connect(self.applyPreset)
        self.resetButton.clicked.connect(self.resetCamera)
        self.cancelButton.clicked.connect(self.close)
        self.presetDropdown.currentTextChanged.connect(self.updatePresetValues)
        self.save_btn.clicked.connect(self.saveCustomPreset)
        self.delete_btn.clicked.connect(self.deletePreset)
        self.apply_btn.clicked.connect(self.applyPreset)

        self.loadUserPresets()
        self.mainLayout.addStretch()

    def loadUserPresets(self):
        """โหลด preset ที่ผู้ใช้บันทึกไว้"""
        if os.path.exists(PRESET_FILE):
            with open(PRESET_FILE, 'r') as f:
                user_presets = json.load(f)
            for name in user_presets:
                if name not in self.default_presets:
                    self.presetDropdown.addItem(name)
        else:
            with open(PRESET_FILE, 'w') as f:
                json.dump({}, f)

    def updatePresetValues(self, presetName):
        all_presets = dict(self.default_presets)
        if os.path.exists(PRESET_FILE):
            with open(PRESET_FILE, 'r') as f:
                user_presets = json.load(f)
                all_presets.update(user_presets)
        if presetName in all_presets:
            focal, aspect, res = all_presets[presetName]
            self.focalLineEdit.setText(focal)
            self.aspectDropdown.setCurrentText(aspect)
            self.resLineEdit.setText(res)

    def applyPreset(self):
        focal = float(self.focalLineEdit.text())
        createNew = self.createCamCheck.isChecked()

        if createNew or not cmds.ls(selection=True, type='camera'):
            cam = cmds.camera(name="PresetCamera")[0]
        else:
            cam = cmds.ls(selection=True, type='camera')[0]

        cmds.setAttr(f"{cam}.focalLength", focal)
        cmds.select(cam)
        QtWidgets.QMessageBox.information(self, "✅ Success", f"Applied preset to: {cam}")

    def resetCamera(self):
        sel = cmds.ls(selection=True, type='camera')
        if not sel:
            QtWidgets.QMessageBox.warning(self, "⚠️ No Camera", "กรุณาเลือกกล้องก่อนรีเซ็ต")
            return
        cam = sel[0]
        cmds.setAttr(f"{cam}.focalLength", 35)
        QtWidgets.QMessageBox.information(self, "🔄 Reset", f"Reset camera: {cam} to normal (35mm)")

    def saveCustomPreset(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Save Preset", "ชื่อพรีเซท:")
        if not ok or not name.strip():
            return
        data = {
            name: (
                self.focalLineEdit.text(),
                self.aspectDropdown.currentText(),
                self.resLineEdit.text()
            )
        }
        if os.path.exists(PRESET_FILE):
            with open(PRESET_FILE, 'r') as f:
                presets = json.load(f)
        else:
            presets = {}
        presets.update(data)
        with open(PRESET_FILE, 'w') as f:
            json.dump(presets, f, indent=4)

        self.presetDropdown.addItem(name)
        QtWidgets.QMessageBox.information(self, "✅ Saved", f"บันทึกพรีเซท '{name}' เรียบร้อยแล้ว")

    def deletePreset(self):
        presetName = self.presetDropdown.currentText()
        if presetName in self.default_presets:
            QtWidgets.QMessageBox.warning(self, "⚠️ Default Preset", "ไม่สามารถลบพรีเซทมาตรฐานได้")
            return
        if not os.path.exists(PRESET_FILE):
            return
        with open(PRESET_FILE, 'r') as f:
            presets = json.load(f)
        if presetName in presets:
            del presets[presetName]
            with open(PRESET_FILE, 'w') as f:
                json.dump(presets, f, indent=4)
            self.presetDropdown.removeItem(self.presetDropdown.currentIndex())
            QtWidgets.QMessageBox.information(self, "🗑️ Deleted", f"ลบ '{presetName}' เรียบร้อยแล้ว")


def run():
    global ui
    try:
        ui.close()
    except:
        pass

    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = CameraPresetDialog(parent=ptr)
    ui.show()
