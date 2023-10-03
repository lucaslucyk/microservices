from setuptools import setup, find_packages
# from pathlib import Path
# import subprocess


# def get_version_from_git_tag() -> str:
#     version = (
#         subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
#         .stdout.decode("utf-8")
#         .strip()
#     )

#     if "-" in version:
#         # when not on tag, git describe outputs: "1.3.3-22-gdf81228"
#         # pip has gotten strict with version numbers
#         # so change it to: "1.3.3+22.git.gdf81228"
#         # See: https://peps.python.org/pep-0440/#local-version-segments
#         v, i, s = version.split("-")
#         version = v + "+" + i + ".git." + s

#     assert "-" not in version
#     assert "." in version

#     return version


# auth_pkg_version: str = get_version_from_git_tag()

# # write version on VERSION file
# assert Path("auth_pkg/version.py").is_file()
# with open("auth_pkg/VERSION", "w", encoding="utf-8") as fh:
#     fh.write("%s\n" % auth_pkg_version)


REPO_URL = "https://github.com/lucaslucyk/microservices"


# get description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="auth_pkg",
    version="0.0.1",
    description="Sample package to use in auth microservice.",
    packages=find_packages(),
    package_data={"auth_pkg": ["VERSION"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.3.0",
        "pydantic-core>=2.6.3",
        "pydantic-settings>=2.0.3",
        "pydantic[email]"
    ],
    url=f"{REPO_URL}/tree/auth/src/auth/src/auth-pkg",
    author="Lucas Lucyk",
    author_email="lucaslucyk@gmail.com",
)
