#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  MXCuBE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with MXCuBE.  If not, see <http://www.gnu.org/licenses/>.

import sys
import copy
import logging
import os

from QtImport import *

import Qt4_queue_item
from Qt4_GraphicsLib import GraphicsItemPoint
import queue_model_objects_v1 as queue_model_objects

from Qt4_create_task_base import CreateTaskBase
from widgets.Qt4_data_path_widget import DataPathWidget


__category__ = 'Qt4_TaskToolbox_Tabs'


class CreateXRFSpectrumWidget(CreateTaskBase):
    def __init__(self, parent = None, name = None, fl = 0):
        CreateTaskBase.__init__(self, parent, name, 
            Qt.WindowFlags(fl), 'XRF spectrum')
 
        if name is not None:
            self.setObjectName(name)

        # Hardware objects ----------------------------------------------------

        # Internal variables --------------------------------------------------
        self.count_time = None

        self.init_models()

        # Graphic elements ----------------------------------------------------
        self._data_path_widget = DataPathWidget(self, 
             data_model = self._path_template, layout = 'vertical')

        self._parameters_widget = loadUi(os.path.join(os.path.dirname(__file__),
                        "ui_files/Qt4_xrf_parameters_widget_layout.ui"))
        
        self.adjust_transmission_cbox = self._parameters_widget.adjust_transmission_cbox
        self.excitation_energy_ledit = self._parameters_widget.excitation_energy_ledit
        self.excitation_energy_ledit.setText("15.00")
        self.count_time_ledit = self._parameters_widget.count_time_ledit
        self.count_time_ledit.setText("10")
        
        # Layout --------------------------------------------------------------
        
        _main_vlayout = QVBoxLayout(self)
        _main_vlayout.addWidget(self._data_path_widget)
        _main_vlayout.addWidget(self._parameters_widget)
        _main_vlayout.setSpacing(6)
        _main_vlayout.setContentsMargins(2, 2, 2, 2)
        _main_vlayout.addStretch(0)

        # SizePolicies --------------------------------------------------------

        # Qt signal/slot connections ------------------------------------------
        self._data_path_widget.pathTemplateChangedSignal.\
             connect(self.path_template_changed)
        self.adjust_transmission_cbox.stateChanged.connect(\
             self.adjust_transmission_state_changed)

        # Other ---------------------------------------------------------------

    def enable_compression(self, state):
        CreateTaskBase.enable_compression(self, False)

    def set_expert_mode(self, state):
        self.adjust_transmission_cbox.setEnabled(state)

    def init_models(self):
        CreateTaskBase.init_models(self)
        self.xrf_spectrum_model = queue_model_objects.XRFSpectrum()
        self._path_template.start_num = 1
        self._path_template.num_files = 1
        self._path_template.suffix = 'raw'
        self._path_template.compression = False
        
    def single_item_selection(self, tree_item):
        CreateTaskBase.single_item_selection(self, tree_item)
        self.xrf_spectrum_model = tree_item.get_model()

        if isinstance(tree_item, Qt4_queue_item.XRFSpectrumQueueItem):
            if self.xrf_spectrum_model.is_executed():
                self.setDisabled(True)
            else:
                self.setDisabled(False)    

            if self.xrf_spectrum_model.get_path_template():
                self._path_template = self.xrf_spectrum_model.get_path_template()

            self._data_path_widget.update_data_model(self._path_template)
        elif not(isinstance(tree_item, Qt4_queue_item.SampleQueueItem) or \
                 isinstance(tree_item, Qt4_queue_item.DataCollectionGroupQueueItem)):
            self.setDisabled(True)

    def approve_creation(self):
        #base_result = CreateTaskBase.approve_creation(self)
        base_result = True
        self.count_time = None
        self.excitation_energy = None
        try:
           self.count_time = float(str(self.count_time_ledit.text()))
        except:
           logging.getLogger("GUI").\
                error("Incorrect count time value.")

        try:
           self.excitation_energy = float(str(self.excitation_energy_ledit.text()))
        except:
           logging.getLogger("GUI").\
                error("Incorrect excitation energy value.")
            
        return base_result and self.count_time and self.excitation_energy


    # Called by the owning widget (task_toolbox_widget) to create
    # a collection. When a data collection group is selected.
    def _create_task(self, sample, shape):
        data_collections = []

        if self.count_time is not None:
            if not shape:
                cpos = queue_model_objects.CentredPosition()
                cpos.snapshot_image = self._graphics_manager_hwobj.get_scene_snapshot()
            else:
                # Shapes selected and sample is mounted, get the
                # centred positions for the shapes
                if isinstance(shape, GraphicsItemPoint):
                    snapshot = self._graphics_manager_hwobj.get_scene_snapshot(shape)

                    cpos = copy.deepcopy(shape.get_centred_position())
                    cpos.snapshot_image = snapshot

            path_template = self._create_path_template(sample, self._path_template)
           
            xrf_spectrum = queue_model_objects.XRFSpectrum(sample, path_template, cpos)
            xrf_spectrum.set_name(path_template.get_prefix())
            xrf_spectrum.set_number(path_template.run_number)
            xrf_spectrum.count_time = self.count_time
            xrf_spectrum.excitation_energy = self.excitation_energy
            xrf_spectrum.adjust_transmission = self.adjust_transmission_cbox.isChecked()
            
            data_collections.append(xrf_spectrum)
        else:
            logging.getLogger("GUI").\
                error("No count time specified.") 

        return data_collections

    def adjust_transmission_state_changed(self, state):
        self.xrf_spectrum_model.adjust_transmission = state > 0
