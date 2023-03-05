# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Description:  ** Add here short description **
# Author:       benedikt.strahm@ilek.uni-stuttgart.de
# Created:      28.09.2022
# Execution:    Set work-dir to this file & run script in ABAQUS CAE
# Status:       In Progress
# ------------------------------------------------------------------------------
# EXECUTION:
# 1. Open CMD in your working directory
# 2. Run script in ABAQUS CAE
# abaqus cae script=preprocessor.py
#
# TAIL LOGS:
# 1. Open CMD in your working directory
# 2. Use powershell to tail logs
# powershell Get-Content -Path abq_thermal_sim_slab.dat -WAIT
# powershell Get-Content -Path abq_thermal_sim_slab.msg -WAIT
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
    from abqhelpers.src import abq_model
except:
    # in Abaqus: add via imp for correct import
    abq_model = imp.load_source(
        'sec.abq_model', os.path.join(abq_path, 'src/abq_model.py'))

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
    from abqhelpers.src import abq_load
except:
    # in Abaqus: add via imp for correct import
    abq_load = imp.load_source(
        'sec.abq_load', os.path.join(abq_path, 'src/abq_load.py'))

try:
    # in Python: add via relative import for type hints
    from abqhelpers.src import abq_step
except:
    # in Abaqus: add via imp for correct import
    abq_step = imp.load_source(
        'sec.abq_step', os.path.join(abq_path, 'src/abq_step.py'))

try:
    # in Python: add via relative import for type hints
    from abqhelpers.src import abq_output
except:
    # in Abaqus: add via imp for correct import
    abq_output = imp.load_source(
        'sec.abq_output', os.path.join(abq_path, 'src/abq_output.py'))

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

modelName = "thermal_sim_slab"

# Delete to restart model
try:
    del mdb.models[modelName]
except:
    pass

# Create model
model = mdb.Model(name=modelName)

# Clean up
try:
    del mdb.models["Model-1"]
except:
    pass

# Part
# ----------------

dir_path = os.getcwd()
parts_path = os.path.join(dir_path, "geometry", "parts")

beton = abq_parts.import_3_d_parts(
    model, os.path.join(parts_path, "C_concrete.sat"),
    bodyNum=16, combine=False, mergeSolidRegions=False)

# Create Sets
# ----------------

# Create Sets
# Solids
for ele in beton:
    abq_parts.create_Set_All_Cells(model, ele, ele)


# Property
# ----------------

# Import Materials from Library
abq_property.import_from_material_library(
    abq_mat_lib, modelName, "concrete_cdp_C50_60_temperature")


# Create Sections
abq_property.create_homogenous_solid_section(
    model, "Section-beton", "concrete_cdp_C50_60_temperature")

# Assign Sections
for ele in beton:
    abq_property.assign_section(model, ele, ele, "Section-beton")

# Assembly
# ----------------

# List w/ all assemblies (instance.name)
beton_asm = []

# Create Assembly
for ele in beton:
    beton_asm.append(abq_assembly.create_Assembly(model, ele, ele))


# Merge Assembly
beton_asm = abq_assembly.create_boolean_merge_assembly(
    model, beton_asm, "beton",)

# Create datum planes of assembly
# ----------------

filenames, filepaths = filemanager.scanSubdirsForFilesWithExtension(
    dir_path, ".dp")

datumIDs = []

for filepath in filepaths:
    with open(filepath) as f:
        for l in f:
            (x, y, z, nx, ny, nz) = [float(x) for x in l.split(",")]
            datumIDs.append(abq_assembly.create_datum_plane_by_point_and_normal(
                model, [x, y, z], [nx, ny, nz]))

for myID in datumIDs:
    abq_assembly.create_partition_by_datum_plane(
        model, beton_asm, myID)


# Set the model constants for heat transfer
# ----------------
abq_model.set_physical_constants(
    model, absoluteZero=0, stefanBoltzmann=5.67037E-11)

# Create Step
# ----------------
abq_step.create_analysis_step_with_temp(
    model, 'fire', 'Initial', 7200, 10000, 1.0, 1e-20,
    5.0, 20.0)

# Get ETK from EN 13501-2
(t, etk_norm, etk_max) = abq_step.get_etk_EN_13501_2(t=14400, dt=600)

# Convert to ABQ-table format
tabledata = tuple(zip(t, etk_norm))

# Create Tabular Amplitude
abq_step.create_tabular_amplitude(
    model, 'etk', tabledata, timeSpan=STEP, smooth=SOLVER_DEFAULT)

# Set initial field temperature for all instances
abq_load.create_predefined_field_all_instances(
    model, 'normal_T', 'Initial', 20.0)

# Select faces of assembly
fire_T = abq_assembly.create_set_by_bounding_box(
    model, 'f', -300, -300, -126, 300, 300, -124, 'fire-T')
normal_T = abq_assembly.create_set_by_bounding_box(
    model, 'f', -300, -300, 124, 300, 300, 126, 'normal-T')

# Create film conditions
h = 1 / 25  # According to DIN 1992-1-2
abq_interaction.create_film_condition(
    model, 'normal-T', 'fire', normal_T, h, 20.0)
abq_interaction.create_film_condition(
    model, 'fire-T', 'fire', fire_T, h, etk_max, sinkAmplitude='etk')

epsilon = 0.70  # According to DIN 1992-1-2
# Create radiation interaction
abq_interaction.create_radiation_to_ambient(
    model, 'fire-T', 'fire', fire_T, epsilon, etk_max,
    ambientTemperatureAmp='etk')

# Create Output Requests
# ----------------

# Time points for output
abq_output.create_time_points(
    model, 'out_fire_n_x_30_min', start=0.0, end=7200.0, increment=1800.0)


# Get variables for thermal analysis
variables = abq_output.get_predefined_field_variables_thermal_analysis()

# Create field output request
abq_output.create_field_output_whole_model(
    model, 'F-Output_out_fire_n_x_30_min', 'fire', 'out_fire_n_x_30_min',
    variables=variables)

# Generate Mesh
# ----------------

abq_mesh.seed_all_active_instances(
    model, size=20.0, deviationFactor=0.1, minSizeFactor=0.1)

elemType1 = mesh.ElemType(elemCode=DC3D8, elemLibrary=STANDARD)
elemType2 = mesh.ElemType(elemCode=DC3D6, elemLibrary=STANDARD)
elemType3 = mesh.ElemType(elemCode=DC3D4, elemLibrary=STANDARD)
elemTypes = (elemType1, elemType2, elemType3)

abq_mesh.assign_mesh_control_all_active_instances(
    model, elemTypes, elemShape=HEX, technique=STRUCTURED)

abq_mesh.generate_mesh_all_active_instances(model)

# Generate Job
# ----------------

# Create Job
abq_job.create_job(model, "abq_thermal_sim_slab", 4)

# Check Job
abq_job.submit_data_check("abq_thermal_sim_slab")

# Submit Job

# SubmitJob(myJobName)

# Save abaqus model
mdb.saveAs('Concrete_beam_4_P_B.cae')
