import spynner
import time
from StringIO import StringIO
debug_stream = StringIO()
import os
bp = os.path.dirname("./")
browser = spynner.Browser(debug_level=spynner.DEBUG, debug_stream=debug_stream)
def wait_load(br):
    # browser.runjs("console.log(document.getElementsById('test').innerHTML = 'test212';)")
    # return  'test212' in browser.html
    # if "$" in str(browser.runjs("document.getElementById('test').innerHTML;").toString()):
    #     browser.runjs('MathJax.Hub.Queue(["Typeset",MathJax.Hub]);')
    print str(browser.runjs("document.getElementById('test').innerHTML;").toString())
    return "MathJax" in str(browser.runjs("document.getElementById('test').innerHTML;").toString())
browser.load("sample-tex.html", 1, wait_callback=wait_load)
print str(browser.runjs("document.getElementsByClassName('MathJax_Display')[0].innerHTML;").toString())
