import qt
import queue_item
import queue_model_objects_v1 as queue_model_objects
import itertools

from create_task_base import CreateTaskBase
from widgets.data_path_widget import DataPathWidget

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

        self._data_path_widget.data_path_widget_layout.child('file_name_label').setText('')
        self._data_path_widget.data_path_widget_layout.child('file_name_value_label').hide()

        v_layout.addWidget(self._workflow_type_gbox)
        v_layout.addWidget(self._data_path_gbox)
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

        if isinstance(tree_item, queue_item.GenericWorkflowQueueItem):
            if tree_item.get_model().is_executed():
                self.setDisabled(True)
            else:
                self.setDisabled(False)
            
            if wf_model.get_path_template():
                self._path_template = wf_model.get_path_template()

            self._data_path_widget.update_data_model(self._path_template)
        elif isinstance(tree_item, queue_item.BasketQueueItem):
            self.setDisabled(False)            
        elif not(isinstance(tree_item, queue_item.SampleQueueItem) or \
                 isinstance(tree_item, queue_item.DataCollectionGroupQueueItem)):
            self.setDisabled(True)


    # def approve_creation(self):
    #     return CreateTaskBase.approve_creation(self)


    # Called by the owning widget (task_toolbox_widget) to create
    # a collection. When a data collection group is selected.
    def _create_task(self, sample, shape):
        tasks = []

        path_template = self._create_path_template(sample, self._path_template)
        path_template.num_files = 0

        wf_type = str(self._workflow_cbox.currentText())
        wf = queue_model_objects.GphlWorkflow()
        workflow_hwobj = self._beamline_setup_hwobj.getObjectByRole(
            'gphl_workflow')
        wf.init_from_workflow_hwobj(wf_type, workflow_hwobj)
        wf.set_name(wf_type)
        # TODO rethink path template, and other data
        wf.path_template = path_template
        
        tasks.append(wf)

        return tasks
