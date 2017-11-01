import os
import qt
from paramsgui import FieldsWidget

class GphlDataDialog(qt.QDialog):

    def __init__(self, parent = None, name = None, fl = 0):
        qt.QWidget.__init__(self, parent, name, fl)

        # AsyncResult to return values
        self._async_result = None
        
        # Layout
        qt.QVBoxLayout(self)
        main_layout = self.layout()
        main_layout.setSpacing(10)
        main_layout.setMargin(6)
        self.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)

        self.setCaption('GPhL Workflow parameters')

        # Info box
        self.info_gbox = qt.QVGroupBox('Info', self, "info_gbox")
        main_layout.addWidget(self.info_gbox)
        self.info_text = qt.QTextEdit(self.info_gbox, 'info_text')
        self.info_text.setTextFormat(0) # PlainText
        self.info_text.setFont(qt.QFont("Courier"))
        self.info_text.setReadOnly(True)

        # Special parameter box
        self.cplx_gbox = qt.QVGroupBox('Indexing solution', self,
                                         "cplx_gbox")
        main_layout.addWidget(self.cplx_gbox)
        self.cplx_widget = None

        # Parameter box
        self.parameter_gbox = qt.QVGroupBox('Parameters', self,
                                           "parameter_gbox")
        main_layout.addWidget(self.parameter_gbox)
        self.params_widget = None

        # Button bar
        button_layout = qt.QHBoxLayout(None,0,6,"button_layout")
        hspacer = qt.QSpacerItem(1,20,qt.QSizePolicy.Expanding,qt.QSizePolicy.Minimum)
        button_layout.addItem(hspacer)
        self.continue_button = qt.QPushButton('Continue', self,
                                              'continue_button')
        button_layout.addWidget(self.continue_button)
        self.cancel_button = qt.QPushButton('Abort', self, "cancel_button")
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        qt.QObject.connect(self.continue_button, qt.SIGNAL("clicked()"),
                           self.continue_button_click)

        qt.QObject.connect(self.cancel_button, qt.SIGNAL("clicked()"),
                           self.cancel_button_click)

        self.resize(qt.QSize(1018,472).expandedTo(self.minimumSizeHint()))
        self.clearWState(qt.Qt.WState_Polished)

    def continue_button_click(self):
        parameters = self.params_widget.get_parameters_map()
        self.accept()
        self._async_result.set(parameters)
        self._async_result = None

    def cancel_button_click(self):
        self.reject()
        self.parent.workflow_model.workflow_hwobj.abort("Manual abort")

    def open_dialog(self, field_list, async_result):

        self._async_result = async_result

        # get special parameters
        parameters = []
        info = None
        cplx = None
        for dd in field_list:
            if info is None and dd.get('variableName') == '_info':
                # Info text - goes to info_gbox
                info = dd
            elif cplx is None and dd.get('variableName') == '_cplx':
                # Complex parameter - goes to cplx_gbox
                cplx = dd
            else:
                parameters.append(dd)

        # Info box
        if info is None:
            self.info_text.setText('')
            self.info_gbox.setTitle('Info')
            self.info_gbox.hide()
        else:
            self.info_text.setText(info.get('defaultValue'))
            self.info_gbox.setTitle(info.get('uiLabel'))
            self.info_gbox.show()

        # Complex box
        if cplx is None:
            if self.cplx_widget:
                self.cplx_widget.delete()
            self.cplx_gbox.hide()
        else:
            if cplx.get('type') == 'textblock':
                self.cplx_widget = qt.QTextEdit(self.cplx_gbox, 'cplx_widget')
                self.cplx_gbox.layout().addWidget(self.cplx_widget)
                self.cplx_gbox.setTitle(cplx.get('uiLabel'))
                self.cplx_widget.setText(cplx.get('defaultValue'))
                self.cplx_widget.setTextFormat(0) # PlainText
                self.cplx_widget.setReadOnly(True)
                self.cplx_gbox.show()
            else:
                raise NotImplementedError(
                    "GPhL complex widget type %s not recognised"
                    % repr(cplx.get('type'))
                )

        # parameters widget
        if self.params_widget is not None:
            self.params_widget.delete()
            self.params_widget = None
        if parameters:
            self.params_widget = FieldsWidget(fields=parameters,
                                              parent=self.parameter_gbox)

            values ={}
            for dd in field_list:
                name = dd['variableName']
                value = dd.get('defaultValue')
                if value is not None:
                    dd[name] = value
            self.params_widget.set_values(values)

        self.show()
        self.setEnabled(True)
