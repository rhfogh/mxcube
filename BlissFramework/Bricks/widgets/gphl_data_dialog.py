import os
import qt
import queue_item
import queue_model_objects_v1 as queue_model_objects

class GphlDataDialogWidgetVerticalLayout(qt.QWidget):
    """Layout, modified from 
    confirm_dialog_widget_vertical_layout.ConfirmDialogWidgetVerticalLayout"""
    def __init__(self, parent=None, name=None, fl=0):
        qt.QWidget.__init__(self, parent, name, fl)

        if not name:
            self.setName("GphlDataDialogWidgetVerticalLayout")


        # GphlDataDialogWidgetVerticalLayout = qt.QHBoxLayout(self,11,6,"GphlDataDialogWidgetVerticalLayout")

        main_layout = qt.QVBoxLayout(self, 0, 15, "GPhL data main layout")

        self.parameter_gbox = qt.QGroupBox(self,"parameter_gbox")
        self.parameter_gbox.setColumnLayout(0,qt.Qt.Vertical)
        self.parameter_gbox.layout().setSpacing(15)
        self.parameter_gbox.layout().setMargin(11)
        parameter_gboxLayout = qt.QVBoxLayout(self.parameter_gbox.layout())
        parameter_gboxLayout.setAlignment(qt.Qt.AlignTop)

        self.parameter_label = qt.QLabel(self.parameter_gbox,"parameter_label")
        parameter_gboxLayout.addWidget(self.parameter_label)

        cbx_layout = qt.QVBoxLayout(None,0,6,"cbx_layout")
        #
        # self.force_dark_cbx = qt.QCheckBox(self.parameter_gbox,"force_dark_cbx")
        # cbx_layout.addWidget(self.force_dark_cbx)
        #
        # self.skip_existing_images_cbx = qt.QCheckBox(self.parameter_gbox,"skip_existing_images_cbx")
        # cbx_layout.addWidget(self.skip_existing_images_cbx)
        #
        #
        # take_snapshots_layout = qt.QHBoxLayout(None,0,3,"snapshots_layout")
        #
        # self.take_snapshots_label = qt.QLabel(self.parameter_gbox, "take_snaphots_label")
        # take_snapshots_layout.addWidget(self.take_snapshots_label)
        #
        # self.take_snapshots_cbox = qt.QComboBox(self.parameter_gbox, "take_snapshosts_cbox")
        # take_snapshots_layout.addWidget(self.take_snapshots_cbox)
        #
        # take_snapshots_hspacer = qt.QSpacerItem(1,20,qt.QSizePolicy.Expanding,qt.QSizePolicy.Minimum)
        # take_snapshots_layout.addItem(take_snapshots_hspacer)
        #
        # cbx_layout.addLayout(take_snapshots_layout)
        #
        # self.missing_one_cbx = qt.QCheckBox(self.parameter_gbox,"missing_one_cbx")
        # cbx_layout.addWidget(self.missing_one_cbx)
        #
        # self.missing_two_cbx = qt.QCheckBox(self.parameter_gbox,"missing_two_cbx")
        # cbx_layout.addWidget(self.missing_two_cbx)
        # parameter_gboxLayout.addLayout(cbx_layout)
        # main_layout.addWidget(self.parameter_gbox)
        #
        # self.file_list_view = qt.QListView(self,"file_list_view")
        # self.file_list_view.addColumn(self.__tr("Sample"))
        # self.file_list_view.header().setClickEnabled(0,self.file_list_view.header().count() - 1)
        # self.file_list_view.addColumn(self.__tr("Directory"))
        # self.file_list_view.addColumn(self.__tr("File name"))
        # self.file_list_view.setSizePolicy(qt.QSizePolicy(qt.QSizePolicy.Expanding,qt.QSizePolicy.Expanding,0,0,self.file_list_view.sizePolicy().hasHeightForWidth()))
        # main_layout.addWidget(self.file_list_view)

        button_layout = qt.QHBoxLayout(None,0,6,"button_layout")
        hspacer = qt.QSpacerItem(1,20,qt.QSizePolicy.Expanding,qt.QSizePolicy.Minimum)
        button_layout.addItem(hspacer)

        self.continue_button = qt.QPushButton(self,"continue_button")
        button_layout.addWidget(self.continue_button)

        self.cancel_button = qt.QPushButton(self,"cancel_button")
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)
        GphlDataDialogWidgetVerticalLayout.addLayout(main_layout)

        self.languageChange()

        self.resize(qt.QSize(1018,472).expandedTo(self.minimumSizeHint()))
        self.clearWState(qt.Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Confirm collect"))
        self.parameter_gbox.setTitle(self.__tr("Summary"))
        self.parameter_label.setText(self.__tr("<summary label>"))
        # self.force_dark_cbx.setText(self.__tr("Force dark current"))
        # self.skip_existing_images_cbx.setText(self.__tr("Skip already collected images"))
        # self.take_snapshots_label.setText(self.__tr("Number of crystal snapshots:"))
        #
        # self.take_snapshots_cbox.clear()
        # for i in self.snapshots_list:
        #     self.take_snapshots_cbox.insertItem(self.__tr(str(i)))
        #
        # self.missing_one_cbx.setText(self.__tr("Missing box one"))
        # self.missing_two_cbx.setText(self.__tr("Missing box two"))
        # self.file_list_view.header().setLabel(0,self.__tr("Sample"))
        # self.file_list_view.header().setLabel(1,self.__tr("Directory"))
        # self.file_list_view.header().setLabel(2,self.__tr("File name"))
        self.continue_button.setText(self.__tr("Continue"))
        self.cancel_button.setText(self.__tr("Cancel"))


    def __tr(self,s,c = None):
        return qt.qApp.translate("GphlDataDialogWidgetVerticalLayout",s,c)


class GphlDataDialog(qt.QDialog):
    def __init__(self, parent = None, name = None, fl = 0):
        qt.QWidget.__init__(self, parent, name, fl)

        # Attributes
        self.ready_event = False
        self.checked_items = []
        self.sample_items = []
        self.files_to_be_written = []
        self.item_run_number_list = []
        self.queue_model_hwobj = None
        
        # Layout
        qt.QVBoxLayout(self)
        self.dialog_layout_widget = GphlDataDialogWidgetVerticalLayout(self)
        #self.dialog_layout_widget.child('take_snapshosts_cbx').hide()
        self.dialog_layout_widget.child('file_list_view').setSorting(-1)
        self.layout().addWidget(self.dialog_layout_widget)

        qt.QObject.connect(self.dialog_layout_widget.continue_button,
                           qt.SIGNAL("clicked()"),
                           self.continue_button_click)

        qt.QObject.connect(self.dialog_layout_widget.cancel_button,
                           qt.SIGNAL("clicked()"),
                           self.cancel_button_click)

        self.dialog_layout_widget.force_dark_cbx.setOn(True)

        self.dialog_layout_widget.missing_one_cbx.hide()
        self.dialog_layout_widget.missing_two_cbx.hide()
        self.setCaption('Confirm collection')


    def set_plate_mode(self, plate_mode):
        self.dialog_layout_widget.snapshots_list = [1,0] if plate_mode else [4,1,2,0]
        self.dialog_layout_widget.languageChange()
 
 
    def disable_dark_current_cbx(self):
        self.dialog_layout_widget.force_dark_cbx.setEnabled(False)
        self.dialog_layout_widget.force_dark_cbx.setOn(False)


    def enable_dark_current_cbx(self):
        self.dialog_layout_widget.force_dark_cbx.setEnabled(True)
        self.dialog_layout_widget.force_dark_cbx.setOn(True)
        

    def set_items(self, checked_items):
        self.sample_items = []
        self.files_to_be_written = []
        self.checked_items = checked_items
        collection_items = []
        current_sample_item = None
        num_images = 0

        self.dialog_layout_widget.file_list_view.clear()

        for item in checked_items:
            if isinstance(item, queue_item.SampleQueueItem):
                self.sample_items.append(item)
                current_sample_item = item                                

            path_template = item.get_model().get_path_template()

            if path_template:
#                 if item.get_model().is_executed():
#                     self.item_run_number_list.append((item, path_template.run_number))

#                     # Increase the run-number for re-collect
#                     new_run_number = self.queue_model_hwobj.\
#                                      get_next_run_number(path_template,
#                                                          exclude_current = False)
#                     item.get_model().set_number(new_run_number)
#                     path_template.run_number = new_run_number

                collection_items.append(item)
                file_paths = path_template.get_files_to_be_written()
                num_images += len(file_paths)

                for fp in file_paths:
                    (dir_name, f_name) = os.path.split(fp)
                    sample_name = current_sample_item.get_model().get_display_name()

                    if sample_name is '':
                        sample_name = current_sample_item.get_model().loc_str

                    last_item =  self.dialog_layout_widget.child('file_list_view').lastItem()
                    fl = FileListViewItem(self.dialog_layout_widget.file_list_view,
                                          last_item, sample_name, dir_name, f_name)

                    if os.path.isfile(fp):
                            fl.set_brush(qt.QBrush(qt.Qt.red))

        num_samples = len(self.sample_items)
        num_collections = len(collection_items)

        self.dialog_layout_widget.\
            parameter_label.setText("Collecting " + str(num_collections) + \
                                  " collection(s) on " + str(num_samples) + \
                                  " sample(s) resulting in " + \
                                  str(num_images) + " image(s).")


    def continue_button_click(self):
        for item in self.checked_items:
            acq_params = None
            if isinstance(item.get_model(), queue_model_objects.DataCollection):
                acq_params = item.get_model().acquisitions[0].acquisition_parameters
            elif isinstance(item.get_model(), queue_model_objects.Characterisation):
                acq_params = item.get_model().reference_image_collection.acquisitions[0].acquisition_parameters
            if acq_params is None:
                continue
            acq_params.take_snapshots = int(self.dialog_layout_widget.take_snapshots_cbox.currentText())
            acq_params.take_dark_current = self.dialog_layout_widget.force_dark_cbx.isOn()
            acq_params.skip_existing_images = self.dialog_layout_widget.skip_existing_images_cbx.isOn()
        
        self.emit(qt.PYSIGNAL("continue_clicked"), (self.sample_items, self.checked_items))
        self.accept()


    def cancel_button_click(self):
#         for item, run_number in self.item_run_number_list:
#             item.get_model().set_number(run_number)
#             path_template = item.get_model().get_path_template()
#             path_template.run_number = run_number
                    
        self.reject()


if __name__ == "__main__":
    a = qt.QApplication(sys.argv)
    qt.QObject.connect(a, qt.SIGNAL("lastWindowClosed()"),
                       a, qt.SLOT("quit()"))
    
    w = GphlDataDialog()
    #a.setMainWidget(w)
    w.setModal(True)
    w.show()
    a.exec_loop()
