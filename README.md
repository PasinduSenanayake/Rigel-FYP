

<h1 align="center">C Pragma Modifier</h1>

<div align="center">

[Python](https://www.python.org/) library for OpenMP pragma modification in C source codes. ( This project is still under development )


</div>

## Pre-Requirements

1. [Python](https://www.python.org/) [ Version - 2.7.10 ~ 2.7.14 ]
2. [PIP](https://pypi.python.org/pypi/pip) [ Version - 9.0.1 ]


## Installation

For the moment cPragmaModifier Python Package available as an open source git project and Pip package.


```sh
pip install cPragmaModifier==1.0.1
```


## API Documentation

### 1. Set scheduling mechansims

Use to add or modify scheduling mechanisms for a considered pragma in a source code. This API doesn't consider syntactic or semantic correctness of the modified code. Developer has to make sure the modification won't break the code.
 #### Usage
```sh
import cPragmaModifier
response = cPragmaModifier.setPragmaSchedule(absolute file path,absolute altered file path,scheduling mechanism, [codeline])
```
Parameters :<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"absolute file path" : Path of the .c file need to be analized [ Required ]<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"absolute altered file path" : Path to the updated .c file need to be saved [ Required ]<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"scheduling mechanism" : Scheduling mechanism that is need to be added [ Required ]<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"codeline" : To which line the given scheduling mechanism need to be added. If this is not specified given scheduling mechanism will be added to all the possible places in source code ( optional )


 #### Response
```sh
response = {
        "error":"Any error occured in the process",
        "content":"",
        "returncode":0/1
        }
```
Responses :<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"returncode" : 0 for unsuccessful process || 1 for successful process

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
