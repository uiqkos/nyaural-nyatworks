from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt', 'r') as f:
        return list(map(str.strip, f.readlines()))


if __name__ == '__main__':
    setup(
        name='nyaural_nyatworks',
        version='0.2',
        author='uiqkos',
        author_email='uiqkos@gmail.com',
        install_requires=get_requirements(),
        packages=find_packages(),
    )
