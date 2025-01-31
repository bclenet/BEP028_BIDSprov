# BIDS Prov example for `dcm2niix`

This example aims at showing the capture of provenance for a [`dcm2niix`](https://github.com/rordenlab/dcm2niix) usecase: converting DICOM data to Nifti files within a BIDS dataset.

Source data for this example can be found here: https://github.com/psychoinformatics-de/hirni-demo. This is a datalad dataset containing anatomical and functional MRI acquisitions. The contents of this dataset can be downloaded using:

```shell
mkdir sourcedata
cd sourcedata
datalad install --recursive https://github.com/psychoinformatics-de/hirni-demo.git
```

> [!NOTE] Note that the dataset must be added inside the `sourcedata/` directory.

## Purpose

The aim of the example is to describe the provenance records inside several files. Here we use sidecars and modality agnostic files inside the `prov/` directory, as follows:

```
.
├── prov
│   ├── environments.prov.jsonld
│   └── software.prov.jsonld
└── sub_02
    ├── ses_20130717141500
    │   └── anat
    │       └── sub-02_ses-20130717141500_T1w.prov.jsonld
    └── ses_20140425155335
        └── func
            └── sub-02_ses-20140425155335_task-oneback_run-1_bold.prov.jsonld
```

* `sub-02_ses-20130717141500_T1w.prov.jsonld` and `sub-02_ses-20140425155335_task-oneback_run-1_bold.prov.jsonld` are "sidecars" defining provenance for the corresponding `.nii` files.
* `environments.prov.jsonld` mutualises the declaration of software environments objects for lower level prov files
* `software.prov.jsonld` mutualises the declaration of software pieces objects for lower level prov files

The python script `code/merge_prov.py` aims at merging all these provenance records into one JSON-LD graph.

```shell
pip install bids-prov==0.1.0
mkdir prov/merged/
python code/merge_prov.py
```

From that, we generate the graph `prov/merged/dcm2niix.prov.jsonld`. Then we were able to plot the graph as a png file. We used this command:

```shell
bids_prov_visualizer --input_file prov/merged/dcm2niix.prov.jsonld --output_file prov/merged/dcm2niix.prov.png
```

![](/examples/dcm2niix/prov/merged/dcm2niix.prov.png)

### Notes

In this example, we rely on the fact that nodes defined in the `prov/*.prov.jsonld` files have `bids::prov/` as base IRIs. Here are the involved nodes:
* `bids::prov/dcm2niix-xce5m9z3`
* `bids::prov/fedora-b7hmkmqd`

### Limitations

The `bids::prov/fedora-b7hmkmqd` node defined in `prov/environments.prov.jsonld` is defined as an `Entity` as the current context (commit [ce0eb77](https://github.com/bids-standard/BEP028_BIDSprov/commit/ce0eb774abd9527e594bd69212a87d5047864678)) does not define the `Environments` term.

Listing all the DICOM files used by the dcm2niix conversion steps would lower readability of the JSON-LD provenance files. Therefore we only listed the following directories as `Entities`:
* `bids::sourcedata/hirni-demo/acq1/dicoms/example-dicom-structural-master/dicoms`
* `bids::sourcedata/hirni-demo/acq2/dicoms/example-dicom-functional-master/dicoms`

although it is not allowed by the current version of the BIDS Prov specification to have directories as `Entities`.
