import pip
import itertools

exceptions = ['pip', 'setuptools']
required = {
        r.req.key: r
        for r in pip.req.parse_requirements('requirements.txt', session=True)
        }

installed = pip.get_installed_distributions()

satified = set()

for installed in installed:
    key = installed.key

    if key in exceptions:
        print("whitelisted {}".format(key))
    elif key in required and installed.version in required[key].specifier:
        satified.add(key)
    else:
        print("uninstall {}".format(key))

for key, requirement in required.items():
    if key not in satified:
        print("install {}".format(requirement))

