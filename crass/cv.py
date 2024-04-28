#!/usr/bin/env python3

import jinja2
import os
import glob
import json
import re
import datetime
import pdfkit
import shutil
import yaml
from tempfile import TemporaryDirectory
from slugify import slugify
from pathlib import Path
import sass

"""
This package allows for continous deployment of multiple variants of your CV, so you can stay up to date with all the fads with minimal effort.

Your CV should be specified inside a yaml file, as described in [SPECIFICATION.md](SPECIFICATION.md)
The information in this CV file can then be masked or modified for a specific purpose. 
The file containing this info is called a VIBE (Variation In Besume Expressison),
the specification of which is described in the [generate vibe function](#generate_vibe). 
"""


def load_json_yaml(path):
    """
    Loads a json, or yaml file from 'path'
    """
    with open(path, "r") as f:
        suffix = Path(path).suffix
        if suffix in [".json"]:
            return json.load(f)
        elif suffix in [".yaml", ".yml"]:
            return yaml.load(f, Loader=yaml.SafeLoader)
        else:
            raise Exception(f"'{path}' doesn't look like yaml or json.")

def kw_mask(obj, mask_value):
    """
    Filters one dictionary based on another.
    Tried to use as common sense rules as possible.
    """
    if isinstance(mask_value, bool):
        # If true, return all unmodified.
        filtered = obj if mask_value else []

    elif isinstance(mask_value, dict):
        filtered = {}
        for key, value in mask_value.items():
            if key in obj.keys():
                filtered[key] = kw_mask(obj[key], value)
            else:
                print(f"Could not find anything called '{key}', options are '{', '.join(obj.keys())}'")
    else:
        filtered = []
        for filter in mask_value:
            options = []  # for printing warning message
            for item in obj:
                options.append(item["slug"])
                if item["slug"] == filter:
                    filtered.append(item)
                    break
            else:
                print(f"Could not find anything called '{filter}', options are '{', '.join(options)}'")
    return filtered


def kw_overwrite(obj, overwrite_values):
    if isinstance(overwrite_values, dict) and isinstance(obj, dict):
        for key, value in overwrite_values.items():
            if key in obj:
                obj[key] = kw_overwrite(obj[key], value)
        return obj
    else:
        return overwrite_values


def html2pdf(html, pdf_path):
    """Attempts to render html to pdf"""
    options = {
        "page-size": "A4",
        "margin-top": "0",
        "margin-right": "0",
        "margin-bottom": "0",
        "margin-left": "0",
        "encoding": "UTF-8",
        "enable-local-file-access": True,
        "keep-relative-links": True
    }
    pdfkit.from_string(html, pdf_path, options=options, verbose=True)


def safe_copy(source, dest):
    """Copy all files from source to dest."""
    # TODO add warning for overwrites
    for file in Path(source).glob(('**/*')):
        destination = Path(dest, Path(file).relative_to(source))

        if not file.is_file():
            destination.mkdir(exist_ok=True, parents=True)
            print(f"Created '{destination}'")

        else:
            shutil.copy(file, destination)
            print(f"Created '{destination}'")


class CurriculumVitae:
    """
    Class representing a CV, with info fo all it's possible configs.
    """
    def __init__(self, path):
        """
        Parameters
        ----------
        path : path to cv file. Can be yaml or json.
        """
        self.cv = load_json_yaml(path)
        self.__ensluginate()

    def __ensluginate(self):
        # Add nice slug to all items.
        # Order in which to use key as slug.
        key_order = ["slug", "name", "network", "organization", "institution", "title", "language"]
        for category in self.cv.values():
            if isinstance(category, dict):
                continue
            for item in category:
                for key in key_order:
                    if key in item:
                        item["slug"] = slugify(item[key])
                        break

    def generate_vibe(self, outputs=["unamed_cv.html"], theme="", theme_options={},
                      name="", includes=False, mask=True, overwrite=False):
        """
        Parameters
        ----------
        outputs: list
                List of paths specifying what outputs you want. 
                Currently supports '.html', '.pdf'.
                Must include at least one output.
                Build directory will be parent of first output.
        theme: str
            Path to theme directory.
            (default is theme_metro)
        theme_options: dict, optional
            Parameters to overwrite those in theme.yaml:options
            (default is {})
        name: str, optional
            Does nothing.
            (default is "")
        includes: str, optional
            Path to include directory.
            Any paths referenced in CV (or overwrites), must be relative to this directory.
            (default is False)
        mask: dict, optional
            Determines what data is used to generate cv.
            (default is True)
            TODO: examples.
        overwrite: dict, optional
            A dictionary mirroring the CV file.
            Any values specified here will overwrite CV values for this build only.
            (default is False)
        """

        if len(outputs) < 1:
            raise Exception("Must have at least one valid output")
        if not theme:
            theme = Path(Path(__file__).parent, './theme_metro')

        # Filter CV data.
        masked_cv = kw_mask(self.cv, mask)

        if overwrite:
            masked_cv = kw_overwrite(masked_cv, overwrite)

        theme_config = load_json_yaml(Path(theme, "theme.yaml"))
        theme_options = {**theme_config["options"], **theme_options}

        # TODO make this work for other config files e.g. theme.yml

        jinja_env = jinja2.environment.Environment(
            loader=jinja2.FileSystemLoader(Path(theme, theme_config["env"]))
        )

        # Get the 'base' template
        template_main = jinja_env.get_template((theme_config["base"]))

        # build_dir = ".build"
        build_dir = Path(outputs[0]).parent

        # TODO do this with less assumptions.
        # TODO If no 'web' output specified, should make tmpdir and use that.

        # Copy THEME includes (css, etc)
        if "includes" in theme_config:
            safe_copy(Path(theme, theme_config["includes"]), build_dir)

        # Copy VIBE includes (images, css overwrites etc)
        if includes:
            safe_copy(includes, build_dir)

        html = template_main.render({"cv": masked_cv, "options": theme_options})

        for output in outputs:
            file_type = Path(output).suffix
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            if file_type == ".html":
                with open(output, "w+") as f:
                    f.write(html)
                print(f"Created {output}")
            elif file_type == ".pdf":
                os.environ["TMP"] = str(build_dir)
                html2pdf(html, output)
                print(f"Created {output}")
            else:
                print(f"File type {file_type} no instructions to make.")
        return

# def copy_includes():
#     shutil.copytree(src, dst)

# def load_data(json_glob):
#     def _ordinal_day(e):
#         return -datetime.date(
#             e.get("year", 1), e.get("month", 1), e.get("day", 1)
#         ).toordinal()

#     datas = []
#     for json_file in glob.glob(json_glob):
#         with open(json_file) as f:
#             data = json.load(f)
#             data = {k: sorted(v, key=_ordinal_day) for k, v in data.items()}
#             entries = list(data.values())[0]
#             for entry in entries:

#                 if "day" in entry and "month" in entry and "year" in entry:
#                     entry_time = datetime.datetime(
#                         entry["year"], entry["month"], entry["day"]
#                     )
#                     if entry_time > now:
#                         entry["year"] = "{} (to appear)".format(entry["year"])
#                     if entry_time > now - datetime.timedelta(days=365):
#                         entry["recent"] = True

#                 if "authors" in entry:
#                     authors = entry["authors"].split(", ")
#                     if len(authors) > 11:
#                         n_to_show = 4
#                         if "Colin Raffel" in authors[n_to_show]:
#                             n_to_show += 1
#                         while "*" in authors[n_to_show]:
#                             n_to_show += 1
#                         entry["authors"] = ", ".join(
#                             entry["authors"].split(", ")[:n_to_show]
#                         )
#                         n_additional = len(authors) - n_to_show
#                         entry["authors"] += f", and {n_additional} others"
#                         if "Colin Raffel" not in entry["authors"]:
#                             entry["authors"] += " including Colin Raffel"

#                     entry["authors"] = re.sub(
#                         r"(Colin Raffel)", r"<b>\1</b>", entry["authors"]
#                     )

#                 if "end" in entry and entry["end"] == "now":
#                     entry["current"] = True
#             datas.append(data)

#     return dict((k, v) for d in datas for (k, v) in d.items())
