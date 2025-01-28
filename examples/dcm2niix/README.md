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

### Limitation #1: type indexing

Notice that starting from line 50 of the file, the generated triplets are not correct.

```turtle
[] prov:Activity <urn:conversion-5a66f5be> ;
...
```

This is probably due to the fact that rdflib 7.1.3 does not conform with JSON-LD 1.1 and is therefore not able to parse graphs using [type indexing](https://www.w3.org/TR/json-ld11/#example-106-indexing-data-in-json-ld-by-type) as we used it e.g. in the `Records_hirni-demo_software` term of the `prov/software.prov.jsonld` file.
Furthermore, all the triplets describing the type of node objects are missing because of rdflib not understanding type indexing.

As a workaround, we replaced the incorrect lines (50 to the end) by triplets describing the type of the objects in the merged document, as presented in `prov/experiment_1/merged_provenance_2.ttl`.

From that we were able to plot the following graph `prov/experiment_1/merged_provenance_2.ttl`. We used the 
```shell
python code/plot_graph.py -i prov/experiment_1/merged_provenance_2.ttl -o prov/experiment_1/merged_provenance_2.png
```

![](/examples/dcm2niix/prov/experiment_1/merged_provenance_2.png)

### Limitation #2: `bids` namespace for files

Defining the `@base` term in the context (see `sub_02/ses_20140425155335/func/sub-02_ses-20140425155335_task-oneback_run-1_bold.prov.json` line 5) allows give a default base IRI to relative IRIs.

In our case, the sidecar provenance files defined under the `sub_02/` (sub-)directory(ies) may want to refer to keywords inside the `prov/` directory. Setting `@base` to the `prov/` directory and passing relative IRIs inside sidecars files resolves this... But parsing the sidecar files with rdflib, we get the following RDF nodes:

```turtle
<file:///data/dev/BEP028_BIDSprov/examples/dcm2niix/prov/fedora>
```

although we would prefer:

```turtle
<bids::prov/fedora>
```

> [!NOTE] Note that we had to alter the .ttl files to remove the root paths of the directories (e.g. replacing `file:///home/user/` with  `file:///data/`)
