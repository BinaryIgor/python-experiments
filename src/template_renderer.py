import re

_VARIABLE_PATTERN_STR = "\\$([a-zA-Z0-9-_.]+)"
VARIABLE_PATTERN = re.compile(_VARIABLE_PATTERN_STR)
OBJECT_VARIABLE_PATTERN = re.compile("(.+?)\\.(.+)")

IF_PATTERN = re.compile("(?s)\\{\\{\\s*if\\s*%s\\s*}}(.*?)\\{\\{\\s*end\\s*}}"
                        % _VARIABLE_PATTERN_STR)
NESTED_IF_PATTERN = re.compile("(?s)\\{-\\s*if\\s*%s\\s*-}(.*?)\\{-\\s*end\\s*-}"
                               % _VARIABLE_PATTERN_STR)

FOR_PATTERN = re.compile("(?s)\\{\\{\\s*for\\s*%s\\s*in\\s*%s\\s*}}[\r\n]*(.*?)\\{\\{\\s*end\\s*}}" %
                         (_VARIABLE_PATTERN_STR, _VARIABLE_PATTERN_STR))

_FIRST_VAR = "_first_"
_LAST_VAR = "_last_"
_NOT_LAST_VAR = "_not_last_"


def render(template, variables):
    def replace_if(match, variables):
        if_var = match.group(1)
        to_render_block = match.group(2).strip()
        return _replace_variables(to_render_block, variables) \
            if variables.get(if_var) else ""

    def replace_for(match):
        el_var = match.group(1)
        coll_var = match.group(2)
        to_render_block = match.group(3)

        coll_value = variables.get(coll_var, [])
        lines_to_replace = []

        extended_variables = variables.copy()

        for i, e in enumerate(coll_value):
            first = i == 0
            extended_variables[_FIRST_VAR] = first
            extended_variables[_LAST_VAR] = i == (len(coll_value) - 1)
            extended_variables[_NOT_LAST_VAR] = not extended_variables[_LAST_VAR]
            extended_variables[el_var] = e

            without_ifs_block = NESTED_IF_PATTERN.sub(
                lambda x: replace_if(x, extended_variables),
                to_render_block)

            sanitized_block = without_ifs_block.strip() \
                if first else without_ifs_block.rstrip()

            lines_to_replace.append(_replace_variables(sanitized_block,
                                                       extended_variables))

        return "\n".join(lines_to_replace)

    without_ifs_template = IF_PATTERN.sub(lambda x: replace_if(x, variables),
                                          template)

    without_fors_template = FOR_PATTERN.sub(replace_for, without_ifs_template)

    return _replace_variables(without_fors_template, variables)


def _replace_variables(template, variables):
    def replace_var(match):
        var_key = match.group(1)

        object_match = OBJECT_VARIABLE_PATTERN.match(var_key)
        if object_match:
            obj_var = object_match.group(1)
            obj_field = object_match.group(2)
            obj_value = variables.get(obj_var, {})

            return str(obj_value.__dict__[obj_field])

        return str(variables.get(var_key, ""))

    return VARIABLE_PATTERN.sub(replace_var, template)
