# TerminalCricket
_Get live cricket scores on your terminal._

To get started with this program clone the repository.  
`git clone https://github.com/imrankhan17/TerminalCricket.git`

You can run the program by simply running `python results.py` (assuming you are in the same directory as the script).

If you want a single command that works wherever you are in your file system e.g. `cric`, you can add an alias to you bash profile.  To do this execute the following commands:  
* `cd ~`  
* `vim .bash_profile` (or use your preferred text editor)  
* Add the line: `alias cric="python /path/to/repo/TerminalCricket/results.py"` (use the path for where you saved the GitHub repo)  
* Save and exit and run `cric` to check it works.

__Example usage:__

`cric` Returns live scores of all international matches (Tests, ODI's and T20I's)  
`cric Test` Returns all Test match scores  
`cric ODI T20I` Returns all ODI and T20I scores  
`cric other` Returns all domestic match scores  
