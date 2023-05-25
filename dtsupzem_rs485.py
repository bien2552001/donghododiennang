import minimalmodbus
import serial
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
import json

# Set up requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

while True:
    # Set up connection to the Pzem-017
    instrument1 = minimalmodbus.Instrument('COM6', 1)
    instrument1.serial.baudrate = 9600
    instrument1.serial.bytesize = 8
    instrument1.serial.parity = serial.PARITY_NONE
    instrument1.serial.stopbits = 2
    instrument1.serial.timeout = 1
    instrument1.address = 1
    instrument1.mode = minimalmodbus.MODE_RTU
    instrument1.clear_buffers_before_each_transaction = True

    # Read Pzem-017
    voltage = instrument1.read_register(0x0000, number_of_decimals=2, functioncode=4, signed=True)
    time.sleep(0.1)
    current = instrument1.read_register(0x0001, number_of_decimals=2, functioncode=4, signed=True)
    time.sleep(0.1)
    power_low = instrument1.read_register(0x0002, functioncode=4, signed=True)
    time.sleep(0.1)
    power_high = instrument1.read_register(0x0003, functioncode=4, signed=True)
    power = ((power_high << 16) + power_low)*0.1
    time.sleep(0.1)
    energy_low = instrument1.read_register(0x0004, functioncode=4, signed=True)
    time.sleep(0.1)
    energy_high = instrument1.read_register(0x0005, functioncode=4, signed=True)
    time.sleep(0.1)
    energy = (energy_high << 16) + energy_low
    time.sleep(1)


    # Set up connection to the DTSU666
    instrument2 = minimalmodbus.Instrument('COM6', 5)
    instrument2.serial.baudrate = 9600
    instrument2.serial.bytesize = 8
    instrument2.serial.parity = serial.PARITY_NONE
    instrument2.serial.stopbits = 1
    instrument2.serial.timeout = 0.5
    instrument2.address = 5
    instrument2.mode = minimalmodbus.MODE_RTU
    instrument2.clear_buffers_before_each_transaction = True


    ##Read DTSU666
    # Điện năng tiêu thụ 
    A_imp = round(instrument2.read_float(0x401E, functioncode=3), 2)
    A_exp = round(instrument2.read_float(0x4028, functioncode=3), 2)
    A_sum = A_imp + A_exp
    #  Điện năng phản kháng Q
    Q1= round(instrument2.read_float(0x4032, functioncode=3), 2)
    Q2= round(instrument2.read_float(0x403C, functioncode=3), 2)
    Q3 = round(instrument2.read_float(0x4046, functioncode=3), 2)
    Q4 = round(instrument2.read_float(0x4050, functioncode=3), 2)
    # Điện áp dây
    Uab = round(instrument2.read_float(0x2000, functioncode=3)/10, 2)
    Ubc = round(instrument2.read_float(0x2002, functioncode=3)/10, 2)
    Uca = round(instrument2.read_float(0x2004, functioncode=3)/10, 2)
    # Điện áp pha 
    Ua = round(instrument2.read_float(0x2006, functioncode=3)/10, 2)
    Ub = round(instrument2.read_float(0x2008, functioncode=3)/10, 2)
    Uc = round(instrument2.read_float(0x200A, functioncode=3)/10, 2)
    # Dòng điện pha 
    Ia = round(instrument2.read_float(0x200C, functioncode=3)/1000, 2)
    Ib = round(instrument2.read_float(0x200E, functioncode=3)/1000, 2)
    Ic = round(instrument2.read_float(0x2010, functioncode=3)/1000, 2)
    # Công suất tiêu thụ pha 
    Pft = round(instrument2.read_float(0x2012, functioncode=3)/10000, 2)
    Pfa = round(instrument2.read_float(0x2014, functioncode=3)/10000, 2)
    Pfb = round(instrument2.read_float(0x2016, functioncode=3)/10000, 2)
    Pfc = round(instrument2.read_float(0x2018, functioncode=3)/10000, 2)
    # Công suất phản kháng pha 
    Qft = round(instrument2.read_float(0x201A, functioncode=3)/10000, 2)
    Qfa = round(instrument2.read_float(0x201C, functioncode=3)/10000, 2)
    Qfb = round(instrument2.read_float(0x201E, functioncode=3)/10000, 2)
    Qfc = round(instrument2.read_float(0x2020, functioncode=3)/10000, 2)
    # Hệ số công suất pha 
    Cosft = round(instrument2.read_float(0x202A, functioncode=3)/1000, 2)
    Cosfa = round(instrument2.read_float(0x202C, functioncode=3)/1000, 2)
    Cosfb = round(instrument2.read_float(0x202E, functioncode=3)/1000, 2)
    Cosfc = round(instrument2.read_float(0x2030, functioncode=3)/1000, 2)
    # Tần số 
    Hz = round(instrument2.read_float(0x2044, functioncode=3)/100, 2)

    # Hiển thị dữ liệu PZEM017
    print('____________________________________Pzem-017_________________________________')
    print('Giá trị điện áp DC là: {0:.2f} V'.format(voltage))
    print('Giá trị dòng điện là: {0:.2f} A'.format(current))
    print('Giá trị công suất là: {0:.2f} W'.format(power))
    print('Giá trị điện năng là: {0:.2f} Wh'.format(energy))

    # Hiển thị dữ liệu DTSU666
    print("_____________Chint DTSU666 Modbus Data________________")
    # Điện năng tiêu thụ 
    print('A_sum: {0:.2f} kWh'.format(A_sum))
    print('A_imp: {0:.2f} kWh'.format(A_imp))
    print('A_exp: {0:.2f} kWh'.format(A_exp))
    # Điện năng phản kháng Q
    print('Q1: {0:.2f} kVArh'.format(Q1))
    print('Q2: {0:.2f} kVArh'.format(Q2))
    print('Q2: {0:.2f} kVArh'.format(Q3))
    print('Q4: {0:.2f} kVArh'.format(Q4))
    # Điện áp dây
    print('Uab: {0:.2f} V'.format(Uab))
    print('Ubc: {0:.2f} V'.format(Ubc))
    print('Uca: {0:.2f} V'.format(Uca))
    # Điện áp pha 
    print('Ua: {0:.2f} V'.format(Ua))
    print('Ub: {0:.2f} V'.format(Ub))
    print('Uc: {0:.2f} V'.format(Uc))
    # Dòng điện pha 
    print('Ia: {0:.2f} A'.format(Ia))
    print('Ib: {0:.2f} A'.format(Ib))
    print('Ic: {0:.2f} A'.format(Ic))
    # Công suất tiêu thụ pha 
    print('Pft: {0:.2f} kW'.format(Pft))
    print('Pfa: {0:.2f} kW'.format(Pfa))
    print('Pfb: {0:.2f} kW'.format(Pfb))
    print('Pfc: {0:.2f} kW'.format(Pfc))
    # Công suất phản kháng pha
    print('Qft: {0:.2f} kVAr'.format(Qft))
    print('Qfa: {0:.2f} kVAr'.format(Qfa))
    print('Qfb: {0:.2f} kVAr'.format(Qfb))
    print('Qfc: {0:.2f} kVAr'.format(Qfc))
    # Hệ số công suất pha 
    print('Cosft: {0:.2f}'.format(Cosft))
    print('Cosfa: {0:.2f}'.format(Cosfa))
    print('Cosfb: {0:.2f}'.format(Cosfb))
    print('Cosfc: {0:.2f}'.format(Cosfc))
    # Tần số
    print('Hz: {0:.2f} Hz'.format(Hz))

    # Chờ 1s
    time.sleep(1)
    #--------------------------------- Post dữ liệu---------------------- 

     # dữ liệu bạn muốn gửi
    dtsu666_data = {
        'A_sum': A_sum,
        'A_imp': A_imp,
        'A_exp': A_exp,
        'Q1': Q1,
        'Q2': Q2,
        'Q3': Q3,
        'Q4': Q4,
        'Uab': Uab,
        'Ubc': Ubc,
        'Uca': Uca,
        'Ua': Ua,
        'Ub': Ub,
        'Uc': Uc,
        'Ia': Ia,
        'Ib': Ib,
        'Ic': Ic,
        'Pft': Pft,
        'Pfa': Pfa,
        'Pfb': Pfb,
        'Pfc': Pfc,
        'Qft': Qft,
        'Qfa': Qfa,
        'Qfbt': Qfb,
        'Qfc': Qfc,
        'Cosft': Cosft,
        'Cosfa': Cosfa,
        'Cosfb': Cosfb,
        'Cosfc': Cosfc,
        'Hz': Hz
    }

    pzem017_data ={
        'U1':voltage,
        'I1':current,
        'P1':power,
        'A1':energy
    }
    # gửi yêu cầu POST đến máy chủ web với dữ liệu
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    # ------------POST DTSU666-----------
    response = requests.post(url='https://localhost:5001/dtsu666', json=dtsu666_data, verify=False)
    # # ------------POST PZEM017-----------
    response = requests.post(url='https://localhost:5001/pzem017', json=pzem017_data, verify=False)
    # Đo đồng hồ DTSU666 sau 10s
    time.sleep(5)