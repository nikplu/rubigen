#!/usr/bin/env python3

from pycparser import c_ast


class Matcher(object):
    def __init__(self, inner_matcher):
        self._inner_matcher = inner_matcher

    @property
    def inner_matcher(self):
        return self._inner_matcher


class NodeMatcher(Matcher):
    def __init__(self, node_class, inner_matcher):
        super().__init__(inner_matcher)
        self._node_class = node_class
        self._binding_name = None

    def match(self, node):
        return node.__class__ == self._node_class

    def bind(self, name: str):
        self._binding_name = name
        return self

    @property
    def node_class(self):
        return self._node_class

    @property
    def binding_name(self):
        return self._binding_name


def decl(inner_matcher=None):
    return NodeMatcher(c_ast.Decl, inner_matcher)


def func_decl(inner_matcher=None):
    return NodeMatcher(c_ast.FuncDecl, inner_matcher)


def _find_matches_impl(ast, matcher, callback, bind_stack):
    for node in ast:
        if matcher.match(node):
            binding_name = getattr(matcher, 'binding_name', None)
            if binding_name is not None:
                bind_stack.append((binding_name, node))

            if matcher.inner_matcher is not None:
                _find_matches_impl(node, matcher.inner_matcher, callback, bind_stack)
            else:
                kwargs = dict(bind_stack)
                callback(**kwargs)

            if binding_name is not None:
                bind_stack.pop()


def find_matches(ast, matcher, callback):
    _find_matches_impl(ast, matcher, callback, [])
