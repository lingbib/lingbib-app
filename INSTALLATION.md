The `lingbib` helper program currently works on Unix-like systems, including Ubuntu Linux and Mac OSX. You should also be able to get it to work under Cygwin on Windows (currently untested).

To use the `lingbib` program, you will need the following:
* Python 2.7 or 3.1+ (tested on 2.7, should work on 3.1-3.4, other versions not supported)
* BibTool >= 2.60

## Installing Python

Python 2.7 is installed by default on recent releases of Ubuntu and OSX. Run `python --version` to check your version.

On other systems, you may have to [download it from the official website][python-download]. Please use version 2.7 to avoid unforeseen problems.

Note: if there are multiple versions of Python available on your system, or if you installed Python manually, you may need to invoke it differently than usual when running `lingbib` (discussed below where relevant).

## Installing BibTool

The author of BibTool provides only the source code, but you can also install it using [Homebrew][homebrew] on OSX (tested) or [Linuxbrew][linuxbrew] on Ubuntu.
* Ubuntu: `brew update && brew install bib-tool`
* OSX:    `brew update && brew install bib-tool`

To install form source, see the [build instructions][build-bibtool].

Note: Ubuntu users should NOT install BibTool through their package manager. The version provided as of Ubuntu 15.04 is still older than 2.60, which contains a critical bug fix relevant to Lingbib.

## Installing the `lingbib` helper program

In the future, `lingbib-app` will be provided as an installable package. In the meantime, you can clone the Git repository to your local computer. There is no need to fork the repository unless you want to contribute code.
```sh
git clone https://github.com/lingbib/lingbib-app.git <target directory>
```

To test that the program works, navigate to the directory and invoke Python on the "lingbib" subdirectory:
```sh
python lingbib
```

If the program runs and does not show any errors other than "Current directory doesn't look like a lingbib repo.", then the dependencies have been installed currently.

If you need to use a version of Python other than the default, or if you installed Python manually, you may need to invoke the program differently. For example, on systems where `python` is a link to `python2.5`, you might need to call use `python2.7 lingbib`. If you installed Python in a non-standard location, you may need to invoke it using the full path: `/PATH/TO/PYTHON2.7 lingbib`.

## Creating a shortcut

Once you have confirmed that the program runs, you will want to make it easily callable. There are several ways to do this.

### Creating an alias

The easiest method is to add the command to your aliases file ("~/.bash_aliases" if you use bash). Call this command "lingbib" or something similar.
```sh
alias lingbib='python /PATH/TO/lingbib'
```

If you have to run the program using a non-default Python installation, replace "python" with "python2.7" or whichever version you have installed. If you have to use a copy of Python installed in a non-standard location, replace "python" with the full path.

Now, restart your terminal session or reload the alias file with `source ~/.bash_aliases`, and run the command from your local Lingbib repo to test it.

### Creating a shell script

Alternatively, you can place a short script to invoke the program in the repository itself. Again, you may need to replace "python" with a specific version or the full path.
```sh
#!/bin/sh
python /PATH/TO/LINGBIB-APP/lingbib $@
```

Next, make the script executable:
```sh
chmod u+x lingbib
```

To test the script, run the script from the Lingbib directory. Note the preceding "./".
```sh
./lingbib
```

You can also put the script in your `~/bin` folder (make sure it's in your PATH). In this case, you can invoke the program like a normal installed program or alias, without a preceding "./".
