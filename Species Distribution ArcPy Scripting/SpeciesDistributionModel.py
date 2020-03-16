# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# SpeciesDistributionModel.py
# Created on: 2020-03-10 20:04:48.00000
# Created By: Daniel Carter
# Description: A simple script that takes
#					-1 Each Data set relating to species events
#					-4 Each Rasters containing environmental variables
#				Then calculates a rastor of 'hazard or possible areas the species exists.'
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
from arcpy import env 
from arcpy.sa import *


# Local variables:
Lymantria_Dispar_Events = "Lymantria_Dispar_Events"
LDEvents = "LDEvents"
Landcover = "Landcover"
LDEventsLandCover = "LDEvents"
US_Elevation = "US Elevation"
LDEventElevation = "LDEvents"
LDElevStats = "C:\\Users\\danny\\OneDrive\\Documents\\ArcGIS\\Default.gdb\\LDElevStats"
US_precipitation = "US precipitation"
LDEventsPrecipitation = "LDEvents"
LDPrecipStats = "C:\\Users\\danny\\OneDrive\\Documents\\ArcGIS\\Default.gdb\\LDPrecipStats"
US_Annual_Minimum_Temp = "US Annual Minimum Temp"
LDEventsMinimumTemp = "LDEvents"
LDTempStats = "C:\\Users\\danny\\OneDrive\\Documents\\ArcGIS\\Default.gdb\\LDTempStats"

arcpy.env.workspace = 'C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project'

arcpy.TableToTable_conversion('C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\Lymantria Dispar - Data\\SpeciesData.csv', 'C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\Lymantria Dispar.gdb', 'LymantriaDispar')
arcpy.management.MakeXYEventLayer('C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\Lymantria Dispar.gdb\\LymantriaDispar', 'decimalLongitude', 'decimalLatitude', 'C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\Lymantria Dispar.gdb\\Lymantria_Dispar_Events')
arcpy.SaveToLayerFile_management('C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\Lymantria Dispar.gdb\\Lymantria_Dispar_Events', 'C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\Lymantria Dispar.gdb\\Lymantria_Dispar_Events')
arcpy.AddMessage("**Species Events Table Converted**")

# Process: Make Feature Layer
arcpy.MakeFeatureLayer_management('C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\Lymantria Dispar.gdb\\Lymantria_Dispar_Events', 'LDEvents', "\"countryCode\" = 'US'", "", "FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;gbifID gbifID VISIBLE NONE;datasetKey datasetKey VISIBLE NONE;occurrence occurrence VISIBLE NONE;kingdom kingdom VISIBLE NONE;phylum phylum VISIBLE NONE;class class VISIBLE NONE;order_ order_ VISIBLE NONE;family family VISIBLE NONE;genus genus VISIBLE NONE;species species VISIBLE NONE;infraspeci infraspeci VISIBLE NONE;taxonRank taxonRank VISIBLE NONE;scientific scientific VISIBLE NONE;verbatimSc verbatimSc VISIBLE NONE;verbatim_1 verbatim_1 VISIBLE NONE;countryCod countryCod VISIBLE NONE;locality locality VISIBLE NONE;stateProvi stateProvi VISIBLE NONE;occurren_1 occurren_1 VISIBLE NONE;individual individual VISIBLE NONE;publishing publishing VISIBLE NONE;decimalLat decimalLat VISIBLE NONE;decimalLon decimalLon VISIBLE NONE;coordinate coordinate VISIBLE NONE;coordina_1 coordina_1 VISIBLE NONE;elevation elevation VISIBLE NONE;elevationA elevationA VISIBLE NONE;depth depth VISIBLE NONE;depthAccur depthAccur VISIBLE NONE;eventDate eventDate VISIBLE NONE;day day VISIBLE NONE;month month VISIBLE NONE;year year VISIBLE NONE;taxonKey taxonKey VISIBLE NONE;speciesKey speciesKey VISIBLE NONE;basisOfRec basisOfRec VISIBLE NONE;institutio institutio VISIBLE NONE;collection collection VISIBLE NONE;catalogNum catalogNum VISIBLE NONE;recordNumb recordNumb VISIBLE NONE;identified identified VISIBLE NONE;dateIdenti dateIdenti VISIBLE NONE;license license VISIBLE NONE;rightsHold rightsHold VISIBLE NONE;recordedBy recordedBy VISIBLE NONE;typeStatus typeStatus VISIBLE NONE;establishm establishm VISIBLE NONE;lastInterp lastInterp VISIBLE NONE;mediaType mediaType VISIBLE NONE;issue issue VISIBLE NONE")
arcpy.SaveToLayerFile_management('LDEvents', 'C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\LDEvents')

arcpy.AddMessage("**Species Events Feature Layer Created**")

# # Process: Landcover Extract Multi Values to Points
arcpy.gp.ExtractMultiValuesToPoints_sa(LDEvents, "Landcover Landcover", "NONE")
arcpy.AddMessage("**Extracted Values from \"Landcover\" Raster**")

# # Process: Elev Extract Multi Values to Points
arcpy.gp.ExtractMultiValuesToPoints_sa(LDEvents, "'US Elevation' US_Eleva_1", "NONE")
arcpy.AddMessage("**Extracted Values from \"Elevation\" Raster**")

# # Process: Precip Extract Multi Values to Points
arcpy.gp.ExtractMultiValuesToPoints_sa(LDEvents, "'US precipitation' US_precipi", "NONE")
arcpy.AddMessage("**Extracted Values from \"Precipitation\" Raster**")

# # Process: Temp Extract Multi Values to Points
arcpy.gp.ExtractMultiValuesToPoints_sa(LDEvents, "'US Annual Minimum Temp' US_Annual", "NONE")
arcpy.AddMessage("**Extracted Values from \"Annual Minimum Temp.\" Raster**")

# # Process: Elevation Summary Statistics
arcpy.Statistics_analysis(LDEventElevation, LDElevStats, "US_Eleva_1 MEAN;US_Eleva_1 STD", "")

# # Process: Precip Summary Statistics
arcpy.Statistics_analysis(LDEventsPrecipitation, LDPrecipStats, "US_precipi MEAN;US_precipi STD", "")

# # Process: Temp Summary Statistics
arcpy.Statistics_analysis(LDEventsMinimumTemp,LDTempStats, "US_Annual MEAN;US_Annual STD", "")

fields = ['MEAN_US_Eleva_1', 'STD_US_Eleva_1']
with arcpy.da.SearchCursor(LDElevStats, fields) as cursor:
	for row in cursor:
		ElevMean = row[0]
		ElevSTD = row[1]

arcpy.AddMessage('Elevation Mean:' + str(ElevMean))
arcpy.AddMessage('Elevation Standard Deviation:' + str(ElevSTD))

ElevSTDhalf = ElevSTD / 2

remapElev = RemapRange([[-1000, ((ElevMean - ElevSTDhalf) - ElevSTD), 0],[((ElevMean - ElevSTDhalf) - ElevSTD), (ElevMean - ElevSTDhalf), 1],[(ElevMean - ElevSTDhalf),(ElevMean + ElevSTDhalf), 2],[(ElevMean + ElevSTDhalf),((ElevMean + ElevSTDhalf) + ElevSTD), 1],[((ElevMean + ElevSTDhalf) + ElevSTD), 5000, 0]])

ElevRe = arcpy.sa.Reclassify(US_Elevation, "Value", remapElev)
ElevReclass = 'ElevReclass'
outputdir = 'C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\'
ElevRe.save(os.path.join(outputdir,ElevReclass))

# Reclassifies a raster off of statistical data

fields = ['MEAN_US_precipi', 'STD_US_precipi']
with arcpy.da.SearchCursor(LDPrecipStats, fields) as cursor:
	for row in cursor:
		precipMean = row[0]
		precipSTD = row[1]

precipSTDhalf = precipSTD / 2

arcpy.AddMessage('Annual Precipitation Mean:' + str(precipMean))
arcpy.AddMessage('Annual Precipitation Standard Deviation:' + str(precipSTD))

remapPrecip = RemapRange([[0, ((precipMean - precipSTDhalf) - precipSTD), 0],[((precipMean - precipSTDhalf) - precipSTD), (precipMean - precipSTDhalf), 1],[(precipMean - precipSTDhalf),(precipMean + precipSTDhalf), 2],[(precipMean + precipSTDhalf),((precipMean + precipSTDhalf) + precipSTD), 1],[((precipMean + precipSTDhalf) + precipSTD), 10000, 0]])

precipRe = arcpy.sa.Reclassify(US_precipitation, "Value", remapPrecip)
precipReclass = 'precipReclass'
outputdir = 'C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\'
precipRe.save(os.path.join(outputdir,precipReclass))

# Relassifies a raster based on Min Temp off of Statistical data

fields = ['MEAN_US_Annual', 'STD_US_Annual']
with arcpy.da.SearchCursor(LDTempStats, fields) as cursor:
	for row in cursor:
		TempMean = row[0]
		TempSTD = row[1]

arcpy.AddMessage('Annual Minimum Temperature Mean:' + str(TempMean))
arcpy.AddMessage('Annual Minimum Temperature Standard Deviation:' + str(TempSTD))

TempSTDhalf = TempSTD / 2

remapTemp = RemapRange([[-80, ((TempMean - TempSTDhalf) - TempSTD), 0],[((TempMean - TempSTDhalf) - TempSTD), (TempMean - TempSTDhalf), 1],[(TempMean - TempSTDhalf),(TempMean + TempSTDhalf), 2],[(TempMean + TempSTDhalf),((TempMean + TempSTDhalf) + TempSTD), 1],[((TempMean + TempSTDhalf) + TempSTD), 4307, 0]])

TempRe = arcpy.sa.Reclassify(US_Annual_Minimum_Temp, "Value", remapTemp)
TempReclass = 'TempReclass'
outputdir = 'C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\'
TempRe.save(os.path.join(outputdir,TempReclass))

# Combines all rasters using RasterAlgebra to create a map showing danger areas of Gypsy Moths

ElevRast = "C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\elevreclass"
PrecipRast = "C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\precipreclass"
TempRast = "C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\tempreclass"

expression = '"elevreclass" * "precipreclass" * "tempreclass"'
arcpy.AddMessage("Calculating final raster...")
arcpy.gp.RasterCalculator_sa(expression, "C:\\Users\\danny\\OneDrive\\Desktop\\ES 342\\Final Project\\FinalProduct")
