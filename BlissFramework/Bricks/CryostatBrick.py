"""
CryostatBrick

[Description]
The Cryostat brick shows temperature and other information from
a cryo cooling device.

[Properties]
------------------------------------------------------------------
| name       | type   | description
------------------------------------------------------------------
| mnemonic   | string |  name of corresponding Hardware Object
| formatString | string |  format string for numbers (defaults to ###.#)
------------------------------------------------------------------

[Signals]

[Slots]

[HardwareObjects]
The corresponding Hardware Object should emit these signals :
- temperatureChanged
- cryoStatusChanged

Example of valid Hardware Object XML :
======================================
<device class="Cryo">
  <username>Cryo</username>
  <controller>/bliss</controller>
  <cryostat>oxford700</cryostat>
</device>
"""
from BlissFramework.BaseComponents import BlissWidget
from BlissFramework import Icons
from qt import *
from BlissFramework.Utils import widget_colors

__category__ = "Synoptic"
__author__ = "A.Beteva"
__version__ = 1.0

class CryostatBrick(BlissWidget):
    def __init__(self, *args):
        BlissWidget.__init__(self, *args)
        
        self.addProperty("mnemonic", "string", "")
        self.addProperty('formatString', 'formatString', '###.#')
        self.addProperty('warningTemp', 'integer', 110)

        self.cryo_hwobj = None #Cryo Hardware Object

        self.containerBox=QVGroupBox("Cryo",self)
        self.containerBox.setInsideMargin(4)
        self.containerBox.setInsideSpacing(0)
        self.containerBox.setAlignment(QLabel.AlignCenter)

        self.temperature=QLabel(self.containerBox)
        self.temperature.setAlignment(QLabel.AlignCenter)
        self.temperature.setPaletteForegroundColor(widget_colors.WHITE)
        font=self.temperature.font()
        font.setStyleHint(QFont.OldEnglish)
        self.temperature.setFont(font)

        self.containerBox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        QVBoxLayout(self)
        self.layout().addWidget(self.containerBox)

    def fontChange(self,oldFont):
        font=self.font()
        size=font.pointSize()
        font.setPointSize(int(1.5*size))
        self.temperature.setFont(font)

    def setTemperature(self, temp, temp_error=None, old={"warning":False}):
        try:
            t = float(temp)
        except TypeError:
            self.temperature.setPaletteBackgroundColor(widget_colors.DARK_GRAY)
            self.temperature.setText("? K")
        else:
            svalue = "%s K" % str(self['formatString'] % temp)
            self.temperature.setText(svalue)

            if temp > self["warningTemp"]:
              self.temperature.setPaletteBackgroundColor(widget_colors.LIGHT_RED)
              if not old["warning"]:
                old["warning"]=True
                QMessageBox.critical(self, "Warning: risk for sample", "Cryo temperature is too high - sample is in danger!\nPlease fix the problem with cryo cooler") 
            else:
              old["warning"]=False 
              self.temperature.setPaletteBackgroundColor(widget_colors.LIGHT_BLUE)

    def propertyChanged(self, property, oldValue, newValue):
        if property == 'mnemonic':
            if self.cryo_hwobj is not None:
                #self.disconnect(self.cryo_hwobj, PYSIGNAL("levelChanged"), self.setLevel)
                self.disconnect(self.cryo_hwobj, PYSIGNAL("temperatureChanged"), self.setTemperature)
                
            self.cryo_hwobj = self.getHardwareObject(newValue)
            if self.cryo_hwobj is not None:
                self.containerBox.setEnabled(True)
                #self.connect(self.cryo_hwobj, PYSIGNAL("levelChanged"), self.setLevel)
                self.connect(self.cryo_hwobj, PYSIGNAL("temperatureChanged"), self.setTemperature)

                #self.setLevel(self.cryo_hwobj.n2level)
                self.setTemperature(self.cryo_hwobj.temp)
            else:
                self.containerBox.setEnabled(False)
                self.setTemperature(None)
                #self.setLevel(None)
        else:
            BlissWidget.propertyChanged(self,property,oldValue,newValue)

    def run(self):
        if self.cryo_hwobj is None:
            self.hide()
