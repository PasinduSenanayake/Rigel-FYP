

<h1 align="center">OmpP Python Package</h1>

<div align="center">

[Python](https://www.python.org/) wrapper for [OmpP](http://www.ompp-tool.com/) codes. ( This project is still under development )


</div>

## Pre-Requirements

1. [Python](https://www.python.org/) [ Version - 2.7.10 ~ 2.7.14 ]
2. [PIP](https://pypi.python.org/pypi/pip) [ Version 9.0.1 ]

## Installation

For the moment OmpP Python Package available as an open source git project and Pip package.


```sh
pip install ompp==1.0.0
```


## API Documentation

### 1. Basic OmpP Report

Basic OmpP report contains all the information related to [kinst-ompp](http://www.ompp-tool.com/downloads/ompp-manual.pdf)
 #### Usage
```sh
import ompp
response = ompp.getBasicProfile(absolute_file_path ,[run time arguments])
```
"absolute_file_path" - Path of the C file need to be analized.<br/>
"run time arguments" - Arguments required for compiled C file (optional)

 #### Response
```sh
response = {
        "error":"Any error occured in the process",
        "content":"Analized information in Json Array",
        "returncode":0/1
        }
```
"returncode" - 0 for unsuccessful process || 1 for successful process


## Questions

For *how-to* questions and other non-issues,
please use [StackOverflow](http://stackoverflow.com/questions/tagged/pyth-ompp) instead of Github issues.
There is a StackOverflow tag called "pyth-ompp" that you can use to tag your questions.

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
