from flask import Markup
from markupsafe import Markup

def register_filters(app):
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        if text is None:
            return ''
        return text.replace('\n', '<br>\n')

    @app.template_filter('nl2br_safe')
    def nl2br_safe_filter(text):
        if text is None:
            return ''
        return Markup(text.replace('\n', '<br>\n'))