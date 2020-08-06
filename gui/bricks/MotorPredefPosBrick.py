#
#  Project: MXCuBE
#  https://github.com/mxcube
#
#  This file is part of MXCuBE software.
#
#  MXCuBE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  MXCuBE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with MXCuBE.  If not, see <http://www.gnu.org/licenses/>.

from gui.BaseComponents import BaseWidget
from gui.utils import Colors, Icons, QtImport


__credits__ = ["MXCuBE collaboration"]
__license__ = "LGPLv3+"
__category__ = "Motor"


class MotorPredefPosBrick(BaseWidget):

    STATE_COLORS = (
        Colors.LIGHT_YELLOW,  # INITIALIZING
        Colors.LIGHT_GREEN,  # ON
        Colors.DARK_GRAY,  # OFF
        Colors.LIGHT_GREEN,  # READY
        Colors.LIGHT_YELLOW,  # BUSY
        Colors.LIGHT_YELLOW,  # MOVING
        Colors.LIGHT_GREEN,  # STANDBY
        Colors.DARK_GRAY,  # DISABLED
        Colors.DARK_GRAY,  # UNKNOWN
        Colors.LIGHT_RED,  # ALARM
        Colors.LIGHT_RED,  # FAULT
        Colors.LIGHT_RED,  # INVALID
        Colors.DARK_GRAY,  # OFFLINE
        Colors.LIGHT_RED,  # LOWLIMIT
        Colors.LIGHT_RED,  # HIGHLIMIT
        Colors.DARK_GRAY,
    )  # NOTINITIALIZED

    def __init__(self, *args):
        BaseWidget.__init__(self, *args)

        # Hardware objects ----------------------------------------------------
        self.motor_hwobj = None

        # Internal values -----------------------------------------------------

        self.positions = None

        # Properties ----------------------------------------------------------
        self.add_property("label", "string", "")
        self.add_property("mnemonic", "string", "")
        self.add_property("icons", "string", "")
        self.add_property("showMoveButtons", "boolean", True)

        # Signals -------------------------------------------------------------

        # Slots ---------------------------------------------------------------
        self.define_slot("setEnabled", ())

        # Graphic elements ----------------------------------------------------
        _main_gbox = QtImport.QGroupBox(self)
        self.label = QtImport.QLabel("motor:", _main_gbox)
        self.positions_combo = QtImport.QComboBox(self)
        self.previous_position_button = QtImport.QPushButton(_main_gbox)
        self.next_position_button = QtImport.QPushButton(_main_gbox)

        # Layout --------------------------------------------------------------
        _main_gbox_hlayout = QtImport.QHBoxLayout(_main_gbox)
        _main_gbox_hlayout.addWidget(self.label)
        _main_gbox_hlayout.addWidget(self.positions_combo)
        _main_gbox_hlayout.addWidget(self.previous_position_button)
        _main_gbox_hlayout.addWidget(self.next_position_button)
        _main_gbox_hlayout.setSpacing(2)
        _main_gbox_hlayout.setContentsMargins(2, 2, 2, 2)

        _main_hlayout = QtImport.QHBoxLayout(self)
        _main_hlayout.addWidget(_main_gbox)
        _main_hlayout.setSpacing(0)
        _main_hlayout.setContentsMargins(0, 0, 0, 0)
        # Size Policy ---------------------------------------------------------

        # Qt signal/slot connections ------------------------------------------
        self.positions_combo.activated.connect(self.position_selected)
        self.previous_position_button.clicked.connect(self.select_previous_position)
        self.next_position_button.clicked.connect(self.select_next_position)

        # Other ---------------------------------------------------------------
        self.positions_combo.setFixedHeight(27)
        self.positions_combo.setToolTip("Moves the motor to a predefined position")
        self.previous_position_button.setIcon(Icons.load_icon("Minus2"))
        self.previous_position_button.setFixedSize(27, 27)
        self.next_position_button.setIcon(Icons.load_icon("Plus2"))
        self.next_position_button.setFixedSize(27, 27)

    def setToolTip(self, name=None, state=None):
        states = ("NOTREADY", "UNUSABLE", "READY", "MOVESTARTED", "MOVING", "ONLIMIT")
        if name is None:
            name = self["mnemonic"]
        if self.motor_hwobj is None:
            tip = "Status: unknown motor " + name
        else:
            if state is None:
                state = self.motor_hwobj.get_state()
            try:
                state_str = states[state]
            except IndexError:
                state_str = "UNKNOWN"
            tip = "State:" + state_str

        self.label.setToolTip(tip)

    def motor_state_changed(self, state):
        # TODO remove this check and use motor_states as in AbstractMotor
        if hasattr(self.motor_hwobj, "motor_states"):
            s = state in (
                self.motor_hwobj.motor_states.READY,
                self.motor_hwobj.motor_states.LOWLIMIT,
                self.motor_hwobj.motor_states.HIGHLIMIT,
            )
        else:
            s = state in (self.motor_hwobj.READY, self.motor_hwobj.ONLIMIT)
        self.positions_combo.setEnabled(s)
        Colors.set_widget_color(
            self.positions_combo,
            MotorPredefPosBrick.STATE_COLORS[state],
            QtImport.QPalette.Button,
        )
        self.setToolTip(state=state)

    def property_changed(self, property_name, old_value, new_value):
        if property_name == "label":
            if new_value == "" and self.motor_hwobj is not None:
                self.label.setText("<i>" + self.motor_hwobj.username + ":</i>")
            else:
                self.label.setText(new_value)
        elif property_name == "mnemonic":
            if self.motor_hwobj is not None:
                self.disconnect(
                    self.motor_hwobj, "stateChanged", self.motor_state_changed
                )
                self.disconnect(
                    self.motor_hwobj, "newPredefinedPositions", self.fill_positions
                )
                self.disconnect(
                    self.motor_hwobj,
                    "predefinedPositionChanged",
                    self.predefined_position_changed,
                )

            self.motor_hwobj = self.get_hardware_object(new_value)

            if self.motor_hwobj is not None:
                self.connect(
                    self.motor_hwobj, "newPredefinedPositions", self.fill_positions
                )
                self.connect(self.motor_hwobj, "stateChanged", self.motor_state_changed)
                self.connect(
                    self.motor_hwobj,
                    "predefinedPositionChanged",
                    self.predefined_position_changed,
                )
                self.fill_positions()
                if self.motor_hwobj.is_ready():
                    self.predefined_position_changed(
                         self.motor_hwobj.get_current_position_name(), 0
                    )
                if self["label"] == "":
                    lbl = self.motor_hwobj.username
                    self.label.setText("<i>" + lbl + ":</i>")
                Colors.set_widget_color(
                    self.positions_combo,
                    MotorPredefPosBrick.STATE_COLORS[0],
                    QtImport.QPalette.Button,
                )
                self.motor_state_changed(self.motor_hwobj.get_state())
        elif property_name == "showMoveButtons":
            if new_value:
                self.previous_position_button.show()
                self.next_position_button.show()
            else:
                self.previous_position_button.hide()
                self.next_position_button.hide()
        elif property_name == "icons":
            icons_list = new_value.split()
            try:
                self.previous_position_button.setIcon(Icons.load_icon(icons_list[0]))
                self.next_position_button.setIcon(Icons.load_icon(icons_list[1]))
            except BaseException:
                pass
        else:
            BaseWidget.property_changed(self, property_name, old_value, new_value)

    def fill_positions(self, positions=None):
        self.positions_combo.clear()
        if self.motor_hwobj is not None:
            if positions is None:
                positions = self.motor_hwobj.get_predefined_positions_list()
        if positions is None:
            positions = []
        for p in positions:
            pos_list = str(p).split()
            pos_name = pos_list[1]
            self.positions_combo.addItem(str(pos_name))

        self.positions = positions
        if self.motor_hwobj is not None:
            if self.motor_hwobj.is_ready():
                self.predefined_position_changed(
                    self.motor_hwobj.get_current_position_name(), 0
                )

    def position_selected(self, index):
        if index >= 0:
            self.motor_hwobj.move_to_position(self.positions[index])
        self.positions_combo.setCurrentIndex(-1)
        self.next_position_button.setEnabled(index < (len(self.positions) - 1))
        self.previous_position_button.setEnabled(index >= 0)

    def predefined_position_changed(self, position_name, offset):
        if self.positions:
            for index, item in enumerate(self.positions):
                if position_name == item:
                    self.positions_combo.setCurrentIndex(index)

    def select_previous_position(self):
        self.position_selected(self.positions_combo.currentIndex() - 1)

    def select_next_position(self):
        self.position_selected(self.positions_combo.currentIndex() + 1)
