import numpy as np

def __norm_and_resample_time_vect(f_hz, original_time_vect):
    time_vect_norm = (original_time_vect - original_time_vect[0])/1000
    T = time_vect_norm[-1]
    F = f_hz
    dt = 1/F
    time_vect_resampled = np.arange(0, T + dt, dt)
    return time_vect_resampled

def __resample_data(data, time_vect):
    import scipy.signal as sc
    resampled_data, _  = sc.resample(data, len(time_vect), time_vect)
    return resampled_data

def read_wii_board_data(file_path):
    import pandas as pd
    data = pd.read_csv(file_path, ' ')
    wii_data = {
        "timeInMs": data.iloc[:, 0].tolist(),
        "topLeftForceInKg": data.iloc[:, 1].tolist(),
        "topRightForceInKg": data.iloc[:, 2].tolist(),
        "bottomLeftForceInKg": data.iloc[:, 3].tolist(),
        "bottomRightForceInKg": data.iloc[:, 4].tolist(),
        "copX": data.iloc[:, 5].tolist(),
        "copY": data.iloc[:, 6].tolist(),
        "totalForceInKg": data.iloc[:, 7].tolist()
    }

    f_hz = 100
    time_vect_resampled = __norm_and_resample_time_vect(f_hz, original_time_vect=np.array(wii_data["timeInMs"]))
    cop_x_resampled = __resample_data(np.array(wii_data["copX"]), time_vect_resampled)
    cop_y_resampled = __resample_data(np.array(wii_data["copY"]), time_vect_resampled)

    wii_data["resampled"] = {
        "fHz": f_hz,
        "timeInSec": time_vect_resampled.tolist(),
        "copX": cop_x_resampled.tolist(),
        "copY": cop_y_resampled.tolist()
    }
    
    return wii_data


if __name__ == "__main__":
    import json
    file_path = 'C:\\Users\\bohdank\\Desktop\\b.csv'
    data = read_wii_board_data(file_path)
    print(json.dumps(data))

    import matplotlib.pyplot as plt
    plt.plot(data["copX"], data["copY"], color='r', marker='o', linestyle='--')
    plt.plot(data["resampledCopX"], data["resampledCopY"], color='b', marker='o', linestyle='--')
    plt.legend(['original (mean F = 90 Hz)', 'resampled (F = 100 Hz)'])
    plt.show()