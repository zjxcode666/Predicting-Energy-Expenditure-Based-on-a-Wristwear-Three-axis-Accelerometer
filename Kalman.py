import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
# import xlwt
out_root = './kalman_result'
os.makedirs(out_root, exist_ok= True)

def kalman(ADC_Value, Q, R, Accumulated_Error, kalman_adc_old, SCOPE):
    if (abs(ADC_Value-kalman_adc_old)/SCOPE > 0.25):
        Old_Input = ADC_Value*0.382 + kalman_adc_old*0.618
    else:
        Old_Input = kalman_adc_old
    Old_Error_All = (Accumulated_Error**2 + Q**2)**(1/2)
    H = Old_Error_All**2/(Old_Error_All**2 + R**2)
    kalman_adc = Old_Input + H * (ADC_Value - Old_Input)
    Accumulated_Error = ((1 - H)*Old_Error_All**2)**(1/2)
    kalman_adc_old = kalman_adc
    return kalman_adc, kalman_adc_old, Accumulated_Error


def kalman_process(datareult, length):
    Q = 0.00001
    R = 0.00002
    Accumulated_Error = 1
    kalman_adc_old = 1
    SCOPE = 50
    adcresult = []
    for j in range(0, length - 1):
        kalman_adc, kalman_adc_old, Accumulated_Error = kalman(datareult[j], Q, R, Accumulated_Error, kalman_adc_old, SCOPE)
        adcresult.append(kalman_adc)
    return adcresult

def process_data(data_path):
    file_name = os.path.basename(data_path)
    datareult1 = []
    datareult2 = []
    datareult3 = [] 
    datareult4 = []
    datareult5 = []
    i= 0
    file = open(data_path)
    for line in file.readlines():
        curLine = line.strip().split("	")
        if i != 0:
            datareult1.append(curLine[0])
            datareult2.append(float(curLine[1]))  
            datareult3.append(float(curLine[2]))  
            datareult4.append(float(curLine[3])) 
            datareult5.append(float(curLine[4]))  
        i=i+1

    s = np.linspace(1,i,i-1)
    datareult_all = [datareult2, datareult3, datareult4, datareult5]
    adcresult_all = [kalman_process(x, i) for x in datareult_all]
    adcresult2, adcresult3, adcresult4, adcresult5 = adcresult_all
    # txt
    file_path = os.path.join(out_root, file_name)
    file_write = open(file_path, 'w')
    row0 = [u'time', u'acc_x', u'acc_y', u'acc_z', u'acc_vm']
    file_write.write('\t'.join(row0) + '\n')
    for i in range(len(datareult1)):
        row = [datareult1[i], adcresult2[i], adcresult3[i], adcresult4[i], adcresult5[i]]
        row = [str(x) for x in row]
        file_write.write('\t'.join(row) + '\n')
    file_write.close()
    # CSV 
    value = [ [datareult1[i], adcresult2[i], adcresult3[i], adcresult4[i], adcresult5[i]] for i in range(len(datareult1))]
    pd1 = pd.DataFrame(value, columns=row0)
    pd1.to_csv(os.path.join(out_root, file_name.split('.')[0] + '.csv'))


  
    plt.figure(figsize=(50,10))
    plt.plot(adcresult2[:1000],'r',lw='2')
    plt.plot(datareult2[:1000],'y')
    plt.savefig(os.path.join(out_root, file_name.split('.')[0] +'fig2.png'))
    plt.figure(figsize=(50,10))
    plt.plot(adcresult3[:1000],'r',lw='2')
    plt.plot(datareult3[:1000],'y')
    plt.savefig(os.path.join(out_root, file_name.split('.')[0] +'fig3.png'))
    plt.figure(figsize=(50,10))
    plt.plot(adcresult4[:1000],'r',lw='2')
    plt.plot(datareult4[:1000],'y')
    plt.savefig(os.path.join(out_root, file_name.split('.')[0] +'fig4.png'))
    plt.figure(figsize=(50,10))
    plt.plot(adcresult5[:1000],'r',lw='2')
    plt.plot(datareult5[:1000],'y')
    plt.savefig(os.path.join(out_root, file_name.split('.')[0] +'fig5.png'))
if __name__ == '__main__':
    file_root = './data'
    file_list = os.listdir(file_root)
    for file_name in file_list:
        process_data(os.path.join(file_root, file_name))