from distutils.core import setup
import py2exe

setup(
    options = {'py2exe': {'bundle_files': 1}},
windows = [
{
"script": "DateStamper.pyw",
"icon_resources":[(1,"icons/icon.ico")]
}
],
    zipfile = None,
)