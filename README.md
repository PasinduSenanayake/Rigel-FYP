

<h1 align="center">C - OpenMp Optimizer </h1>

<div align="center">

[OpenMp](http://www.openmp.org/) Optimizer for C codes. ( This research project is still under development )


</div>

## Pre-Requirements

1. [Python](https://www.python.org/) [ Version - 2.7.10 ~ 2.7.14 ]
2. [PIP](https://pypi.python.org/pypi/pip) [ Version 9.0.1 ]

## Installation

For the moment C - OpenMp Optimizer is only available as an open source git project.

After cloning the git repository, execute
```sh
python Initialize.py
```

## Initialization

Valid .c file is required for the execution of optimizer. Copy all the required files in to Sandbox folder.
```sh
python Initializer.py -fp FPATH [-fa FARGUMENTS] [-ca CARGUMENTS]
```
Example :
```sh
    python Initializer.py -fp $Home/test.c -fa 2 -ca "-lgmp -lssl"
```
Parameters :<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-fp : Absolute path to the .c file [ Required ]<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-fa : Arguments required for executable file ( Optional )<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-ca : Arguments required for the .c file compilation  [ except "-fopenmp" ] ( Optional )<br /><br />
Output:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For this moment, this execution will provide some advices related to achievable performance enhancements in scheduling mechanisms. ( Only if the input .c file contains 'parallel for' loops.)
## Framework

### 1. Dependency Manager

This framework contains a python dependency manager.
1. Install a new dependency <br/>
```sh
python Handler.py install [depName] [specific version]
```
Example :
```sh
    python Handler.py install ompp 1.0.1
```
2. Uninstall a dependency <br/>
```sh
python Handler.py uninstall [depName] [specific version]
```
Example :
```sh
    python Handler.py uninstall ompp 1.0.1
```

3. Update the entire dependenies after remote dependency adding( ex: git pull)<br/>
```sh
python Handler.py updateAll
```
### 2. OmpP profiler
[OmpP](http://www.ompp-tool.com/) profiler is a [OpenMp](http://www.openmp.org/) related profiling tool. [OmpP](https://github.com/PasinduSenanayake/Rigel-FYP/tree/ompppackage) repository contains API documentation.

## Questions

For *how-to* questions and other non-issues,
please use [StackOverflow](http://stackoverflow.com/questions/tagged/C-OpenMp-Opt) instead of Github issues.
There is a StackOverflow tag called "C-OpenMp-Opt" that you can use to tag your questions.

## Examples

Are you looking for an example project to get started? We don't currently have any. But we would love to host one or  more as soon as possible.

## Documentation

For the moment this is the only documentation we have.

## Contributing

We'd greatly appreciate any [contribution](/CONTRIBUTING.md) you make. :)

## Changelog

Recently Updated?
Please read the [changelog](https://github.com/PasinduSenanayake/Rigel-FYP/releases).

## Roadmap

The future plans and high priority features and enhancements can be found in the [ROADMAP.md]() file. ( Currently under development )

## Thanks

Thank you In order :)
## License

This project is licensed under the terms of the
[MIT license](/LICENSE).
