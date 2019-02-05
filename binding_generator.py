#!/usr/bin/env python3

from pcpp import Preprocessor
import pycparser_fake_libc
import pycparser
import io
import ast_matchers as am
from generator_backend import GeneratorBackend, GeneratorEnvironment, BindableFunction


_func_decl_matcher = am.decl(am.func_decl()).bind('decl')


class Options(object):
    input_file = None
    output_directory = None
    out_prefix = None
    include_paths = None
    pp_definitions = None
    show_ast = None


def preprocess(options):
    pp = Preprocessor()

    if options.pp_definitions:
        for d in options.pp_definitions:
            if '=' not in d:
                d += '=1'
            d = d.replace('=', ' ', 1)
            pp.define(d)

    # always parse the source as ISO C
    pp.define('__STDC__ 1')

    if options.include_paths:
        for i in options.include_paths:
            pp.add_path(i)
    pp.add_path(pycparser_fake_libc.directory)

    with open(options.input_file) as f:
        pp.parse(f)

    mem_f = io.StringIO()
    pp.write(mem_f)

    return mem_f.getvalue()


def parse_into_ast(pp_source, options):
    parser = pycparser.CParser()
    return parser.parse(pp_source, options.input_file)


def generate_bindings_from_ast(ast, options, backend):
    env = GeneratorEnvironment()

    functions = []

    def matcher_callback(decl):
        functions.append(BindableFunction(decl))

    am.find_matches(ast, _func_decl_matcher, matcher_callback)

    env.functions = functions

    backend.generate(options, env)


def generate_bindings(options: Options, backend: GeneratorBackend):
    pp_source = preprocess(options)
    print(pp_source)
    ast = parse_into_ast(pp_source, options)
    if options.show_ast:
        ast.show()
    generate_bindings_from_ast(ast, options, backend)
