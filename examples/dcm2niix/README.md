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

The `prov/dcm2niix.prov.jsonld` file contains all provenance traces relative to the conversion steps.

We are able to visualize these provenance files using the following commands (current directory is `examples/dcm2niix/`):

```shell
pip install -r ../../requirements.txt
python ../../bids_prov/visualize.py --input_file prov/dcm2niix.prov.jsonld --output_file prov/dcm2niix.prov.png
```
![](/examples/dcm2niix/prov/dcm2niix.prov.png)

## Limitations

### Using the JSON-LD playground

The `prov/dcm2niix.prov.jsonld` file can be tested inside the [JSON-LD playground](https://json-ld.org/playground/), although the context IRI must be changed to: `https://raw.githubusercontent.com/bids-standard/BEP028_BIDSprov/master/context.json`

### `Used` key for activities

Although the BIDS-Prov spec mentions:

> Used : OPTIONAL. UUID. Identifier of an entity used by this activity (the corresponding Entity must be defined with its own Entity record).

We represented used entities in a list to link all the dicom files of a directory to the corresponding conversion activity.

### `Environments` not defined in the context

We cannot use an `Environments` list because the current context (commit ce0eb77) does not define the `Environments` term. Therefore, we defined the `urn:fedora-b7hmkmqd` environments as an `Entity`.

### High number of dicom files

Listing all the DICOM files used by the dcm2niix conversion steps would lower readability of the JSON-LD provenance files. Therefore we only listed the following directories as `Entities`:

```
bids::sourcedata/hirni-demo/acq1/dicoms/example-dicom-structural-master/dicoms
bids::sourcedata/hirni-demo/acq2/dicoms/example-dicom-functional-master/dicoms
```

although it is not allowed by the current version of the BIDS Prov specification to have directories as `Entities`.

### `TaskName` not generated

As specified in [this issue](https://github.com/rordenlab/dcm2niix/issues/148), `dcm2niix` is not able to propagate the value of `TaskName` (name of the task in the case of task-fMRI) automatically because this information is not in the dicom metadata.

In our case, the following line must be added manually in the `sub-02_ses-20140425155335_task-oneback_run-1_bold.json` file:

```json
    "TaskName": "oneback",
```
