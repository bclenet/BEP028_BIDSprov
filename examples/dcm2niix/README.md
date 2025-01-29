# BIDS Prov example for `dcm2niix`

This example aims at showing the capture of provenance for a [`dcm2niix`](https://github.com/rordenlab/dcm2niix) usecase: converting DICOM data to Nifti files within a BIDS dataset.

Source data for this example can be found here: https://github.com/psychoinformatics-de/hirni-demo. This is a datalad dataset containing anatomical and functional MRI acquisitions. The contents of this dataset can be downloaded using:
```shell
mkdir sourcedata
cd sourcedata
datalad install --recursive https://github.com/psychoinformatics-de/hirni-demo.git
```

> [!NOTE] Note that the dataset must be added inside the `sourcedata/` directory.

## Experiment #1

The aim of the experiment is to describe the provenance records inside several files. Here we use sidecars and modality agnostic files inside the `prov/` directory, as follows:
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

* `sub-02_ses-20130717141500_T1w.prov.jsonld` and `sub-02_ses-20140425155335_task-oneback_run-1_bold.prov.jsonld` are sidecars defining provenance for the corresponding `.nii` files.
* `environments.prov.jsonld` mutualises the declaration of software environments objects for lower level prov files
* `software.prov.jsonld` mutualises the declaration of software pieces objects for lower level prov files

The python script `code/exp1_merge_prov.py` aims at merging all these provenance records into one RFD graph.

```shell
pip install -r code/requirements.txt
mkdir prov/experiment_1/
python code/exp1_merge_prov.py
```

From that, we generate the RDF graph `prov/experiment_1/merged_provenance.ttl`. Then we were able to plot the graph as a png file. We used this command:

```shell
python code/plot_graph.py -i prov/experiment_1/merged_provenance_2.ttl -o prov/experiment_1/merged_provenance_2.png
```

![](/examples/dcm2niix/prov/experiment_1/merged_provenance.png)

### Notes

In this example, we rely on the fact that nodes defined in the `prov/*.prov.jsonld` files have `bids::prov/` as base IRIs. Here are the involved nodes:
* `bids::prov/dcm2niix`
* `bids::prov/fmriprep`
* `bids::prov/fedora`

### Limitations

The `bids::prov/fedora` node defined in `prov/environments.prov.jsonld` (see grey node in the above graph plot) is not recognized as a `prov:Entity` as the current context (commit [ce0eb77](https://github.com/bids-standard/BEP028_BIDSprov/commit/ce0eb774abd9527e594bd69212a87d5047864678)) does not define the `Environments` term.

We cannot list all the 
