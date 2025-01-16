# A `dcm2niix` example for BIDS-Prov

This example aim at showing provenance traces from a DICOM to Nifti conversion, performed by `dcm2niix` on a Linux-based (Fedora) operating system.

## `dcm2niix` installation

```shell
sudo yum install dcm2niix
```

## Source dataset

We get raw data from https://github.com/psychoinformatics-de/hirni-demo.git, a demo datalad dataset containing dicoms.

```shell
# Get example dicom(s) in a sourcedata/ directory
mkdir sourcedata
cd sourcedata
datalad install --recursive https://github.com/psychoinformatics-de/hirni-demo.git
cd acq1
datalad get ./*
cd ../acq2
datalad get ./*
ls -1
    acq1
    acq2
    code
    dataset_description.json
    README
    studyspec.json
cd ..
```

## Conversions

With this setup we are ready to convert dicoms to nifti files using `dcm2niix`.

```shell
dcm2niix -o . -f sub-%i/ses-%t/anat/sub-%i_ses-%t_T1w sourcedata/acq1/dicoms/example-dicom-structural-master/dicoms/
dcm2niix -o . -f sub-%i/ses-%t/func/sub-%i_ses-%t_task-oneback_run-1_bold sourcedata/acq1/dicoms/example-dicom-structural-master/dicoms/

# Control results
tree sub-02/
    sub-02/
    ├── ses-20130717141500
    │   └── anat
    │       ├── sub-02_ses-20130717141500_T1w.json
    │       └── sub-02_ses-20130717141500_T1w.nii
    └── ses-20140425155335
        └── func
            ├── sub-02_ses-20140425155335_task-oneback_run-1_bold.json
            └── sub-02_ses-20140425155335_task-oneback_run-1_bold.nii
```

## Associated provenance

See the `dcm2niix.prov.jsonld` file.

## Limitations

### `Used` key for activities

Although the BIDS-Prov spec mentions:

> Used : OPTIONAL. UUID. Identifier of an entity used by this activity (the corresponding Entity must be defined with its own Entity record).

We represented used entities in a list to link all the dicom files of a directory to the corresponding conversion activity.

### High number of dicom files

As there is a high number of dicom files (384 in `acq1/` and 5460 in `acq2/`), we did not create an entity for each of these. Only the first three files of each directory were represented.
