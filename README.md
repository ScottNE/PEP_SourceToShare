# PEP
PeriEventPlus FiberPhotomoetry Analysis

TDTfilter had to be corrected. It was not properly setting the ranges for the data. Graphs were cut off.


03/02/2021
Changed the bit numbering for the PeriEvent extraction so that it is the same as the RawDataExtraction; ie, 0-7 rather than 1-8.


03/29/2021
Fixed a heatmap issue. The Y-axis label was reversed because the 'extent' parameter had the Y min and max in the wrong order (if the 'origin' parameter is left to the default of 'upper', the origin (0,0) is at the upper left)

