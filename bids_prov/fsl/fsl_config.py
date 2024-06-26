import json
import os

from typing import Mapping, Union
from os.path import expanduser
from boutiques.searcher import Searcher
from boutiques.puller import Puller


TYPES = (
    "File",
    # "String",
    "Number",
    "Flag",
)


def get_or_load(fn):
    """
    A decorator that takes another function as a parameter, in this case `get_config`. Its purpose is to check whether
    we already have the desired boutiques description functions in local memory. If so, we open the file,
    otherwise we call the fn function and store the results in memory.

    fn should return a json serializable object

    results will be stored in the home directory ('~')
    """

    def wrapper(*args, **kwargs):
        filename = os.path.join(expanduser("~"), fn.__name__)
        filename += "_".join(args)
        filename += ".json"
        if os.path.exists(filename):
            print(f"loading dumped results from {filename}")
            with open(filename, "r") as fd:
                d = json.load(fd)
                return d
        else:
            d = fn(*args, **kwargs)
            with open(filename, "w") as fd:
                json.dump(d, fd)
            return d

    return wrapper


@get_or_load
def get_config(agent: str) -> Mapping[str, Mapping[str, object]]:
    """get a config by querying bosh (tool to access Boutiques documents, see https://boutiques.github.io/) with `agent`
    eq to running ```bosh search``` from the command-line
    """
    print("agent", agent)
    searcher = Searcher(agent)
    print("searcher", searcher)
    results = searcher.search()
    print("results", results)
    ids = [_["ID"] for _ in results]
    print("ids", ids)
    paths = Puller(ids).pull()
    print("paths", paths)
    res = dict()
    for path, result in zip(paths, results):
        print("path, result", path, result)
        try:
            with open(path, "r") as fd:
                d = json.load(fd)
        except Exception:
            print(f"could not load config from {result['TITLE']}")
            continue
        res[result["TITLE"]] = d

    return res


list_command = ["overlay",
                "epi_reg",
                "paste",
                "fsl_tsplot",
                "featregapply",
                "fslmaths",
                "tsplot",
                "cluster",
                "mp_diffpow.sh",
                "fslFixText",
                "mcflirt",
                "cluster2html",
                "fslmerge",
                "slicer",
                "susan",
                "film_gls",
                "mkdir",
                "imrm",
                "ln",
                "ptoz",
                "echo",
                "mv",
                "flirt",
                "immv",
                "fslroi",
                "fslstats",
                "printf",
                "fsl_sub",
                "contrast_mgr",
                "convert_xfm",
                "bet2",
                "feat_model",
                "pngappend",
                "smoothest",
                "mainfeatreg",
                "rmdir",
                "rm",
                "cp"]
for cmd in list_command:
    print("\n\n cmd", cmd)
    bosh_config = get_config(cmd)
