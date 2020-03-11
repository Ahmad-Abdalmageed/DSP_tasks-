import numpy as np
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
    print(dimensions)
    if len(dimensions) == 2:
        data = data[:, 0]
        print("de channeled ")
        dimensions = (dimensions[0],)
    signalDict = {'frequency':samplingFrequency, 'data':data, 'dim': dimensions}
    return signalDict


def fourierTransform(signalDict):
    """
    apply fourier transform on the data;
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
        data_ft = fftpack.rfft(signal)
        data_freqs = fftpack.rfftfreq(len(signal), d=1 / samplingFrequency)
    dataDict = {'transformedData': data_ft, 'dataFrequencies': data_freqs}
    print("the data", data_ft)

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
        dataInverse = (fftpack.irfft(transfomerdData))
        print("inverse", dataInverse)

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
    # N = len(data) // 10
    freqBands = (0, 62.5, 125, 250, 500, 10**3, 2*10**3, 4*10**3, 8*10**3, 16*10**3, len(data))
    # freqBands = [N*i for i in range(10)]
    dataBands = []
    for i in range(len(freqBands)-1):
        # bands = [indx for indx, val in enumerate(freqs) if val >= freqBands[i] and val < freqBands[i+1]] ## equal sign هه

        bands = []
        for indx, val in enumerate(freqs):
            if val >= freqBands[i] and val < freqBands[i + 1]:
                bands.append(indx)

        dataBands.append(data[bands])
    return dataBands

def windowModification(dataModified, bandIndx, gains):
        """
        a helper function to apply window
        :param dataModified: the data to be modified
        :param bandIndx: the indicies of the band
        :param gain: the gain desired
        :return: array data
        """
        data = np.copy(dataModified)
        for slider, value in gains.items():
            if type(value) != type(...) :
                data[slider] = np.multiply(np.array(data[slider]), value)
            else: pass
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
    bandIndx = sliderID
    gain = sliderVal
    dataModified = np.copy(dataBands)
    if windowType == 'Rectangle':
        dataModified = windowModification(dataModified, bandIndx, gain)

    if windowType == 'Hanning':
        for slider, value in gain.items():
            if type(value) != type(...) :
                hanning = np.hanning(len(dataModified[slider])*2)
                low = len(hanning) // 4
                high = 3 * low
                if sliderID != 0:
                    # Check if dataBefore length is +  --->>> data > hamming
                    difSizeBefore = len(dataModified[slider - 1]) - len(hanning[: low])

                    if difSizeBefore > 0:
                        onesBefore = np.ones(difSizeBefore)
                        # Create array of ones ---->>> Add ones to dataBefore
                        hanningBefore = np.concatenate(onesBefore, hanning[: low])
                        dataModified[sliderID - 1] *= value * hanningBefore

                    # Check if dataBefore length is -  --->>> data < hamming
                    elif difSizeBefore < 0:
                        # Slice dataBefore from 0 to its length ---->>> multiply by hamming
                        slicedHanningBefore = hanning[len(dataModified[slider - 1]): low]
                        dataModified[sliderID - 1] *= value * slicedHanningBefore

                    # Hanning == len of data
                    else:
                        dataModified[sliderID - 1] *= value * hanning[: low]

                # Apply hanning after
                if sliderID != 9:
                    difSizeAfter = len(dataModified[slider + 1]) - len(hanning[high: ])

                    # Data >> hanning
                    if difSizeAfter > 0:
                        onesAfter = np.ones(difSizeAfter)
                        # Create array of ones ---->>> Add ones to difSizeAfter
                        hanningAfter = np.concatenate((hanning[high: ], onesAfter))
                        dataModified[sliderID + 1] *= value * hanningAfter

                    # Check if difSizeAfter length is -  --->>> data < hamming
                    elif difSizeAfter < 0:
                        # Slice dataBefore from 0 to its length ---->>> multiply by hamming
                        slicedHanningAfter = hanning[high: len(dataModified[slider + 1])]
                        dataModified[sliderID + 1] *= value * slicedHanningAfter

                    # Hanning == len of data
                    else:
                        dataModified[sliderID + 1] *= value * hanning[high: ]

                # Effective area of hanning
                gain[slider] = value * hanning[low : high]

        dataModified = windowModification(dataModified, bandIndx, gain)

    if windowType == 'Hamming':
        for slider, value in gain.items():
            if type(value) != type(...) :
                # if value is int :
                    hamming = np.hamming(len(dataModified[slider])*2)
                    low = len(hamming) // 4
                    high = 3 * low
                    gain[slider] = value * hamming[low : high]
        dataModified = windowModification(dataModified, bandIndx, gain)
    return dataModified


if __name__ == '__main__':
    # audioFile = loadAudioFile('audio/Casio-MT-45-16-Beat.wav')
    # # print(audioFile['data'])
    # fourierDict= fourierTransform(audioFile)
    # # print(fourierDict['transformedData'])
    # dataBands = createBands(fourierDict)
    # # print(dataBands)
    # mod = applyWindowFunction(1, 5, dataBands)
    # # print(mod)
    # inv = inverseFourierTransform(mod, audioFile['dim'])
    # print(type(inv))
    # for i in dataBands:
    #     print(i)
    # print(np.real(np.concatenate(dataBands)))
    # print(np.real(fourierDict['transformedData']))
    #
    # print(dataBands['dataBands'])
    # dataBands[1] = applyWindowFunction(1, 2, dataBands)
    # dataBands[1] = applyWindowFunction(1, 3, dataBands)
    # dataBands[1] = applyWindowFunction(1, 4, dataBands)


    array1 = np.array([10, 100, 20])
    array2 = np.array([3, 30, 1])
    result = array1 - array2
    print(result)
