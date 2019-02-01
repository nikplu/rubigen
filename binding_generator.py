#!/usr/bin/env python3

from pcpp import Preprocessor
import pycparser_fake_libc
import pycparser
from pycparser import c_ast, c_generator
import io
import ast_matchers as am


_func_decl_matcher = am.decl(am.func_decl().bind('func_decl'))


class Options(object):
    input_file = None
    output_directory = None
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


def transform_to_func_ptr(d):
    ptr_decl = c_ast.PtrDecl([], d)
    typedef = c_ast.Typedef(d.type.declname, [], ['typedef'], ptr_decl)
    return typedef


def generate_bindings_from_ast(ast, options):
    func_decls = []

    def matcher_callback(func_decl):
        func_decls.append(func_decl)
    am.find_matches(ast, _func_decl_matcher, matcher_callback)

    print(func_decls)
    gen = c_generator.CGenerator()
    for f in func_decls:
        print(gen.visit(transform_to_func_ptr(f)))


def generate_bindings(options):
    print(options.__dict__)
    pp_source = preprocess(options)
    print(pp_source)
    ast = parse_into_ast(pp_source, options)
    if options.show_ast:
        ast.show()
    generate_bindings_from_ast(ast, options)
