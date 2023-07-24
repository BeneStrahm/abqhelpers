# batch
General for all scripts: Copy to folder in which the CAE / preprocessor.py / postprocessor.py is located and execute from there

## start
Executes Abaqus with the script preprocessor.py. Open GUI to visualize the files. Used to prepare the files required for the simulation (.inp /.cae)

## start_noGUI
Executes Abaqus with the script preprocessor.py. No GUI mode to accelerate the process. Used to prepare the files required for the simulation (.inp /.cae)

## cleanup
Deletes all auxiliary files created by Abaqus

## copyToHPC
Copies the whole folder where the script is located to the specified path in a new folder, which has the same name as the folder where the script is located.

## start - copyToHPC - cleanup
Executes start_noGUI, cleanup and then copyToHPC