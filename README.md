# Helper functions for the mdCATH dataset

This repository contains utility functions related to the mdCATH dataset described in the paper [mdCATH: A Large-Scale MD Dataset for Data-Driven Computational Biophysics](https://arxiv.org/abs/2407.14794v1). The dataset files are available at https://huggingface.co/datasets/compsciencelab/mdCATH .

## Command-line conversion

Converts an mdCATH h5 file to the corresponding PDB and XTC.

#### Usage

```bash
convert_mdCATH.py [-h] [--basename BASENAME] [--temp_list TEMP_LIST [TEMP_LIST ...]] [--replica_list REPLICA_LIST [REPLICA_LIST ...]] fn
```

**Note:** Requires the `mdtraj` and `h5py` packages.


## Python: MDTraj and MoleculeKit/HTMD

A Python function is provided to convert to an MDTraj trajectory object for further analysis. See  docstrings inside `convert_mdCATH.py` for Python usage. 


## VMD/TCL

The `load_mdCATH` VMD/TCL procedure loads molecular dynamics (MD) simulation data from a specified HDF5 file of the mdCATH dataset into VMD.  

**Note:** The utilities `h5ls` and `h5dump` are required and must be accessible in the system's path.


#### Usage
```tcl
load_mdCATH filename temperature replica
```

#### Parameters

- `filename`: Path to the HDF5 file containing the MD simulation data.
- `temperature`: Temperature (K) of the simulation data to load (320, 348, 379, 413, or 450).
- `replica`: Identifier of the simulation replica (0 to 4).


#### Return Values
- On successful execution, the function sets up the molecular visualization with the loaded data but does not return a value.
- On failure, returns an error with a specific message detailing the cause of the failure.



#### Example Call
```tcl
source load_mdCATH.tcl
load_mdCATH cath_dataset_153lA00.h5 320 1
```
This call loads the MD simulation data from `path/to/simulation.h5` for the simulation run at 320 Kelvin and the first replica.

#### Notes
- Ensure that the environment variable `TMPDIR` is set as it is used to define temporary file paths.
- This procedure assumes that the required utilities `h5ls` and `h5dump` are installed and accessible in the system's path.


## Citation

> Antonio Mirarchi, Toni Giorgino and Gianni De Fabritiis. *mdCATH: A Large-Scale MD Dataset for Data-Driven Computational Biophysics*. https://arxiv.org/abs/2407.14794 

```
@misc{mirarchi2024mdcathlargescalemddataset,
      title={mdCATH: A Large-Scale MD Dataset for Data-Driven Computational Biophysics}, 
      author={Antonio Mirarchi and Toni Giorgino and Gianni De Fabritiis},
      year={2024},
      eprint={2407.14794},
      archivePrefix={arXiv},
      primaryClass={q-bio.BM},
      url={https://arxiv.org/abs/2407.14794}, 
}
```

