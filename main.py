#!/usr/bin/env python3

import argparse
from importlib.util import module_from_spec, spec_from_file_location
import logging
import sys

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lance un script")
    parser.add_argument(
        "filename",
        type=str,
        help="Chemin vers le fichier de script, format python",
    )
    args = parser.parse_args()

    spec = spec_from_file_location("module", args.filename)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    logging.basicConfig(filename="lccdocs.log", level=logging.INFO)

    if hasattr(module, "main"):
        module.main()
    else:
        print("Erreur : le script n'a pas de méthode main")
        sys.exit(1)
