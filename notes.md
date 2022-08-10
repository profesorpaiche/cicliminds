# Notes

Here are some notes related to the project `cicliminds`.

- No clear installation guides:
    - [X] There is an ¿issue? while installing `cartopy`. Its latest update
      requires the use of Proj version >= 8.0.0. For LTS OS (like Ubuntu 20.04),
      the repos has a version 6.x.x and does not allow the installation of
      `cartopy`. It can be fixed by installing a new version using `conda` as it
      is said in their (webpage)[https://proj.org/install.html].
    - [X] According to the repo, one should verify if `cicliminds` package is
      accessible from the notebook, but it does not mention how to check that or
      what to do in case this does not happen. If one goes to the repo of the
      package, there are also no instructions of how to install the packages. For
      a non-python user, this is a problem (like me).
        - [X] Link to the repo and instructions for installation.
      get it, or how it is related to `DATA_DIR` and `MODEL_WEIGHTS_DIR`.
    - [X] `jupyter lab` does not work in my system, instead `jupyter-lab` can be
      used.
    - [X] After launching `jupyter lab`, there is no instructions on how to
      proceed or how to launch the interface.

- [O] It should be explicit that this project is only the UI of the "program",
  and all the "brain" is done in another package which needs to be install. So,
  clearer installation steps for the `cicliminds` is needed.
    - [.] Included as description, needs improvement.

- [O] Consider create a `setup` script to deal with the console variables. It
  will include `DATA_DIR`, `MODEL_WEIGHTS_DIR`, and the creation of the
  respective directories.
    - [ ] Still needs the creation of directories.

- [O] Is `DATA_DIR` and `MODEL_WEIGHTS_DIR` related with the data used in the
  program? If so, is this the place where the program needs to connect to CDS?
    - [X] Q1 -> yes, Q2 -> yes.
    - [O] Data must be downloaded from the CDS and place it `DATA_DIR`.
    - [o] I don't know where `weights` data comes from (for sure not from
      `DATA_DIR` files).
        - [O] FIXME: For the moment a dummy file was created inside
          `MODEL_WEIGHTS_DIR`.
        - [ ] Ask for information.

- [X] Install `cicliminds-lib`.
    - [X] Error with `xmca` packages because of the incorrect `cartopy` library
      (seems like be a problem only in my system -> it was a problem of my
      system).

- [X] FIXME: Error in `cicliminds-lib` library. Tries to download a zip file from
  a link that is not correct (maybe it was change since the time the library was
  created)
    - [X] Install the last version `regionmask`.
    - [X] `cicliminds-libs` calls an old version of `regionmask` (0.6).
      Update the `setup.cfg`.
    - [X] Update deprecated functions from `regionmask`.

- [.] Create the list of variables (For the moment the only idea is hard coding
  it, which is not ideal).

- [o] Chech the CDS toolbox. -> Doesn't look like an option

- [O] The app should be able to download data from the CDS or to import it from
  the user.

- [ ] The already defined functions and widgets need to be cleaned.

Some caveats with the intallation:

- Don't use python3.10 because its `pipenv` package doesn't work properly.
- Be sure to have the python headers in order to install packages like
  `cartopy`.
- Download data from the CDS.

# Changelog

- 2022-04-19:
    - Improving the installation part in `README.md`.
- 2022-05-26:
    - Updating the libraries required in `cicliminds-lib`.
- 2022-06-05:
    - FIXED: Name convention not recognized by the app.
    - FIXME: Dummy weights file created.
- 2022-06-06:
    - FIXED: Updated deprecated functions from `regionmask`.
    - The app works (seems like...)
