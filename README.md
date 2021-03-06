Use standard python packages in your Blender add-ons
====================================================

Blender add-ons are written in Python, and Python has a huge and rich library of packages available (namely https://pypi.org). However, there is no obvious way to make use of these packages from a Blender add-on. This is an effort at allowing add-ons to specify requirements, and allow users to download and install them easily.

See `__init__.py` for a simple example plugin that uses the `random-words` package to create random words in Blender at the click of a button. The preferences panel allows the user to install the requirements, after which a "Random Words" panel will appear in the "N" menu.

The idea is all the requirements checking and installation is in `blender_pydeps.py`, which you can just import, and focus on writing your add-on.

```
from .blender_pydeps import PythonRequirements

python_requirements = PythonRequirements([
    'firstpackage',
    'secondpackage>=3.2.1',
    ('third_package', __import__),
    ('fourth-package', lambda _: __import__('fourth_package)),
])

if python_requirements.requirements_installed:
    print("Requirements are already installed")

python_requirements.install_missing_requirements()
```

You can specify your requirements in various different ways, as illustrated above. When the code checks each one, it will behave in slightly different ways.

* The code will check whether `firstpackage` is installed by seeing if it shows up in the output of `pip list`. When it installs it, it'll install any available version as no specific version is requested. If you just want to get the package installed by all means necessary, you can use this lazy option.
* `secondpackage` will also be checked using `pip list`, but the version will also be checked, and if the package needs to be installed or upgraded the requested version will be passed to `pip install`.
* `third_package` will be checked using the `__import__` function, to which the package name will be passed. If the package name can be imported, the package is considered to be installed. If you do this for all your requirements, the slightly slow and skanky `pip list` stage will be skipped.
* Some packages, like `fourth-package`, don't have modules that are named the same as the package (in this case the `-` would make the module name invalid). So we've provided a callable which will try to import the correct module name. If you like, you can pass a more involved function that checks the version etc.

Incidentlally, nothing in `blender_pydeps.py` is actually tied to Blender, so in theory there might be other uses for the same code.


Status
======

Not very well tested. It seems to work on my Ubuntu 20.10 machine, and on Windows 10 (running Blender as administrator). I suspect it might work on macOS but I hvan't tried it. Feel free to report issues.


Issues and Limitations
======================

Some packages require a development environment, C headers etc. These packages are unlikely to install on most end-users' machines. The code passes the `--prefer-binary` switch to pip when installing, so if there's a choice between an older binary and a newer source-based package, it'll favour the former.

If you *do* have a development environment and you want to install packages from source on your machine, you could try something like the following:

```
python_requirements = PythonRequirements([
    "opencv-python",
])
_environ = dict(os.environ)
try:
    os.environ['C_INCLUDE_PATH'] = "/usr/include/python3.7m"
    os.environ['CPLUS_INCLUDE_PATH'] = "/usr/include/python3.7m"
    python_requirements.install_requirements()
finally:
    os.environ.clear()
    os.environ.update(_environ)
```


Credit
======
Heavily inspired by Robert Guetzkow's similar project, https://github.com/robertguetzkow/blender-python-examples/.
