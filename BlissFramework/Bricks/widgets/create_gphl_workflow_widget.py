import qt
import queue_item
import queue_model_objects_v1 as queue_model_objects

from General import States

from create_task_base import CreateTaskBase
from widgets.data_path_widget import DataPathWidget
from widgets.processing_widget import ProcessingWidget
from widgets.gphl_acquisition_widget import GphlAcquisitionWidget
from widgets.gphl_data_dialog import GphlDataDialog

class CreateGphlWorkflowWidget(CreateTaskBase):
    def __init__(self, parent = None, name = None, fl = 0):
        CreateTaskBase.__init__(self, parent, name, fl, 'GphlWorkflow')

        # Data attributes
        self._workflow_hwobj = None

        self.current_prefix = None

        # Tracks selected workflow to recognise when workflow changes
        self._previous_workflow = None

        #Layout
        v_layout = qt.QVBoxLayout(self, 2, 5, "main_v_layout")

        self._workflow_type_gbox = qt.QVGroupBox('Workflow type', self,
                                                 'workflow_rtype')

        self._workflow_cbox = qt.QComboBox(self._workflow_type_gbox)

        self.init_models()

        self._data_path_gbox = qt.QVGroupBox('Data location', self,
                                             'data_path_gbox')
        self._data_path_widget = DataPathWidget(self._data_path_gbox,
                                                data_model = self._path_template,
                                                layout = 'vertical')


        data_path_layout = self._data_path_widget.data_path_widget_layout
        # NBNB TODO change layout to remove invisible but space-using widgets
        data_path_layout.child('file_name_label').setText('')
        data_path_layout.child('file_name_value_label').hide()
        data_path_layout.child('run_number_label').setText('')
        data_path_layout.child('run_number_ledit').hide()

        self._processing_gbox = qt.QVGroupBox('Crystal data', self,
                                              'processing_gbox')

        self._processing_widget = ProcessingWidget(
            self._processing_gbox, data_model=self._processing_parameters
        )
        processing_layout = self._processing_widget.layout_widget
        processing_layout.child('num_residues_label').hide()
        processing_layout.child('num_residues_ledit').hide()

        self._acquisition_gbox = qt.QVGroupBox('Acquisition', self,
                                               'acquisition_gbox')
        self._gphl_acquisition_widget = GphlAcquisitionWidget(
            self._acquisition_gbox
        )

        # self._parameters_gbox = qt.QVGroupBox('Workflow parameters', self,
        #                                       'parameters_gbox')
        # self._gphl_parameters_widget = GphlParameters(
        #     self._parameters_gbox
        # )

        v_layout.addWidget(self._workflow_type_gbox)
        v_layout.addWidget(self._data_path_gbox)
        v_layout.addWidget(self._processing_gbox)
        v_layout.addWidget(self._acquisition_gbox)
        # v_layout.addWidget(self._parameters_gbox)
        v_layout.addStretch()

        # set up popup data dialog
        self.gphl_data_dialog = GphlDataDialog(self, 'GPhL Workflow Data')
        self.gphl_data_dialog.setModal(True)

        self.connect(self._data_path_widget.data_path_widget_layout.child('prefix_ledit'), 
                     qt.SIGNAL("textChanged(const QString &)"), 
                     self._prefix_ledit_change)

        self.connect(self._data_path_widget.data_path_widget_layout.child('run_number_ledit'),
                     qt.SIGNAL("textChanged(const QString &)"), 
                     self._run_number_ledit_change)

        self.connect(self._data_path_widget,
                     qt.PYSIGNAL("path_template_changed"),
                     self.handle_path_conflict)

        self.connect(self._workflow_cbox,
                     # qt.SIGNAL("textChanged(const QString &)"),
                     qt.SIGNAL('activated ( const QString &)'),
                     self.workflow_selected)

        self.connect(self.gphl_data_dialog, qt.PYSIGNAL("continue_clicked"),
                     self.data_acquired)

    def initialise_workflows(self, workflow_hwobj):
        self._workflow_hwobj = workflow_hwobj
        self._workflow_cbox.clear()
        # self._gphl_parameters_widget.set_workflow(workflow_hwobj)

        if self._workflow_hwobj is not None:
            workflow_dict = workflow_hwobj.get_available_workflows()
            first_name = list(workflow_dict)[0]
            for workflow_name in list(workflow_dict):
                self._workflow_cbox.insertItem(workflow_name)
            # self._workflow_cbox.setCurrentItem(0)
            self.workflow_selected(first_name, reset=True)

            workflow_hwobj.connect('gphlParametersNeeded',
                                   self.gphl_data_dialog.open_dialog)

        # Set hardwired and default values
        self._gphl_acquisition_widget.set_param_value('char_energy',
            workflow_hwobj.getProperty('characterisation_energy')
        )
        # Placeholder. Must be set to match hardwired detector distance
        self._gphl_acquisition_widget.set_param_value('detector_resolution', -1)

    def workflow_selected(self, name, reset=False):
        # necessary as this comes in as a QString object
        name = str(name)
        if reset or name != self._previous_workflow:
            self._workflow_cbox.setCurrentText(name)
            self._previous_workflow = name

            parameters = self._workflow_hwobj.get_available_workflows()[name]
            beam_energies = parameters.get('beam_energies', {})
            if bool(beam_energies):
                self._data_path_gbox.show()
                self._processing_gbox.show()
                self._acquisition_gbox.show()
                # self._parameters_gbox.show()
                self._gphl_acquisition_widget.display_energy_widgets(
                    list(beam_energies)
                )
                self.set_beam_energies(beam_energies)
                # These parameters are hardwired - for now
                self._gphl_acquisition_widget.set_parameter_enabled('detector_resolution', True)
                self._gphl_acquisition_widget.set_parameter_enabled('char_energy', False)
            else:
                self._gphl_acquisition_widget.display_energy_widgets([])
                self._processing_gbox.hide()
                self._acquisition_gbox.hide()

            prefix = parameters.get('prefix')
            if prefix is not None:
                self.current_prefix = prefix

    def data_acquired(self):
        """Data gathered from popup, continue execution"""
        pass

    def set_beam_energies(self, beam_energy_dict):
        parameter_dict = self._gphl_acquisition_widget.get_parameter_dict()
        for tag, energy in beam_energy_dict.items():
            if tag in parameter_dict:
                self._gphl_acquisition_widget.set_param_value(tag, energy)
            else:
                raise ValueError("GPhL: No active beam energy named %s"
                                 % tag)

    def single_item_selection(self, tree_item):
        CreateTaskBase.single_item_selection(self, tree_item)
        wf_model = tree_item.get_model()

        if isinstance(tree_item, queue_item.SampleQueueItem):
            sample_model = tree_item.get_model()
            self._processing_parameters = sample_model.processing_parameters
        else:

            if isinstance(tree_item, queue_item.GphlWorkflowQueueItem):
                if tree_item.get_model().is_executed():
                    self.setDisabled(True)
                else:
                    self.setDisabled(False)

                if wf_model.get_path_template():
                    self._path_template = wf_model.get_path_template()

                self._data_path_widget.update_data_model(self._path_template)

            elif isinstance(tree_item, queue_item.BasketQueueItem):
                self.setDisabled(False)
            elif not isinstance(tree_item, queue_item.DataCollectionGroupQueueItem):
                self.setDisabled(True)

        self._processing_widget.update_data_model(self._processing_parameters)

    def init_models(self):
        CreateTaskBase.init_models(self)
        self._init_models()

    def _init_models(self):
        self._processing_parameters = queue_model_objects.ProcessingParameters()
        self._processing_parameters.num_residues = 0
        self._processing_parameters.process_data = False
        # self.workflow_selected(self._workflow_cbox.currentText())

    def continue_button_click(self, sample_items, checked_items):
        """Intercepts the datacollection continue_button click for parameter setting"""
        tree_brick = self._tree_brick
        if tree_brick:
            for item in checked_items:
                model = item.get_model()
                if isinstance(model, queue_model_objects.GphlWorkflow):
                    dialog = tree_brick.dc_tree_widget.confirm_dialog
                    ss = dialog.dialog_layout_widget.take_snapshots_cbox.currentText()
                    model.set_snapshot_count(int(ss) if ss else 0)

    # Called by the owning widget (task_toolbox_widget) to create
    # a collection. When a data collection group is selected.
    def _create_task(self, sample, shape):
        tasks = []

        path_template = self._create_path_template(sample, self._path_template)
        path_template.num_files = 0

        ho = self._workflow_hwobj
        if ho.get_state() == States.OFF:
            # We will be setting up the connection now - time to connect to quit
            qt.QObject.connect(qt.qApp, qt.SIGNAL("aboutToQuit()"),
                               ho.shutdown)

            tree_brick = self._tree_brick
            if tree_brick:
                qt.QObject.connect(tree_brick.dc_tree_widget.confirm_dialog,
                                   qt.PYSIGNAL("continue_clicked"),
                                   self.continue_button_click)

        wf = queue_model_objects.GphlWorkflow(self._workflow_hwobj)
        wf.set_type(str(self._workflow_cbox.currentText()))

        if self.current_prefix:
            path_template.base_prefix = self.current_prefix
        # TODO rethink path template, and other data
        wf.path_template = path_template
        wf.processing_parameters = self._processing_parameters
        wf.set_name(wf.path_template.get_prefix())
        wf.set_number(wf.path_template.run_number)

        acq_widget = self._gphl_acquisition_widget
        txt = acq_widget.get_parameter_value('expected_resolution')
        wf.set_expected_resolution(float(txt) if txt else None)
        txt = acq_widget.get_parameter_value('detector_resolution')
        wf.set_detector_resolution(float(txt) if txt else None)
        txt = acq_widget.get_parameter_value('char_energy')
        wf.set_characterisation_energy(float(txt) if txt else None)

        dd = {}
        for tag in self._gphl_acquisition_widget._energy_tags:
            value = acq_widget.get_parameter_value(tag)
            if value:
                dd[tag] = float(value)
        wf.set_beam_energies(dd)
        
        tasks.append(wf)

        return tasks
