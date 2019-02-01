#!/usr/bin/env python3

from pycparser import c_ast


def invoke_callback(callback, active_bindings):
    callback(**active_bindings)


class NodeMatcher(object):
    def __init__(self, node_class, inner_matcher):
        self._node_class = node_class
        self._inner_matcher = inner_matcher
        self._binding_name = None

    def bind(self, name: str):
        self._binding_name = name
        return self

    def is_matching(self, node):
        return node.__class__ == self._node_class

    def match(self, node, callback, active_bindings: dict):
        for inner_node in node:
            if self.is_matching(inner_node):
                binding_name = self.binding_name
                if binding_name is not None:
                    active_bindings = active_bindings.copy()
                    active_bindings[binding_name] = inner_node

                if self.inner_matcher is not None:
                    self._inner_matcher.match(inner_node, callback, active_bindings)
                else:
                    invoke_callback(callback, active_bindings)

    @property
    def node_class(self):
        return self._node_class

    @property
    def inner_matcher(self):
        return self._inner_matcher

    @property
    def binding_name(self):
        return self._binding_name


def array_decl(inner_matcher=None):
    return NodeMatcher(c_ast.ArrayDecl, inner_matcher)


def array_ref(inner_matcher=None):
    return NodeMatcher(c_ast.ArrayRef, inner_matcher)


def assignment(inner_matcher=None):
    return NodeMatcher(c_ast.Assignment, inner_matcher)


def binary_op(inner_matcher=None):
    return NodeMatcher(c_ast.BinaryOp, inner_matcher)


def break_(inner_matcher=None):
    return NodeMatcher(c_ast.Break, inner_matcher)


def case(inner_matcher=None):
    return NodeMatcher(c_ast.Case, inner_matcher)


def cast(inner_matcher=None):
    return NodeMatcher(c_ast.Cast, inner_matcher)


def compound(inner_matcher=None):
    return NodeMatcher(c_ast.Compound, inner_matcher)


def compound_literal(inner_matcher=None):
    return NodeMatcher(c_ast.CompoundLiteral, inner_matcher)


def constant(inner_matcher=None):
    return NodeMatcher(c_ast.Constant, inner_matcher)


def continue_(inner_matcher=None):
    return NodeMatcher(c_ast.Continue, inner_matcher)


def decl(inner_matcher=None):
    return NodeMatcher(c_ast.Decl, inner_matcher)


def decl_list(inner_matcher=None):
    return NodeMatcher(c_ast.DeclList, inner_matcher)


def default(inner_matcher=None):
    return NodeMatcher(c_ast.Default, inner_matcher)


def do_while(inner_matcher=None):
    return NodeMatcher(c_ast.DoWhile, inner_matcher)


def ellipsis_param(inner_matcher=None):
    return NodeMatcher(c_ast.EllipsisParam, inner_matcher)


def empty_statement(inner_matcher=None):
    return NodeMatcher(c_ast.EmptyStatement, inner_matcher)


def enum(inner_matcher=None):
    return NodeMatcher(c_ast.Enum, inner_matcher)


def enumerator(inner_matcher=None):
    return NodeMatcher(c_ast.Enumerator, inner_matcher)


def enumerator_list(inner_matcher=None):
    return NodeMatcher(c_ast.EnumeratorList, inner_matcher)


def expr_list(inner_matcher=None):
    return NodeMatcher(c_ast.ExprList, inner_matcher)


def for_(inner_matcher=None):
    return NodeMatcher(c_ast.For, inner_matcher)


def func_call(inner_matcher=None):
    return NodeMatcher(c_ast.FuncCall, inner_matcher)


def func_decl(inner_matcher=None):
    return NodeMatcher(c_ast.FuncDecl, inner_matcher)


def func_def(inner_matcher=None):
    return NodeMatcher(c_ast.FuncDef, inner_matcher)


def goto(inner_matcher=None):
    return NodeMatcher(c_ast.Goto, inner_matcher)


def id_(inner_matcher=None):
    return NodeMatcher(c_ast.ID, inner_matcher)


def identifier_type(inner_matcher=None):
    return NodeMatcher(c_ast.IdentifierType, inner_matcher)


def if_(inner_matcher=None):
    return NodeMatcher(c_ast.If, inner_matcher)


def init_list(inner_matcher=None):
    return NodeMatcher(c_ast.InitList, inner_matcher)


def label(inner_matcher=None):
    return NodeMatcher(c_ast.Label, inner_matcher)


def named_initializer(inner_matcher=None):
    return NodeMatcher(c_ast.NamedInitializer, inner_matcher)


def param_list(inner_matcher=None):
    return NodeMatcher(c_ast.ParamList, inner_matcher)


def ptr_decl(inner_matcher=None):
    return NodeMatcher(c_ast.PtrDecl, inner_matcher)


def return_(inner_matcher=None):
    return NodeMatcher(c_ast.Return, inner_matcher)


def struct(inner_matcher=None):
    return NodeMatcher(c_ast.Struct, inner_matcher)


def struct_ref(inner_matcher=None):
    return NodeMatcher(c_ast.StructRef, inner_matcher)


def switch(inner_matcher=None):
    return NodeMatcher(c_ast.Switch, inner_matcher)


def ternary_op(inner_matcher=None):
    return NodeMatcher(c_ast.TernaryOp, inner_matcher)


def type_decl(inner_matcher=None):
    return NodeMatcher(c_ast.TypeDecl, inner_matcher)


def typedef(inner_matcher=None):
    return NodeMatcher(c_ast.Typedef, inner_matcher)


def typename(inner_matcher=None):
    return NodeMatcher(c_ast.Typename, inner_matcher)


def unary_op(inner_matcher=None):
    return NodeMatcher(c_ast.UnaryOp, inner_matcher)


def union(inner_matcher=None):
    return NodeMatcher(c_ast.Union, inner_matcher)


def while_(inner_matcher=None):
    return NodeMatcher(c_ast.While, inner_matcher)


def pragma(inner_matcher=None):
    return NodeMatcher(c_ast.Pragma, inner_matcher)


def find_matches(ast, matcher, callback):
    matcher.match(ast, callback, {})
