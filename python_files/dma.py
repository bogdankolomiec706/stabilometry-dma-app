import subprocess
import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd

from dfa_wrapper import get_log_log_plot_bending_point, calculate_alpha_exp, get_log_log_plot_bending_point_with_debug

def get_curr_path():
    import os
    current_path = f"{os.getcwd()}\\resources\\app\\python_files"
    if os.path.isdir(current_path) == False:
        current_path = f"{os.getcwd()}\\python_files"
    # return current_path
    import pathlib
    return pathlib.Path(__file__).parent

current_path = get_curr_path()

def calc_scaling_exponent(log_n, log_F):
    (_, index) = get_log_log_plot_bending_point(log_n, log_F)
    (alpha, b) = __calc_scaling_exponent(log_n, log_F, index)
    return (alpha, b, index)


def __calc_scaling_exponent(log_n, log_F, index):
    return calculate_alpha_exp(log_n, log_F, index)


def __exract_vectors_from_dma_data(data: str):
    rows = data.split('\n')
    array = [__row_to_float_array(row) for row in rows if ',' in row]
    log_n = np.array([row[0] for row in array])
    log_F = np.array([row[1] for row in array])
    return (log_n, log_F)


def __exract_vectors_from_direct_dma_data(data: str):
    rows = data.split('\n')
    array = [__row_to_float_array(row) for row in rows if ',' in row]
    angle_in_rads = np.array([row[1] for row in array])
    log_n = np.array([row[2] for row in array])
    log_F = np.array([row[3] for row in array])
    return (angle_in_rads, log_n, log_F)


def __row_to_float_array(row):
    return [float(el) for el in row.split(',')]


def __execute_program_on_file(cmd, data_path):
    cmd = "{} {}".format(cmd, data_path)
    out = subprocess.getoutput(cmd)
    (data, metadata) = out.split('Input')
    return __exract_vectors_from_dma_data(data)


def dma_d2(x_vector, y_vector):
    data_file_path = f"{current_path}\\temp_data.csv"
    np_array = np.column_stack((x_vector, y_vector))
    df = pd.DataFrame(np_array)
    df.transpose()
    df.to_csv(data_file_path, index=False, header=False)

    cmd = f"{current_path}\\2d_DMA0.exe {data_file_path}"
    out = subprocess.getoutput(cmd)
    (data, metadata) = out.split('Input')
    return __exract_vectors_from_dma_data(data)


def dma_directed(x_vector, y_vector):
    data_file_path = f"{current_path}\\temp_data.csv"
    np_array = np.column_stack((x_vector, y_vector))
    df = pd.DataFrame(np_array)
    df.transpose()
    df.to_csv(data_file_path, index=False, header=False)
    cmd = f"{current_path}\\direcDMA0.exe -c 1 2 -b 64 {data_file_path}"
    out = subprocess.getoutput(cmd)
    (data, metadata) = out.split('Input')
    return __exract_vectors_from_direct_dma_data(data)


def exponent_for_angle(x_vector, y_vector):
    (angle_in_rads, log_n, log_F) = dma_directed(x_vector, y_vector)
    unique_angle_vector = np.unique(angle_in_rads)

    alpha_vector = []
    for angle in unique_angle_vector:
        index_mask = angle_in_rads == angle
        angle_log_n = log_n[index_mask]
        angle_log_F = log_F[index_mask]
        (alpha, _, _) = calc_scaling_exponent(angle_log_n, angle_log_F)
        alpha_vector.append(alpha)

    return (unique_angle_vector, alpha_vector)
