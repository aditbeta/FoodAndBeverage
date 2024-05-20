import setuptools

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setuptools.setup(name='travel_booking_system',
                 packages=['travel_booking_system'],
                 install_requires=install_requires)
