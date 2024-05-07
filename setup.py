import setuptools

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setuptools.setup(name='booking_management',
                 packages=['booking_management'],
                 install_requires=install_requires)
