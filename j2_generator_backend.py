#!/usr/bin/env python3

from generator_backend import GeneratorBackend, GeneratorEnvironment
from jinja2 import Template
from pycparser import c_ast, c_generator
import copy
import ast_matchers as am
import os


class Jinja2GeneratorBackend(GeneratorBackend):
    def __init__(self, header_template: Template, source_template: Template):
        self._header_template = header_template
        self._source_template = source_template
        self._c_generator = c_generator.CGenerator()

    def _c_from_typedef(self, func_typedef):
        return self._c_generator.visit(func_typedef)

    @staticmethod
    def _typedef_from_decl(decl_of_func, name):
        new_func_decl = copy.deepcopy(decl_of_func.type)
        type_decl = am.find_nearest_type_decl(new_func_decl)
        type_decl.declname = name
        ptr_decl = c_ast.PtrDecl([], new_func_decl)
        typedef = c_ast.Typedef(name, [], ['typedef'], ptr_decl)
        return typedef

    @staticmethod
    def _render_template(template, template_context, out_path):
        with open(out_path, 'w') as f:
            f.write(template.render(template_context))

    def _generate_header_file(self, template_context, out_path):
        print('Writing header file to ' + out_path)
        self._render_template(self._header_template, template_context, out_path)

    def _generate_source_file(self, template_context, out_path):
        print('Writing source file to ' + out_path)
        self._render_template(self._source_template, template_context, out_path)

    def generate(self, options, env: GeneratorEnvironment):
        input_file_basename = os.path.basename(options.input_file)
        header_path = options.output_file_pattern.format(ext='.h')
        source_path = options.output_file_pattern.format(ext='.c')
        header_rel_path = os.path.relpath(header_path, os.path.dirname(source_path))
        ns = options.bindings_namespace
        template_context = {
            'env': env,
            'input_file_basename': input_file_basename,
            'header_path': header_path,
            'header_rel_path': header_rel_path,
            'source_path': source_path,
            'ns': ns,
            'c_from_typedef': self._c_from_typedef,
            'typedef_from_decl': self._typedef_from_decl
        }
        self._generate_header_file(template_context, header_path)
        self._generate_source_file(template_context, source_path)
