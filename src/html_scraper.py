import re

META_TAG_PATTERN = re.compile("(?s)<meta(.*?)/?>")
PROPERTIES_PATTERN = re.compile("(\\S+)\\s*=\\s*\"(.+?)\"")
SCRIPT_TAG_PATTERN = re.compile("(?s)<script(.*?)>(.*?)</script>")


def meta_tags_properties(html):
    return [_properties_of_group(r) for r in META_TAG_PATTERN.findall(html)]


def _properties_of_group(group):
    return {k: v for k, v in PROPERTIES_PATTERN.findall(group)}


def matching_property_values(html,
                             property_key,
                             property_regex):
    property_pattern = re.compile(f"{property_key}\\s*=\\s*\"({property_regex}?)\"")
    return property_pattern.findall(html)


def script_tags_data(html):
    return [(s.strip(), _properties_of_group(props))
            for props, s in SCRIPT_TAG_PATTERN.findall(html)]
