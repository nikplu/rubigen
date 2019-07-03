#!/usr/bin/env python3

import argparse
import binding_generator
from j2_generator_backend import Jinja2GeneratorBackend
from jinja2 import Template


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='The path to the input file')
    parser.add_argument('output_pattern', help='The pattern to generate the path to the output file')
    parser.add_argument('namespace', help='The namespace the generated bindings should be put in')
    parser.add_argument('-I', action='append', dest='include_paths', metavar='PATH', help='Add an include path')
    parser.add_argument(
        '-include', action='append', dest='force_includes',
        help='Force inclusion of the specified file at the top of the input file')
    parser.add_argument(
        '-D', action='append', dest='pp_definitions', metavar='MACRO[=VAL]', help='Add a preprocessor definition')
    parser.add_argument('--show-ast', action='store_true')
    parser.add_argument('--show-preprocessed-source', action='store_true')
    args = parser.parse_args()
    options = binding_generator.Options()
    options.input_file = args.input
    options.output_file_pattern = args.output_pattern
    options.bindings_namespace = args.namespace
    options.include_paths = args.include_paths
    options.force_includes = args.force_includes
    options.pp_definitions = args.pp_definitions
    options.show_ast = args.show_ast
    options.show_preprocessed_source = args.show_preprocessed_source
    with open('templates/default_binding_header.h.j2', 'r') as f:
        binding_header_template = f.read()
    with open('templates/default_binding_source.c.j2', 'r') as f:
        binding_source_template = f.read()
    binding_generator.generate_bindings(
        options, Jinja2GeneratorBackend(
            Template(binding_header_template),
            Template(binding_source_template)))


if __name__ == '__main__':
    main()
