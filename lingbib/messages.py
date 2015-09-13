from util import *

UNSTAGED_CHANGES_ERROR = """\
You have unstaged changes in the current working directory.
They must be stashed or committed before you can add a new entry.
To stash changes, run 'git stash'.
When you are back on this branch, unstash them with 'git stash pop'.
If you want to commit the changes instead, you must stage
them with 'git add' and then commit them with 'git commit'."""

UNCOMITTED_STAGED_CHANGES_ERROR = """\
You have staged but uncommitted changes in your index.
You must commit them with 'git commit' before continuing."""