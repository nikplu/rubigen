#!/usr/bin/env python3

import argparse
import binding_generator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='The path to the input file')
    parser.add_argument('output', help='The path to the output directory')
    parser.add_argument('-I', action='append', dest='include_paths', metavar='PATH', help='Add an include path')
    parser.add_argument(
        '-D', action='append', dest='pp_definitions', metavar='MACRO[=VAL]', help='Add a preprocessor definition')
    parser.add_argument('--show-ast', action='store_true')
    args = parser.parse_args()
    options = binding_generator.Options()
    options.input_file = args.input
    options.output_directory = args.output
    options.include_paths = args.include_paths
    options.pp_definitions = args.pp_definitions
    options.show_ast = args.show_ast
    binding_generator.generate_bindings(options)


if __name__ == '__main__':
    main()
