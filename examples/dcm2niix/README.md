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

We describe the provenance records inside the following files:
```
.
├── prov
│   ├── bidsprov_context.json
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
* `bidsprov_context.json` is the BIDS Prov context from https://purl.org/nidash/bidsprov/context.json, with minor changes.
* `environments.prov.jsonld` mutualises the declaration of software environments objects for lower level prov files
* `software.prov.jsonld` mutualises the declaration of software pieces objects for lower level prov files

The python script `code/exp1_merge_prov.py` aims at merging all these provenance records into one RFD graph.

```shell
pip install -r code/requirements.txt
mkdir prov/experiment_1/
python code/exp1_merge_prov.py
```

From that, we generate the RDF graph `prov/experiment_1/merged_provenance.ttl`.

Notice that starting from line 50 of the file, the generated triplets are not correct.
```turtle
[] prov:Activity <urn:conversion-5a66f5be> ;
```

This is probably due to the fact that rdflib 7.1.3 does not conform with JSON-LD 1.1 and is therefore not able to parse graphs using [type indexing](https://www.w3.org/TR/json-ld11/#example-106-indexing-data-in-json-ld-by-type) as we used it e.g. in the `Records_hirni-demo_software` term of the `prov/software.prov.jsonld` file.
Furthermore, all the triplets describing the type of node objects are missing because of rdflib not understanding type indexing.

As a workaround, replaced the incorrect lines (50 to the end) by triplets describing the type of the objects in the merged document, as presented in `prov/experiment_1/merged_provenance_2.ttl`.
From that we were able to plot the following graph `prov/experiment_1/merged_provenance_2.ttl`.
![](/examples/dcm2niix/prov/experiment_1/merged_provenance_2.png)
