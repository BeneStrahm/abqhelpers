# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  ** Add here short description **
# Author:       benedikt.strahm@ilek.uni-stuttgart.de
# Created:      28.09.2022
# Execution:    Set work-dir to this file & run script in ABAQUS CAE
# Status:       In Progress
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------

from abaqus import *
from abaqusConstants import *
from driverUtils import *

# ------------------------------------------------------------------------------
# Install
# ------------------------------------------------------------------------------
# import custom libraries
import os
import imp

# path to abqhelpers
abq_path = "C:/Users/ac135564/GitHub/abqhelpers/"
abq_mat_lib = os.path.join(abq_path, "abaqus_plugins/MatLibrary.lib")

try:
    # in Python: add via relative import for type hints
    from abqhelpers.helpers import filemanager
except:
    # in Abaqus: add via imp for correct import
    filemanager = imp.load_source(
        'helpers.filemanager', os.path.join(abq_path, 'helpers/filemanager.py'))

try:
    # in Python: add via relative import for type hints
    from abqhelpers.src import abq_parts
except:
    # in Abaqus: add via imp for correct import
    abq_parts = imp.load_source(
        'sec.abq_parts', os.path.join(abq_path, 'src/abq_parts.py'))

try:
    # in Python: add via relative import for type hints
    from abqhelpers.src import abq_property
except:
    # in Abaqus: add via imp for correct import
    abq_property = imp.load_source(
        'sec.abq_property', os.path.join(abq_path, 'src/abq_property.py'))

try:
    # in Python: add via relative import for type hints
    from abqhelpers.src import abq_assembly
except:
    # in Abaqus: add via imp for correct import
    abq_assembly = imp.load_source(
        'sec.abq_assembly', os.path.join(abq_path, 'src/abq_assembly.py'))

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


# Model
# ----------------
name = "Concrete_Frame_4_P_B"
model = mdb.Model(name=name)

# Part
# ----------------

dir_path = os.getcwd()
parts_path = os.path.join(dir_path, "parts")

concrete_beams = abq_parts.import_3_d_parts(model, os.path.join(
    parts_path, "concrete_beam.sat"))
load_plates = abq_parts.import_3_d_parts(model, os.path.join(
    parts_path, "load_plate.sat"), bodyNum=2, combine=False, mergeSolidRegions=False)
support_plates = abq_parts.import_3_d_parts(model, os.path.join(
    parts_path, "support_plate.sat"), bodyNum=2, combine=False, mergeSolidRegions=False)

# Create datum planes
filenames, filepaths = filemanager.scanSubdirsForFilesWithExtension(
    dir_path, ".dp")

myIDs = []

for filepath in filepaths:
    with open(filepath) as f:
        for l in f:
            (x, y, z) = l.split(",")
            abq_parts.create_datum_plane_by_principal(
                model, "concrete_beam-0", YZPLANE, float(x))

for myID in myIDs:
    abq_parts.create_partition_by_datum_plane(model, 'concrete_beam-0', myID)

# Create Sets
for ele in concrete_beams:
    abq_parts.create_Set_All_Cells(model, ele, ele)
for ele in load_plates:
    abq_parts.create_Set_All_Cells(model, ele, ele)
for ele in support_plates:
    abq_parts.create_Set_All_Cells(model, ele, ele)


# Assembly
# ----------------


for ele in concrete_beams:
    abq_assembly.create_Assembly(model, ele, ele)
for ele in load_plates:
    abq_assembly.create_Assembly(model, ele, ele)
for ele in support_plates:
    abq_assembly.create_Assembly(model, ele, ele)


# Save abaqus model
mdb.saveAs('compression.cae')
