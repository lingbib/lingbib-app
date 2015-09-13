# lingbib-app
Helper program for Lingbib users.

This program is under development. Documentation will be added as it reaches completion.

## Installation

In the future, `lingbib-app` will be provided as an installable package. In the meantime, you can clone the git repository to your local computer and add a command to your alias file. The following instructions work for Python 2.7 and higher.

First, navigate to the location where you want to create the installation directory and run the following command:

```sh
git clone https://github.com/lingbib/lingbib-app
```

To test that the program works, enter the directory and invoke the "lingbib" subdirectory as a Python package using `python lingbib`.

Next, add the command to your aliases file ("~/.bash_aliases" if you use `bash`). Call this command "lingbib", "lb" or something similar. 

```sh
alias lingbib='python /PATH/TO/lingbib'
```

If you use a different shell, you may need to create the alias differently. Alternatively, you can make an shell script in your `~/bin` folder (Linux/OSX) containing the command `python /PATH/TO/lingbib $@`. In this case, make sure you include a shebang line (#!/bin/sh) and make the script executable (chmod u+x ~bin/SCRIPT). On Windows, you can create a batch file somewhere in your PATH (Windows). 

Restart your terminal, and you should be able run the program using the alias or script you created.


## Usage

This program should only be used from a local [lingbib][lingbib] repository. Run it without arguments to see the usage message.


[lingbib]: https://github.com/lingbib/lingbib
