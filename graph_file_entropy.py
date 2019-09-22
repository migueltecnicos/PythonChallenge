# -*- coding: utf8 -*-
import math

def calcula_entropia(fichero):

    # read the whole file into a byte array
    f = open(fichero, "rb")
    byteArr = map(ord, f.read())
    f.close()
    fileSize = len(byteArr)

    # calculate the frequency of each byte value in the file
    freqList = []
    for b in range(256):
        ctr = 0
        for byte in byteArr:
            if byte == b:
                ctr += 1
        freqList.append(float(ctr) / fileSize)

    # Shannon entropy
    ent = 0.0
    for freq in freqList:
        if freq > 0:
            ent = ent + freq * math.log(freq, 2)
    ent = -ent
    # print 'Shannon entropy (min bits per byte-character):'
    # print ent
    # print
    # print 'Min possible file size assuming max theoretical compression efficiency:'
    # print (ent * fileSize), 'in bits'
    # print (ent * fileSize) / 8, 'in bytes'
    return fichero + " presenta entropia: " + str(ent)

    ###  Modifications to file_entropy.py to create the Histogram start here ###
    ### by Ken Hartman  www.KennethGHartman.com
"""    
    import numpy as np
    import matplotlib.pyplot as plt
    
    N = len(freqList)
    
    ind = np.arange(N)  # the x locations for the groups
    width = 1.00        # the width of the bars
    
    #fig = plt.figure()
    fig = plt.figure(figsize=(11,5),dpi=100)
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, freqList, width)
    ax.set_autoscalex_on(False)
    ax.set_xlim([0,255])
    
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Byte')
    ax.set_title('Frequency of Bytes 0 to 255\nFILENAME: ' + sys.argv[1])
    
    plt.show()
"""