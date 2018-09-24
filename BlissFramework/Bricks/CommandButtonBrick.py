#from qt import *

import qt
from BlissFramework import BaseComponents 

__category__ = 'Sample changer'

class CommandButtonBrick(BaseComponents.BlissWidget):

    def __init__(self, *args):
        BaseComponents.BlissWidget.__init__(self,*args)

        self.addProperty("sc_hwobj", "string", "")
        self.addProperty("md_hwobj", "string", "")
        self.addProperty('label', 'string', "")

        self.sc_hwobj = None
        self.md_hwobj = None


        containerBox = qt.QVGroupBox("CrystalDirect",self)
        containerBox.setInsideMargin(4)
        containerBox.setInsideSpacing(0)
        containerBox.setAlignment(qt.QLabel.AlignCenter)
        self.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Fixed)

        paramsBox = qt.QWidget(containerBox)
        qt.QGridLayout(paramsBox, 2, 2)
        lblCrystal = qt.QLabel("Current crystal ID: ", paramsBox)
        #self.leditCrystalID = qt.QLineEdit(paramsBox)
        self.lblCrystalID = qt.QLabel(paramsBox)
        self.lblCrystalID.setAlignment(qt.QLabel.AlignLeft)
        self.lblCrystalID.setText("???")
        self.btn_get_id = qt.QPushButton("Get crystal ID", paramsBox)
        self.connect(self.btn_get_id, qt.SIGNAL("clicked()"), self.get_id_clicked)

        paramsBox.layout().setSpacing(2)
        paramsBox.layout().setMargin(2)
        paramsBox.layout().addWidget(lblCrystal, 0, 0)
        paramsBox.layout().addWidget(self.lblCrystalID, 0, 1)
        paramsBox.layout().addWidget(self.btn_get_id, 0, 2)
        
        #initialize CrystalDirect working mode button
        self.btn_initialize = qt.QPushButton("InitializeCrystalDirect", containerBox)
        self.btn_initialize.setText("Initialize CrystalDirect")
        self.connect(self.btn_initialize, qt.SIGNAL("clicked()"), self.initialize_cd)

        qt.QVBoxLayout(self, 0, 0)
        self.layout().addWidget(containerBox)

    def propertyChanged(self, property_name, old_value, new_value):
        if property_name == 'sc_hwobj':
            self.sc_hwobj = self.getHardwareObject(new_value)
        elif property_name == 'md_hwobj':
            self.md_hwobj = self.getHardwareObject(new_value)


    def initialize_cd(self):
        self.sc_hwobj.initializeCrystalDirectWorkingMode()
        self.md_hwobj.manualCentringRequired()

    def get_id_clicked(self):
        lbl = self.sc_hwobj.get_crystal_id()
        self.lblCrystalID.setText(lbl)
        
