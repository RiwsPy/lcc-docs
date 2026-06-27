#!/usr/bin/env python3
import argparse
from importlib.util import module_from_spec, spec_from_file_location
import logging
import sys

import i18n  # noqa

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lance un script")
    parser.add_argument(
        "filename",
        type=str,
        help="Chemin vers le fichier de script, format python",
    )
    parser.add_argument(
        "--language",
        "-l",
        type=str,
        help="Langue du script",
    )
    args = parser.parse_args()

    spec = spec_from_file_location(args.filename, args.filename)
    assert spec is not None and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    error_format = (
        "%(asctime)s - %(levelname)s - %(name)s|%(funcName)s:%(lineno)d - %(message)s"
    )

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_file = logging.FileHandler("lccdocs.log", encoding="utf-8")
    log_file.setFormatter(logging.Formatter(error_format))
    logger.addHandler(log_file)

    log_console = logging.StreamHandler()
    log_console.setFormatter(logging.Formatter(error_format))
    logger.addHandler(log_console)

    if hasattr(module, "main"):
        module.main(**args.__dict__)
    else:
        print("Erreur : le script n'a pas de méthode main")
        sys.exit(1)
