# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  Shows a cut trough an object in the Z Plane
# Author:       benedikt.strahm@ilek.uni-stuttgart.de
# Created:      04.08.2023
# Execution:    Copy to Abaqus CAE input
# Status:       Done
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------

from abaqus import *
from abaqusConstants import *
import displayGroupMdbToolset as dgm
import displayGroupOdbToolset as dgo

# ------------------------------------------------------------------------------
# Execution
# ------------------------------------------------------------------------------
# 1) Load ODB
# 2) Switch to Vizualisation module
# 3) Copy code do Abaqus CAE

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------

# XY Plane
position = -41.00
plane = 'Z-Plane'
view = 'Back'
minValue = 0
maxValue = 0.90 / 1000
numIntervals = 10
component = 'PEEQ'

# # XZ Plane
# position = 0.00
# plane = 'Y-Plane'
# view = 'Bottom'
# minValue = 0
# maxValue = 0.90 / 1000
# numIntervals = 6
# component = 'PEEQ'

# Change View
o = session.openOdb(name='Concrete_beam_4_P_B.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o)
session.viewports['Viewport: 1'].view.setValues(session.views[view])
session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)

# Create Cut
session.viewports['Viewport: 1'].odbDisplay.setValues(viewCut=ON)
session.viewports['Viewport: 1'].odbDisplay.setValues(
    viewCutNames=(plane, ), viewCut=ON)
session.viewports['Viewport: 1'].odbDisplay.viewCuts[plane].setValues(
    position=position, showModelOnCut=True, showModelBelowCut=False,
    showModelAboveCut=False)

# Coloring by Material
cmap = session.viewports['Viewport: 1'].colorMappings['Material']
session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
session.viewports['Viewport: 1'].disableMultipleColors()
session.viewports['Viewport: 1'].setColor(globalTranslucency=False)

# Select element set by Name
elementSets = ()
# Loop over all instances
for instanceName in o.rootAssembly.instances.keys():
    # Loop over element sets in instance
    for elementSet in o.rootAssembly.instances[instanceName].elementSets.keys():
        if 'BETON' in elementSet:
            elementSets += (instanceName + '.' + elementSet, )
        elif 'VERGUSS' in elementSet:
            elementSets += (instanceName + '.' + elementSet, )

# Replace display group
leaf = dgo.LeafFromElementSets(elementSets=elementSets)
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)

# Show PEEQT
# -----------------------
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel=component, outputPosition=ELEMENT_CENTROID,)

# Set limits
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    maxAutoCompute=OFF, maxValue=maxValue, minAutoCompute=OFF, minValue=minValue)

# Set colorbar
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    spectrum='Blue to red', numIntervals=numIntervals)

# Set contour
session.viewports['Viewport: 1'].odbDisplay.display.setValues(
    plotState=(CONTOURS_ON_UNDEF, ))

# Setup Viewport
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triad=ON)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    compass=OFF)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(title=OFF)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    annotations=ON)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(state=ON)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    legendFont='-*-verdana-medium-r-normal-*-*-80-*-*-p-*-*-*')
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    legendTitle=OFF)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    legendDecimalPlaces=7, legendNumberFormat=FIXED)
