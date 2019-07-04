#!/usr/bin/env python3

import copy
import ast_matchers as am
import os
from generator_backend import GeneratorBackend, GeneratorEnvironment
from jinja2 import Environment
from pycparser import c_ast, c_generator
from dataclasses import dataclass


@dataclass
class Output:
    name: str
    output_path: str
    template_name: str


class Jinja2GeneratorBackend(GeneratorBackend):
    def __init__(self, outputs: [Output], j2_env: Environment):
        self._outputs = outputs
        self._output_name_index = {x.name: x for x in self._outputs}  # type: {str: Output}
        self._j2_env = j2_env
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

    def _render_template(self, template_name, template_context, out_path):
        with open(out_path, 'w') as f:
            template = self._j2_env.get_template(template_name)
            f.write(template.render(template_context))

    def _rel_outpath(self, to_name: str, from_name: str):
        to_path = self._output_name_index[to_name].output_path
        from_path = self._output_name_index[from_name].output_path
        from_dirname = os.path.dirname(from_path)
        return os.path.relpath(to_path, from_dirname)

    @staticmethod
    def _strip_prefix(text: str, prefix: str):
        return text[len(prefix):] if text.startswith(prefix) else text

    def generate(self, options, env: GeneratorEnvironment):
        self._j2_env.filters['stripprefix'] = self._strip_prefix
        self._j2_env.filters['c_from_typedef'] = self._c_from_typedef
        self._j2_env.filters['typedef_from_decl'] = self._typedef_from_decl

        input_file_basename = os.path.basename(options.input_file)
        ns = options.bindings_namespace
        force_includes = options.force_includes
        pp_definitions = options.pp_definitions
        template_context = {
            'env': env,
            'input_file_basename': input_file_basename,
            'ns': ns,
            'force_includes': force_includes,
            'pp_definitions': pp_definitions
        }

        for output in self._outputs:
            print('[{}] {} -> {}'.format(output.name, output.template_name, output.output_path))
            template_context['rel_outpath'] = lambda x: self._rel_outpath(x, output.name)
            self._render_template(output.template_name, template_context, output.output_path)
