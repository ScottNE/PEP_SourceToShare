#!/usr/bin/env python
# coding: utf-8

import RawDataExtract
import PeriEventExtract
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk
import base64




def SaveSettings(*args):
    
    SettingsFileName = tkinter.filedialog.asksaveasfilename(title="Save Settings", defaultextension=".txt",initialfile = "PEP_Settings.txt")
    if (SettingsFileName == ''):
        return

    SettingsFileStream1 = open(SettingsFileName, 'w')
    SettingsFileStream1.write(RawIsos1Entry.get() + "\n")
    SettingsFileStream1.write(RawIsos2Entry.get() + "\n")
    SettingsFileStream1.write(RawGCaMP1Entry.get() + "\n")
    SettingsFileStream1.write(RawGCaMP2Entry.get() + "\n")
    SettingsFileStream1.write(RawTTLBox1Entry.get() + "\n")
    SettingsFileStream1.write(RawTTLBox2Entry.get() + "\n")
    SettingsFileStream1.write(str(RawEventTTLtoggleVar.get()) + "\n")
    SettingsFileStream1.write(str(RawDownSampleCheckVar.get()) + "\n")
    if(RawDownSampleCheckVar.get() == 1):
        if (RawDownSampleRadio.get() == 1):
            SettingsFileStream1.write("1\n")
            SettingsFileStream1.write("0\n")
        elif (RawDownSampleRadio.get() == 2):
            SettingsFileStream1.write("0\n")
            SettingsFileStream1.write("1\n")
    else:
        SettingsFileStream1.write("0\n")
        SettingsFileStream1.write("0\n")
    SettingsFileStream1.write(RawDownSampleEntry.get() + "\n")
    
    SettingsFileStream1.write(PeriEventEpocEntry.get() + "\n")
    SettingsFileStream1.write(PeriEventBitNumEntry.get() + "\n")
    SettingsFileStream1.write(str(PeriEventTTLtoggleVar.get()) + "\n")
    SettingsFileStream1.write(str(PeriEventWriteTransposedVar.get()) + "\n")
    SettingsFileStream1.write(str(PeriEventSetEpochRangeVar.get()) + "\n")
    SettingsFileStream1.write(str(PeriEventStartTTLEntry.get()) + "\n")
    SettingsFileStream1.write(str(PeriEventEndTTLEntry.get()) + "\n")
    SettingsFileStream1.write(PeriEventIsosEntry.get() + "\n")
    SettingsFileStream1.write(PeriEventGCaMPEntry.get() + "\n")
    SettingsFileStream1.write(PeriEventSamplesToAverageEntry.get() + "\n")
    SettingsFileStream1.write(PeriEventStartWindowEntry.get() + "\n")
    SettingsFileStream1.write(PeriEventEndWindowEntry.get() + "\n")
    SettingsFileStream1.write(PeriEventBaselineStartEntry.get() + "\n")
    SettingsFileStream1.write(PeriEventBaselineEndEntry.get() + "\n")
    SettingsFileStream1.write(str(PeriEventFitToIsoVar.get()) + "\n")
    
    SettingsFileStream1.close




def LoadSettings(*args):
    
    SettingsFileName = tkinter.filedialog.askopenfilename(title="Load Settings", defaultextension=".txt",initialfile = "PEP_Settings.txt")
    if (SettingsFileName == ''):
        return

    SettingsFileStream1 = open(SettingsFileName, 'r')
    
    RawIsos1 = SettingsFileStream1.readline().rstrip()
    RawIsos2 = SettingsFileStream1.readline().rstrip()
    RawGCaMP1 = SettingsFileStream1.readline().rstrip()
    RawGCaMP2 = SettingsFileStream1.readline().rstrip()
    RawTTLBox1 = SettingsFileStream1.readline().rstrip()
    RawTTLBox2 = SettingsFileStream1.readline().rstrip()
    RawTTLtoggle = SettingsFileStream1.readline().rstrip()
    RawDownSample = SettingsFileStream1.readline().rstrip()
    RawDownSampleRemoveEveryNth = SettingsFileStream1.readline().rstrip()
    RawDownSampleKeepEveryN = SettingsFileStream1.readline().rstrip()
    RawDownSampleN = SettingsFileStream1.readline().rstrip()

    PeriEventEpoc = SettingsFileStream1.readline().rstrip()
    PeriEventBitNum = SettingsFileStream1.readline().rstrip()
    PeriEventTTLtoggleCheck = SettingsFileStream1.readline().rstrip()
    PeriEventWriteTransposedCheck = SettingsFileStream1.readline().rstrip()
    PeriEventSetEpochRange = SettingsFileStream1.readline().rstrip()
    PeriEventStartTTL = SettingsFileStream1.readline().rstrip()
    PeriEventEndTTL = SettingsFileStream1.readline().rstrip()
    PeriEventIsos = SettingsFileStream1.readline().rstrip()
    PeriEventGCaMP = SettingsFileStream1.readline().rstrip()
    PeriEventSamplesToAverage = SettingsFileStream1.readline().rstrip()
    PeriEventStartWindow = SettingsFileStream1.readline().rstrip()
    PeriEventEndWindow = SettingsFileStream1.readline().rstrip()
    PeriEventBaselineStart = SettingsFileStream1.readline().rstrip()
    PeriEventBaselineEnd = SettingsFileStream1.readline().rstrip()
    PeriEventFitToIsosbesticCheck = SettingsFileStream1.readline().rstrip()

    SettingsFileStream1.close

    RawIsos1Entry.delete(0,'end')
    RawIsos1Entry.insert(0,RawIsos1)
    RawIsos2Entry.delete(0,'end')
    RawIsos2Entry.insert(0,RawIsos2)
    RawGCaMP1Entry.delete(0,'end')
    RawGCaMP1Entry.insert(0,RawGCaMP1)
    RawGCaMP2Entry.delete(0,'end')
    RawGCaMP2Entry.insert(0,RawGCaMP2)
    RawTTLBox1Entry.delete(0,'end')
    RawTTLBox1Entry.insert(0,RawTTLBox1)
    RawTTLBox2Entry.delete(0,'end')
    RawTTLBox2Entry.insert(0,RawTTLBox2)
    if (RawTTLtoggle == '1'):
        RawEventTTLtoggle.select()
    elif (RawTTLtoggle == '0'):
        RawEventTTLtoggle.deselect()
    if (RawDownSample == '1'):
        RawDownSampleCheck.select()
    elif (RawDownSample == '0'):
        RawDownSampleCheck.deselect()
    if(RawDownSample == '1'):
        if (RawDownSampleRemoveEveryNth == '1'):
            RawDownSampleRadio.set(1)
        if (RawDownSampleKeepEveryN == '1'):
            RawDownSampleRadio.set(2)
    RawDownSampleEntry.delete(0,'end')
    RawDownSampleEntry.insert(0,RawDownSampleN)

    PeriEventEpocEntry.delete(0,'end')
    PeriEventEpocEntry.insert(0,PeriEventEpoc)
    if (PeriEventBitNum):
        PeriEventBitNumEntry.delete(0,'end')
        PeriEventBitNumEntry.insert(0,PeriEventBitNum)
    else:
         PeriEventBitNumEntry.delete(0,'end')   
    if (PeriEventTTLtoggleCheck == '1'):
        PeriEventTTLtoggle.select()
    elif (PeriEventTTLtoggleCheck == '0'):
        PeriEventTTLtoggle.deselect()
    if (PeriEventWriteTransposedCheck == '1'):
        PeriEventWriteTransposed.select()
    elif (PeriEventWriteTransposedCheck == '0'):
        PeriEventWriteTransposed.deselect()
    if (PeriEventSetEpochRange == '1'):
        PeriEventSetEpochRangeCheck.select()
    elif (PeriEventSetEpochRange == '0'):
        PeriEventSetEpochRangeCheck.deselect()
    if (PeriEventSetEpochRange == '1'):
        PeriEventStartTTLEntry.config(state='enabled')
        PeriEventStartTTLEntry.delete(0,'end')
        PeriEventStartTTLEntry.insert(0,PeriEventStartTTL)
        PeriEventEndTTLEntry.config(state='enabled')
        PeriEventEndTTLEntry.delete(0,'end')
        PeriEventEndTTLEntry.insert(0,PeriEventEndTTL)
    PeriEventIsosEntry.delete(0,'end')
    PeriEventIsosEntry.insert(0,PeriEventIsos)
    PeriEventGCaMPEntry.delete(0,'end')
    PeriEventGCaMPEntry.insert(0,PeriEventGCaMP)
    PeriEventSamplesToAverageEntry.delete(0,'end')
    PeriEventSamplesToAverageEntry.insert(0,PeriEventSamplesToAverage)
    PeriEventStartWindowEntry.delete(0,'end')
    PeriEventStartWindowEntry.insert(0,PeriEventStartWindow)
    PeriEventEndWindowEntry.delete(0,'end')
    PeriEventEndWindowEntry.insert(0,PeriEventEndWindow)
    PeriEventBaselineStartEntry.delete(0,'end')
    PeriEventBaselineStartEntry.insert(0,PeriEventBaselineStart)
    PeriEventBaselineEndEntry.delete(0,'end')
    PeriEventBaselineEndEntry.insert(0,PeriEventBaselineEnd)
    if (PeriEventFitToIsosbesticCheck == '1'):
        PeriEventFitToIsosbestic.select()
    elif (PeriEventFitToIsosbesticCheck == '0'):
        PeriEventFitToIsosbestic.deselect()





def noClose():
    pass   



root_DataExport = tkinter.Tk()

icon = 'AAABAAEAMDAAAAEAIACoJQAAFgAAACgAAAAwAAAAYAAAAAEAIAAAAAAAgCUAAAAAAAAAAAAAAAAAAAAAAAAAAAD/AAAA/wAAAP8AAAD/VQIN/gQI//8ECP//BAj//wQI//8ECP//BAj//wQI//8ECP//BAj//wQI//8ECP//Llv//4D//6oAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP+A//+qgP///wAAAP8AAAD/AAAA/wAAAP8AAAD/gP//qi5b//8ECP//BAj//wQI//8ECP//BAj//wQI//8ECP//BAj//wQI//8AAAD//gcm//4HJv/+Byb/VQIN/hMc//8THP//Exz//xMc//8THP//Exz//xMc//8THP//Exz//xMc//8THP//N2j//4D//6oAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm/wAAAP+A//+qgP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qjdo//8THP//Exz//xMc//8THP//Exz//xMc//8THP//Exz//xMc//8AAAD//gcm//4HJv/+Byb/VQIN/iEw//8hMP//ITD//yEw//8hMP//ITD//yEw//8hMP//ITD//yEw//8hMP//QXX//4D//6oAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm/wAAAP+A//+qgP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qkF1//8hMP//ITD//yEw//8hMP//ITD//yEw//8hMP//ITD//yEw//8AAAD//gcm//4HJv/+Byb/VQIN/i9D//8vQ///L0P//y9D//8vQ///L0P//y9D//8vQ///L0P//y9D//8vQ///SoL//4D//6oAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm/wAAAP+A//+qgP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qkqC//8vQ///L0P//y9D//8vQ///L0P//y9D//8vQ///L0P//y9D//8AAAD//gcm//4HJv/+Byb/VQIN/jxV//88Vf//PFX//zxV//88Vf//PFX//zxV//88Vf//PFX//zxV//88Vf//U47//4D//6oAAAD//gcm//4HJv8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP+A///igP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qlOO//88Vf//PFX//zxV//88Vf//PFX//zxV//88Vf//PFX//zxV//8AAAD//gcm//4HJv/+Byb/VQIN/khm//9IZv//SGb//0hm//9IZv//SGb//0hm//9IZv//SGb//0hm//9IZv//W5n//4D//6oAAAD//gcm//4HJv8AAAD/gP//4oD///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qluZ//9IZv//SGb//0hm//9IZv//SGb//0hm//9IZv//SGb//0hm//8AAAD//gcm//4HJv/+Byb/VQIN/lN3//9Td///U3f//1N3//9Td///U3f//1N3//9Td///U3f//1N3//9Td///YqT//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qmKk//9Td///U3f//1N3//9Td///U3f//1N3//9Td///U3f//1N3//8AAAD//gcm//4HJv/+Byb/VQIN/lyF//9chf//XIX//1yF//9chf//XIX//1yF//9chf//XIX//1yF//9chf//aK7//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qmiu//9chf//XIX//1yF//9chf//XIX//1yF//9chf//XIX//1yF//8AAAD//gcm//4HJv/+Byb/VQIN/mWU//9llP//ZZT//2WU//9llP//ZZT//2WU//9llP//ZZT//2WU//9llP//brf//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qm63//9llP//ZZT//2WU//9llP//ZZT//2WU//9llP//ZZT//2WU//8AAAD//gcm//4HJv/+Byb/VQIN/m6h//9uof//bqH//26h//9uof//bqH//26h//9uof//bqH//26h//9uof//dMD//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qnTA//9uof//bqH//26h//9uof//bqH//26h//9uof//bqH//26h//8AAAD//gcm//4HJv/+Byb/VQIN/nWu//91rv//da7//3Wu//91rv//da7//3Wu//91rv//da7//3Wu//91rv//ecn//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qnnJ//91rv//da7//3Wu//91rv//da7//3Wu//91rv//da7//3Wu//8AAAD//gcm//4HJv/+Byb/VQIN/nu6//97uv//e7r//3u6//97uv//e7r//3u6//97uv//e7r//3u6//97uv//fdH//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qn3R//97uv//e7r//3u6//97uv//e7r//3u6//97uv//e7r//3u6//8AAAD//gcm//4HJv/+Byb/VQIN/oHF//+Bxf//gcX//4HF//+Bxf//gcX//4HF//+Bxf//gcX//4HF//+Bxf//gdj//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoHY//+Bxf//gcX//4HF//+Bxf//gcX//4HF//+Bxf//gcX//4HF//8AAAD//gcm//4HJv/+Byb/VQIN/obO//+Gzv//hs7//4bO//+Gzv//hs7//4bO//+Gzv//hs7//4bO//+Gzv//hN///4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoTf//+Gzv//hs7//4bO//+Gzv//hs7//4bO//+Gzv//hs7//4bO//8AAAD//gcm//4HJv/+Byb/VQIN/onX//+J1///idf//4nX//+J1///idf//4nX//+J1///idf//4nX//+J1///huT//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qobk//+J1///idf//4nX//+J1///idf//4nX//+J1///idf//4nX//8AAAD//gcm//4HJv/+Byb/VQIN/ozf//+M3///jN///4zf//+M3///jN///4zf//+M3///jN///4zf//+M3///iOr//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qojq//+M3///jN///4zf//+M3///jN///4zf//+M3///jN///4zf//8AAAD//gcm//4HJv/+Byb/VQIN/o7m//+O5v//jub//47m//+O5v//jub//47m//+O5v//jub//47m//+O5v//ie///4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qonv//+O5v//jub//47m//+O5v//jub//47m//+O5v//jub//47m//8AAAD//gcm//4HJv/+Byb/VQIN/o7t//+O7f//ju3//47t//+O7f//ju3//47t//+O7f//ju3//47t//+O7f//ivP//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qorz//+O7f//ju3//47t//+O7f//ju3//47t//+O7f//ju3//47t//8AAAD//gcm//4HJv/+Byb/VQIN/o/y//+P8v//j/L//4/y//+P8v//j/L//4/y//+P8v//j/L//4/y//+P8v//ivb//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qor2//+P8v//j/L//4/y//+P8v//j/L//4/y//+P8v//j/L//4/y//8AAAD//gcm//4HJv/+Byb/VQIN/o72//+O9v//jvb//472//+O9v//jvb//472//+O9v//jvb//472//+O9v//ifn//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qon5//+O9v//jvb//472//+O9v//jvb//472//+O9v//jvb//472//8AAAD//gcm//4HJv/+Byb/VQIN/4z6//+M+v//jPr//4z6//+M+v//jPr//4z6//+M+v//jPr//4z6//+M+v//iPz//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoj8//+M+v//jPr//4z6//+M+v//jPr//4z6//+M+v//jPr//4z6//8AAAD//gcm//4HJv/+Byb/VQIN/4f9//+H/f//h/3//4f9//+H/f//h/3//4f9//+J/f//ifz//4n8//+J/P//hv3//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoT+//+H/f//h/3//4f9//+H/f//h/3//4f9//+H/f//ifz//4n8//8AAAD//gcm//4HJv/+Byb/VQIN/4D//6qA//+qgP//qoD//6qA//+qgP//qoD//6qA//+qhP7/44b+//+G/v//hP7//4D//6oAAAD//gcm//4HJv8AAAD/gP//jYD//6qA//+qgP//qoD//6qA///GgP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//cYD//6qA//+qgP//qoD//6qA//+qgP//qoD//6qA//+qg////4X+//8AAAD//gcm//4HJv/+Byb/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/VQIN/oH//+KB////gf///4D//6oAAAD//gcm//4HJv8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/gP//xoD///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/eO7uW4D///8AAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb/4QYi/zgCCP6C////gv///4D//6oAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///wAAAP/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv8AAAD/AAAA/4D//3EAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm/1UCDf6F/v//hf7//4D//6oAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///wAAAP/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb/AAAA/4D//1UAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm/1UCDf6H/f//h/3//4D//6oAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///wAAAP/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb/AAAA/4D//1UAAAD//gcm//4HJv/+Byb/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP/+Byb//gcm/3EDEf6G/P/kifv//4D//6oAAAD//gcm//4HJv8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/gP//xoD///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA//4HJv/+Byb/AAAA/4D//1UAAAD//gcm//4HJv/+Byb/AAAA/4D//6qA//+qgP//qoD//6qA//+qgP//cQAAAP/+Byb//gcm/+EGIv84Agj+hfz//4D//6oAAAD//gcm//4HJv8AAAD/gP//jYD//6qA//+qgP//qoD//6qA///GgP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//cYD//6qA//+qgP//qoD//6qA//+qAAAA//4HJv/+Byb/AAAA/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP//qgAAAP8AAAD//gcm//4HJv9VAg3+hfv//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////AAAA/wAAAP/+Byb//gcm/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP///4D//3EAAAD//gcm//4HJv9VAg3+hfn//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////gP//4gAAAP/+Byb//gcm/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP///4D//6oAAAD//gcm//4HJv9VAg3+hfb//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP///4D//6oAAAD//gcm//4HJv9VAg3+hPT//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP///4D//6oAAAD//gcm//4HJv9VAg3+g/H//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP///4D//6oAAAD//gcm//4HJv9VAg3+gu7//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP///4D//6oAAAD//gcm//4HJv9VAg3+gOv//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP///4D//6oAAAD//gcm//4HJv9VAg3+fuj//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP///4D//6oAAAD//gcm//4HJv9VAg3+fOP//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP///4D//6oAAAD//gcm//4HJv9VAg3+et///4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP///4D//6oAAAD//gcm//4HJv9VAg3+d9v//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP///4D//6oAAAD//gcm//4HJv9VAg3+dNb//4D//6oAAAD//gcm//4HJv8AAAD/gP///4D///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP//xgAAAP8AAAD//gcm//4HJv9VAg3+cdH//4D//6oAAAD//gcm//4HJv8AAAD/gP//4oD///+A////gP///4D///+A////gP///4D///+A////gP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////AAAA/wAAAP/+Byb//gcm/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/4D///+A////gP///4D///+A////gP//qgAAAP/+Byb//gcm//4HJv9VAg3+bcz//4D//6oAAAD//gcm//4HJv8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP+A///igP///wAAAP/+Byb//gcm//4HJv8AAAD/gP//qoD///+A////gP///4D///+A////AAAA//4HJv/+Byb/AAAA/wAAAP8AAAD//gcm//4HJv/+Byb/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP/+Byb//gcm/4wEFf+R///gheX//4D//6oAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm/wAAAP+A//+qgP///wAAAP/+Byb//gcm//4HJv8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA//4HJv/+Byb/AAAA/5T//6wAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm/1UCDf6J8///hu3//4D//6oAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm/wAAAP+A//+qgP///wAAAP/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb/AAAA/4///+8AAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm/1UCDf6C8f//c9T//4D//6oAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm/wAAAP+A//+qgP///wAAAP/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb/AAAA/4n///MAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm/1UCDf545v//eOb//4D//6oAAAD//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm/wAAAP+A//+qgP///wAAAP/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv/+Byb//gcm//4HJv8AAAD/AAAA/4X///gAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/jAQV/4D//41my///den//4D//6oAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP+A//+qgP///wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/ffn5yID//+UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='

icondata= base64.b64decode(icon)
## The temp file is icon.ico
BJIcon = "icon.ico"
iconfile = open(BJIcon,"wb")
## Extract the icon
iconfile.write(icondata)
iconfile.close()

# dir = os.getcwd()
# print(dir)
# BJIcon = dir + '\BJ_FPhot.ico'

root_DataExport.iconbitmap(BJIcon)
root_DataExport.title("PeriEventPlus")

s = ttk.Style()
s.configure('TNotebook.Tab', font=('Helevitica','12','bold') , foreground='dark blue')

tab_parent = ttk.Notebook(root_DataExport)

RawDataExportTab = ttk.Frame(tab_parent,borderwidth=10,relief='raised')
PeriEventDataExportTab = ttk.Frame(tab_parent,borderwidth=10,relief='raised')

tab_parent.add(RawDataExportTab, text="Export Raw Data", padding='0.1i')
tab_parent.add(PeriEventDataExportTab, text="Export PeriEventData", padding='0.1i')

tab_parent.pack(expand=True, fill='both')



PeriEventProcessbutton = tkinter.Button(PeriEventDataExportTab, text = 'Process directories', activebackground = 'green', padx=50, pady=10, bd = 5, command = lambda: PeriEventExtract.CommonProcess(PeriEventEpocEntry,PeriEventBitNumEntry,PeriEventTTLtoggleVar.get(),PeriEventWriteTransposedVar.get(),PeriEventFitToIsoVar.get(),PeriEventSetEpochRangeVar.get(),PeriEventStartTTLEntry,PeriEventEndTTLEntry,PeriEventIsosEntry,PeriEventGCaMPEntry,PeriEventSamplesToAverageEntry,PeriEventStartWindowEntry,PeriEventEndWindowEntry,PeriEventBaselineStartEntry,PeriEventBaselineEndEntry)) 
PeriEventProcessbutton.grid(row=1,pady=20,padx=5,column=1,columnspan=3,sticky="ew")

PeriEventEpocEntryText = tkinter.Label(PeriEventDataExportTab, bd = 5, text="Epoc label: ")
PeriEventEpocEntryText.grid(row=2,column=1,sticky="w")

PeriEventEpocEntry = tkinter.Entry(PeriEventDataExportTab, bd = 5, width = 15)
PeriEventEpocEntry.grid(row=2,column=1,sticky="e")
PeriEventEpocEntry.insert(0,"BOX1")

PeriEventBitNumEntryText = tkinter.Label(PeriEventDataExportTab, bd = 5, text="    Bit#: ")
PeriEventBitNumEntryText.grid(row=3,column=1,sticky="w")

PeriEventBitNumEntry = tkinter.Entry(PeriEventDataExportTab, bd = 5, width = 15)
PeriEventBitNumEntry.grid(row=3,column=1,sticky="e")
PeriEventBitNumEntry.insert(0,"3")

PeriEventTTLtoggleVar = tkinter.IntVar()
PeriEventTTLtoggle = tkinter.Checkbutton(PeriEventDataExportTab, bd = 5, text="Single toggle bit(0 or 1)?", variable = PeriEventTTLtoggleVar, command = lambda: PeriEventExtract.SetToggleTTLDefault(PeriEventTTLtoggleVar,PeriEventBitNumEntry))
PeriEventTTLtoggle.grid(row=4,column=1,sticky="e")

PeriEventWriteTransposedVar = tkinter.IntVar()
PeriEventWriteTransposed = tkinter.Checkbutton(PeriEventDataExportTab, bd = 5, text="Write transposed data files?", variable = PeriEventWriteTransposedVar)
PeriEventWriteTransposed.grid(row=5,column=1,sticky="w")

PeriEventRowForSpace = tkinter.Label(PeriEventDataExportTab, bd = 5, text=" ")
PeriEventRowForSpace.grid(row=6,column=1,sticky="w")

PeriEventSetEpochRangeVar = tkinter.IntVar()
PeriEventSetEpochRangeCheck = tkinter.Checkbutton(PeriEventDataExportTab, text = "Restrict Epoch range?", variable = PeriEventSetEpochRangeVar, command = lambda: PeriEventExtract.SetRangeDefault(PeriEventSetEpochRangeVar,PeriEventStartTTLEntry,PeriEventEndTTLEntry))
PeriEventSetEpochRangeCheck.grid(row=8,column=1,sticky="sw")

PeriEventStartTTLText = tkinter.Label(PeriEventDataExportTab, bd = 5, text="Start at Epoc#: ")
PeriEventStartTTLText.grid(row=9,column=1,sticky="w")

PeriEventStartTTLEntry = tkinter.Entry(PeriEventDataExportTab, bd = 5, width = 15)
PeriEventStartTTLEntry.grid(row=9,column=1,sticky="e")
PeriEventStartTTLEntry.insert(0,"1")
PeriEventStartTTLEntry.config(state='disabled')

PeriEventEndTTLText = tkinter.Label(PeriEventDataExportTab, bd = 5, text="End at Epoc#: ")
PeriEventEndTTLText.grid(row=10,column=1,sticky="w")

PeriEventEndTTLEntry = tkinter.Entry(PeriEventDataExportTab, bd = 5, width = 15)
PeriEventEndTTLEntry.grid(row=10,column=1,sticky="e")
PeriEventEndTTLEntry.insert(0,"25")
PeriEventEndTTLEntry.config(state='disabled')

PeriEventRowForSpace3 = tkinter.Label(PeriEventDataExportTab, bd = 5, text=" ")
PeriEventRowForSpace3.grid(row=11,column=1,sticky="w")

PeriEventIsosEntryText = tkinter.Label(PeriEventDataExportTab, bd = 5, text="Isosbestic label: ")
PeriEventIsosEntryText.grid(row=12,column=1,sticky="w")

PeriEventIsosEntry = tkinter.Entry(PeriEventDataExportTab, bd = 5, width = 15)
PeriEventIsosEntry.grid(row=12,column=1,sticky="e")
PeriEventIsosEntry.insert(0,"_405A")

PeriEventGCaMPEntryText = tkinter.Label(PeriEventDataExportTab, bd = 5, text="'GCaMP' label: ")
PeriEventGCaMPEntryText.grid(row=13,column=1,sticky="w")

PeriEventGCaMPEntry = tkinter.Entry(PeriEventDataExportTab, bd = 5, width = 15)
PeriEventGCaMPEntry.grid(row=13,column=1,sticky="e")
PeriEventGCaMPEntry.insert(0,"_470A")

PeriEventRowForSpace4 = tkinter.Label(PeriEventDataExportTab, bd = 5, text=" ")
PeriEventRowForSpace4.grid(row=14,column=1,sticky="w")

PeriEventSamplesToAverageText = tkinter.Label(PeriEventDataExportTab, bd = 13, text="Samples to average: ")
PeriEventSamplesToAverageText.grid(row=15,column=1,sticky="w")

PeriEventSamplesToAverageEntry = tkinter.Entry(PeriEventDataExportTab, bd = 5, width = 15)
PeriEventSamplesToAverageEntry.grid(row=15,column=1,sticky="e")
PeriEventSamplesToAverageEntry.insert(0,"10")

PeriEventRowForSpace5 = tkinter.Label(PeriEventDataExportTab, bd = 5, text=" ")
PeriEventRowForSpace5.grid(row=15,column=1,sticky="w")

PeriEventStartWindowEntryText = tkinter.Label(PeriEventDataExportTab, bd = 5, text="Time before Epoc (sec): ")
PeriEventStartWindowEntryText.grid(row=16,column=1,sticky="w")

PeriEventStartWindowEntry = tkinter.Entry(PeriEventDataExportTab, bd = 5, width = 15)
PeriEventStartWindowEntry.grid(row=16,column=1,sticky="e")
PeriEventStartWindowEntry.insert(0,"-10")

PeriEventEndWindowEntryText = tkinter.Label(PeriEventDataExportTab, bd = 5, text="Time after Epoc (sec): ")
PeriEventEndWindowEntryText.grid(row=17,column=1,sticky="w")

PeriEventEndWindowEntry = tkinter.Entry(PeriEventDataExportTab, bd = 5, width = 15)
PeriEventEndWindowEntry.grid(row=17,column=1,sticky="e")
PeriEventEndWindowEntry.insert(0,"20")

PeriEventRowForSpace6 = tkinter.Label(PeriEventDataExportTab, bd = 5, text=" ")
PeriEventRowForSpace6.grid(row=18,column=1,sticky="w")

PeriEventBaselineStartEntryText = tkinter.Label(PeriEventDataExportTab, bd = 5, text="Baseline start(sec): ")
PeriEventBaselineStartEntryText.grid(row=19,column=1,sticky="w")

PeriEventBaselineStartEntry = tkinter.Entry(PeriEventDataExportTab, bd = 5, width = 15)
PeriEventBaselineStartEntry.grid(row=19,column=1,sticky="e")
PeriEventBaselineStartEntry.insert(0,"-10")

PeriEventBaselineEndEntryText = tkinter.Label(PeriEventDataExportTab, bd = 5, text="Baseline end(sec): ")
PeriEventBaselineEndEntryText.grid(row=20,column=1,sticky="w")

PeriEventBaselineEndEntry = tkinter.Entry(PeriEventDataExportTab, bd = 5, width = 15)
PeriEventBaselineEndEntry.grid(row=20,column=1,sticky="e")
PeriEventBaselineEndEntry.insert(0,"-6")

PeriEventRowForSpace7 = tkinter.Label(PeriEventDataExportTab, bd = 5, text=" ")
PeriEventRowForSpace7.grid(row=21,column=1,sticky="w")

PeriEventFitToIsoVar = tkinter.IntVar()
PeriEventFitToIsosbestic = tkinter.Checkbutton(PeriEventDataExportTab, bd = 5, text="Fit to Isosbestic?", variable = PeriEventFitToIsoVar)
PeriEventFitToIsosbestic.grid(row=22,column=1,sticky="w")

PeriEventLoadSettingsButton = tkinter.Button(PeriEventDataExportTab, text = 'Load Settings', padx=15, pady=5, bd = 5, command = lambda: LoadSettings())
PeriEventLoadSettingsButton.grid(row=23,column=1,padx=5,pady=20,sticky="w")

PeriEventSaveSettingsButton = tkinter.Button(PeriEventDataExportTab, text = 'Save Settings', padx=15, pady=5, bd = 5, command = lambda: SaveSettings())
PeriEventSaveSettingsButton.grid(row=23,column=1,padx=5,pady=20,sticky="e")

PeriEventQuitButton = tkinter.Button(PeriEventDataExportTab, text = 'Quit', activebackground = 'red', padx=113, pady=10, bd = 5, command =  lambda: PeriEventExtract.terminate(root_DataExport))
PeriEventQuitButton.grid(row=24,column=1,padx=5)





RawProcessbutton = tkinter.Button(RawDataExportTab, text = 'Process directories', activebackground = 'green', padx=50, pady=10, bd = 5, command = lambda: RawDataExtract.CommonProcess(RawIsos1Entry,RawIsos2Entry,RawGCaMP1Entry,RawGCaMP2Entry,RawTTLBox1Entry,RawTTLBox2Entry,RawEventTTLtoggleVar,RawDownSampleCheckVar,RawDownSampleRadio,RawDownSampleEntry)) 
RawProcessbutton.grid(row=1,pady=20,padx=5,column=1,columnspan=3,sticky="ew")

RawIsosEntryText = tkinter.Label(RawDataExportTab, bd = 5, text="Isosbestic labels: ")
RawIsosEntryText.grid(row=2,column=1,sticky="w")

RawIsos1Entry = tkinter.Entry(RawDataExportTab, bd = 5, width = 15)
RawIsos1Entry.grid(row=2,column=2,sticky="e")
RawIsos1Entry.insert(0,"_405A")

RawIsos2Entry = tkinter.Entry(RawDataExportTab, bd = 5, width = 15)
RawIsos2Entry.grid(row=2,column=3,sticky="w")
RawIsos2Entry.insert(0,"_405B")

RawGCaMPEntryText = tkinter.Label(RawDataExportTab, bd = 5, text="'GCaMP' labels: ")
RawGCaMPEntryText.grid(row=3,column=1,sticky="w")

RawGCaMP1Entry = tkinter.Entry(RawDataExportTab, bd = 5, width = 15)
RawGCaMP1Entry.grid(row=3,column=2,sticky="e")
RawGCaMP1Entry.insert(0,"_470A")

RawGCaMP2Entry = tkinter.Entry(RawDataExportTab, bd = 5, width = 15)
RawGCaMP2Entry.grid(row=3,column=3,sticky="w")
RawGCaMP2Entry.insert(0,"_470B")

RawTTLEntryText = tkinter.Label(RawDataExportTab, bd = 5, text="TTL labels: ")
RawTTLEntryText.grid(row=4,column=1,sticky="w")

RawTTLBox1Entry = tkinter.Entry(RawDataExportTab, bd = 5, width = 15)
RawTTLBox1Entry.grid(row=4,column=2,sticky="e")
RawTTLBox1Entry.insert(0,"BOX1")

RawTTLBox2Entry = tkinter.Entry(RawDataExportTab, bd = 5, width = 15)
RawTTLBox2Entry.grid(row=4,column=3,sticky="w")
RawTTLBox2Entry.insert(0,"BOX2")

RawEventTTLtoggleVar = tkinter.IntVar()
RawEventTTLtoggle = tkinter.Checkbutton(RawDataExportTab, bd = 5, text="Single toggle bit(0 or 1)?", variable = RawEventTTLtoggleVar, command = lambda: RawDataExtract.SetToggleTTLDefault(RawEventTTLtoggleVar,RawTTLBox1Entry,RawTTLBox2Entry))
RawEventTTLtoggle.grid(row=5,column=1,sticky="w")

RawEventSpace1 = tkinter.Label(PeriEventDataExportTab, bd = 5, text=" ")
RawEventSpace1.grid(row=6,column=1,sticky="w")

RawDownSampleCheckVar = tkinter.IntVar()
RawDownSampleCheck = tkinter.Checkbutton(RawDataExportTab, text = "Down sample?", variable = RawDownSampleCheckVar, command = lambda: RawDataExtract.SetDownSampleDefault(RawDownSampleRadio, RawDownSampleCheckVar))
RawDownSampleCheck.grid(row=7,column=1,sticky="w")

RawDownSampleRadio = tkinter.IntVar()
RawDownSampleRemoveEveryNth = tkinter.Radiobutton(RawDataExportTab, text="Remove every Nth number", variable=RawDownSampleRadio, value=1)
RawDownSampleRemoveEveryNth.grid(row=8,column=1,sticky="w")

RawDownSampleKeepEveryN = tkinter.Radiobutton(RawDataExportTab, text="Keep every Nth number", variable=RawDownSampleRadio, value=2)
RawDownSampleKeepEveryN.grid(row=9,column=1,sticky="w")

RawDownSampleEntryText = tkinter.Label(RawDataExportTab, text="N =")
RawDownSampleEntryText.grid(row=9,column=2,sticky="w")

RawDownSampleEntry = tkinter.Entry(RawDataExportTab, bd = 5, width = 15)
RawDownSampleEntry.grid(row=9,column=2,sticky="e")
RawDownSampleEntry.insert(0,"2")

RawEventSpace2 = tkinter.Label(PeriEventDataExportTab, bd = 5, text=" ")
RawEventSpace2.grid(row=11,column=1,sticky="w")

RawEventLoadSettingsButton = tkinter.Button(RawDataExportTab, text = 'Load Settings', padx=20, pady=5, bd = 5, command =  lambda: LoadSettings())
RawEventLoadSettingsButton.grid(row=15,column=1,padx=5)

RawEventSaveSettingsButton = tkinter.Button(RawDataExportTab, text = 'Save Settings', padx=20, pady=5, bd = 5, command =  lambda: SaveSettings())
RawEventSaveSettingsButton.grid(row=15,column=2,padx=5)

RawQuitButton = tkinter.Button(RawDataExportTab, text = 'Quit', activebackground = 'red', padx=86, pady=10, bd = 5, command =  lambda: RawDataExtract.terminate(root_DataExport))
RawQuitButton.grid(row=18,pady=20,padx=5,column=1,columnspan=3,sticky="ew")

RawDataExportTab.grid_rowconfigure(6, weight=1)
RawDataExportTab.grid_rowconfigure(11, weight=1)


tab_parent.select(PeriEventDataExportTab)


root_DataExport.protocol("WM_DELETE_WINDOW",noClose)


while (1): root_DataExport.mainloop()

# The above while loop should not be necessary, but without it
#  the 'PeriEvent' tab causes the application to quite after it runs
#  its 'CommonProcess' function.
# 