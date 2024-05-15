from setuptools import setup, find_packages

# Read requirements from your requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='whissle_audio_api',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'audio_api=audio_api.app:create_app',
        ],
    },
)
