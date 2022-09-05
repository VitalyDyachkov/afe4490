import numpy as np
import matplotlib.pyplot as plt
import re,random

from copy import deepcopy
STEP1_FILE_NAME = 'step1_decimation_data.txt'
STEP2_FILE_NAME = 'step2_average.txt'
STEP3_FILE_NAME = 'step3_move_average.txt'

STEP_OFFSET = 200
DATA_STEP = 100
DECIMATOR = 20
cnt_data = 0
cnt_pics = 0
array_index = []
#функция поиска пика
def FindPeak(array_mid,size, min_height):

    i = 1
    width = 0
    cnt_idx = 0

    global cnt_pics
    global array_index

    while i < size-1:
        if array_mid[i] > min_height and array_mid[i] > array_mid[i-1]:
            width = 1
        while i+width < size and array_mid[i] == array_mid[i+width]:
            width += 1
        if array_mid[i] > array_mid[i + width] and cnt_idx < 15:
            array_index.append(i)
            cnt_pics += 1
            cnt_idx += 1
        else:
            i += width

#входные данные АЦП 500 Гц
input_file = open('data.txt', 'r')
#выходные данные децимации с запятой(для массива в программу)
n_data_f = open('out_point_data.txt', 'w')

cent_data = open('cent_data.txt', 'w')
#выходные данные децимации
w_f = open(STEP1_FILE_NAME, 'w')
#данные после операции вычитания постоянной состовляющей и инверсии
m_f = open(STEP2_FILE_NAME, 'w')
# Скользящее среднее
moveaverage_f = open(STEP3_FILE_NAME, 'w')

# входные данные пересчитанные в Вольты IR
v_adc_f = open('v_ired_data_spo2.txt', 'r')
# входные данные пересчитанные в Вольты RED
red_v_adc_f = open('v_red_data_spo2.txt', 'r')
# выходные данные пересчитанные в Вольты IR с запятой для Excel
rep_v_adc_f = open('replace_v_ired_data_spo2.txt', 'w')
# выходные данные пересчитанные в Вольты RED с запятой для Excel
red_rep_v_adc_f = open('replace_v_red_data_spo2.txt', 'w')

# данные после фильтра
filtred_f = open("filtrd_fdata.txt", 'w')
# данные до обработки
in_digital_f = open("in_dig_data.txt", 'w')

i = 0
step = 10
med = 0
rand_buff = []
v_ir_data = []
v_r_data = []
data_list = []
an_x_data = []
an_data = []

re_data = []

add = 0.0
# #IR заменим точки на запятые в текстовом файле со значениями ацп в Вольтах
# while True:
#     line = v_adc_f.readline()
#     if line != '':
#         v_ir_data.append(float(line))
#     i += 1
#     re_string = line.replace(".", ",", 1)
#     rep_v_adc_f.write(re_string)
#     if not line:
#         v_adc_f.close()
#         rep_v_adc_f.close()
#         i = 0
#         break
# #RED заменим точки на запятые в текстовом файле со значениями ацп в Вольтах
# while True:
#     line = red_v_adc_f.readline()
#     if line != '':
#         v_r_data.append(float(line))
#     i += 1
#     re_string = line.replace(".", ",", 1)
#     red_rep_v_adc_f.write(re_string)
#     if not line:
#         red_rep_v_adc_f.close()
#         red_rep_v_adc_f.close()
#         i = 0
#         break
# STEP0.
while True:
    line = input_file.readline()
    i += 1
    if not line:
        i = 0
        break
    cnt_data += 1
    i = 0
    data_list.append(line.strip())
    cent_data.write(line.strip() + '\n')
    if cnt_data == DATA_STEP * DECIMATOR:
        break
input_file.close()
input_file = open('data.txt', 'r')
# STEP1.
# Decimation
cnt_data = 0
while True:
    line = input_file.readline()
    i += 1
    if not line:
        i = 0
        break
    if i == DECIMATOR:
        cnt_data += 1
        i = 0
        # data_list.append(line.strip())
        w_f.write(line.strip() + '\n')
    if cnt_data == DATA_STEP:
        break
    n_data_f.write(line.strip() + '\n')
input_file.close()
n_data_f.close()
# print(data_list)
w_f.close()
w_f = open(STEP1_FILE_NAME, 'r')
# STEP2.
# Average search
while True:
    one_line = w_f.readline()
    if one_line != '':
        t_med = int(one_line)
        an_x_data.append(t_med)
        med += t_med
    if not one_line:
        print("MED", med)
        med /= len(re.findall(r"[\n']+", open(STEP1_FILE_NAME).read()))
        print("CNT STRING->>", len(re.findall(r"[\n']+", open(STEP1_FILE_NAME).read())))
        print("MEDIANE->>", med)
        print("an_x_data", an_x_data)
        for i in range(len(re.findall(r"[\n']+", open(STEP1_FILE_NAME).read()))):
            line = -1 * (an_x_data[i] - med)
            an_data.append(line)
            re_string = str(line)
            re_string = re_string.replace(".", ",", 1)
            m_f.write(re_string + '\n')

        print("an_data", an_data)
        # STEP3.
        # Move average
        buff = np.arange(len(an_data), dtype=float)
        for i in range(len(an_data)):
            buff = an_data.copy()
        for i in range(len(an_data) - 3):
            buff[i] = buff[i + 1] + buff[i + 2] #+ buff[i + 3]+ buff[i + 4] + buff[i + 5] + buff[i + 6] + buff[i + 7]
        for i in range(len(buff)):
            re_string = str(int(buff[i]))
            re_string = re_string.replace(".", ",", 1)
            moveaverage_f.write(re_string + '\n')
            print(buff[i])
        for i in range(len(buff)):
            add += buff[i]

        print("ADDIDITION=", add)
        mid_value = add / len(buff)
        print("ADDIDITION=", mid_value)

        for i in range(len(array_index)):
            print("IDX->", array_index[i])

        moveaverage_f.close()
        m_f.close()
        w_f.close()

        # for i in range(500):
        #     rand_buff.append(random.randint(-16536, 16536))
        #     in_digital_f.write(str(rand_buff[i]) + '\n')

        # plt.plot(rand_buff)

        dec_buf = []
        # for i in range(500):
        #     if i % 2 == 0:
        #         dec_buf.append(rand_buff[i])
        #         filtred_f.write(str(dec_buf[len(dec_buf) - 1]) + '\n')
        # for i in range(499):
        #     if i == 0:
        #         dec_buf.append(rand_buff[i])
        #     else:
        #         dec_buf.append((rand_buff[i + 1] - rand_buff[i]))
        #     filtred_f.write(str(dec_buf[len(dec_buf) - 1]) + '\n')
        # plt.plot(dec_buf)
        # plt.plot(buff)
        # plt.plot(an_x_data)
        # plt.plot(v_ir_data)
        # plt.plot(v_r_data)
        # plt.plot(moveaverage_f)
        for i in range (1000):
            dec_buf.append(np.sin(0.03 * i))
            in_digital_f.write(str(dec_buf[i]) + '\n')

        # plt.plot(dec_buf)

        for i in range(999):
            if i == 0:
                rand_buff.append(dec_buf[i])
                filtred_f.write(str(rand_buff[i]) + '\n')
            else:
                rand_buff.append((dec_buf[i + 1] - dec_buf[i]))
                filtred_f.write(str(rand_buff[i]) + '\n')
        for i in range(999):
            if i == 0:
                re_data.append(rand_buff[i])
                var = re_data[i]
            else:
                re_data.append(var + rand_buff[i])
                var = re_data[i]
        # plt.plot(rand_buff)
        # plt.plot(re_data)
        # plt.show()
        plt.plot(an_x_data, label="STEP1")
        plt.plot(an_data, label="STEP2")
        plt.plot(buff, label="STEP3")
        plt.legend()
        plt.show()
        in_digital_f.close()
        filtred_f.close()
        # FindPeak(buff, len(buff), mid_value)
        break



