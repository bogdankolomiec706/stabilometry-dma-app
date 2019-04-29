import json
import dma
import wii_board_data_reader as wii
import sys

# wii_board_data_file_path = 'C:\\Users\\bohdank\\Desktop\\b.json'
wii_board_data_file_path = sys.argv[1]

if '.csv' in wii_board_data_file_path:
    wii_data = wii.read_wii_board_data(wii_board_data_file_path)
    (angle, alpha) = dma.exponent_for_angle(wii_data["resampled"]["copX"], wii_data["resampled"]["copY"])
    wii_data["directedDma"] = {
        "angle": angle.tolist(),
        "alpha": alpha
    }
    wii_board_data_file_path = wii_board_data_file_path.replace('.csv', '.json')
    json.dump(wii_data, open(wii_board_data_file_path, 'w'))
    print(wii_board_data_file_path)
else:
    raise ValueError(f"{wii_board_data_file_path} - is non accceptible file extension was passed")

# print(wii_data) # to bit output length
