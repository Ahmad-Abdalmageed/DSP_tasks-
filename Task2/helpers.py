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
    dimensions = data.shape
    if len(dimensions) == 2:
        data = data[:,  0]
        print("de channeled ")
        dimensions = (dimensions[0],)
    signalDict = {'frequency':samplingFrequency, 'data':data, 'dim': dimensions}
    return signalDict


def fourierTransform(signalDict):
    """
    apply fourier transform on the data
    :param signalDict: a dictionary with:
     'frequency'-- Sampling frequency
     'data' -- Signal Data
    :return: Data Transformed with:
                        'transformedData' --- absolute of the fourier transform
                        'dataFrequencies'--- Frequencies of the signal
    """
    signal = signalDict['data']
    samplingFrequency = signalDict['frequency']
    dim = signalDict['dim']
    if len(dim) == 2 :
        data_ft = fftpack.fft2(signal)
        data_freqs = fftpack.fftfreq(len(signal), d= 1/samplingFrequency)
    else:
        data_ft = fftpack.fft(signal)
        data_freqs = fftpack.fftfreq(len(signal), d=1 / samplingFrequency)
    dataDict = {'transformedData': data_ft, 'dataFrequencies': data_freqs}

    return dataDict


def inverseFourierTransform(transfomerdData, dim):
    """
    apply inverse Fourier Transform
    :param: transformedData: the fourier transformed data
    :return: Real inverse transform data
    """
    if len(dim) == 2:
        print("2 dimensional inverse")
        dataInverse = np.real(fftpack.ifft2(transfomerdData))
    else:
        dataInverse = np.real(fftpack.ifft(transfomerdData))
    return dataInverse


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

    print(len(data))
    freqBands = (0, 31.25, 62.5, 125, 250, 500, 10**3, 2*10**3, 4*10**3, 8*10**3, 16*10**3, len(data))
    dataBands = []
    for i in range(len(freqBands)-1):
        bands = [val for indx, val in enumerate(data) if indx >= freqBands[i] and indx < freqBands[i+1]] ## equal sign هه
        dataBands.append(bands)
    print(len(np.concatenate(dataBands)))
    return dataBands


def windowModification(dataModified, bandIndx, gain):
        """
        a helper function to apply window
        :param dataModified: the data to be modified
        :param bandIndx: the indicies of the band
        :param gain: the gain desired
        :return: array data
        """
        data = np.copy(dataModified)

        print("band before gain", data[bandIndx])
        data[bandIndx] = np.multiply(np.array(data[bandIndx]), gain)
        print("band after gain", data[bandIndx])
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
    print("slider val", gain)
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
    audioFile = loadAudioFile('audio/Casio-MT-45-16-Beat.wav')
    print(audioFile['data'])
    fourierDict= fourierTransform(audioFile)
    print(fourierDict['transformedData'])
    dataBands = createBands(fourierDict)
    print(dataBands)
    mod = applyWindowFunction(1, 5, dataBands)
    print(mod)
    inv = inverseFourierTransform(mod, audioFile['dim'])
    print(type(inv))
    # for i in dataBands:
    #     print(i)
    # print(np.real(np.concatenate(dataBands)))
    # print(np.real(fourierDict['transformedData']))
    #
    # print(dataBands['dataBands'])
    # dataBands[1] = applyWindowFunction(1, 2, dataBands)
    # dataBands[1] = applyWindowFunction(1, 3, dataBands)
    # dataBands[1] = applyWindowFunction(1, 4, dataBands)
