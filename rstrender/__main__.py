#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import tempfile
import webbrowser

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('filepath', help='path to .rst file')
parser.add_argument('--online-converter', '-c', help='use livesphinx.herokuapp.com API', action='store_true')
args = parser.parse_args()


if args.online_converter:
    from .online import convert_rst2html
else:
    from .local import rst2html as convert_rst2html


script = '''
<script>
setTimeout(()=>location.reload(), 10000)
</script>
'''

class MyHandler(FileSystemEventHandler):
    def __init__(self, filepath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tmp_file = tempfile.NamedTemporaryFile('w', delete=True, suffix='.html')
        self.convert_write(filepath)
        print('file://' + self.tmp_file.name)
        self.open_in_browser()


    def convert_write(self, filepath):
        converted = convert_rst2html(filepath)
        if converted:
            self.tmp_file.truncate(0)
            self.tmp_file.write(converted+script)
            self.tmp_file.flush()

    def on_modified(self, event):
        if not event.is_directory and event.event_type =='modified':
            self.convert_write(event.src_path)

    def open_in_browser(self):
        url = 'file://' + self.tmp_file.name
        webbrowser.open(url)

    def stop(self):
        self.tmp_file.close()



# with tempfile.NamedTemporaryFile('w', delete=True, suffix='.html') as f:
# # with open("file.html", 'w') as f:
#     url = 'file://' + f.name
#     f.write(css+resp.text)
#     webbrowser.open(url)
#     import time
#     time.sleep(20)



if __name__ == "__main__":
    event_handler = MyHandler(args.filepath)
    observer = Observer()
    observer.schedule(event_handler, path=args.filepath, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    event_handler.stop()
