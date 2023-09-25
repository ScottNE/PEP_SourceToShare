#!/usr/bin/env python
# coding: utf-8

import numpy as np
from sklearn.metrics import auc
import matplotlib.pyplot as plt
import matplotlib 
import scipy.stats as stats
import tdt
from tdt import read_block, epoc_filter
import os
import sys
import tkinter
import base64
import time




def SetToggleTTLDefault(TTLtoggleVar,PeriEventBitNumEntry):
    if (TTLtoggleVar.get() == 1):
        PeriEventBitNumEntry.delete(0,'end')
        PeriEventBitNumEntry.config(state='disabled')
    else:
        PeriEventBitNumEntry.config(state='normal')
    return




def SetRangeDefault(SetEpochRangeVar,StartTTLEntry,EndTTLEntry):
    if (SetEpochRangeVar.get() == 0):
        StartTTLEntry.config(state='disabled')
        EndTTLEntry.config(state='disabled')
    else:
        StartTTLEntry.config(state='normal')
        EndTTLEntry.config(state='normal')
    return




def DeltaFoverF(RawData, BaselineStartTime, BaselineEndTime, period, FirstTTLindx):
    # find start index and end index
    deltaFoverFs = []
    StartIndex = FirstTTLindx - (abs(int(BaselineStartTime))/period)
    EndIndex = FirstTTLindx - (abs(int(BaselineEndTime))/period)
    if (StartIndex >= 0):
        for SessionData in RawData:
            rawSum = 0
            rawNumber = 0
            for x in SessionData[int(StartIndex):int(EndIndex)]:
                rawSum = rawSum+float(x)
                rawNumber = rawNumber+1
            if (rawNumber> 0):
                BaselineMean = (rawSum/rawNumber)
                deltaFoverFs.append(np.array([(x-BaselineMean)/(BaselineMean) for x in SessionData]))
    return deltaFoverFs





def GetPathName():
    PathName = tkinter.filedialog.askdirectory(title = "Select DIrectory")
    return PathName





def GetBits(BitValue):
    BitValList = []
    for x in range(0,256):
        if (BitValue & x):
            BitValList.append(x)
    return BitValList





def ImportData(PathName):
    #PathName = 'C:\\Users\\scott\\Documents\\TDT_Zweifel\\Juarez_FiberPhotometry\\Kchannel dlight imaging\\imaging day 7 pav\\853-191015-121431'
    ImportedData = ''
    try:
        ImportedData = read_block(PathName)
    except IOError:
        tkinter.messagebox.showerror("CANNOT READ FILE!","Error data file may not exist or is corrupt.")
    except:
        tkinter.messagebox.showerror("DATA FILE ERROR!","   Error reading data files.    ")
    finally:
        return ImportedData





def Trim(data,ISOS,GCaMP,StartTTLNum,EndTTLNum):
    # # Optionally remove artifacts. If any waveform is above ARTIFACT level, or
    # # below -ARTIFACT level, remove it from the data set.
    # total1 = np.size(data.streams[GCaMP].filtered)
    # total2 = np.size(data.streams[ISOS].filtered)

    # # List comprehension checking if any single array in 2D filtered array is > Artifact or < -Artifact
    # data.streams[GCaMP].filtered = [x for x in data.streams[GCaMP].filtered 
    #                             if not np.any(x > ARTIFACT) or np.any(x < -ARTIFACT)]
    # data.streams[ISOS].filtered = [x for x in data.streams[ISOS].filtered 
    #                            if not np.any(x > ARTIFACT) or np.any(x < -ARTIFACT)]

    # Delete arrays that lie outside of user-entered TTLnum (trial number) limits
    y = range(StartTTLNum,EndTTLNum+1)
    z = []
    data.streams[GCaMP].filtered = [z for x,z in enumerate(data.streams[GCaMP].filtered) if x in y]
    z = []
    data.streams[ISOS].filtered = [z for x,z in enumerate(data.streams[ISOS].filtered) if x in y]

    # # Get the total number of rejected arrays
    # bad1 = total1 - np.size(data.streams[GCaMP].filtered)
    # bad2 = total2 - np.size(data.streams[ISOS].filtered)
    # total_artifacts = bad1 + bad2

    return data





def GetMeans(data,GCaMP,ISOS,N):
    # Applying a time filter to a uniformly sampled signal means that the length of each segment could vary by one sample. 
    # Let's find the minimum length so we can trim the excess off before calculating the mean.
    min1 = np.min([np.size(x) for x in data.streams[GCaMP].filtered])
    min2 = np.min([np.size(x) for x in data.streams[ISOS].filtered])
    data.streams[GCaMP].filtered = [x[1:min1] for x in data.streams[GCaMP].filtered]
    data.streams[ISOS].filtered = [x[1:min2] for x in data.streams[ISOS].filtered]

    # Downsample and average 10x via a moving window mean
    # Average every 10 samples into 1 value
    F405 = []
    F470 = []
    for lst in data.streams[ISOS].filtered: 
        small_lst = []
        for i in range(0, min2, N):
            small_lst.append(np.mean(lst[i:i+N-1])) # This is the moving window mean
        F405.append(small_lst)

    for lst in data.streams[GCaMP].filtered: 
        small_lst = []
        for i in range(0, min1, N):
            small_lst.append(np.mean(lst[i:i+N-1]))
        F470.append(small_lst)

    #Create a mean signal, standard error of signal, and DC offset
    meanF405 = np.mean(F405, axis=0)
    stdF405 = np.std(F405, axis=0)/np.sqrt(len(data.streams[ISOS].filtered))
    dcF405 = np.mean(meanF405)
    meanF470 = np.mean(F470, axis=0)
    stdF470 = np.std(F470, axis=0)/np.sqrt(len(data.streams[GCaMP].filtered))
    dcF470 = np.mean(meanF470)

    return data,F405,F470,meanF405,meanF470,stdF405,stdF470,dcF405,dcF470






def GetDeltaFoverF_DownSample(data,N):
    # Applying a time filter to a uniformly sampled signal means that the length of each segment could vary by one sample. 
    # Let's find the minimum length so we can trim the excess off before calculating the mean.
    min = np.min([np.size(x) for x in data])
    data = [x[1:min] for x in data]

    # Downsample and average via a moving window mean
    # Average every N samples into 1 value
    DeltaFoverFDown = []
    for lst in data: 
        small_lst = []
        for i in range(0, min, N):
            small_lst.append(np.mean(lst[i:i+N-1])) # This is the moving window mean
        DeltaFoverFDown.append(np.array(small_lst))

    return DeltaFoverFDown





def FitData(F405,F470,FitToISO):
    # # Fitting 405 channel onto 470 channel to detrend signal bleaching
    # Scale and fit data. Algorithm sourced from Tom Davidson's Github:
    # https://github.com/tjd2002/tjd-shared-code/blob/master/matlab/photometry/FP_normalize.m
    if (FitToISO):
        Y_fit_all = []
        Y_dF_all = []
        for x, y in zip(F405, F470):
            x = np.array(x)
            y = np.array(y)
            bls = np.polyfit(x, y, 1)
            fit_line = np.multiply(bls[0], x) + bls[1]
            Y_fit_all.append(fit_line)
            Y_dF_all.append(y-fit_line)
        
        return Y_dF_all,Y_fit_all
    else:
        Y_fit_all = []
        y = np.array(F470)
    
        return y,Y_fit_all





def GetZscoreSTDerror(Y_dF_all,ts2,BASELINE_PER):
    # Getting the z-score and standard error
    zall = []
    for dF in Y_dF_all: 
       ind = np.where((np.array(ts2)<BASELINE_PER[1]) & (np.array(ts2)>BASELINE_PER[0]))
       zb = np.mean(dF[ind])
       zsd = np.std(dF[ind])
       zall.append((dF - zb)/zsd)
   
    zerror = np.std(zall, axis=0)/np.sqrt(np.size(zall, axis=0))

    return zerror,zall




def CalculateAUC(ts2,zall):
# Quantify changes as an area under the curve for no cue (-5 sec) vs cue (0 sec)

    AUC = [] # no CS, CS
    ind1 = np.where((np.array(ts2)<-3) & (np.array(ts2)>-5))
    AUC1= auc(ts2[ind1], np.mean(zall, axis=0)[ind1])
    ind2 = np.where((np.array(ts2)>0) & (np.array(ts2)<2))
    AUC2= auc(ts2[ind2], np.mean(zall, axis=0)[ind2])
    AUC.append(AUC1)
    AUC.append(AUC2)

    return AUC,ind1,ind2
    



    
def MakePlots(*args):

    (REF_EPOC_Label,DisplayBit,N,data,TRANGE,GCaMP,ISOS,meanF405,meanF470,dcF405,dcF470,stdF470,stdF405,F405,F470,PathName,BASELINE_PER,FitToISO) = args
    # # Plot epoc averaged response
    # Create the time vector for each stream store
    ts1 = TRANGE[0] + np.linspace(1, len(meanF470), len(meanF470))/data.streams[GCaMP].fs*N
    ts2 = TRANGE[0] + np.linspace(1, len(meanF405), len(meanF405))/data.streams[ISOS].fs*N

    # Subtract DC offset to get signals on top of one another
    meanF405 = meanF405 - dcF405
    meanF470 = meanF470 - dcF470

    # Start making a figure with 4 subplots
    # First plot is the 405 and 470 averaged signals
    fig = plt.figure(figsize=(9, 14))

    fig.suptitle('File: %s' % (os.path.basename(PathName)), fontsize=8)

    ax0 = fig.add_subplot(411) # work with axes and not current plot (plt.)

    # Plotting the traces
    p1, = ax0.plot(ts1, meanF470, linewidth=2, color='green', label='GCaMP')
    p2, = ax0.plot(ts2, meanF405, linewidth=2, color='blueviolet', label='ISOS')

    # Plotting standard error bands
    p3 = ax0.fill_between(ts1, meanF470+stdF470, meanF470-stdF470,
                        facecolor='green', alpha=0.2)
    p4 = ax0.fill_between(ts2, meanF405+stdF405, meanF405-stdF405,
                        facecolor='blueviolet', alpha=0.2)

    # Plotting a line at t = 0
    p5 = ax0.axvline(x=0, linewidth=3, color='slategray', label='Bit '+ DisplayBit +' Onset')

    # Finish up the plot
    ax0.set_xlabel('Seconds')
    ax0.set_ylabel('mV')
    ax0.set_title('Response to %s, bit number %s,  %i epocs'
                % (REF_EPOC_Label, DisplayBit, len(data.streams[GCaMP].filtered)))
    ax0.legend(handles=[p1, p2, p5], loc='upper right')
    ax0.set_ylim(min(np.min(meanF470-stdF470), np.min(meanF405-stdF405)),
                max(np.max(meanF470+stdF470), np.max(meanF405+stdF405)))
    ax0.set_xlim(TRANGE[0], TRANGE[1])

    plt.close() # Jupyter cells will output any figure calls made, so if you don't want to see it just yet, close existing axis
                # https://stackoverflow.com/questions/18717877/prevent-plot-from-showing-in-jupyter-notebook
                # Note that this is not good code practice - Jupyter lends it self to these types of bad workarounds 

    # Fitting 405 channel onto 470 channel to detrend signal bleaching
    Y_dF_all,Y_fit_all = FitData(F405,F470,FitToISO)
    zerror,zall = GetZscoreSTDerror(Y_dF_all,ts2,BASELINE_PER)


    # Heat Map based on z score of 405 fit subtracted 470
    ax1 = fig.add_subplot(412)
    #cs = ax1.imshow(zall, cmap="YlOrBr", interpolation='none', aspect="auto", extent=[TRANGE[0], TRANGE[1]+TRANGE[0], 0, len(data.streams[GCaMP].filtered)]) #old heatmap command
    #cs = ax1.imshow(zall, cmap="YlGnBu", interpolation='none', aspect="auto", extent=[TRANGE[0], TRANGE[1], 0, len(data.streams[GCaMP].filtered)])  #new heatmap command
    #needed to reverse the order of the Y indices in parameter 'extent' because there is an 'origin' paramter that has the default of 'upper'
    # when the 'origin' parameter is set to 'upper', the origin (0,0) is upper left
    cs = ax1.imshow(zall, cmap="YlGnBu", interpolation='none', aspect="auto", extent=[TRANGE[0], TRANGE[1], len(data.streams[GCaMP].filtered), 0])
    cbar = fig.colorbar(cs, pad=0.01, fraction=0.02)


    ax1.set_title('Individual z-Score Traces')
    ax1.set_ylabel('TTLs')
    ax1.set_xlabel('Seconds from TTL Onset')

    plt.close() # Suppress figure output again


    # Plot the z-score trace for the 470 with std error bands
    ax2 = fig.add_subplot(413)
    p6 = ax2.plot(ts2, np.mean(zall, axis=0), linewidth=2, color='green', label='GCaMP')
    p7 = ax2.fill_between(ts1, np.mean(zall, axis=0)+zerror
                        ,np.mean(zall, axis=0)-zerror, facecolor='green', alpha=0.2)
    p8 = ax2.axvline(x=0, linewidth=3, color='slategray', label='Bit number '+ DisplayBit +' Onset')
    ax2.set_ylabel('z-Score')
    ax2.set_xlabel('Seconds')
    ax2.set_xlim(TRANGE[0], TRANGE[1])
    ax2.set_title('Bit number'+ DisplayBit)

    plt.close()
    

    AUC,ind1,ind2 = CalculateAUC(ts2,zall)

    # Run a two-sample T-test
    t_stat,p_val = stats.ttest_ind(np.mean(zall, axis=0)[ind1],
                            np.mean(zall, axis=0)[ind2], equal_var=False)


    # Make a bar plot
    ax3 = fig.add_subplot(414)
    p9 = ax3.bar(np.arange(len(AUC)), AUC, color=[.8, .8, .8], align='center', alpha=0.5)

    # statistical annotation
    x1, x2 = 0, 1 # columns indices for labels
    y, h, col = max(AUC) + 2, 2, 'k'
    if (p_val < 0.05):
        ax3.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
        p10 = ax3.text((x1+x2)*.5, y+h, "*", ha='center', va='bottom', color=col)

    # Finish up the plot
    ax3.set_ylim(0,y+2*h)
    ax3.set_ylabel('AUC')
    ax3.set_title('Control vs Bit '+ DisplayBit)
    ax3.set_xticks(np.arange(-1, len(AUC)+1))
    ax3.set_xticklabels(['','No Bit '+ DisplayBit,'Bit '+ DisplayBit,''])


    fig.tight_layout()
    
    return fig,AUC,zerror,zall




# def popupmsg(msg):
#     popup = tkinter.Tk()
#     popup.wm_title("")
#     label = tkinter.Label(popup, text=msg, bg = "red")
#     label.pack(side="top", fill="x", pady=10)
#     OKButton = tkinter.Button(popup, text="Okay", command = popup.destroy)
#     OKButton.pack(padx = 5, pady = 5)
#     popup.mainloop()



def CommonProcess(*args):
    
    EpocEntry,BitNumEntry,TTLtoggleVar,TransposedVar,FitToISO,SetEpochRangeVar,StartTTLEntry,EndTTLEntry,IsosEntry,GCaMPEntry,SamplesToAverageEntry,StartWindowEntry,EndWindowEntry,BaselineStartEntry,BaselineEndEntry = args

    time.sleep(.2)

    PathName = GetPathName()
    if (PathName == ''):
        return
    
    DirectoriesToProcess = [x for x in os.listdir(PathName) if os.path.isdir(os.path.join(PathName,x))]

    for DirectoryName in DirectoriesToProcess:

        SubPathName = os.path.join(PathName,DirectoryName)

        data = ImportData(SubPathName)
        
        matplotlib.rcParams['font.size'] = 10 #set font size for all plots
        matplotlib.rcParams['pdf.fonttype'] = 42 #fonts compatible with Adobe Illustrator
        matplotlib.rcParams['ps.fonttype'] = 42
        
        REF_EPOC = EpocEntry.get()
        if (REF_EPOC == ''):
            REF_EPOC = 'BOX1' 
        

        if (not REF_EPOC.isdigit()):        
            EpocNames = tdt.StructType.keys(data.epocs)
            EpocNames = list(EpocNames)
            if (not (REF_EPOC in EpocNames)):
                errormessage = "\n" + DirectoryName + ":\n\n" + REF_EPOC + " is not an Epoc!\n\n Epocs are: \n\n" + "\n".join(EpocNames) + "\n"
                tkinter.messagebox.showerror('INCORRECT EPOC', errormessage)
                continue
        REF_EPOC_Label = REF_EPOC
        REF_EPOC_Label.replace('\\','')
        REF_EPOC_Label.replace('/','')

        REF_EPOC = data.epocs[REF_EPOC].name

        if (TTLtoggleVar == 1):
            BitValueList = [data.epocs[REF_EPOC_Label].data[0]]
            DisplayBit = REF_EPOC_Label
        else:
            BitNum = BitNumEntry.get()
            if (BitNum == ''):
                BitNum = '3'
            #BitNum = int(BitNum)-1  
            BitNum = int(BitNum)    #Changed bit numbering to 0-7
            BitVal = 2**BitNum
            BitValueList = []
            BitValueList = GetBits(BitVal)
            DisplayBit = str(BitNum)


        if (SetEpochRangeVar == 1):
            StartTTLNum = int(StartTTLEntry.get()) - 1
            EndTTLNum = int(EndTTLEntry.get()) - 1
            if (StartTTLNum<0):
                StartTTLNum = 0
            if (EndTTLNum<=0):
                EndTTLNum = 1
            if (StartTTLNum >= EndTTLNum):
                errormessage = "End epoch needs to be larger than start epoch!\n" 
                tkinter.messagebox.showerror('ILLEGAL RANGE', errormessage)
                return

        ISOS = IsosEntry.get()
        if (ISOS == ''):
            ISOS = '_405G' # 405nm channel
        
        GCaMP = GCaMPEntry.get()
        if (GCaMP == ''):
            GCaMP = '_470G' # 470nm channel
        
        StartWindowTime = int(StartWindowEntry.get())
        EndWindowTime = int(EndWindowEntry.get())
        if (StartWindowTime == 0):
            StartWindowTime = -10
        if (EndWindowTime == 0):
            EndWindowTime = 20

        BaselineStartTime = int(BaselineStartEntry.get())
        BaselineEndTime = int(BaselineEndEntry.get())
        if (BaselineStartTime == 0):
            BaselineStartTime = -10
        

        TRANGE = [StartWindowTime, EndWindowTime] # window size [start time relative to epoc onset, window duration]
        #TRANGE = [-10, 20]
        
        BASELINE_PER = [BaselineStartTime, BaselineEndTime] # baseline period within our window
        #BASELINE_PER = [-10, -6]
        
        #ARTIFACT = float("inf") # optionally set an artifact rejection level
        
        N = int(SamplesToAverageEntry.get()) # Average every SamplesToAverageEntry samples into 1 value
        if (N == 0):
            N = 1

        # Use epoc_filter to extract data around our epoc event
        # Using the 't' parameter extracts data only from the time 
        # range around our epoc event. Use the 'values' parameter to 
        # specify allowed values of the REF_EPOC to extract.  For 
        # stream events, the chunks of data are stored in cell arrays 
        # structured as data.streams[GCaMP].filtered

        data_final = epoc_filter(data, REF_EPOC, values=[BitValueList[0]], t=TRANGE)
        for BitCount,x in enumerate(BitValueList):
            if (BitCount > 0):
                data_filtered = epoc_filter(data, REF_EPOC, values=[x], t=TRANGE)
                if (data_filtered.streams[GCaMP].filtered):
                    for FilteredDataGCaMP in data_filtered.streams[GCaMP].filtered:
                        data_filteredAsNParrayGCaMP = np.asarray(FilteredDataGCaMP)
                        data_final.streams[GCaMP].filtered.append(data_filteredAsNParrayGCaMP)
                    for FilteredDataISOS in data_filtered.streams[ISOS].filtered:
                        data_filteredAsNParrayISOS = np.asarray(FilteredDataISOS)
                        data_final.streams[ISOS].filtered.append(data_filteredAsNParrayISOS)
     
        if (len(data_final.streams[GCaMP].filtered)):
            data = data_final
        else:
            errormessage = "No events found for " + REF_EPOC + ".\n" 
            tkinter.messagebox.showerror('NO EVENTS FOUND', errormessage)
            return

        if (SetEpochRangeVar == 1):
            data = Trim(data,ISOS,GCaMP,StartTTLNum,EndTTLNum)

        data,F405,F470,meanF405,meanF470,stdF405,stdF470,dcF405,dcF470 = GetMeans(data,GCaMP,ISOS,N)

        fig,AUC,zerror,zall = MakePlots(REF_EPOC_Label,DisplayBit,N,data,TRANGE,GCaMP,ISOS,meanF405,meanF470,dcF405,dcF470,stdF470,stdF405,F405,F470,SubPathName,BASELINE_PER,FitToISO)

        period_405 = 1/data.streams[ISOS].fs
        period_470 = 1/data.streams[GCaMP].fs

        FirstTTLindx_405 = abs(int(StartWindowTime))/period_405
        FirstTTLindx_470 = abs(int(StartWindowTime))/period_470

        DeltaFoverF_405 = DeltaFoverF(data.streams[ISOS].filtered, BaselineStartTime, BaselineEndTime, period_405, FirstTTLindx_405)
        DeltaFoverF_470 = DeltaFoverF(data.streams[GCaMP].filtered, BaselineStartTime, BaselineEndTime, period_470, FirstTTLindx_470)

        DeltaFoverF_DownSample_405 = GetDeltaFoverF_DownSample(DeltaFoverF_405,N)
        DeltaFoverF_DownSample_470 = GetDeltaFoverF_DownSample(DeltaFoverF_470,N)
        
        ResultFigurePath = SubPathName + '\\ResultsFigure_' + REF_EPOC_Label + '_Bit#'+ DisplayBit+'.pdf'
        ResultDataPath = SubPathName + '\\ResultsData_' + REF_EPOC_Label + '_Bit#' + DisplayBit
        RawDataPath = SubPathName + '\\RawData_' + REF_EPOC_Label + '_Bit#' + DisplayBit
        DeltaFoverFPath = SubPathName + '\\DeltaFoverF_' + REF_EPOC_Label + '_Bit#' + DisplayBit
        DeltaFoverF_DownSamplePath = SubPathName + '\\DeltaFoverF_DownSample_' + REF_EPOC_Label + '_Bit#' + DisplayBit
        TransposeMeanDataPath = SubPathName + '\\TRANS_MeanData_' + REF_EPOC_Label + '_Bit#' + DisplayBit
        TransposeZDataPath = SubPathName + '\\TRANS_Z-scoreData_' + REF_EPOC_Label + '_Bit#' + DisplayBit
        TransposeRawDataPath = SubPathName + '\\TRANS_RawData_' + REF_EPOC_Label + '_Bit#' + DisplayBit
        TransposeDeltaFoverFPath = SubPathName + '\\TRANS_DeltaFoverF_' + REF_EPOC_Label + '_Bit#' + DisplayBit
        TransposeDeltaFoverFDownSPath = SubPathName + '\\TRANS_DeltaFoverFDownSample_' + REF_EPOC_Label + '_Bit#' + DisplayBit

        #Save plot in format that is Adobe Illustrator-friendly
        fig.savefig(ResultFigurePath, transparent=True)

        #Save text file for processed data
        DataFileStream = open(ResultDataPath+".txt", 'w')
        
        meanF405TabDelimited = "\t".join(str(list(meanF405)).split())
        meanF405TabDelimited = meanF405TabDelimited.replace(',','')
        meanF405TabDelimited = meanF405TabDelimited.replace('[','')
        meanF405TabDelimited = meanF405TabDelimited.replace(']','')
        
        meanF470TabDelimited = "\t".join(str(list(meanF470)).split())
        meanF470TabDelimited = meanF470TabDelimited.replace(',','')
        meanF470TabDelimited = meanF470TabDelimited.replace('[','')
        meanF470TabDelimited = meanF470TabDelimited.replace(']','')
        
        stdF405TabDelimited = "\t".join(str(list(stdF405)).split())
        stdF405TabDelimited = stdF405TabDelimited.replace(',','')
        stdF405TabDelimited = stdF405TabDelimited.replace('[','')
        stdF405TabDelimited = stdF405TabDelimited.replace(']','')

        stdF470TabDelimited = "\t".join(str(list(stdF470)).split())
        stdF470TabDelimited = stdF470TabDelimited.replace(',','')
        stdF470TabDelimited = stdF470TabDelimited.replace('[','')
        stdF470TabDelimited = stdF470TabDelimited.replace(']','')

        # F data is downsampled (take mean of every N points) and DC components are
        # subtracted to 'detrend' so get rid of drift.
        # The mean of the F data is the mean taken over all the TTL events
        DataFileStream.write("Mean "+ISOS+" :\n"+meanF405TabDelimited+"\n\n")
        DataFileStream.write("Mean "+GCaMP+" :\n"+meanF470TabDelimited+"\n\n")
        DataFileStream.write("Std Error "+ISOS+" :\n"+stdF405TabDelimited+"\n\n")
        DataFileStream.write("Std Error "+GCaMP+" :\n"+stdF470TabDelimited+"\n\n")

        # Write mean data transposed
        if (TransposedVar):
            TransDataFileStream = open(TransposeMeanDataPath+".txt", 'w')
            TransDataFileStream.write("Means: Rows = Time" + "\n")
            TransDataFileStream.write("Mean "+ISOS+" \tStd Error "+ISOS+" \tMean "+GCaMP+" \tStd Error "+GCaMP+"\n")
            for i,value in enumerate(meanF405):
                TransDataFileStream.write(str(value)+"\t"+str(stdF405[i])+"\t"+str(meanF470[i])+"\t"+str(stdF470[i])+"\n")
            TransDataFileStream.close
                
        if (AUC):
            zerrorTabDelimited = "\t".join(str(list(zerror)).split())
            zerrorTabDelimited = zerrorTabDelimited.replace(',','')
            zerrorTabDelimited = zerrorTabDelimited.replace('[','')
            zerrorTabDelimited = zerrorTabDelimited.replace(']','')

            AUCTabDelimited = "\t".join(str(list(AUC)).split())
            AUCTabDelimited = AUCTabDelimited.replace(',','')
            AUCTabDelimited = AUCTabDelimited.replace('[','')
            AUCTabDelimited = AUCTabDelimited.replace(']','')

            # zall is the z-score data for each TTL occurence in the time range specified
            # so it is a list of numpy arrays - each array represents a TTL event
            DataFileStream.write("Z-scores :\n")
            for zallEventArray in zall:
                zallTabDelimited = "\t".join(str(list(zallEventArray)).split())
                zallTabDelimited = zallTabDelimited.replace(',','')
                zallTabDelimited = zallTabDelimited.replace('[','')
                zallTabDelimited = zallTabDelimited.replace(']','')
                DataFileStream.write(zallTabDelimited +"\n")
            DataFileStream.write("\n")

            # Z error is the std error for z-score data above
            DataFileStream.write("Z-error :\n"+zerrorTabDelimited+"\n\n")
            DataFileStream.write("Z-score AUC :\n"+AUCTabDelimited+"\n\n")

             # Write Transposed Z-score data
            if (TransposedVar):
                TransDataFileStream = open(TransposeZDataPath+".txt", 'w')
                TransDataFileStream.write("Z-scores (Rows = Time, Columns = TTL events) :\n")
                MaxColumn = zall[0].shape[0]
                for CurrentColumn in range(0,MaxColumn):
                    CurrentTransFileLine = ""
                    for EventArray in zall:
                        CurrentTransFileLine += str(EventArray[CurrentColumn]) + "\t"
                    TransDataFileStream.write(CurrentTransFileLine + "\n")
                TransDataFileStream.close
        
        DataFileStream.close


        # Save text file for raw data, 'filtered' refers to taking the window around the TTL
        DataFileStream = open(RawDataPath+".txt", 'w')
        
        DataFileStream.write("Raw data for "+ISOS+" events:\n")
        for rawISOSEvent in data.streams[ISOS].filtered:
            rawISOSTabDelimited = "\t".join(str(list(rawISOSEvent)).split())
            rawISOSTabDelimited = rawISOSTabDelimited.replace(',','')
            rawISOSTabDelimited = rawISOSTabDelimited.replace('[','')
            rawISOSTabDelimited = rawISOSTabDelimited.replace(']','')
            DataFileStream.write(rawISOSTabDelimited +"\n")
        DataFileStream.write("\n")
            
        DataFileStream.write("Raw data for "+GCaMP+" events:\n")
        for rawGCaMPEvent in data.streams[GCaMP].filtered:
            rawGCaMPTabDelimited = "\t".join(str(list(rawGCaMPEvent)).split())
            rawGCaMPTabDelimited = rawGCaMPTabDelimited.replace(',','')
            rawGCaMPTabDelimited = rawGCaMPTabDelimited.replace('[','')
            rawGCaMPTabDelimited = rawGCaMPTabDelimited.replace(']','')
            DataFileStream.write(rawGCaMPTabDelimited +"\n")
        DataFileStream.write("\n")

        DataFileStream.close

        # Write Transposed Raw data
        if (TransposedVar):
            TransDataFileStream = open(TransposeRawDataPath+".txt", 'w') 
            TransDataFileStream.write("Raw " + ISOS + " data (Rows = Time, Columns = TTL events) :\n")
            MaxColumn = data.streams[ISOS].filtered[0].shape[0]
            for CurrentColumn in range(0,MaxColumn):
                CurrentTransFileLine = ""
                for EventArray in data.streams[ISOS].filtered:
                    CurrentTransFileLine += (str(EventArray[CurrentColumn]) + "\t")
                TransDataFileStream.write(CurrentTransFileLine + "\n")

            TransDataFileStream.write("\nRaw " + GCaMP + " data (Rows = Time, Columns = TTL events) :\n")
            MaxColumn = data.streams[GCaMP].filtered[0].shape[0]
            for CurrentColumn in range(0,MaxColumn):
                CurrentTransFileLine = ""
                for EventArray in data.streams[GCaMP].filtered:
                    CurrentTransFileLine += (str(EventArray[CurrentColumn]) + "\t")
                TransDataFileStream.write(CurrentTransFileLine + "\n")
            TransDataFileStream.close


        # Save text file for deltaFoverF
        DataFileStream = open(DeltaFoverFPath+".txt", 'w')
 
        DataFileStream.write("DeltaFoverF for "+ISOS+" events:\n")
        for DeltaFoverFEvent in DeltaFoverF_405:
            DeltaFoverFISOSTabDelimited = "\t".join(str(list(DeltaFoverFEvent)).split())
            DeltaFoverFISOSTabDelimited = DeltaFoverFISOSTabDelimited.replace(',','')
            DeltaFoverFISOSTabDelimited = DeltaFoverFISOSTabDelimited.replace('[','')
            DeltaFoverFISOSTabDelimited = DeltaFoverFISOSTabDelimited.replace(']','')
            DataFileStream.write(DeltaFoverFISOSTabDelimited +"\n")
        DataFileStream.write("\n")           

        DataFileStream.write("DeltaFoverF for "+GCaMP+" events:\n")
        for DeltaFoverFEvent in DeltaFoverF_470:
            DeltaFoverFGCaMPTabDelimited = "\t".join(str(list(DeltaFoverFEvent)).split())
            DeltaFoverFGCaMPTabDelimited = DeltaFoverFGCaMPTabDelimited.replace(',','')
            DeltaFoverFGCaMPTabDelimited = DeltaFoverFGCaMPTabDelimited.replace('[','')
            DeltaFoverFGCaMPTabDelimited = DeltaFoverFGCaMPTabDelimited.replace(']','')
            DataFileStream.write(DeltaFoverFGCaMPTabDelimited +"\n")
        DataFileStream.write("\n")           

        DataFileStream.close

        # Write Transposed DeltaFoverF data
        if (TransposedVar):
            TransDataFileStream = open(TransposeDeltaFoverFPath+".txt", 'w') 
            TransDataFileStream.write("DeltaFoverF " + ISOS + " data (Rows = Time, Columns = TTL events) :\n")
            MaxColumn = DeltaFoverF_405[0].shape[0]
            for CurrentColumn in range(0,MaxColumn):
                CurrentTransFileLine = ""
                for EventArray in DeltaFoverF_405:
                    CurrentTransFileLine += (str(EventArray[CurrentColumn]) + "\t")
                TransDataFileStream.write(CurrentTransFileLine + "\n")

            TransDataFileStream.write("\nDeltaFoverF " + GCaMP + " data (Rows = Time, Columns = TTL events) :\n")
            MaxColumn = DeltaFoverF_470[0].shape[0]
            for CurrentColumn in range(0,MaxColumn):
                CurrentTransFileLine = ""
                for EventArray in DeltaFoverF_470:
                    CurrentTransFileLine += (str(EventArray[CurrentColumn]) + "\t")
                TransDataFileStream.write(CurrentTransFileLine + "\n")
            TransDataFileStream.close


        # Save text file for deltaFoverF_Downsample
        DataFileStream = open(DeltaFoverF_DownSamplePath+".txt", 'w')
 
        DataFileStream.write("DeltaFoverFDownSample for "+ISOS+" events:\n")
        for DeltaFoverFEvent in DeltaFoverF_DownSample_405:
            DeltaFoverFISOSTabDelimited = "\t".join(str(list(DeltaFoverFEvent)).split())
            DeltaFoverFISOSTabDelimited = DeltaFoverFISOSTabDelimited.replace(',','')
            DeltaFoverFISOSTabDelimited = DeltaFoverFISOSTabDelimited.replace('[','')
            DeltaFoverFISOSTabDelimited = DeltaFoverFISOSTabDelimited.replace(']','')
            DataFileStream.write(DeltaFoverFISOSTabDelimited +"\n")
        DataFileStream.write("\n")           

        DataFileStream.write("DeltaFoverFDownSample for "+GCaMP+" events:\n")
        for DeltaFoverFEvent in DeltaFoverF_DownSample_470:
            DeltaFoverFGCaMPTabDelimited = "\t".join(str(list(DeltaFoverFEvent)).split())
            DeltaFoverFGCaMPTabDelimited = DeltaFoverFGCaMPTabDelimited.replace(',','')
            DeltaFoverFGCaMPTabDelimited = DeltaFoverFGCaMPTabDelimited.replace('[','')
            DeltaFoverFGCaMPTabDelimited = DeltaFoverFGCaMPTabDelimited.replace(']','')
            DataFileStream.write(DeltaFoverFGCaMPTabDelimited +"\n")
        DataFileStream.write("\n")           

        DataFileStream.close

        # Write Transposed DeltaFoverF_DownSample data
        if (TransposedVar):
            TransDataFileStream = open(TransposeDeltaFoverFDownSPath+".txt", 'w') 
            TransDataFileStream.write("DeltaFoverFDownSample " + ISOS + " data (Rows = Time, Columns = TTL events) :\n")
            MaxColumn = DeltaFoverF_DownSample_405[0].shape[0]
            for CurrentColumn in range(0,MaxColumn):
                CurrentTransFileLine = ""
                for EventArray in DeltaFoverF_DownSample_405:
                    CurrentTransFileLine += (str(EventArray[CurrentColumn]) + "\t")
                TransDataFileStream.write(CurrentTransFileLine + "\n")

            TransDataFileStream.write("\nDeltaFoverFDownSample " + GCaMP + " data (Rows = Time, Columns = TTL events) :\n")
            MaxColumn = DeltaFoverF_DownSample_470[0].shape[0]
            for CurrentColumn in range(0,MaxColumn):
                CurrentTransFileLine = ""
                for EventArray in DeltaFoverF_DownSample_470:
                    CurrentTransFileLine += (str(EventArray[CurrentColumn]) + "\t")
                TransDataFileStream.write(CurrentTransFileLine + "\n")
            TransDataFileStream.close



    tkinter.messagebox.showinfo('   DONE   ', 'DONE')

    return
    




def noClose():
    pass     
      

def terminate(root):
    root.destroy()
    sys.exit()
