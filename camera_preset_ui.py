try:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
except:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance

import maya.OpenMayaUI as omui

def getMayaMainWindow():
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)

class CameraPresetUI(QtWidgets.QDialog):
    def __init__(self, parent=getMayaMainWindow()):
        super(CameraPresetUI, self).__init__(parent)
        self.setWindowTitle("Camera Preset Tool")
        self.setMinimumWidth(350)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.buildUI()

    def buildUI(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        preset_layout = QtWidgets.QHBoxLayout()
        self.preset_dropdown = QtWidgets.QComboBox()
        self.preset_dropdown.addItems([
            "Cinematic 35mm",
            "Medium Shot 50mm",
            "Close-up 85mm",
            "Product Showcase",
            "Turntable Preview",
            "Social Portrait",
            "Social Square",
            "My Custom Preset 01"
        ])

        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.save_btn = QtWidgets.QPushButton("Save")
        self.delete_btn = QtWidgets.QPushButton("Delete")

        preset_layout.addWidget(self.preset_dropdown)
        preset_layout.addWidget(self.apply_btn)
        preset_layout.addWidget(self.save_btn)
        preset_layout.addWidget(self.delete_btn)

        options_layout = QtWidgets.QFormLayout()
        self.focal_input = QtWidgets.QLineEdit("35")
        self.aspect_dropdown = QtWidgets.QComboBox()
        self.aspect_dropdown.addItems(["16:9", "1:1", "9:16", "2.35:1"])
        self.resolution_input = QtWidgets.QLineEdit("1920 x 1080")
        self.dof_checkbox = QtWidgets.QCheckBox("Depth of Field")

        options_layout.addRow("Focal Length (mm):", self.focal_input)
        options_layout.addRow("Aspect Ratio:", self.aspect_dropdown)
        options_layout.addRow("Resolution:", self.resolution_input)
        options_layout.addRow("", self.dof_checkbox)

        bottom_btn_layout = QtWidgets.QHBoxLayout()
        self.create_cam_checkbox = QtWidgets.QCheckBox("Create New Camera")
        self.reset_btn = QtWidgets.QPushButton("Reset Camera")
        bottom_btn_layout.addWidget(self.create_cam_checkbox)
        bottom_btn_layout.addWidget(self.reset_btn)

        self.apply_main_btn = QtWidgets.QPushButton("APPLY")
        self.apply_main_btn.setStyleSheet("font-weight: bold; height: 30px;")

        main_layout.addLayout(preset_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(options_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(bottom_btn_layout)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.apply_main_btn)

def run():
    global ui

    try:
        ui.close()
    except:
        pass

    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = CameraPresetUI(parent=ptr)
    ui.show()