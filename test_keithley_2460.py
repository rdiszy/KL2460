import pyvisa

rm = pyvisa.ResourceManager()
#print(rm.list_resources())
smu = keithley_2460(rm.open_resource('USB0::0x0346::0x2570::4560771233::INSTR'))
#smu.ke2460.write('*RST')
time.sleep(2)
# get_unique_scpi_list is a list of SCPI commands which are different from Power-On values
print(smu.get_unique_scpi_list())
