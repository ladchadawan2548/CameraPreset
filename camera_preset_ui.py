try:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
except:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

ROOT_RESOURCE_DIR = 'C:/Users/ladch/OneDrive/maya/2024/scripts/CameraPreset/picture'

def get_selected_camera_shape():
    sel = cmds.ls(selection=True)
    if not sel:
        return None
    node = sel[0]
    if cmds.objectType(node) == "camera":
        return node
    shapes = cmds.listRelatives(node, shapes=True) or []
    for s in shapes:
        if cmds.objectType(s) == "camera":
            return s
    return None


class CameraPresetDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('🎬 Camera Preset Tool 🎥')
        self.resize(450, 450)
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.setStyleSheet('''
            QDialog { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #94BBE9, stop:0.5 #F9F4A2, stop:1 #AEEECD); }
            QLineEdit, QComboBox, QPushButton, QSlider {
                border-radius: 8px; font-size: 14px; font-family: DIN Medium;
            }
        ''')


        self.headerLabel = QtWidgets.QLabel('🎬 CAMERA PRESET TOOL 🎥')
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headerLabel.setStyleSheet('font-size:16px; font-weight:bold; color:#004f6e;')
        self.mainLayout.addWidget(self.headerLabel)


        self.imageLabel = QtWidgets.QLabel()
        pix = QtGui.QPixmap(f"{ROOT_RESOURCE_DIR}/05.png")
        if not pix or pix.isNull():
            pix = QtGui.QPixmap(300, 200)
            pix.fill(QtGui.QColor("transparent"))
        scaled_pix = pix.scaled(QtCore.QSize(300, 300), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.imageLabel.setPixmap(scaled_pix)
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.imageLabel)


        self.presetLayout = QtWidgets.QHBoxLayout()
        self.presetDropdown = QtWidgets.QComboBox()
        self.default_presets = {
            "Cinematic 35mm": 35,
            "Medium Shot 50mm": 50,
            "Close-up 85mm": 85,
            "Product Showcase": 70,
            "Turntable Preview": 35,
            "Social Portrait": 35,
            "Social Square": 50,
            "Isometric": 35
        }
        self.presetDropdown.addItems(self.default_presets.keys())
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
        self.presetLayout.addWidget(self.save_btn)
        self.presetLayout.addWidget(self.delete_btn)
        self.mainLayout.addLayout(self.presetLayout)


        focalLayout = QtWidgets.QHBoxLayout()
        lbl = QtWidgets.QLabel("Focal Length:")
        lbl.setFixedWidth(100)
        self.focalSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.focalSlider.setRange(10, 300)
        self.focalSlider.setValue(35)
        self.focalSlider.setTickInterval(5)
        self.focalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.focalValueLabel = QtWidgets.QLabel("35 mm")
        self.focalValueLabel.setFixedWidth(60)
        focalLayout.addWidget(lbl)
        focalLayout.addWidget(self.focalSlider)
        focalLayout.addWidget(self.focalValueLabel)
        self.mainLayout.addLayout(focalLayout)


        cropLayout = QtWidgets.QHBoxLayout()
        cropLabel = QtWidgets.QLabel("Crop Setting:")
        cropLabel.setFixedWidth(100)
        self.cropCombo = QtWidgets.QComboBox()
        self.cropCombo.addItems(["No Crop", "4:3", "16:9", "Cinematic 2.39"])
        cropLayout.addWidget(cropLabel)
        cropLayout.addWidget(self.cropCombo)
        self.mainLayout.addLayout(cropLayout)

 
        filmGateLayout = QtWidgets.QHBoxLayout()
        filmGateLabel = QtWidgets.QLabel("Film Gate:")
        filmGateLabel.setFixedWidth(100)
        self.filmGateCombo = QtWidgets.QComboBox()
        self.filmGateCombo.addItems(["None", "4:3", "16:9", "Cinematic 2.39"])
        filmGateLayout.addWidget(filmGateLabel)
        filmGateLayout.addWidget(self.filmGateCombo)
        self.mainLayout.addLayout(filmGateLayout)

        self.mainLayout.addStretch()


        bottomLayout = QtWidgets.QHBoxLayout()
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
        self.cancelButton = QtWidgets.QPushButton("⛔ CANCEL 🥓")
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
        bottomLayout.addWidget(self.applyButton)
        bottomLayout.addWidget(self.cancelButton)
        self.mainLayout.addLayout(bottomLayout)


        self.focalSlider.valueChanged.connect(self.on_focal_changed)
        self.cropCombo.currentIndexChanged.connect(self.on_crop_changed)
        self.filmGateCombo.currentIndexChanged.connect(self.on_film_gate_changed)
        self.presetDropdown.currentTextChanged.connect(self.on_preset_changed)
        self.applyButton.clicked.connect(self.on_apply_clicked)
        self.cancelButton.clicked.connect(self.close)
        self.save_btn.clicked.connect(self.save_custom_preset)
        self.delete_btn.clicked.connect(self.delete_preset)

        self.load_user_presets()


    def on_focal_changed(self, value):
        self.focalValueLabel.setText(f"{value} mm")
        cam_shape = get_selected_camera_shape()
        if cam_shape:
            try:
                cmds.setAttr(f"{cam_shape}.focalLength", value)
            except Exception as e:
                cmds.warning(f"Cannot set focalLength: {e}")

    def on_crop_changed(self, index):
        mapping = {
            0: None,                    # No Crop
            1: (1600, 1200),            # 4:3
            2: (1920, 1080),            # 16:9
            3: (2048, 858),             # 2.39 cinematic
        }
        res = mapping.get(index)
        if res:
            w, h = res
            try:
                cmds.setAttr("defaultResolution.width", int(w))
                cmds.setAttr("defaultResolution.height", int(h))
            except Exception as e:
                cmds.warning(f"Cannot set defaultResolution: {e}")

    def on_film_gate_changed(self, index):
        cam_shape = get_selected_camera_shape()
        mapping = {
            0: None,                 # None
            1: (0.612, 0.459),       # 4:3
            2: (0.825, 0.464),       # 16:9
            3: (0.980, 0.410),       # 2.39 cinematic
        }
        filmback = mapping.get(index)
        if cam_shape and filmback:
            hAper, vAper = filmback
            try:
                cmds.setAttr(f"{cam_shape}.horizontalFilmAperture", hAper)
                cmds.setAttr(f"{cam_shape}.verticalFilmAperture", vAper)
                cmds.setAttr(f"{cam_shape}.displayGateMask", 1)
                cmds.setAttr(f"{cam_shape}.gateMaskOpacity", 1)
                cmds.setAttr(f"{cam_shape}.filmFit", 1)
            except Exception as e:
                cmds.warning(f"Cannot set film gate: {e}")
        elif cam_shape:
            cmds.setAttr(f"{cam_shape}.displayGateMask", 0)

    def on_preset_changed(self, preset_name):
        if preset_name in self.default_presets:
            val = int(self.default_presets[preset_name])
            self.focalSlider.setValue(val)
        else:
            try:
                if os.path.exists(PRESET_FILE):
                    with open(PRESET_FILE, 'r') as f:
                        user_presets = json.load(f)
                    if preset_name in user_presets:
                        self.focalSlider.setValue(int(user_presets[preset_name]))
            except Exception:
                pass

    def on_apply_clicked(self):
        cam_shape = get_selected_camera_shape()
        focal = self.focalSlider.value()
        if not cam_shape:
            QtWidgets.QMessageBox.warning(self, "No Camera", "Please select a camera to apply preset.")
            return
        try:
            cmds.setAttr(f"{cam_shape}.focalLength", focal)
            cam_transform = cmds.listRelatives(cam_shape, parent=True)[0]
            cmds.select(cam_transform)
            QtWidgets.QMessageBox.information(self, "✅ Applied", f"Applied {focal}mm to {cam_transform}")
        except Exception as e:
            cmds.warning(f"Apply failed: {e}")


    def save_custom_preset(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Save Preset", "Preset name:")
        if not ok or not name.strip():
            return
        value = self.focalSlider.value()
        presets = {}
        if os.path.exists(PRESET_FILE):
            try:
                with open(PRESET_FILE, 'r') as f:
                    presets = json.load(f)
            except Exception:
                presets = {}
        presets[name] = int(value)
        try:
            os.makedirs(os.path.dirname(PRESET_FILE), exist_ok=True)
            with open(PRESET_FILE, 'w') as f:
                json.dump(presets, f, indent=2)
        except Exception as e:
            cmds.warning(f"Cannot save preset: {e}")
            return
        self.presetDropdown.addItem(name)
        QtWidgets.QMessageBox.information(self, "Saved", f"Preset '{name}' saved ({value}mm)")

    def delete_preset(self):
        name = self.presetDropdown.currentText()
        if name in self.default_presets:
            QtWidgets.QMessageBox.warning(self, "Cannot delete", "Default preset cannot be deleted")
            return
        if not os.path.exists(PRESET_FILE):
            return
        try:
            with open(PRESET_FILE, 'r') as f:
                presets = json.load(f)
            if name in presets:
                del presets[name]
                with open(PRESET_FILE, 'w') as f:
                    json.dump(presets, f, indent=2)
                idx = self.presetDropdown.currentIndex()
                self.presetDropdown.removeItem(idx)
                QtWidgets.QMessageBox.information(self, "Deleted", f"Preset '{name}' deleted")
        except Exception as e:
            cmds.warning(f"Cannot delete preset: {e}")

    def load_user_presets(self):
        if os.path.exists(PRESET_FILE):
            try:
                with open(PRESET_FILE, 'r') as f:
                    presets = json.load(f)
                for k in presets:
                    if k not in self.default_presets:
                        self.presetDropdown.addItem(k)
            except Exception:
                pass


def run():
    global ui
    try:
        ui.close()
    except Exception:
        pass
    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = CameraPresetDialog(parent=ptr)
    ui.show()
