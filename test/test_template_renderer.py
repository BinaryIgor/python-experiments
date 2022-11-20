from unittest import TestCase

from src import template_renderer

VARIABLES_TEMPLATE = """
Hello $some_var1!

Some long and probably boring text...

Best,
$some_var2
""".strip()

RENDERED_VARIABLES_TEMPLATE = """
Hello nice-user!

Some long and probably boring text...

Best,
nicer-user
""".strip()

IF_TEMPLATE = """
<body>
    {{ if $some-var }}
    <div>$to_show_var is being shown!</div>
    {{ end }}
</body>
""".strip()

IF_TRUE_RENDERED_TEMPLATE = """
<body>
    <div>22 is being shown!</div>
</body>
""".strip()

IF_FALSE_RENDERED_TEMPLATE = """
<body>
    
</body>
""".strip()

FOR_TEMPLATE = """
<body>
    {{ for $e in $items }}
    <p>{- if $_first_ -}!!!{- end -}$e - $suffix</p>
    {- if $_last_ -}
    <p>Last one!</p>
    {- end -}
    {{ end }}
</body>
""".strip()

FOR_RENDERED_TEMPLATE = """
<body>
    <p>!!!first var - addon</p>
    <p>2 var - addon</p>
    <p>last_one - addon</p>
    <p>Last one!</p>
</body>
""".strip()

FOR_OBJECTS_TEMPLATE = """
INSERT INTO user (id, name) VALUES 
    {{ for $e in $items }}
    ($e.id, '$e.name'){- if $_not_last_ -},{- end -}
    {{ end }};
""".strip()

FOR_OBJECTS_RENDERED_TEMPLATE = """
INSERT INTO user (id, name) VALUES 
    (22, 'Second Object'),
    (101, 'One Hundredth Object'),
    (1111, 'Last Object');
""".strip()


class SomeObject:

    def __init__(self, id, name):
        self.id = id
        self.name = name


class TestTemplateRenderer(TestCase):

    def test_should_render_template_with_variables(self):
        self.assertEqual(RENDERED_VARIABLES_TEMPLATE,
                         template_renderer.render(VARIABLES_TEMPLATE,
                                                  {"some_var1": "nice-user",
                                                   "some_var2": "nicer-user"}))

    def test_should_render_template_with_if_true(self):
        self.assertEqual(IF_TRUE_RENDERED_TEMPLATE,
                         template_renderer.render(IF_TEMPLATE,
                                                  {"some-var": True,
                                                   "to_show_var": 22}))

    def test_should_render_template_with_if_false(self):
        self.assertEqual(IF_FALSE_RENDERED_TEMPLATE,
                         template_renderer.render(IF_TEMPLATE,
                                                  {"some-var": False}))

    def test_should_render_template_with_for(self):
        self.assertEqual(FOR_RENDERED_TEMPLATE,
                         template_renderer.render(FOR_TEMPLATE,
                                                  {
                                                      'items': ['first var',
                                                                '2 var',
                                                                "last_one"],
                                                      'suffix': "addon"
                                                  }))

    def test_should_render_template_with_for_objects(self):
        self.assertEqual(FOR_OBJECTS_RENDERED_TEMPLATE,
                         template_renderer.render(FOR_OBJECTS_TEMPLATE,
                                                  {
                                                      'items': [
                                                          SomeObject(22, "Second Object"),
                                                          SomeObject(101, "One Hundredth Object"),
                                                          SomeObject(1111, "Last Object")]
                                                  }))
