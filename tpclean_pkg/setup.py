import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='tpclean',  
     version='0.6.5',
     author="Tino Pietrassyk",
     author_email="pietrassyk@gmail.com",
     description="Custom library of functions for Data Science workflow automation",
     long_description=long_description,
    long_description_content_type="text/markdown",
     url="https://github.com/Pietrassyk/tpclean",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
