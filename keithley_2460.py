import time

class keithley_2460():

    def __init__(self, pyvisa_instr):
        self.ke2460 = pyvisa_instr # this is the pyvisa instrument, rm.open_resource('USB0::0x0466::0x2860::04074562::INSTR')

    def get_all_scpi_list(self):
        function_list = ['CURRent', 'VOLTage', 'RESistance']
        function_1_list = ['CURRent', 'VOLTage']
        result_list = []
        for function in function_list:
            for dict in [self.calculate_dict, self.display_dict, self.sense_dict]:
                for command in dict:
                    time.sleep(0.1)
                    #                    print(command.format(function,"?"))
                    result = (self.ke2460.query(command.format(function, "?"))).rstrip('\r\n')
                    result = " " + result
                    result_list.append(command.format(function, result))
        #                    print(command.format(function, result))
        for function in function_1_list:
            for dict in [self.source_dict]:
                for command in dict:
                    time.sleep(0.1)
                    #                    print(command.format(function,"?"))
                    result = (self.ke2460.query(command.format(function, "?"))).rstrip('\r\n')
                    result = " " + result
                    result_list.append(command.format(function, result))
        #                    print(command.format(function, result))
        for line in range(1, 7):
            for command in self.digital_dict:
                time.sleep(0.1)
                result = (self.ke2460.query(command.format(line, "?"))).rstrip('\r\n')
                result = " " + result
                result_list.append(command.format(line, result))
        #                print(command.format(line, result))
        for dict in [self.display_dict_1, self.format_dict, self.output_dict_1, self.sense_dict_1,
                     self.source_dict_1]:
            for command in dict:
                time.sleep(0.1)
                result = (self.ke2460.query(command.format("?"))).rstrip('\r\n')
                result = " " + result
                result_list.append(command.format(result))
        #                print(command.format(result))
        return result_list

    def get_unique_scpi_list(self):
        unique_scpi_list = []
        inst_settings_list = self.get_all_scpi_list()
        for setting in inst_settings_list:
            if (setting not in self.settings_por_scpi_list):
                unique_scpi_list.append(setting)
        return unique_scpi_list

    sample_settings_smu_list = [ 'SOURce:FUNC VOLT',
                                 'SOURce:VOLT 4.000',
                                 'SOURce:VOLT:ILIM 7.000',
                                 'SENSe:FUNC "CURR"',
                                 'SENSe:CURR:DC:RANG:AUTO ON' ]

    # function is CURRent, RESistance, VOLTage {0}, value is {1}
    calculate_dict = { "CALCulate1:{0}:MATH:FORMat{1}"       : "select math operation to be performed when math operations are enabled: MXB, PERCent, RECiprocal",
                       "CALCulate1:{0}:MATH:MBFactor{1}"     : "select the offset, b, for the y = mx + b operation: valid range is -1e12 to +1e12",
                       "CALCulate1:{0}:MATH:MMFactor{1}"     : "select the scale factor, m, for the y = mx + b math operation: valid range is -1e12 to +1e12",
                       "CALCulate1:{0}:MATH:PERCent{1}"      : "select the reference constant that is used when math operations are set to percent: valid range is -1e12 to +1e12",
                       "CALCulate1:{0}:MATH:STATe{1}"        : "enables or disables math operation: OFF or 0, ON or 1",
                       "CALCulate2:{0}:LIMit1:CLEar:AUTO{1}" : "selects if test result for limit 1 should be cleared automatically or not: OFF or 0, ON or 1",
                       "CALCulate2:{0}:LIMit2:CLEar:AUTO{1}" : "selects if test result for limit 2 should be cleared automatically or not: OFF or 0, ON or 1",
                       "CALCulate2:{0}:LIMit1:LOWer{1}"      : "selects the lower limit 1 for tests: valid range -9.99e11 to 9.99e11",
                       "CALCulate2:{0}:LIMit2:LOWer{1}"      : "selects the lower limit 2 for tests: valid range -9.99e11 to 9.99e11",
                       "CALCulate2:{0}:LIMit1:STATe{1}"      : "enables or disables a limit 1 test on the measurement from the selected measure function: OFF or 0, ON or 1",
                       "CALCulate2:{0}:LIMit2:STATe{1}"      : "enables or disables a limit 2 test on the measurement from the selected measure function: OFF or 0, ON or 1",
                       "CALCulate2:{0}:LIMit1:UPPer{1}"      : "selects the upper limit 1 for a limit test: valid range -9.99e11 to 9.99e11",
                       "CALCulate2:{0}:LIMit2:UPPer{1}"      : "selects the upper limit 2 for a limit test: valid range -9.99e11 to 9.99e11" }

    # line is 1 thru 6 {0}, value is {1}
    digital_dict = { "DIGital:LINE{0}:MODE{1}"  : "selects the mode of the digital I/O line: valid values are IN, OUT, OPENdrain, MASTer, ACCeptor",
                     "DIGital:LINE{0}:STATe{1}" : "sets a digital I/O line high or low when the line is set for digital control: 0, 1" }

    # function is CURRent, RESistance, VOLTage {0}, value is {1}
    display_dict   = { "DISPlay:{0}:DIGits{1}" : "select the number of digits that are displayed for measurements on the front panel: valid values are 3, 4, 5, 6" }

    # value is {0}
    display_dict_1 = { "DISPlay:LIGHt:STATe{0}"    : "select the light output level of the front-panel display: valid values are ON100, ON75, ON50, ON25, OFF and BLACkout",
                       "DISPlay:READing:FORMat{0}" : "select the format that is used to display measurement readings on the front-panel: valid vaules are EXPonent, k, m, or u" }

    # value is {0}
    format_dict = { "FORMat:ASCii:PRECision{0}" : "select the precision (number of digits) for all numbers returned in the ASCII format: valid values are 0 for auto, 1 thru 16",
                    "FORMat:BORDer{0}"          : "select the byte order for the IEEE-754 binary formats: valid values are NORMal and SWAPped",
                    "FORMat{0}"                 : "select the data format that is used when transferring readings over the remote interface: valid values are ASCii, REAL, SREal" }

    # function is CURRent or VOLTage {0}, value is {1}
    output_dict = { "OUTPut1:{0}:SMODe{1}" : "select the state of the source when the output is turned off : valid values are NORMal, HIMPedance, ZERO, GUARd" }

    # value is {0}
    output_dict_1 = { "OUTPut1:STATe{0}" : "enables or disables the source output: OFF or 0, ON or 1" }

    # function is CURRent, RESistance, VOLTage {0}, value is {1}
    sense_dict = { "{0}:AVERage:COUNt{1}"     : "selects the number of measurements that are averaged when filtering is enabled: valid values 1 thru 100",
                   "{0}:AVERage{1}"           : "enables or disables the averaging filter for measurements of the selected function: OFF or 0, ON or 1",
                   "{0}:AVERage:TCONtrol{1}"  : "selects the type of averaging filter that is used for the selected measure function: valid values are REPeat or MOVing",
                   "{0}:AZERo{1}"             : "enables or disables automatic updates to the internal reference measurements (autozero): OFF or 0, ON or 1",
                   "{0}:DELay:USER1{1}"       : "select a user-defined 1 delay that you can use in the trigger model: valid value is 0, 167ns thru 10,000s",
                   "{0}:DELay:USER2{1}"       : "select a user-defined 2 delay that you can use in the trigger model: valid value is 0, 167ns thru 10,000s",
                   "{0}:DELay:USER3{1}"       : "select a user-defined 3 delay that you can use in the trigger model: valid value is 0, 167ns thru 10,000s",
                   "{0}:DELay:USER4{1}"       : "select a user-defined 4 delay that you can use in the trigger model: valid value is 0, 167ns thru 10,000s",
                   "{0}:DELay:USER5{1}"       : "select a user-defined 5 delay that you can use in the trigger model: valid value is 0, 167ns thru 10,000s",
                   "{0}:NPLCycles{1}"         : "select the time that the input signal is measured for the selected function: valid values are 0.01 thru 10",
                   "{0}:OCOMpensated{1}"      : "enables or disables offset compensation: OFF or 0, ON or 1",
                   "{0}:RANGe:AUTO{1}"        : "select manual or automatical range for the selected measure: OFF or 0, ON or 1",
                   "{0}:RANGe:AUTO:LLIMit{1}" : "select the lower limit for measurements when the range is automatic: valid values are 1e-6 to 5A, 0.2 to 20V, 2 to 20e6 Ohm",
                   "{0}:RANGe:AUTO:ULIMit{1}" : "select the upper limit for measurements when the range is automatic: valid values are 1e-6 to 7A, 0.2 to 100V, 2 to 200e6 Ohm",
                   "{0}:RANGe{1}"             : "select the positive full-scale measure range: valid values are 1e-6 to 7A, 0.2 to 100V, 2 to 200e6 Ohm",
                   "{0}:RELative{1}"          : "select relative offset value: valid values are -7.35 to 7.35A, -105 to 105V, -210e6 to 210e6 Ohm",
                   "{0}:RELative:STATe{1}"    : "enables or disables the application of a relative offset value to the measurement: OFF or 0, ON or 1",
                   "{0}:RSENse{1}"            : "selects local (2-wire) or remote (4-wire) sensing: valid values are OFF or 0 (for 2 wire), ON or 1 (for 4 wire)" }

    # value is {0}
    sense_dict_1 = { "COUNt{0}"             : "select the number of measurements to make: valid values are 1 to 300,000",
                     "FUNCtion{0}"          : "selects the active measure function: Valid values are VOLTage, CURRent, RESistance" }

    # function is CURRent or VOLTage {0}, value is {1}
    source_dict = { "SOURce1:{0}:DELay{1}"            : "select the source delay: valid values are 0 thru 4 seconds",
                    "SOURce1:{0}:DELay:AUTO{1}"       : "enables or disables the automatic delay that occurs when the source is turned on: OFF or 0, ON or 1",
                    "SOURce1:{0}:DELay:USER1{1}"      : "select a user-defined 1 delay that you can use in the trigger model: valid values are 0 to 10,000",
                    "SOURce1:{0}:DELay:USER2{1}"      : "select a user-defined 2 delay that you can use in the trigger model: valid values are 0 to 10,000",
                    "SOURce1:{0}:DELay:USER3{1}"      : "select a user-defined 3 delay that you can use in the trigger model: valid values are 0 to 10,000",
                    "SOURce1:{0}:DELay:USER4{1}"      : "select a user-defined 4 delay that you can use in the trigger model: valid values are 0 to 10,000",
                    "SOURce1:{0}:DELay:USER5{1}"      : "select a user-defined 5 delay that you can use in the trigger model: valid values are 0 to 10,000",
                    "SOURce1:{0}:HIGH:CAPacitance{1}" : "enables or disables high-capacitance mode: OFF or 0, ON or 1",
                    "SOURce1:{0}{1}"                  : "select a fixed amplitude for the selected source function: valid values are -7.35A to 7.35A, or 100mV to 105V",
                    "SOURCE1:{0}:RANGe{1}"            : "select the range for the source for the selected source function: valid values are -7.35A to 7.35A, or -105 to 105V",
                    "SOURce1:{0}:RANGe:AUTO{1}"       : "select if range is manual or automatic for the selected source function: OFF or 0, ON or 1",
                    "SOURce1:{0}:READ:BACK{1}"        : "select if the instrument records the measured source value or the configured source value: OFF or 0, ON or 1",
#                    "SOURce1:LIST:{0}{1}"             : "select a list of custom values for a sweep: -7.35A to 7.35A, or -105 to 105V",
                    "{0}:UNIT{1}"                     : "select the units of measurement that are displayed on the front panel and reading buffer: valid values are OHM, WATT, AMP, VOLT"
                    }

    # value is {0}
    source_dict_1 = { "SOURce1:CURRent:VLIMit{0}"     : "selects the source limit for voltage measurement: valid values are 0.2V to 105V",
                      "SOURce1:VOLTage:ILIMit{0}"     : "selects the source limit for current measurement: valid values are 1e-6 to 7.35A",
                      "SOURce1:FUNCtion{0}"           : "select source function: valid values are VOLTage or CURRent",
                      "SOURce1:VOLTage:PROTection{0}" : "select the overvoltage protection setting of the source output: valid values are PROT2, thru PROT180" }

    # value is {0}
    status_dict = { "STATus:OPERation:ENABle{0}"    : "select the contents of the questionable event enable register of the status model: valid values are 0 to 65535",
                    "STATus:QUEStionable:ENABle{0}" : "select the contents of the questionable event enable register of the status mode: valid values are 0 to 65535" }

    settings_por_scpi_list = [ 'CALCulate2:CURRent:LIMit1:LOWer -1',
                               'CALCulate2:CURRent:LIMit1:CLEar:AUTO 1',
                               'CALCulate2:CURRent:LIMit2:CLEar:AUTO 1',
                               'CALCulate1:CURRent:MATH:PERCent 1',
                               'CALCulate2:CURRent:LIMit2:LOWer -1',
                               'CALCulate2:CURRent:LIMit2:STATe 0',
                               'CALCulate2:CURRent:LIMit2:UPPer 1',
                               'CALCulate2:CURRent:LIMit1:UPPer 1',
                               'CALCulate1:CURRent:MATH:MMFactor 1',
                               'CALCulate1:CURRent:MATH:STATe 0',
                               'CALCulate1:CURRent:MATH:FORMat PERC',
                               'CALCulate2:CURRent:LIMit1:STATe 0',
                               'CALCulate1:CURRent:MATH:MBFactor 0',
                               'DISPlay:CURRent:DIGits 5',
                               'CURRent:AZERo 1',
                               'CURRent:NPLCycles 1',
                               'CURRent:OCOMpensated 0',
                               'CURRent:AVERage:TCONtrol REP',
                               'CURRent:DELay:USER3 0',
                               'CURRent:RANGe:AUTO:ULIMit 1E-05',
                               'CURRent:RELative 0',
                               'CURRent:DELay:USER5 0',
                               'CURRent:DELay:USER1 0',
                               'CURRent:AVERage:COUNt 10',
                               'CURRent:RSENse 0',
                               'CURRent:RANGe:AUTO 1',
                               'CURRent:DELay:USER4 0',
                               'CURRent:DELay:USER2 0',
                               'CURRent:RANGe 1E-06',
                               'CURRent:RELative:STATe 0',
                               'CURRent:AVERage 0',
                               'CURRent:RANGe:AUTO:LLIMit 1E-06',
                               'CALCulate2:VOLTage:LIMit1:LOWer -1',
                               'CALCulate2:VOLTage:LIMit1:CLEar:AUTO 1',
                               'CALCulate2:VOLTage:LIMit2:CLEar:AUTO 1',
                               'CALCulate1:VOLTage:MATH:PERCent 1',
                               'CALCulate2:VOLTage:LIMit2:LOWer -1',
                               'CALCulate2:VOLTage:LIMit2:STATe 0',
                               'CALCulate2:VOLTage:LIMit2:UPPer 1',
                               'CALCulate2:VOLTage:LIMit1:UPPer 1',
                               'CALCulate1:VOLTage:MATH:MMFactor 1',
                               'CALCulate1:VOLTage:MATH:STATe 0',
                               'CALCulate1:VOLTage:MATH:FORMat PERC',
                               'CALCulate2:VOLTage:LIMit1:STATe 0',
                               'CALCulate1:VOLTage:MATH:MBFactor 0',
                               'DISPlay:VOLTage:DIGits 5',
                               'VOLTage:AZERo 1',
                               'VOLTage:NPLCycles 1',
                               'VOLTage:OCOMpensated 0',
                               'VOLTage:AVERage:TCONtrol REP',
                               'VOLTage:DELay:USER3 0',
                               'VOLTage:RANGe:AUTO:ULIMit 2',
                               'VOLTage:RELative 0',
                               'VOLTage:DELay:USER5 0',
                               'VOLTage:DELay:USER1 0',
                               'VOLTage:AVERage:COUNt 10',
                               'VOLTage:RSENse 0',
                               'VOLTage:RANGe:AUTO 1',
                               'VOLTage:DELay:USER4 0',
                               'VOLTage:DELay:USER2 0',
                               'VOLTage:RANGe 0.2',
                               'VOLTage:RELative:STATe 0',
                               'VOLTage:AVERage 0',
                               'VOLTage:RANGe:AUTO:LLIMit 0.2',
                               'CALCulate2:RESistance:LIMit1:LOWer -1',
                               'CALCulate2:RESistance:LIMit1:CLEar:AUTO 1',
                               'CALCulate2:RESistance:LIMit2:CLEar:AUTO 1',
                               'CALCulate1:RESistance:MATH:PERCent 1',
                               'CALCulate2:RESistance:LIMit2:LOWer -1',
                               'CALCulate2:RESistance:LIMit2:STATe 0',
                               'CALCulate2:RESistance:LIMit2:UPPer 1',
                               'CALCulate2:RESistance:LIMit1:UPPer 1',
                               'CALCulate1:RESistance:MATH:MMFactor 1',
                               'CALCulate1:RESistance:MATH:STATe 0',
                               'CALCulate1:RESistance:MATH:FORMat PERC',
                               'CALCulate2:RESistance:LIMit1:STATe 0',
                               'CALCulate1:RESistance:MATH:MBFactor 0',
                               'DISPlay:RESistance:DIGits 5',
                               'RESistance:AZERo 1',
                               'RESistance:NPLCycles 1',
                               'RESistance:OCOMpensated 0',
                               'RESistance:AVERage:TCONtrol REP',
                               'RESistance:DELay:USER3 0',
                               'RESistance:RANGe:AUTO:ULIMit 2E+08',
                               'RESistance:RELative 0',
                               'RESistance:DELay:USER5 0',
                               'RESistance:DELay:USER1 0',
                               'RESistance:AVERage:COUNt 10',
                               'RESistance:RSENse 0',
                               'RESistance:RANGe:AUTO 1',
                               'RESistance:DELay:USER4 0',
                               'RESistance:DELay:USER2 0',
                               'RESistance:RANGe 2E+08',
                               'RESistance:RELative:STATe 0',
                               'RESistance:AVERage 0',
                               'RESistance:RANGe:AUTO:LLIMit 2',
                               'SOURCE1:CURRent:RANGe 1E-06',
                               'SOURce1:CURRent:DELay:USER2 0',
                               'SOURce1:CURRent:DELay:USER3 0',
                               'SOURce1:CURRent:HIGH:CAPacitance 0',
                               'SOURce1:CURRent:DELay:AUTO 1',
                               'SOURce1:CURRent:DELay:USER4 0',
                               'SOURce1:CURRent:READ:BACK 1',
                               'SOURce1:CURRent:DELay 0.001',
                               'CURRent:UNIT AMP',
                               'SOURce1:CURRent 0',
                               'SOURce1:CURRent:RANGe:AUTO 1',
                               'SOURce1:CURRent:DELay:USER1 0',
                               'SOURce1:CURRent:DELay:USER5 0',
                               'SOURce1:LIST:CURRent  ',
                               'SOURCE1:VOLTage:RANGe 0.2',
                               'SOURce1:VOLTage:DELay:USER2 0',
                               'SOURce1:VOLTage:DELay:USER3 0',
                               'SOURce1:VOLTage:HIGH:CAPacitance 0',
                               'SOURce1:VOLTage:DELay:AUTO 1',
                               'SOURce1:VOLTage:DELay:USER4 0',
                               'SOURce1:VOLTage:READ:BACK 1',
                               'SOURce1:VOLTage:DELay 1E-03',
                               'VOLTage:UNIT VOLT',
                               'SOURce1:VOLTage 0',
                               'SOURce1:VOLTage:RANGe:AUTO 1',
                               'SOURce1:VOLTage:DELay:USER1 0',
                               'SOURce1:VOLTage:DELay:USER5 0',
                               'SOURce1:LIST:VOLTage  ',
                               'DIGital:LINE1:STATe 1',
                               'DIGital:LINE1:MODE DIG,IN',
                               'DIGital:LINE2:STATe 1',
                               'DIGital:LINE2:MODE DIG,IN',
                               'DIGital:LINE3:STATe 1',
                               'DIGital:LINE3:MODE DIG,IN',
                               'DIGital:LINE4:STATe 1',
                               'DIGital:LINE4:MODE DIG,IN',
                               'DIGital:LINE5:STATe 1',
                               'DIGital:LINE5:MODE DIG,IN',
                               'DIGital:LINE6:STATe 1',
                               'DIGital:LINE6:MODE DIG,IN',
                               'DISPlay:READing:FORMat PREF',
                               'DISPlay:LIGHt:STATe ON50',
                               'FORMat ASC',
                               'FORMat:ASCii:PRECision 0',
                               'FORMat:BORDer SWAP',
                               'OUTPut1:STATe 0',
                               'COUNt 1',
                               'FUNCtion "CURR:DC"',
                               'SOURce1:VOLTage:ILIMit 0.000105,
                               'SOURce1:FUNCtion VOLT',
                               'SOURce1:CURRent:VLIMit 7.35',
                               'SOURce1:VOLTage:PROTection NONE' ]
