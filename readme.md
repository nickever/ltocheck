# LTO Check

Command line interface and GUI tool to compare a master csv to an LTO csv.
Compares the file size, frame count and MD5 Hash for every video file listed in the master csv.

## Getting Started



### Prerequisites

Requires Python 3.6+

To install python 3.6, use Homebrew.

Install Homebrew:
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Install Python 3.6+:
```
$ brew install python
```

### Installing

There are two methods to install this package. The simple method is to run the 'package_installer.sh' 
file included in the package, which will check for and then if needed install Homebrew, Python3 and the ltocheck
package. To execute the package installer use:

```
$ /PATH/TO/package_installer.sh
```

Alternatively, install the prerequisites listed above and then install ltocheck as a local python3 pip package:

```
$ pip3 install -e /PATH/TO/ltocheck/
```

## Usage

This tool can be used with either the GUI or CLI as preferred.  

### GUI

To access the GUI, run $ ltocheck without args from terminal.



### CLI

To access the CLI, run $ ltocheck with two required positional args, plus any optional args:

```
$ ltocheck -m [master_csv_path] -l [lto_csv_path] 
```

```
usage: ltocheck [-h] [-m MASTER_CSV_PATH] [-l LTO_CSV_PATH] [-d OUT_PATH]
                [-o OUT_NAME] [-v] [--version]

Command line interface tool to compare a master csv with an LTO csv
https://github.com/nickever/lto_check

optional arguments:
  -h, --help            show this help message and exit
  -m MASTER_CSV_PATH, --master_csv_path MASTER_CSV_PATH
                        master csv input file path (required)
  -l LTO_CSV_PATH, --lto_csv_path LTO_CSV_PATH
                        LTO csv input file path (required)
  -d OUT_PATH, --out_path OUT_PATH
                        output destination path
  -o OUT_NAME, --out_name OUT_NAME
                        output filename
  -v, --verbose         verbosity (-v) or debug mode (-vv)
  --version             show program's version number and exit
```

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details
