#!/usr/bin/env python3

import argparse
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from .cv import build_site


def main(argv=None):
    parser = argparse.ArgumentParser(prog="crass", description="Build every variant (vibe) of a CV.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build", help="Build every vibe, plus an index page.")
    serve = subparsers.add_parser("serve", help="Build, then serve the output locally.")

    for subparser in [build, serve]:
        subparser.add_argument("cv", nargs="?", default="CurriculumVitae.yaml",
                               help="CV file, yaml or json (default: CurriculumVitae.yaml).")
        subparser.add_argument("vibes", nargs="?", default="vibes.yaml",
                               help="Vibes file, yaml or json (default: vibes.yaml).")
        subparser.add_argument("--out", default="docs",
                               help="Output directory, vibe outputs are relative to this (default: docs).")
        subparser.add_argument("--no-index", action="store_true",
                               help="Don't write an index.html for flicking between vibes.")
    serve.add_argument("--port", type=int, default=8000, help="Port to serve on (default: 8000).")

    args = parser.parse_args(argv)
    build_site(args.cv, args.vibes, args.out, index=not args.no_index)

    if args.command == "serve":
        handler = functools.partial(SimpleHTTPRequestHandler, directory=args.out)
        with ThreadingHTTPServer(("", args.port), handler) as server:
            print(f"Serving '{args.out}' at http://localhost:{args.port}")
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    main()
