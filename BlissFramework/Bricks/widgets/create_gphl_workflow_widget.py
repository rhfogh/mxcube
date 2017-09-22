import qt
import queue_item
import queue_model_objects_v1 as queue_model_objects

import General
from create_task_base import CreateTaskBase
from widgets.data_path_widget import DataPathWidget
from widgets.processing_widget import ProcessingWidget
from widgets.gphl_acquisition_widget import GphlAcquisitionWidget

class CreateGphlWorkflowWidget(CreateTaskBase):
    def __init__(self, parent = None, name = None, fl = 0):
        CreateTaskBase.__init__(self, parent, name, fl, 'GphlWorkflow')

        # Data attributes
        self.workflows = {}
        
        self.init_models()

        #Layout
        v_layout = qt.QVBoxLayout(self, 2, 5, "main_v_layout")

        self._workflow_type_gbox = qt.QVGroupBox('Workflow type', self,
                                                 'workflow_rtype')

        self._workflow_cbox = qt.QComboBox(self._workflow_type_gbox)

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

        v_layout.addWidget(self._workflow_type_gbox)
        v_layout.addWidget(self._data_path_gbox)
        v_layout.addWidget(self._processing_gbox)
        v_layout.addWidget(self._acquisition_gbox)
        v_layout.addStretch()

        self.connect(self._data_path_widget.data_path_widget_layout.child('prefix_ledit'), 
                     qt.SIGNAL("textChanged(const QString &)"), 
                     self._prefix_ledit_change)

        self.connect(self._data_path_widget.data_path_widget_layout.child('run_number_ledit'),
                     qt.SIGNAL("textChanged(const QString &)"), 
                     self._run_number_ledit_change)

        self.connect(self._data_path_widget,
                     qt.PYSIGNAL("path_template_changed"),
                     self.handle_path_conflict)

    def set_workflow(self, workflow_hwobj):
        self._workflow_hwobj = workflow_hwobj
        self.workflows.clear()
        self._workflow_cbox.clear()

        if self._workflow_hwobj is not None:
            for workflow in self._workflow_hwobj.get_available_workflows():
                self._workflow_cbox.insertItem(workflow['name'])
                self.workflows[workflow['name']] = workflow


    def set_shape_history(self, shape_history_hwobj):
        pass

    # def init_models(self):
    #     CreateTaskBase.init_models(self)


    def single_item_selection(self, tree_item):
        CreateTaskBase.single_item_selection(self, tree_item)
        wf_model = tree_item.get_model()

        if isinstance(tree_item, queue_item.SampleQueueItem):
            sample_model = tree_item.get_model()
            self._processing_parameters = sample_model.processing_parameters
            #self._processing_parameters = copy.deepcopy(self._processing_parameters)
            self._processing_widget.update_data_model(self._processing_parameters)
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


    # def approve_creation(self):
    #     return CreateTaskBase.approve_creation(self)

    def init_models(self):
        CreateTaskBase.init_models(self)
        self._init_models()

    def _init_models(self):
        self._processing_parameters = queue_model_objects.ProcessingParameters()


    # Called by the owning widget (task_toolbox_widget) to create
    # a collection. When a data collection group is selected.
    def _create_task(self, sample, shape):
        tasks = []

        path_template = self._create_path_template(sample, self._path_template)
        path_template.num_files = 0

        wf_type = str(self._workflow_cbox.currentText())
        wf = queue_model_objects.GphlWorkflow()
        # TODO rethink path template, and other data
        wf.path_template = path_template
        wf.processing_parameters = self._processing_parameters
        workflow_hwobj = self._beamline_setup_hwobj.getObjectByRole(
            'gphl_workflow')
        wf.init_from_hwobj(wf_type, workflow_hwobj)
        wf.set_name(wf.path_template.get_prefix())
        wf.set_number(wf.path_template.run_number)

        acq_widget = self._gphl_acquisition_widget
        txt = acq_widget.get_parameter_value('resolution')
        wf.set_resolution(float(txt) if txt else None)

        dd = {}
        for tag in ('mad_1_energy', 'mad_2_energy', 'mad_3_energy'):
            is_on, label, value = acq_widget.get_parameter_value(tag)
            if is_on and label and value:
                dd[label] = General.h_over_e/float(value)
        wf.set_wavelengths(dd)
        
        tasks.append(wf)

        return tasks
