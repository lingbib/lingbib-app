Bugfixes:
* Fix "setdefaults" to fetch before setting tracking
* Fix error printing in "setdefaults" and elsewhere to prepend "GIT:" line by line

Features:
* Add proper check for Bibtool at program start
* Add setup of personal repo with username prompt
* Add links to reference materials in program output
* Add a global config file
* Add setting to use personal repo or not
* Change config check to recognize whether the user is using a personal repo

Check if feasible:
* Add setup of unified style sheet from semprag repo (or decide to rely on manual installation)

Future:
* Finalize dependencies
* Check compatibility with different versions of Python and decide what to support
* Determine mechanism for installation and package accordingly
