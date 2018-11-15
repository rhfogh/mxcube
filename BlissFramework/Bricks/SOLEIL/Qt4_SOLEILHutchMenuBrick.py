#
#  Project: MXCuBE
#  https://github.com/mxcube.
#
#  This file is part of MXCuBE software.
#
#  MXCuBE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  MXCuBE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#  along with MXCuBE.  If not, see <http://www.gnu.org/licenses/>.

import os
import logging
import traceback

from QtImport import *

from BlissFramework import Qt4_Icons
from BlissFramework.Utils import Qt4_widget_colors
from BlissFramework.Qt4_BaseComponents import BlissWidget

from Qt4_HutchMenuBrick import Qt4_HutchMenuBrick

__credits__ = ["MXCuBE colaboration"]
__version__ = "2.3"
__category__ = "SOLEIL"


class Qt4_SOLEILHutchMenuBrick(Qt4_HutchMenuBrick):
    """
    Descript. : HutchMenuBrick is used to perform sample centring
    """ 

    def create_layout(self):
        _main_layout = QHBoxLayout(self)
        _main_layout.addWidget(self.centre_button)
        _main_layout.addWidget(self.accept_button)
        #_main_layout.addWidget(self.reject_button)
        _main_layout.addWidget(self.create_line_button)
        _main_layout.addWidget(self.draw_grid_button)
        #_main_layout.addWidget(self.auto_focus_button)
        _main_layout.addWidget(self.snapshot_button)
        #_main_layout.addWidget(self.refresh_camera_button)
        #_main_layout.addWidget(self.visual_align_button)
        _main_layout.addWidget(self.select_all_button)
        _main_layout.addWidget(self.clear_all_button)
        _main_layout.addWidget(self.realign_button)
        _main_layout.addWidget(self.auto_center_button)
        _main_layout.addStretch(0)
        _main_layout.setSpacing(0)
        _main_layout.setContentsMargins(0, 0, 0, 0)