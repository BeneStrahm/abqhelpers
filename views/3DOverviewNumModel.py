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
import os

# ------------------------------------------------------------------------------
# Execution
# ------------------------------------------------------------------------------
# 1) Switch to Mesh module
# 2) Copy code do Abaqus CAE

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------

# Get current working directory
cwd = os.getcwd()

# Change View
session.viewports['Viewport: 1'].view.rotate(xAngle=90, yAngle=0, zAngle=0,
                                             mode=MODEL)
session.viewports['Viewport: 1'].view.rotate(xAngle=0, yAngle=0, zAngle=90,
                                             mode=MODEL)
session.viewports['Viewport: 1'].view.rotate(xAngle=180, yAngle=0, zAngle=0,
                                             mode=MODEL)
session.viewports['Viewport: 1'].view.rotate(xAngle=0, yAngle=0, zAngle=90,
                                             mode=MODEL)
session.viewports['Viewport: 1'].view.rotate(xAngle=0, yAngle=0, zAngle=90,
                                             mode=MODEL)
session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)

# Coloring
cmap = session.viewports['Viewport: 1'].colorMappings['Material']
session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
session.viewports['Viewport: 1'].disableMultipleColors()
session.viewports['Viewport: 1'].setColor(globalTranslucency=True)

# Setup Viewport
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triad=ON)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    compass=OFF)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(title=OFF)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    annotations=ON)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(state=OFF)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    legendFont='-*-verdana-medium-r-normal-*-*-80-*-*-p-*-*-*')
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    legendTitle=OFF)

# Export to PNG
# Create folder if not exists
if not os.path.exists(os.path.join(cwd, 'viewExports')):
    os.makedirs(os.path.join(cwd, 'viewExports'))

# Export Frame
fileName = os.path.join(
    cwd, 'viewExports', 'Numerical_Model_Shaded' + '.png')
session.printToFile(
    fileName=fileName, format=PNG,
    canvasObjects=(session.viewports['Viewport: 1'],))


# Re-Setup Render Style
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    renderStyle=HIDDEN, visibleEdges=FEATURE)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    translucencyFactor=0.15)

# Export Frame
fileName = os.path.join(
    cwd, 'viewExports', 'Numerical_Model_Hidden' + '.png')
session.printToFile(
    fileName=fileName, format=PNG,
    canvasObjects=(session.viewports['Viewport: 1'],))
