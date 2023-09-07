# TI mmwave .dat Decoder

A script for converting the .dat files coming from the TI mmwaveDemoVisualizer into .csv files.

It makes use of the Texas Instruments parser for OOB (Out-of-the-Box) demo, written in Python.

The output CSV will have a number of rows corresponding to the number of object found in each frame times the number of frames recoded.

The output file's header is composed as follows:

- `frame_number`
- `x`
- `y`
- `z`
- `v`
- `azimuth`
- `snr`

Where x, y, and z are the coordinates in meters, v is the velocity in m/s and snr is the Signal to Noise Ratio

## Requirements

I suggest to build a Python virtual environment to execute the script.

In that case the procedure is the following:

### Setup the virtual environment

Open a terminal and find your Python version by typing `python` and pressing the tab key. This outputs a message with the current version, e.g. python3.11.

Then, according to that build the environment by typing

```CLI
python<version> -m venv <envname>
```

As `envname` you can choose whatever you prefer.

### Activation and pip update

Once built you have to activate the virtual environment. You can do so by typing in the terminal:

```CLI
source <envname>/bin/activate
```

Then you can update the pip manager to the last available version with:

```CLI
pip install -U pip
```

### Install teh required libraries

As a final setup step you have to install all teh dependencies necessary to properly run the scripts. You can find them arranged in the `requirements.txt` file.

Thus, you can simple run the following line in the terminal:

```CLI
pip install -r requirements.txt
```

You're Done!

## Usage

If you have followed the procedure above, please be sure to have you virtual environment active.

To run the decoder, you just have to type the following line in the terminal.

```
python decode_dat.py
```

This will start the script which requires you to insert the path of the .dat file you want to decode.

> Please insert the filename with the extension specified, e.g. file1.dat

If all went correctly, you then have to specify the output filename. By default the script saves all the outputs in a folder called *out_data* automatically created.

> Please type the filename with the .csv extension.


