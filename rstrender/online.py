
import requests


url = "https://livesphinx.herokuapp.com/srv/rst2html/"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}


css = '''
<style>
html {display:flex; justify-content:center}
body {
  min-width:50%; max-width:90%;
  background-color: black;
  color: white;
}

</style>
<link id="flasky" rel="stylesheet" type="text/css" href="https://livesphinx.herokuapp.com/static/sphinx/flasky.css">
<link id="pygments" rel="stylesheet" type="text/css" href="https://livesphinx.herokuapp.com/static/sphinx/pygments.css"/>
'''



def convert_rst2html(rst_path):
    with open(rst_path, 'r') as doc:
        body = doc.read()

    resp = requests.post(url, data="rst="+body, headers=headers)
    if resp.status_code == 200:
        return css+resp.text
