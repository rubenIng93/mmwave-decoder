import os

import numpy as np
import pandas as pd

from parser_mmw_demo import parser_one_mmw_demo_output_packet


def populate_result_dictionary(dictionary, frame_number, results):
    """
    Used the results to populate the dictionary initialized
    with columns `frame_name`, `x`, `y`, `z`, `v`, `azimuth`, `snr`

    Args:
        dictionary (dict): the initialized dict
        frame_number (int): the frame number
        results (tuple): results coming from the `parser_one_mmw_demo_output_packet`
    """
    dictionary["frame_number"].append(frame_number)
    dictionary["x"].append(results[6][obj])
    dictionary["y"].append(results[7][obj])
    dictionary["z"].append(results[8][obj])
    dictionary["v"].append(results[9][obj])
    dictionary["azimuth"].append(results[11][obj])
    dictionary["snr"].append(results[13][obj])


if __name__ == "__main__":
    # let the user specify the input path
    data_path = input("Specify the input data: ")

    # load the file
    with open(data_path, "rb") as f:
        data = f.read()

    data = np.frombuffer(data, dtype="uint8")
    byte_count = len(data)
    # data is a sequence of uint8, where each packet starts with the magic word
    # [2 1 4 3 6 5 8 7], let's understand how many packets do we have

    magic_word = np.array([2, 1, 4, 3, 6, 5, 8, 7], dtype="uint8")

    # find the index of where the magic_word starts
    condition = data == magic_word[0]
    possible_idxs = np.argwhere(condition)

    # for each index check if the subsequent values match the magic_word
    # store the starting indx if any
    frame_start_idx = []
    for idx in possible_idxs.squeeze():
        # magic word length is 8
        if np.all(data[idx : idx + 8] == magic_word):
            frame_start_idx.append(idx)

    print(f"Found {len(frame_start_idx)} packets/frames")

    # create an empty dict to store the data
    output_columns = ["frame_number", "x", "y", "z", "v", "azimuth", "snr"]
    # dict comprehansion to initialize it
    output_data_dict = {k: [] for k in output_columns}

    for frame_number, idx in enumerate(frame_start_idx):
        temp_data = data[idx:]
        temp_byte_count = len(temp_data)
        # decode the frame
        results = parser_one_mmw_demo_output_packet(temp_data, temp_byte_count)
        # check if the frame is correct (results[0] must be 0)
        if results[0] == 0:
            # ready to store
            # results has the following variables
            # result, headerStartIndex, totalPacketNumBytes, numDetObj, numTlv, subFrameNumber,
            # detectedX_array, detectedY_array, detectedZ_array, detectedV_array,
            # detectedRange_array, detectedAzimuth_array, detectedElevAngle_array,
            # detectedSNR_array, detectedNoise_array
            # commonly coordinates, speed, and snr are enough

            # iterate over the number of objects in each frame
            count_objects = results[3]
            # check that is not 0
            if count_objects > 0:
                for obj in range(count_objects):
                    # populate the dict
                    populate_result_dictionary(output_data_dict, frame_number, results)

    # convert the dictionary in a pandas dataframe
    df = pd.DataFrame(output_data_dict)

    if not os.path.exists("out_data"):
        os.makedirs("out_data")

    out_filename = input("Specify the output Filename: ")

    # save the df as csv
    df.to_csv(os.path.join("out_data", out_filename), index=None)
