import numpy as np
import scipy as sp
from scipy import fftpack
from scipy.io import wavfile

## These are helper functions
def loadAudioFile(filePath):
    """
    load the audio file
    :param path: path of the wav file
    :return: a dictionary with sampling freq. and data inside the file
    """
    samplingFrequency, data = wavfile.read(filePath)
    signalDict = {'frequency':samplingFrequency, 'data':data}
    return signalDict

def fourierTransform(signalDict):
    """
    apply fourier transform on the data
    :param signalDict: a dictionary with:
     'frequency'-- Sampling frequency
     'data' -- Signal Data
    :return: Data Transformed with:
                        'trasformedData' --- absolute of the fourier transform
                        'dataFrequencies'--- Frequencies of the signal
    """
    signal = signalDict['data']
    samplingFrequency = signalDict['frequency']

    data_ft = fftpack.fft(signal)
    data_ft = (np.abs(data_ft) * 2) / len(signal)

    data_freqs = fftpack.fftfreq(len(signal), d= 1/samplingFrequency)

    dataDict = {'transformedData': data_ft, 'dataFrequencies': data_freqs}

    return dataDict

def inverseFourierTransform():
    """
    apply inverse Fourier Transform
    :param
    :return:
    """

def createBands(dataDict):
    """
    create bands for the signal
    :param dataDict: a dictionary with:
                                    'transformedData' -- the absolute of the fourier transform
                                    'dataFrequencies' -- frequencies present in the signal

    :return: array of bands within the signal
    """
    freqs = dataDict['dataFrequencies']
    data = dataDict['transformedData']

    freqBands = (0, 31.25, 62.5, 125, 250, 500, 10**3, 2*10**3, 4*10**3, 8*10**3, 16*10**3)
    dataBands = []
    for i in range(len(freqBands)-1):
        indices = [indx for indx, val in enumerate(freqs) if val > freqBands[i] and val < freqBands[i+1]]
        dataBands.append(data[indices])
    return dataBands

def windowModification(dataModified, bandIndx, gain):
        data = dataModified
        data[bandIndx] = np.multiply(np.array(data[bandIndx]), gain)
        data = np.concatenate(data)
        return data

def applyWindowFunction(sliderID, sliderVal, dataBands, windowType = "Rectangle"):
    """
        take the value from slider and apply the window given

    :param sliderID: integer representing the id of slider
    :param sliderVal: the gain value
    :param dataBands: list of arrays containing the bands os signal
    :param windowType: window mode
    :return: data modified with the mode and gain
    """
    bandIndx = sliderID -1
    gain = sliderVal
    dataModified = dataBands
    bandRange = len(dataModified[bandIndx])
    hanningWindow = np.hanning(bandRange)
    hammingWindow = np.hamming(bandRange)


    if windowType == 'Rectangle': # TODO: convert multiple lines to function
        dataModified = windowModification(dataModified, bandIndx, gain)
    if windowType == 'Hanning':
        hanningMod = gain * hanningWindow
        dataModified = windowModification(dataModified, bandIndx, hanningMod)
    if windowType == 'Hamming':
        hammingMod = gain * hammingWindow
        dataModified = windowModification(dataModified, bandIndx, hammingMod)

    return dataModified

if __name__ == '__main__':
    data = {'transformedData': np.arange(20, 200, 1), 'dataFrequencies': np.arange(20, 200, 1)}

    print("Length of transformedData: ", len(data['transformedData']))
    bands = createBands(data)
    # print(bands)

    # print(applyWindowFunction(1, 6, bands, 'hamming'))
    afterWindow = applyWindowFunction(1, 6, bands, 'hamming')
    print(len(afterWindow))
