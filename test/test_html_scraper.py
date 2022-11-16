from unittest import TestCase
from src import paths, html_scraper
from os import path

with open(path.join(paths.root_dir(), "files", "to-scrape.html")) as f:
    HTML = f.read()

FIRST_EXPECTED_SCRIPT = """
        (function () {
            const KEY = "MODE";
            const LIGHT_MODE = 'light';
            const DARK_MODE = 'dark';

            const currentMode = () => {
                const mode = localStorage.getItem(KEY);
                if (mode) {
                    return mode;
                }
                return DARK_MODE;
            }

            const setDarkMode = () => document.documentElement.classList.add(DARK_MODE);

            const setLightMode = () => document.documentElement.classList.remove(DARK_MODE);

            const mode = currentMode();
            if (mode == LIGHT_MODE) {
                setLightMode();
            } else {
                setDarkMode();
            }
        })();
    """.strip()

SECOND_EXPECTED_SCRIPT = """
        const URL_PROPERTY_REGEX = /url\((.*)\)/;

        function setupMode() {
            const KEY = "MODE";

            const LIGHT_MODE = 'light';
            const DARK_MODE = 'dark';
            const DARK_MODE_ICON = "0";
            const LIGHT_MODE_ICON = "1";

            const DISPLAY_MOBILE_NAV_CLASS = "display";

            const topNav = document.querySelector(".top-nav");
            const themeMode = document.querySelector('.theme-mode');
            const topNavMobile = document.querySelector('.top-nav-mobile');
            const navMobile = document.getElementById('nav-mobile-menu');
            const navMobileClose = document.querySelector('#nav-mobile-close');

            const currentMode = () => {
                const mode = localStorage.getItem(KEY);
                if (mode) {
                    return mode;
                }
                return DARK_MODE;
            }

            const setDarkMode = () => {
                document.documentElement.classList.add(DARK_MODE);
                localStorage.setItem(KEY, DARK_MODE)
                themeMode.textContent = DARK_MODE_ICON;
            };

            const setLightMode = () => {
                document.documentElement.classList.remove(DARK_MODE);
                localStorage.setItem(KEY, LIGHT_MODE)
                themeMode.textContent = LIGHT_MODE_ICON;
            };

            if (currentMode() == LIGHT_MODE) {
                setLightMode();
            } else {
                setDarkMode();
            }

            themeMode.addEventListener('click', e => {
                if (currentMode() == LIGHT_MODE) {
                    setDarkMode();
                } else {
                    setLightMode();
                }
                document.dispatchEvent(new Event("themeChange"));
            });

            navMobile.addEventListener('click', () => topNavMobile.classList.add(DISPLAY_MOBILE_NAV_CLASS));

            topNav.addEventListener("click", e => e.stopPropagation());

            navMobileClose.addEventListener('click', () => topNavMobile.classList.remove(DISPLAY_MOBILE_NAV_CLASS));
        }

        setupMode();
""".strip()


class TestHtmlScraper(TestCase):

    def test_should_return_meta_tags_properties(self):
        expected_properties = [
            {'charset': "UTF-8"},
            {"name": "viewport", "content": "width=device-width, initial-scale=1"},
            {"property": "description",
             "content": "Personal site of Igor Roztropiński"},
            {"name": "author", "content": "Igor Roztropiński"}
        ]

        self.assertEqual(expected_properties,
                         html_scraper.meta_tags_properties(HTML))

    def test_should_return_all_href_values(self):
        expected_href_values = [
            "/css/styles_1666107074.css",
            "home", "about", "skills", "experience", "code",
            "https://youtube.com",
            "home", "about", "skills", "experience", "code"
        ]

        self.assertEqual(expected_href_values,
                         html_scraper.matching_property_values(HTML, "href", ".*"))

    def test_should_return_absolute_href_values(self):
        expected_href_values = ["https://youtube.com"]

        self.assertEqual(expected_href_values,
                         html_scraper.matching_property_values(HTML, "href", "http.*"))

    def test_should_return_all_property_values_matching_pattern(self):
        expected_property_values = ["top-nav fade-in hidden",
                                    "hidden-link",
                                    "top-nav-mobile fade-in hidden",
                                    "hidden"]

        self.assertEqual(expected_property_values,
                         html_scraper.matching_property_values(HTML, "class",
                                                               "top-.*|hidden.*"))

    def test_should_return_all_script_tags_data(self):
        expected_script_tags_data = [
            (FIRST_EXPECTED_SCRIPT, {}),
            (SECOND_EXPECTED_SCRIPT, {}),
            ("", {"type": "module", "src": "/js/rain-app_1666107074.js"}),
            ("", {"type": "module", "src": "/js/app_1666107074.js"})]

        self.assertEqual(expected_script_tags_data,
                         html_scraper.script_tags_data(HTML))
