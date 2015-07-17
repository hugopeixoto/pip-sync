import pip

exceptions = ['pip', 'setuptools']

def diff(requirements, installed):
    requirements = { r.req.key: r for r in requirements }

    to_be_installed = set()
    to_be_uninstalled = set()

    satisfied = set()

    for module in installed:
        key = module.key

        if key in exceptions:
            pass
        elif key not in requirements:
            to_be_uninstalled.add(module.as_requirement())
        elif module.version in requirements[key].specifier:
            satisfied.add(key)

    for key, requirement in requirements.items():
        if key not in satisfied:
            to_be_installed.add(requirement.req)

    return (to_be_installed, to_be_uninstalled)


def sync(to_be_installed, to_be_uninstalled):
    if to_be_uninstalled:
        pip.main(["uninstall", '-y'] + [str(req) for req in to_be_uninstalled])

    if to_be_installed:
        pip.main(["install"] + [str(req) for req in to_be_installed])

def run():
    requirements = pip.req.parse_requirements('requirements.txt', session=True)
    installed = pip.get_installed_distributions()

    to_be_installed, to_be_uninstalled = diff(requirements, installed)

    sync(to_be_installed, to_be_uninstalled)


if __name__ == '__main__':
    run()
