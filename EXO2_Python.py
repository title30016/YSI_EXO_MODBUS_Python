#!/usr/bin/env python
# coding: utf-8

# In[26]:


def parameter_iden(code):
    ParameterCode = [1,2,3,4,5,6,7,10,12,17,18,19,20,21,22,23,28,37,47,48,
     51,52,53,54,95,101,106,108,110,112,145,190,191,193,194,211,212,214,216,218,
    223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241]


    ParameterName = ['Temperature, °C',
                     'Temperature, °F', 
                     'Temperature, °K',
                    'Conductivity, mS/cm',
                    'Conductivity, μS/cm',
                    'Specific Conductance, mS/cm',
                    'Specific Conductance, μS/cm',
                    'TDS, g/L',
                    'Salinity, PPT',
                    'pH, mV',
                    'pH',
                    'ORP, mV',
                    'Pressure, psia',
                    'Pressure, psig',
                    'Depth, m',
                    'Depth, ft',
                    'Battery, V',
                    'Turbidity, NTU',
                    'NH3 (Ammonia), mg/L',
                    'NH4 (Ammonium), mg/L',
                    'Date, DDMMYY',
                    'Date, MMDDYY',
                    'Date, YYMMDD,',
                    'Time, HHMMSS',
                    'TDS, kg/L',
                    'NO3 (Nitrate), mV',
                    'NO3 (Nitrate), mg/L',
                    'NH4 (Ammonium), mV',
                    'TDS, mg/L',
                    'Chloride, mg/L',
                    'Chloride, mV',
                    'TSS, mg/L',
                    'TSS, g/L',
                    'Chlorophyll, ug/L',
                    'Chlorophyll, RFU',
                    'ODO, %Sat',
                    'ODO, mg/L',
                    'ODO, %Sat Local',
                    'BGA-PC, RFU',
                    'BGA-PE, RFU',
                    'Turbidity, FNU',
                    'Turbidity, Raw',
                    'BGA-PC, μg/L',
                    'BGA-PE, μg/L',
                    'fDOM, RFU',
                    'fDOM, QSU',
                    'Wiper Position, V',
                    'External Power, V',
                    'BGA-PC, Raw',
                    'BGA-PE, Raw',
                    'fDOM, Raw',
                    'Chlorophyll, Raw',
                    'Potassium, mV',
                    'Potassium, mg/L',
                    'nLF Conductivity, mS/cm',
                    'nLF Conductivity, μS/cm',
                    'Wiper Peak Current, mA',
                    'Vertical Position, m',
                    'Vertical Position, ft']
    ParameterName = ParameterName[ParameterCode.index(code)]
    return ParameterName


# In[27]:


import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"Device: {port.device}, Description: {port.description}")
    if 'USB' in port.description: COM = port.device


# In[28]:


import serial

# Set the correct serial port (e.g., /dev/ttyUSB0)
serial_port = COM  # Replace with your actual port

try:
    # Open the serial connection
    ser = serial.Serial(port=serial_port, baudrate=9600, timeout=1)

    if ser.is_open:
        print(f"Connection successful on port {serial_port}")
        # Optional: Write a test command or read a response to check communication
        ser.write(b'Hello')  # Replace with a relevant command for your device
        response = ser.read(10)  # Adjust the number of bytes to read
        print(f"Received: {response}")

        # Close the connection
        ser.close()
    else:
        print(f"Failed to open connection on port {serial_port}")

except serial.SerialException as e:
    print(f"Error: {e}")


# In[29]:


#! pip install pymodbus


# In[30]:


#! pip install --upgrade pymodbus


# In[31]:


from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

# Initialize Modbus client
client = ModbusSerialClient(
    port=COM ,       # Your COM port
    baudrate=9600,      # Baud rate
    parity='N',         # No parity
    stopbits=1,         # Stop bits
    bytesize=8,         # Data bits
    timeout=2           # Timeout for the connection
)

# Connect to the Modbus device
if client.connect():
    print("Connection successful on COM14")

    # Attempt to read holding registers (use appropriate function call)
    try:
        # Specify the Modbus address correctly if needed
        result = client.read_holding_registers(128,20, slave=1)  # replace `slave` with correct argument if it differs
        if not result.isError():  # Check if there was an error
            print(f"Received data: {result.registers}")
        else:
            print("Failed to read from device: Error in response")

    except ModbusException as e:
        print(f"Error while reading: {e}")

    # Close the connection
    client.close()
else:
    print("Failed to connect to the Modbus device on COM14")
        
# Extract the first 5 registers for Sonde_ParameterCodeList
sonde_parameter_code_list = result.registers[:15]  # Adjust indices based on the actual structure of your data

print("Sonde Parameter Code List:", sonde_parameter_code_list)
        


# In[ ]:





# In[32]:


import struct
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

# Initialize Modbus client
client = ModbusSerialClient(
    port='COM14',
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=2
)

# Connect to the Modbus device
if client.connect():
    print("Connection successful on COM14")
    
    Value_list = []
    position = 385
    
    for i in sonde_parameter_code_list:
        
        if i != 0:

            try:
                # Read the two registers that store the floating-point value
                result = client.read_holding_registers(position, 2, slave=1)
                if not result.isError():
                    # Combine the two 16-bit registers into a single 32-bit integer
                    high = result.registers[0]  # High 16 bits
                    low = result.registers[1]   # Low 16 bits

                    # Combine into a 32-bit integer
                    combined = (high << 16) + low

                    # Convert the 32-bit integer to a floating-point number
                    float_value = struct.unpack('!f', struct.pack('!I', combined))[0]

                    print(f"Floating-point value: {float_value}")
                    Value_list.append(float_value)
                    position = position+2
                else:
                    print("Failed to read from device: Error in response")

            except ModbusException as e:
                print(f"Error while reading: {e}")

    # Close the connection
    client.close()
else:
    print("Failed to connect to the Modbus device on COM14")


# In[33]:


sonde_parameter_name_list = []

for i in sonde_parameter_code_list:
    if i != 0 :
        sonde_parameter_name_list.append(parameter_iden(i))
sonde_parameter_name_list


# In[34]:


import pandas as pd


# Create a DataFrame
df = pd.DataFrame({
    'Parameter Name': sonde_parameter_name_list,
    'Value': Value_list
})

df


# In[42]:


dict_representation = df.to_dict(orient='records')
print(dict_representation)


# In[ ]:




