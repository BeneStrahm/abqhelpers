# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  Four Point Bending Test on Concrete Beam
# Author:       benedikt.strahm@ilek.uni-stuttgart.de
# Created:      15.12.2022
# Execution:    Set work-dir to this file & run script in ABAQUS CAE
# Status:       In Progress
# ------------------------------------------------------------------------------
# EXECUTION:
# 1. Open CMD in your working directory
# 2. Run script in ABAQUS CAE
# abaqus cae script=4_P_B_Concrete_Beam.py
#
# TAIL LOGS:
# 1. Open CMD in your working directory
# 2. Use powershell to tail logs
# powershell Get-Content -Path Concrete_beam_4_P_B.dat -WAIT
# powershell Get-Content -Path Concrete_beam_4_P_B.msg -WAIT
# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------

from abaqus import *
from abaqusConstants import *
from driverUtils import *
from caeModules import *

# ------------------------------------------------------------------------------
# Install
# ------------------------------------------------------------------------------
# import custom libraries
import os
import imp
import re
import numpy as np

# Requires full path to abqhelpers
abq_path = 'C:/Users/ac135564/GitHub/abqhelpers/'

# Requires full path to abqhelpers - Material Library
abq_mat_lib = os.path.join(abq_path, 'abaqus_plugins/MatLibrary.lib')

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

try:
    # in Python: add via relative import for type hints
    from abqhelpers.src import abq_interaction
except:
    # in Abaqus: add via imp for correct import
    abq_interaction = imp.load_source(
        'sec.abq_interaction', os.path.join(abq_path, 'src/abq_interaction.py'))

try:
    # in Python: add via relative import for type hints
    from abqhelpers.src import abq_step
except:
    # in Abaqus: add via imp for correct import
    abq_step = imp.load_source(
        'sec.abq_step', os.path.join(abq_path, 'src/abq_step.py'))

try:
    # in Python: add via relative import for type hints
    from abqhelpers.src import abq_mesh
except:
    # in Abaqus: add via imp for correct import
    abq_mesh = imp.load_source(
        'sec.abq_mesh', os.path.join(abq_path, 'src/abq_mesh.py'))

try:
    # in Python: add via relative import for type hints
    from abqhelpers.src import abq_job
except:
    # in Abaqus: add via imp for correct import
    abq_job = imp.load_source(
        'sec.abq_job', os.path.join(abq_path, 'src/abq_job.py'))

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------

# Model
# ----------------

modelName = 'Concrete_beam_4_P_B'

# Delete to restart model
try:
    del mdb.models[modelName]
except:
    pass

# Create model
model = mdb.Model(name=modelName)

# Clean up
try:
    del mdb.models['Model-1']
except:
    pass

# Part
# ----------------

dir_path = os.getcwd()
parts_path = os.path.join(dir_path, 'geometry', 'parts')

concrete_beam = abq_parts.import_3_d_parts(model, os.path.join(
    parts_path, 'concrete_beam.sat'))
load_plates = abq_parts.import_3_d_parts(model, os.path.join(
    parts_path, 'load_plate.sat'), bodyNum=2, combine=False, mergeSolidRegions=False)
support_plates = abq_parts.import_3_d_parts(model, os.path.join(
    parts_path, 'support_plate.sat'), bodyNum=2, combine=False, mergeSolidRegions=False)
reinforcement = abq_parts.import_3_d_parts(model, os.path.join(
    parts_path, 'reinforcement.sat'))


# Create reference points
# ----------------

filenames, filepaths = filemanager.scanSubdirsForFilesWithExtension(
    dir_path, '.rp')

# structure of list:
# referencePoint[0] = referencePoint
# referencePoint[1] = types
referencePoints = []

for i, filepath in enumerate(filepaths):
    with open(filepath) as f:
        for j, l in enumerate(f):
            # clean up line
            l = re.sub(r'[\n\t\s]*', '', l)
            l = l.split(',')
            # read coordinates from file
            (x, y, z) = [float(x) for x in l[0:3]]
            # read types from file
            types = l[3:]
            # Create reference point
            referencePoints.append([abq_parts.create_reference_point(
                x, y, z, model, filenames[i].replace('.rp', '')), types])

# Create Sets
# ----------------

# Create Sets - solids
for ele in concrete_beam:
    abq_parts.create_Set_All_Cells(model, ele, ele)
for ele in load_plates:
    abq_parts.create_Set_All_Cells(model, ele, ele)
for ele in support_plates:
    abq_parts.create_Set_All_Cells(model, ele, ele)

# Create Sets - linear elements
for ele in reinforcement:
    abq_parts.create_Set_All_Edges(model, ele, ele)


# Property
# ----------------

# Import Materials from Library
abq_property.import_from_material_library(
    abq_mat_lib, modelName, 'concrete_cdp_c50_60')
abq_property.import_from_material_library(
    abq_mat_lib, modelName, 'support_stiff')
abq_property.import_from_material_library(
    abq_mat_lib, modelName, 'reinforcement_b500')


# Create Sections
abq_property.create_homogenous_solid_section(
    model, 'section-concrete', 'concrete_cdp_C50_60')
abq_property.create_homogenous_solid_section(
    model, 'section-stiff', 'support_stiff')

abq_property.create_circular_beam_section(
    model, 'section-reinforcement', 'reinforcement_b500', radius=6)

# Assign Sections
for ele in concrete_beam:
    abq_property.assign_section(model, ele, ele, 'section-concrete')
for ele in load_plates:
    abq_property.assign_section(model, ele, ele, 'section-stiff')
for ele in support_plates:
    abq_property.assign_section(model, ele, ele, 'section-stiff')
for ele in reinforcement:
    abq_property.assign_section(model, ele, ele, 'section-reinforcement')

# Assign beam orientation
for ele in reinforcement:
    abq_property.assign_beam_section_orientation(
        model, ele, n1=(0.0, 0.0, -1.0))

# Assembly
# ----------------

# List w/ all assemblies (instance.name)
concrete_beams_asm = []
load_plates_asm = []
support_plates_asm = []
reinforcement_asm = []

# Create Assembly
for ele in concrete_beam:
    concrete_beams_asm.append(abq_assembly.create_Assembly(model, ele, ele))
for ele in load_plates:
    load_plates_asm.append(abq_assembly.create_Assembly(model, ele, ele))
for ele in support_plates:
    support_plates_asm.append(abq_assembly.create_Assembly(model, ele, ele))
for ele in reinforcement:
    reinforcement_asm.append(abq_assembly.create_Assembly(model, ele, ele))

# Merge Assembly
concrete_dummy_plates = concrete_beams_asm + \
    load_plates_asm + support_plates_asm

concrete_dummy_plates_asm = abq_assembly.create_boolean_merge_assembly(
    model, concrete_beams_asm + load_plates_asm + support_plates_asm, "concrete-dummy-plates",)

# Create datum planes
# ----------------

filenames, filepaths = filemanager.scanSubdirsForFilesWithExtension(
    dir_path, '.dp')

datumIDs = []

for filepath in filepaths:
    with open(filepath) as f:
        for l in f:
            (x, y, z, nx, ny, nz) = [float(x) for x in l.split(',')]
            datumIDs.append(abq_assembly.create_datum_plane_by_point_and_normal(
                model, [x, y, z], [nx, ny, nz]))

for myID in datumIDs:
    abq_assembly.create_partition_by_datum_plane(
        model, concrete_dummy_plates_asm, myID)

# Interaction
# ----------------

# Create Embedded Region
for ele in reinforcement_asm:
    abq_interaction.create_embedded_region(
        model, 'reinforcement', ele, concrete_dummy_plates_asm)


# Create MPC Beam Constraint
for referencePoint in referencePoints:
    if 'mpc_beam' in referencePoint[1]:
        abq_interaction.create_mpc_beam_constraint(
            model, referencePoint[0], concrete_dummy_plates_asm)

# Step
# ----------------

# Create Supports
for referencePoint in referencePoints:
    if 'hinge' in referencePoint[1]:
        abq_step.create_hinge_support_at_RP(
            model, referencePoint[0], bcName='hinge_', stepName='Initial')

    if 'roller' in referencePoint[1]:
        abq_step.create_roller_support_at_RP(
            model, referencePoint[0], bcName='roller_', stepName='Initial')

# Create Analyis Step
abq_step.create_analysis_step(
    model, 'load_disp', 'Initial', 0.01, 1E-06, 1, 1000000, OFF)

# Create Loading
for referencePoint in referencePoints:
    if 'load_u3' in referencePoint[1]:
        abq_step.create_vertical_disp_at_RP(
            model, referencePoint[0], uz=-10, bcName='load_disp_', stepName='load_disp')

# Generate Mesh
# ----------------

abq_mesh.seed_all_active_instances(
    model, size=20.0, deviationFactor=0.1, minSizeFactor=0.1)

elemType1 = mesh.ElemType(elemCode=C3D20R)
elemTypes = (elemType1,)

abq_mesh.assign_mesh_control_all_active_instances(
    model, elemTypes, elemShape=TET, technique=FREE)

abq_mesh.generate_mesh_all_active_instances(model)

# Generate Job
# ----------------

# Create Job
abq_job.create_job(model, 'Concrete_beam_4_P_B', 4)

# Check Job
# abq_job.submit_data_check('Concrete_beam_4_P_B')

# Save abaqus model
# mdb.saveAs('Concrete_beam_4_P_B.cae')
