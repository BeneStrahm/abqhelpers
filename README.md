# abqhelpers

## Import abqhelpers

Abaqus doesn't easily suppport importing custom libraries. A workaround is to use 'imp' to import modules in each of the scripts. Changes the abq_path variable to wherever this folder is located and import using imp:

    # import custom libraries
    import imp

    # path to abqhelpers
    abq_path = "C:/Users/ac135564/GitHub/abqhelpers/"

    filemanager = imp.load_source('helpers.filemanager', os.path.join(
        abq_path, 'helpers/filemanager.py'))

In order to use the imported module use the object's methods:

    filemanager.scanFolder('C:/')

## License

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg