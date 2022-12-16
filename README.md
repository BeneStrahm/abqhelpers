# abqhelpers

## CAD - FEA
In order to create the model's geometry, Rhino can be used. The gh folder contains Grasshopper components allowing to export object's layerwise to .sat files, which can be subsequently imported in Abaqus using the PY - FEA methods.

Further, Reference Points and Datum Planes can be defined in Rhino, exported via Grasshopper and imported in Abaqus using the PY - FEA methods. 
## PY - FEA
The src folder contains a collections of Python Scripts allowing to create and  manipulate Abaqus Models.

They are built in the same order as in Abaqus (Part, Property, Assembly,..) and should be used also in this order. 

For a simple example, see the samples. 
## Import abqhelpers
This should be done in the begining of each script, simply copy the stuff from the sample to your script. This allows you to use all methods of abqhelpers. Make sure to set the correct paths. 

Abaqus doesn't easily support importing custom libraries. A workaround is to use 'imp' to import modules in each of the scripts. Changes the abq_path variable to wherever this folder is located and import using imp:

    # import custom libraries
    import imp

    # path to abqhelpers
    abq_path = "C:/Users/ac135564/GitHub/abqhelpers/"

    filemanager = imp.load_source('helpers.filemanager', os.path.join(
        abq_path, 'helpers/filemanager.py'))

In order to use the imported module use the object's methods:

    filemanager.scanFolder('C:/')

## License

[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg