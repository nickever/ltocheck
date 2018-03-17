# LTO Check

CLI tool to compare a master csv to an LTO csv. Compares file size, frame quantity and MD5 Hash.

## Getting Started

### Prerequisites

* Python 3.4+
* Works on Linux or Mac OSX

### Installing

LTO Check can be installed from the PyPi package with the pip command:

```
$ sudo pip install ltocheck
```

To check which version you are running, or that it has installed correctly use:

```
$ pip list 
```

### Usage

LTO Check has a command-line interface (CLI). The ltocheck command takes two required arguments; first, a master csv file listing all the files on the master source media, and secondly, an lto csv file listing all the files on the lto tape. 

```
$ ltocheck ~/path/to/master.csv ~/path/to/lto.csv
```
The tool will compare file name, size, frame count and MD5 hash for all files present on the master csv, compared to the lto csv and output a list and count of any missing files or mis-matched files. 

The tool has three more optional arguements to choose the output name (-o) and filepath (-d) of the output csv report as well as a verbose (-v) option for verbose output to terminal.

```
$ $ ltocheck ~/path/to/master.csv ~/path/to/lto.csv -d ~/path/to/reportout/ -o report.csv 
```


## Authors

* **Nick Everett** - *Initial work* - [NickEver](https://github.com/nickever)

See also the list of [contributors](https://github.com/nickever/ltocheck/contributors) who participated in this project.

## License

This project is licensed under the GNU v3.0 License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Thanks to Josh & Mike at Mission Digital
