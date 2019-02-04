#!/usr/bin/env python3

from pycparser import c_ast
from dataclasses import dataclass


@dataclass
class BindableFunction:
    decl: c_ast.Decl


class GeneratorEnvironment(object):
    functions: [BindableFunction] = None


class GeneratorBackend(object):
    def generate(self, options, env: GeneratorEnvironment):
        raise NotImplementedError()
