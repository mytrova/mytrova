from setuptools import find_packages
from setuptools import setup

if __name__ == "__main__":
    setup(
        name="data_task_1",
        version="0.0.2",
        description="",
        packages=find_packages(),
        install_requires=["httpx==0.24.1"],
        include_package_data=True,
        entry_points={'console_scripts': ['run_loader = data_task_1.cli:main']}
    )