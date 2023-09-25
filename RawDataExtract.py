#!/usr/bin/env python
# coding: utf-8

#import the read_block function from the tdt package
#also import other python packages we care about
import tdt
from tdt import read_block, epoc_filter
import os
import sys
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk
import base64
import time
from statistics import mean




def GetPathName():
    PathName = tkinter.filedialog.askdirectory(title = "Select DIrectory")
    return PathName





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





def SetToggleTTLDefault(TTLtoggleVar,RawTTLBox1Entry,RawTTLBox2Entry):
    if (TTLtoggleVar.get() == 1):
        RawTTLBox1Entry.delete(0,'end')
        RawTTLBox2Entry.delete(0,'end')
    return






def GetBits(BitValue):
    BitValList = []
    for x in range(0,8):
        if (BitValue & 2**x):
            BitValList.append(str(x))
    return BitValList





def SaveRawData(data,TTLbox,GCaMPbox,ISOSbox,RawEventTTLtoggle,DownSampleToggle,DownSampleChoice,DownSampleNumber,SubPathName):

    TTLbox_OnsetTimes = data.epocs[TTLbox].onset.tolist()
    TTLbox_BitVals = data.epocs[TTLbox].data.tolist()
    TTLbox_NumOnsets = len(TTLbox_OnsetTimes)
    #TTLbox_Data = {Times:Vals for (Times,Vals) in zip(TTLbox_OnsetTimes, TTLbox_BitVals) if (Vals!=0)}

    PeriodBox1 = 1/data.streams[GCaMPbox].fs
    SampleTime = 0
    TTLboxCount = 0
    DownSampleCount = 0
    MarkTTL = 0
    
    rawExportVals = []

    rawISOSboxData = data.streams[ISOSbox].data.tolist()
    rawGCaMPdata = data.streams[GCaMPbox].data.tolist()

    Box1TTLvals = ['' for _ in rawISOSboxData]
    Box1TTLbits = ['' for _ in rawISOSboxData]

    if (DownSampleToggle == 1):

        for indx,val in enumerate(rawISOSboxData):

            while (TTLboxCount < TTLbox_NumOnsets and int(TTLbox_BitVals[TTLboxCount]) == 0):
                TTLboxCount = TTLboxCount+1
            if ((TTLboxCount < TTLbox_NumOnsets) and (TTLbox_OnsetTimes[TTLboxCount]>=SampleTime) and (TTLbox_OnsetTimes[TTLboxCount]<=(SampleTime + (PeriodBox1*int(DownSampleNumber)))) and (int(TTLbox_BitVals[TTLboxCount]) != 0)):
                MarkTTL = 1

            if ((indx % int(DownSampleNumber)) == 0):
                if (DownSampleChoice == 2):
                    DownSampleCount = DownSampleCount+1
                    
                    if (MarkTTL == 1):
                        if (RawEventTTLtoggle == 1):
                            Box1TTLvals[DownSampleCount] = ('1')
                            Box1TTLbits[DownSampleCount] = ("\t")                            
                        else:
                            Box1TTLvals[DownSampleCount] = (str(int(TTLbox_BitVals[TTLboxCount])))
                            Box1TTLbits[DownSampleCount] = ("\t".join(GetBits(int(TTLbox_BitVals[TTLboxCount]))))
                        TTLboxCount = TTLboxCount+1
                        MarkTTL = 0

                    rawExportVals.append(str(SampleTime)+"\t"+str(rawGCaMPdata[indx])+"\t"+str(val)+"\t"+Box1TTLvals[DownSampleCount]+"\t"+("\t".join(Box1TTLbits[DownSampleCount])))                
            else:
                if (DownSampleChoice == 1):
                    DownSampleCount = DownSampleCount+1

                    if (MarkTTL == 1):
                        if (RawEventTTLtoggle == 1):
                            Box1TTLvals[DownSampleCount] = ('1')
                            Box1TTLbits[DownSampleCount] = ("\t")
                        else:
                            Box1TTLvals[DownSampleCount] = (str(int(TTLbox_BitVals[TTLboxCount])))
                            Box1TTLbits[DownSampleCount] = ("\t".join(GetBits(int(TTLbox_BitVals[TTLboxCount]))))
                        TTLboxCount = TTLboxCount+1
                        MarkTTL = 0

                    rawExportVals.append(str(SampleTime)+"\t"+str(rawGCaMPdata[indx])+"\t"+str(val)+"\t"+Box1TTLvals[DownSampleCount]+"\t"+("\t".join(Box1TTLbits[DownSampleCount])))                   

            SampleTime = SampleTime + PeriodBox1

 
        if (DownSampleChoice == 1):
            FinalDownSample = 1 - (1/int(DownSampleNumber))
            FinalDownSample = round(FinalDownSample,2)
        else: 
            FinalDownSample = 1/int(DownSampleNumber)
            FinalDownSample = round(FinalDownSample,2)
        
        RawDataPath = SubPathName + '\\NonEpochRawData_' + ISOSbox + '_' + GCaMPbox + '_' + str(FinalDownSample) + 'X.txt'
        ExportVals = "\n".join(rawExportVals)

    else:
        rawISOSvals = rawISOSboxData.copy()
        for indx,val in enumerate(rawISOSboxData):
            
            while (TTLboxCount < TTLbox_NumOnsets and int(TTLbox_BitVals[TTLboxCount]) == 0):
                TTLboxCount = TTLboxCount+1
            if (TTLboxCount < TTLbox_NumOnsets and (TTLbox_OnsetTimes[TTLboxCount]>=SampleTime) and (TTLbox_OnsetTimes[TTLboxCount]<=(SampleTime + PeriodBox1))):
                while (TTLboxCount < TTLbox_NumOnsets and (TTLbox_OnsetTimes[TTLboxCount]>=SampleTime) and (TTLbox_OnsetTimes[TTLboxCount]<=(SampleTime + PeriodBox1))):
                    if (RawEventTTLtoggle == 1):
                        Box1TTLvals[indx] = ('1')
                        Box1TTLbits[indx] = ("\t")
                    else:
                        Box1TTLvals[indx] = (str(int(TTLbox_BitVals[TTLboxCount])))
                        Box1TTLbits[indx] = ("\t".join(GetBits(int(TTLbox_BitVals[TTLboxCount]))))

                    TTLboxCount = TTLboxCount+1

            rawISOSvals[indx] = str(SampleTime)+"\t"+str(rawGCaMPdata[indx])+"\t"+str(val)+"\t"+Box1TTLvals[indx]+"\t"+("\t".join(Box1TTLbits[indx]))

            SampleTime = SampleTime + PeriodBox1

        RawDataPath = SubPathName + '\\NonEpochRawData_' + ISOSbox + "_" + GCaMPbox + '.txt'
        ExportVals = "\n".join(rawISOSvals)
    
    ExportVals = ExportVals.replace(',','')
    ExportVals = ExportVals.replace('[','')
    ExportVals = ExportVals.replace(']','')
    ExportVals = ExportVals.replace(' ','')
 
    DataFileStream1 = open (RawDataPath, 'w')
    DataFileStream1.write("Raw data for "+ISOSbox+" :\n")
    DataFileStream1.write("Time(sec)\tGCaMP\tISOS\tTTL value\tBits\n")
    DataFileStream1.write(ExportVals +"\n")
    DataFileStream1.write("\n")
    DataFileStream1.close

    return







def CommonProcess(*args):
    
    Isos1Entry,Isos2Entry,GCaMP1Entry,GCaMP2Entry,TTLBox1Entry,TTLBox2Entry,RawEventTTLtoggleVar,DownSampleCheckVar,DownSampleRadio,DownSampleEntry = args

    PathName = GetPathName()
    if (PathName == ''):
        return
    
    DirectoriesToProcess = [x for x in os.listdir(PathName) if os.path.isdir(os.path.join(PathName,x))]

    for DirectoryName in DirectoriesToProcess:

        SubPathName = os.path.join(PathName,DirectoryName)
 
        ISOSbox1 = Isos1Entry.get()
        if (ISOSbox1 == ''):
            ISOSbox1 = '_405A' # 405nm channel box1
    
        GCaMPbox1 = GCaMP1Entry.get()
        if (GCaMPbox1 == ''):
            GCaMPbox1 = '_470A' # 470nm channel box1

        ISOSbox2 = Isos2Entry.get()
        if (ISOSbox2 == ''):
            ISOSbox2 = '_405B' # 405nm channel box2
    
        GCaMPbox2 = GCaMP2Entry.get()
        if (GCaMPbox2 == ''):
            GCaMPbox2 = '_470B' # 470nm channel box2

        TTLbox1 = TTLBox1Entry.get()
        TTLbox2 = TTLBox2Entry.get()

        RawEventTTLtoggle = RawEventTTLtoggleVar.get()

        DownSampleToggle = DownSampleCheckVar.get()
        DownSampleChoice = DownSampleRadio.get()
        DownSampleNumber = DownSampleEntry.get()

        data = ImportData(SubPathName)

        TTLNames = tdt.StructType.keys(data.epocs)

        TTLNames = list(TTLNames)

        if ((not (TTLbox1 in TTLNames)) and (not (TTLbox2 in TTLNames))):
            errormessage = "\n" + DirectoryName + ":\n\n" + TTLbox1 + " and " + TTLbox2 + " not a TTL labels!\n\n TTLs are: \n\n" + "\n".join(TTLNames) + "\n"
            tkinter.messagebox.showerror('INCORRECT TTL', errormessage)
            continue
        else:
            if (not (TTLbox1 in TTLNames)):
                if (TTLbox1 != ''):
                    errormessage = "\n" + DirectoryName + ":\n\n" + TTLbox1 + " is not a TTL.\n\n TTLs are: \n\n" + "\n".join(TTLNames) + "\n"
                    tkinter.messagebox.showerror('Warning', errormessage)
                TTLbox1 = ''
            if (not (TTLbox2 in TTLNames)):
                if (TTLbox2 != ''):
                    errormessage = "\n" + DirectoryName + ":\n\n" + TTLbox2 + " is not a TTL.\n\n TTLs are: \n\n" + "\n".join(TTLNames) + "\n"
                    tkinter.messagebox.showerror('Warning', errormessage)
                TTLbox2 = ''

        # Save tab-delimited text files for raw data; in structure example: data.streams._405_.data
        if (data):

            if (TTLbox1 != ''):
                SaveRawData(data,TTLbox1,GCaMPbox1,ISOSbox1,RawEventTTLtoggle,DownSampleToggle,DownSampleChoice,DownSampleNumber,SubPathName)
            if (TTLbox2 != ''):
                SaveRawData(data,TTLbox2,GCaMPbox2,ISOSbox2,RawEventTTLtoggle,DownSampleToggle,DownSampleChoice,DownSampleNumber,SubPathName)


    tkinter.messagebox.showinfo('   DONE   ', 'DONE')

    return

   





def noClose():
    pass   





def SetDownSampleDefault(DownSampleRadio, DownSampleCheckVar):
    if (DownSampleRadio.get() > 0 and DownSampleCheckVar.get() == 0):
        DownSampleRadio.set(0)
    elif (DownSampleRadio.get() == 0 and DownSampleCheckVar.get() > 0):
        DownSampleRadio.set(2)

    



def terminate(root):
    root.destroy()
    sys.exit()

