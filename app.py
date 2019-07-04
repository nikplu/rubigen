#!/usr/bin/env python3

import os
import argparse
import binding_generator
from j2_generator_backend import Jinja2GeneratorBackend, Output
from jinja2 import Environment, FileSystemLoader, ChoiceLoader


class FatalCliError(RuntimeError):
    pass


def _parse_outputs(output_strs, out_prefix):
    outputs = []
    for output_str in output_strs:
        try:
            name, output_path, template_str = output_str.split('=')
        except ValueError:
            raise FatalCliError(
                '{} cannot be parsed as an output designator'.format(output_str))
        if out_prefix is not None:
            output_path = os.path.join(out_prefix, output_path)
        outputs.append(Output(name, output_path, template_str))
    return outputs


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='the path to the input file')
    parser.add_argument('namespace', help='the namespace the generated bindings should be put in')
    parser.add_argument('-I', action='append', dest='include_paths', metavar='PATH', help='add an include path')
    parser.add_argument(
        '-include', action='append', dest='force_includes',
        help='force inclusion of the specified file at the top of the input file')
    parser.add_argument(
        '-D', action='append', dest='pp_definitions', metavar='MACRO[=VAL]', help='add a preprocessor definition')
    parser.add_argument('-T', action='append', dest='template_dirs', help='add a template directory')
    parser.add_argument('-o', action='append', dest='outputs',
                        help='generate an output file at FILE using TEMPLATE with the name NAME',
                        metavar='NAME=FILE=TEMPLATE')
    parser.add_argument('--out-prefix', help='output path prefix')
    parser.add_argument('--show-ast', action='store_true')
    parser.add_argument('--show-preprocessed-source', action='store_true')
    args = parser.parse_args()
    options = binding_generator.Options(
        input_file = args.input,
        bindings_namespace = args.namespace,
        include_paths = args.include_paths,
        force_includes = args.force_includes,
        pp_definitions = args.pp_definitions,
        show_ast = args.show_ast,
        show_preprocessed_source = args.show_preprocessed_source
    )

    loaders = [FileSystemLoader('templates')]
    if args.template_dirs is not None:
        loaders += [FileSystemLoader(x) for x in args.template_dirs]

    j2_env = Environment(loader=ChoiceLoader(loaders))

    try:
        if args.outputs is None:
            raise FatalCliError('no outputs')

        outputs = _parse_outputs(args.outputs, args.out_prefix)
        binding_generator.generate_bindings(options, Jinja2GeneratorBackend(outputs, j2_env))
    except FatalCliError as e:
        print('fatal: ' + str(e))
        parser.print_help()


if __name__ == '__main__':
    _main()
