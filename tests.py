from main import modify_page


def wrap_html_body_and_test(source, result):
    html = '''<html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <style type="text/css">
                        lorems
                    </style>
                    <title>Title</title>
                </head>
                <body>
                    {0}
                </body>
            </html>'''
    assert modify_page(html.format(source)) == html.format(result)


def test_simple_text():
    text_source = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus consequat tellus sapien. 
                    Maecenas viverra magna ut ex porta interdum. In venenatis ex quis dignissim auctor.'''
    text_result = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus consequat tellus™ sapien™. 
                    Maecenas viverra magna ut ex porta interdum. In venenatis ex quis dignissim auctor™.'''
    wrap_html_body_and_test(text_source, text_result)


def test_with_html_tags():
    text_source = '''<div class="lorems">Lorem ipsum dolor sit amet, <strong lorems="1">consectetur adipiscing 
                    elit.</strong> Phasellus consequat tellus sapien. 
                    Maecenas viverra magna ut ex porta interdum. In venenatis ex quis dignissim auctor.</div>'''
    text_result = '''<div class="lorems">Lorem ipsum dolor sit amet, <strong lorems="1">consectetur adipiscing 
                    elit.</strong> Phasellus consequat tellus™ sapien™. 
                    Maecenas viverra magna ut ex porta interdum. In venenatis ex quis dignissim auctor™.</div>'''
    wrap_html_body_and_test(text_source, text_result)
