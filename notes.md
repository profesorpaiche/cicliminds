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
    - [ ] There is no explanation about the data used in the project, where to
      get it, or how it is related to `DATA_DIR` and `MODEL_WEIGHTS_DIR`.
    - [X] `jupyter lab` does not work in my system, instead `jupyter-lab` can be
      used.
    - [X] After launching `jupyter lab`, there is no instructions on how to
      proceed or how to launch the interface.

- [O] It should be explicit that this project is only the UI of the "program",
  and all the "brain" is done in another package which needs to be install. So,
  clearer installation steps for the `cicliminds` is needed.
    - [.] Included as description, needs improvement.

- [ ] Consider create a `setup` script to deal with the console variables. It
  will include `DATA_DIR`, `MODEL_WEIGHTS_DIR`, and the creation of the
  respective directories.

- [.] Is `DATA_DIR` and `MODEL_WEIGHTS_DIR` related with the data used in the
  program? If so, is this the place where the program needs to connect to CDS?
    - [O] Q1 -> maybe yes, Q2 -> maybe yes.
    - [ ] FIXME: Need sample data to continue with the app.

- [X] Install `cicliminds-lib`.
    - [X] Error with `xmca` packages because of the incorrect `cartopy` library
      (seems like be a problem only in my system -> it was a problem of my system).

- [X] FIXME: Error in `cicliminds-lib` library. Tries to download a zip file from
  a link that is not correct (maybe it was change since the time the library was
  created)
    - [X] Install the last version `regionmask`.
    - [X] `cicliminds-libs` calls an old version of `regionmask` (0.6).
      Update the `setup.cfg`.

-  Some caveats with the intallation:
    - Don't use python3.10 because its `pipenv` package doesn't work properly.
    - Be sure to have the python headers in order to install packages like `cartopy`.

# Changelog

- 2022-04-19:
    - Improving the installation part in `README.md`.
- 2022-05-26:
    - Updating the libraries required in `cicliminds-lib`.
