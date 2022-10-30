
import os

from docutils.core import publish_string

CWD = os.path.dirname(os.path.abspath(__file__))

# see http://docutils.sourceforge.net/docs/user/config.html
default_rst_opts = {
    'no_generator': True,
    'no_source_link': True,
    'tab_width': 4,
    'file_insertion_enabled': False,
    'raw_enabled': False,
    'stylesheet_path': None,
    'traceback': True,
    'halt_level': 5,
    'syntax_highlight': 'long',
}



def rst2html(rst_path, theme=None, opts=None):
    rst_opts = default_rst_opts.copy()
    if opts:
        rst_opts.update(opts)
    rst_opts['template'] = os.path.join(CWD, 'themes', 'template.txt')

    stylesheets = ['common.css', 'flasky.css', 'pygments.css']
    if theme:
        stylesheets.append('%s/%s.css' % (theme, theme))
    rst_opts['stylesheet'] = ','.join([os.path.join(CWD, 'themes', p) for p in stylesheets ])

    with open(rst_path, 'r') as doc:
        rst = doc.read()

    out = publish_string(rst, writer_name='html', settings_overrides=rst_opts)
    # print(out.decode())
    return out.decode()
