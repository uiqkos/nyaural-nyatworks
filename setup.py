from setuptools import setup


def get_requirements():
    with open('requirements.txt', 'r') as f:
        return list(map(str.strip, f.readlines()))


if __name__ == '__main__':
    setup(
        name='nyaural_nyatworks',
        version='0.1',
        author='uiqkos',
        author_email='uiqkos@gmail.com',
        install_requires=get_requirements(),
        packages=['nya_app', 'nya_ml', 'nya_ml_research', 'nya_scraping', 'nya_utils'],
    )
