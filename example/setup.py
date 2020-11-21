from setuptools import setup


setup(
    name="example-brotli-project",
    version="0.1.0",
    py_modules=["example_brotli_project"],
    install_requires=[
        "brotli; implementation_name == 'cpython'",
        "brotlicffi; implementation_name != 'cpython'"
    ],
    entry_points={
        "console_scripts": [
            "example-brotli-project=example_brotli_project:main"
        ]
    }
)
