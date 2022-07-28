import ast
from pathlib import Path
from typing import List

import parso
from jedi import Script
from jedi.api import classes, helpers
from jedi.api.helpers import validate_line_column
from jedi.inference.gradual.conversion import convert_names, convert_values
from parso.python.tree import Module, PythonNode


class MMScript(Script):

    def __init__(self, code=None, *, path=None, environment=None, project=None, scope=None):
        self.scope = scope
        super().__init__(code, path=path, environment=environment, project=project)

    @validate_line_column
    def goto(
        self,
        line=None,
        column=None,
        *,
        follow_imports=False,
        follow_builtin_imports=False,
        only_stubs=False,
        prefer_stubs=False,
    ):
        """Goes to the name that defined the object under the cursor.
        Optionally you can follow imports. Multiple objects may be returned,
        depending on an if you can have two different versions of a function.

        :param follow_imports: The method will follow imports.
        :param follow_builtin_imports: If ``follow_imports`` is True will try
            to look up names in builtins (i.e. compiled or extension modules).
        :param only_stubs: Only return stubs for this method.
        :param prefer_stubs: Prefer stubs to Python objects for this method.
        :rtype: list of :class:`.Name`
        """
        tree_name = self._module_node.get_name_of_position((line, column))
        if tree_name is None:
            # Without a name we really just want to jump to the result e.g.
            # executed by `foo()`, if we the cursor is after `)`.
            return self.infer(line, column, only_stubs=only_stubs, prefer_stubs=prefer_stubs)
        name = self._get_module_context().create_name(tree_name)

        # Make it possible to goto the super class function/attribute
        # definitions, when they are overwritten.
        names = []
        if name.tree_name.is_definition() and name.parent_context.is_class():
            class_node = name.parent_context.tree_node
            class_value = self._get_module_context().create_value(class_node)
            mro = class_value.py__mro__()
            next(mro)  # Ignore the first entry, because it's the class itself.
            for cls in mro:
                names = cls.goto(tree_name.value)
                if names:
                    break

        base_files = find_base_files(self._module_node, self.path.parent)
        if name.tree_name.is_definition() and base_files:
            defs = search_def_in_bases(name.string_name, base_files)
            if defs:
                return defs

        if not names:
            names = list(name.goto())

        if follow_imports:
            names = helpers.filter_follow_imports(names, follow_builtin_imports)
        names = convert_names(
            names,
            only_stubs=only_stubs,
            prefer_stubs=prefer_stubs,
        )

        defs = [classes.Name(self._inference_state, d) for d in set(names)]
        # Avoid duplicates
        return list(set(helpers.sorted_definitions(defs)))

    @validate_line_column
    def infer(self, line=None, column=None, *, only_stubs=False, prefer_stubs=False):
        """Return the definitions of under the cursor. It is basically a
        wrapper around Jedi's type inference.

        This method follows complicated paths and returns the end, not the
        first definition. The big difference between :meth:`goto` and
        :meth:`infer` is that :meth:`goto` doesn't
        follow imports and statements. Multiple objects may be returned,
        because depending on an option you can have two different versions of a
        function.

        :param only_stubs: Only return stubs for this method.
        :param prefer_stubs: Prefer stubs to Python objects for this method.
        :rtype: list of :class:`.Name`
        """
        pos = line, column
        leaf = self._module_node.get_name_of_position(pos)
        if leaf is None:
            leaf = self._module_node.get_leaf_for_position(pos)
            if leaf is None or leaf.type == "string":
                if (leaf.parent.type == "argument" and leaf.parent.children[0].value == "type"):
                    defs = get_type_defs(leaf, self)
                    if defs:
                        return defs
                return []
            if leaf.end_pos == (line, column) and leaf.type == "operator":
                next_ = leaf.get_next_leaf()
                if next_.start_pos == leaf.end_pos and next_.type in (
                        "number",
                        "string",
                        "keyword",
                ):
                    leaf = next_

        context = self._get_module_context().create_context(leaf)

        values = helpers.infer(self._inference_state, context, leaf)
        values = convert_values(
            values,
            only_stubs=only_stubs,
            prefer_stubs=prefer_stubs,
        )

        defs = [classes.Name(self._inference_state, c.name) for c in values]
        # The additional set here allows the definitions to become unique in an
        # API sense. In the internals we want to separate more things than in
        # the API.
        return helpers.sorted_definitions(set(defs))


def find_base_files(module: Module, root_path: Path) -> list:
    definitions = helpers.get_module_names(module, all_scopes=False)
    for definition in definitions:
        if definition.value == "_base_":
            base_node: ast.Assign = ast.parse(definition.parent.get_code()).body[0]

            if not isinstance(base_node, ast.Assign):
                return []
            target = base_node.value
            if isinstance(target, (ast.List, ast.Tuple)):
                base_files = target.elts
            elif isinstance(target, ast.Constant):
                base_files = [target]
            else:
                return []

            return [root_path / file.value for file in base_files]
    return []


def search_def_in_bases(name, base_files):
    for base in base_files:
        script = MMScript(path=base)
        defs = script._get_module_context().goto(name, script._module_node.end_pos)
        if defs:
            defs = [classes.Name(script._inference_state, d) for d in set(defs)]
            return list(set(helpers.sorted_definitions(defs)))
        nested_base_files = find_base_files(script._module_node, base.parent)
        defs = search_def_in_bases(name, nested_base_files)
        if defs:
            return defs
    return []


def find_full_arg_name(leaf: PythonNode) -> str:
    parent = leaf.search_ancestor("expr_stmt", "argument")
    if parent.type == "argument":
        return find_full_arg_name(parent) + "." + parent.children[0].value
    else:
        return parent.children[0].value


def get_type_defs(leaf: PythonNode, script: MMScript):
    from jedi.inference.imports import goto_import

    from .scopes import PatternItem, parse_pattern_list

    pattern_list: List[PatternItem] = parse_pattern_list(script.scope)
    if pattern_list is None:
        return []

    full_arg_name = find_full_arg_name(leaf)
    registry = None
    for item in pattern_list:
        if item.pattern.match(full_arg_name):
            if item.imports is not None:
                item.imports()
            registry = item.registry()

    if registry is not None:
        class_ = registry.get(leaf.value.strip("'\""))
        pseudo_node = parso.parse(f"from {class_.__module__} import {class_.__name__}")
        classes_ = goto_import(
            script._get_module_context(),
            pseudo_node.children[0].get_last_leaf(),
        )
        defs = [classes.Name(script._inference_state, c) for c in classes_]
        return defs
    return []
