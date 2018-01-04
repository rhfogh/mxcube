"""GPhL bespoke input widget. Built from DataCollectParametersWidget"""

import logging

from PyQt4 import QtCore
from PyQt4 import QtGui
from widgets.Qt4_widget_utils import DataModelInputBinder

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

__category__ = 'Qt4_TaskToolbox_Tabs'

class GphlAcquisitionData(object):
    """Dummy container class for global phasing acquisition data

    Attributes are set in the GphlAcquisitionWidget"""
    pass

class GphlAcquisitionWidget(QtGui.QWidget):

    def __init__(self, parent=None, name='gphl_acquisition_widget'):
        QtGui.QWidget.__init__(self,parent)
        if name is not None:
            self.setObjectName(name)

        # Properties ----------------------------------------------------------

        # Signals ------------------------------------------------------------

        # Slots ---------------------------------------------------------------

        # Hardware objects ----------------------------------------------------

         # Internal variables -------------------------------------------------
        self.beam_energy_tags = ()
        self._widget_data = OrderedDict()
        self._data_object = GphlAcquisitionData()

        # Graphic elements ----------------------------------------------------
        _parameters_widget = QtGui.QWidget(self)
        QtGui.QGridLayout(_parameters_widget)
        _parameters_widget.layout().setColumnStretch(2, 1)

        # Layout --------------------------------------------------------------
        # This seems to be necessary to make widget visible
        _main_vlayout = QtGui.QVBoxLayout(self)
        _main_vlayout.addWidget(_parameters_widget)
        _main_vlayout.setSpacing(0)
        _main_vlayout.setContentsMargins(0, 0, 0, 0)

        row = 0
        field_name = 'expected_resolution'
        label_name = self._get_label_name(field_name)
        # setattr(data_object, field_name, 0.0)
        label_str = "Expected resolution (A) :"
        # setattr(data_object, label_name, label_str)
        label=QtGui.QLabel(label_str, _parameters_widget)
        _parameters_widget.layout().addWidget(label, row, 0)
        self._widget_data[label_name] = (label, str, None, label_str)
        # parameter_mib.bind_value_update(label_name, label, str)
        widget = QtGui.QLineEdit()
        widget.setAlignment(QtCore.Qt.AlignLeft)
        _parameters_widget.layout().addWidget(widget, row, 1)
        self._widget_data[field_name] = (
            widget, float, QtGui.QDoubleValidator(0.01, 20, 2, self), 0.0
        )
        # parameter_mib.bind_value_update(field_name, widget, float,
        #                                 QtGui.QDoubleValidator(0.01, 20, 2, self))

        row += 1
        label_name = 'beam_energies_label'
        label_str = "Beam energies (keV):"
        # setattr(data_object, label_name, label_str)
        label=QtGui.QLabel(label_str, _parameters_widget)
        _parameters_widget.layout().addWidget(label, row, 0)
        self._widget_data[label_name] = (label, str, None, label_str)
        # parameter_mib.bind_value_update(label_name, label, str)

        self.beam_energy_tags = ('energy_1', 'energy_2', 'energy_3',
                                 'energy_4',)

        ii = 0
        for label_str in ("First beam energy", "Second beam energy",
                          "Third beam energy", "Fourth beam energy"):
            ii += 1
            row += 1
            field_name = 'energy_%s' % ii
            label_name = self._get_label_name(field_name)
            # setattr(data_object, field_name, 0.0)
            # setattr(data_object, label_name, label_str)
            label=QtGui.QLabel(label_str, _parameters_widget)
            _parameters_widget.layout().addWidget(label, row, 0)
            self._widget_data[label_name] = (label, str, None, label_str)
            # parameter_mib.bind_value_update(label_name, label, str)
            widget = QtGui.QLineEdit()
            widget.setAlignment(QtCore.Qt.AlignLeft)
            _parameters_widget.layout().addWidget(widget, row, 1)
            self._widget_data[field_name] = (
                widget, float, QtGui.QDoubleValidator(0.01, 200, 2, self), 0.0
            )
            # parameter_mib.bind_value_update(field_name, widget, float,
            #     QtGui.QDoubleValidator(0.0, 200, 2, self)
            # )

        #
        #
        #
        #
        #
        #
        # # # Layout --------------------------------------------------------------
        # # # NB is used in setup_parameter_widget function; so must be set first
        # # QtGui.QGridLayout(self._parameter_box, 8, 3)
        # # self._parameter_box.layout().setColStretch(2, 1)
        #
        # # Graphic elements ----------------------------------------------------
        # self._parameter_box = QtGui.QWidget(parent)
        # wdg = self.setup_parameter_widget(
        #     'expected_resolution', self.PARAMETERS['expected_resolution']
        # )
        # wdg.setText('0.0')
        # label = QtGui.QLabel("Beam energies (keV):", self._parameter_box)
        # self._label_dict['_beam_energies_label'] = label
        # for tag in self._energy_tags:
        #     self._beam_energy_map[tag] = None
        #     self.setup_parameter_widget(tag, self.PARAMETERS[tag])
        #
        # self._parameter_box.layout().addWidget(label, 1, 0,)

    # def setup_parameter_widget(self, param_id, values):
    #     param_label=values[0]
    #     param_row=values[1]
    #     param_column=values[2]
    #     param_span=values[3]
    #     param_class=values[4]
    #     param_class_args=list(values[5])
    #     param_class_align=values[6]
    #     param_class_validator=values[7]
    #     connect_signals=values[8]
    #
    #     if param_label:
    #         label=QtGui.QLabel("%s:" % param_label, self._parameter_box)
    #         self._parameter_box.layout().addWidget(label, param_row, param_column)
    #         self._label_dict[param_id]=label
    #     param_class_args.append(self._parameter_box)
    #     input_widget=param_class(*param_class_args)
    #     if param_class_align is not None:
    #         input_widget.setAlignment(param_class_align)
    #     if param_class_validator is not None:
    #         class_validator=param_class_validator[0]
    #         validator=class_validator(input_widget)
    #         try:
    #             validator_bottom=param_class_validator[1]
    #         except IndexError:
    #             pass
    #         else:
    #             validator.setBottom(validator_bottom)
    #         input_widget.setValidator(validator)
    #     self._parameter_box.layout().addMultiCellWidget(input_widget, param_row, param_row, param_column + 1, param_column + 1 + param_span)
    #     self._parameter_dict[param_id]=input_widget
    #
    #     try:
    #         connect_on_changed=connect_signals[0]
    #     except IndexError:
    #         connect_on_changed=None
    #     if connect_on_changed=="SIGNAL":
    #         exec("QObject.connect(input_widget, SIGNAL('textChanged(const QString &)'), self.%sChanged)" % param_id)
    #     elif connect_on_changed=="PYSIGNAL":
    #         exec("QObject.connect(input_widget, PYSIGNAL('textChanged'), self.%sChanged)" % param_id)
    #     try:
    #         connect_on_return=connect_signals[1]
    #     except IndexError:
    #         connect_on_return=None
    #     if connect_on_return=="SIGNAL":
    #         exec("QObject.connect(input_widget, SIGNAL('returnPressed()'), self.%sPressed)" % param_id)
    #     elif connect_on_return=="PYSIGNAL":
    #         exec("QObject.connect(input_widget, PYSIGNAL('returnPressed'), self.%sPressed)" % param_id)
    #     try:
    #         connect_on_activated=connect_signals[2]
    #     except IndexError:
    #         connect_on_activated=None
    #     if connect_on_activated=="SIGNAL":
    #         exec("QObject.connect(input_widget, SIGNAL('activated(int)'), self.%sActivated)" % param_id)
    #     elif connect_on_activated=="PYSIGNAL":
    #         exec("QObject.connect(input_widget, PYSIGNAL('activated'), self.%sActivated)" % param_id)
    #     try:
    #         connect_on_toggled=connect_signals[3]
    #     except IndexError:
    #         connect_on_toggled=None
    #     if connect_on_toggled=="SIGNAL":
    #         exec("QObject.connect(input_widget, SIGNAL('toggled(bool)'), self.%sToggled)" % param_id)
    #     elif connect_on_toggled=="PYSIGNAL":
    #         exec("QObject.connect(input_widget, PYSIGNAL('toggled'), self.%sToggled)" % param_id)
    #
    #     return input_widget

    #
    # def get_parameter_value(self, param_id):
    #     try:
    #         param=self._parameter_dict[param_id]
    #     except KeyError:
    #         return None
    #     if param.isVisible():
    #         return param.text()
    #     else:
    #         return None

    def setEnabled(self, value):
        super(GphlAcquisitionWidget, self).setEnabled(value)
        for tag in self._widget_data:
            self.set_parameter_enabled(tag, value, warn=False)

    def set_parameter_enabled(self, tag, value, warn=True):
        tt = self._widget_data.get(tag)
        if tt:
            if hasattr(tt[0], 'setEnabled'):
                tt[0].setEnabled(value)
            elif warn:
                logging.getLogger().warning(
                    "%s Widget has no attribute setEnabled" % tag
                )
        elif warn:
            logging.getLogger().warning(
                "%s field not found in GphlAcquisitinoWidget" % tag
            )


    def get_data_object(self):
        return self._data_object


    def populate_widget(self, beam_energies={}, **kw):

        # Dummy object to support _mib
        data_object = self._data_object = GphlAcquisitionData()
        parameter_mib = self._parameter_mib = DataModelInputBinder(data_object)
        widget_data = self._widget_data

        skip_fields = []
        for tag in self.beam_energy_tags[len(beam_energies):]:
            skip_fields.append(tag)
            skip_fields.append(self._get_label_name(tag))
        if not beam_energies:
            skip_fields.append('beam_energies_label')

        for tag, tt in widget_data.items():
            if tag in skip_fields:
                tt[0].hide()
            else:
                widget, w_type, validator, value = tt
                widget.show()

                setattr(data_object, tag, value)
                parameter_mib.bind_value_update(tag, widget, w_type, validator)

        # Passed-in values override defaults
        for tag, val in kw.items():
            self.set_parameter_value(tag, val)

        parameter_mib.init_bindings()

    # def display_energy_widgets(self, energies_dict):
    #     """energies is a role:value ORDERED dictionary"""
    #     parameter_mib = self._parameter_mib
    #     tuples = tuple(energies_dict.items())
    #     for ii, tag in enumerate(self.beam_energy_tags):
    #         label_name = self._get_label_name(tag)
    #         if ii < len(energies_dict):
    #             role, energy = tuples[ii]
    #             setattr(self._data_object, tag, energy)
    #             setattr(self._data_object, label_name,
    #                     "      %s energy:" % role)
    #             parameter_mib.show_field(tag)
    #             parameter_mib.show_field(label_name)
    #         else:
    #             parameter_mib.show_field(tag, False)
    #             parameter_mib.show_field(label_name, False)
    #     if energies_dict:
    #         parameter_mib.show_field('beam_energies_label')
    #     else:
    #         parameter_mib.show_field('beam_energies_label', False)
    #
    #     parameter_mib.init_bindings()

    def get_energy_dict(self):
        """get role:value dict for energies"""
        result = OrderedDict()
        for tag in self.beam_energy_tags:
            if hasattr(self._data_object, tag):
                role = getattr(self._data_object, self._get_label_name(tag))
                result[role] = getattr(self._data_object, tag)
        #
        return result

    # def get_parameter_dict(self):
    #     invalid_fields = self._parameter_mib.validate_all()
    #     result = self._parameter_mib.get_field_values()
    #     for tag in invalid_fields:
    #         del result[tag]
    #     #
    #     return result

    # def get_validation_dict(self):
    #     params={}
    #     for param_id in self.PARAMETERS:
    #         if self._parameter_dict[param_id].hasAcceptableInput():
    #             valid=True
    #         else:
    #             valid=False
    #         params[param_id]=valid
    #     return params

    def set_parameter_value(self, name, value):
        if hasattr(self._data_object, name):
            self._data_object.name = value
            self._parameter_mib._update_widget(name)
        else:
            raise ValueError(
                "GPhL acquisition widget has no parameter named %s" % name
            )

    def _get_label_name(self, name):
        return name + '_label'
