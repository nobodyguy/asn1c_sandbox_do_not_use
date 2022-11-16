# Doxygen filter for ASN.1 syntax

The ASN.1 Doxygen filter is a python3 based parser for the ASN.1 syntax. It is
intended to be used with the documentation generation utility, [Doxygen][1].
This filter is distributed under the MIT license.

## Installation:
Add this repo as a submodule in the folder where your source files are present
or clone this repo to the folder where you have the source files.

## Usage:
**NOTE:** This repo **MUST** be in your source files folder.
Use the following commands to run Doxygen on your ASN.1 files commented using
the [Commenting Style Guide][2]:
```sh
cd <your_src_files_folder>/asn1-doxygen-filter/
doxygen <doxygen_config_file_name>
```

You may also use the GUI frontend tool for Doxygen called [doxywizard][3] to
run this filter using:
```sh
doxywizard <doxygen_config_file_name>
```

Go to the "Run" tab and hit "Run Doxygen". Once its operation is completed, you
may see the output by hitting the "Show HTML Output" button on the same tab.

## Debugging:
For debugging the filter itself, Use the following command to run the filter
script without Doxygen:
```sh
./asn1-doxygen-filter <filename>
```
NOTE: This will not generate the HTML documentation for you but will give you
an idea of how your file is parsed and fed to Doxygen.

## Dependencies
*   python3 (3.5.x)
*   doxygen (1.8.1x)

## References
Please refer the [Commenting Style][2] file to see how
to comment your ASN.1 files so that this filter works properly.

Also, refer the [sample doxygen configuration][4] file for a typical
Doxygen configuration to be used with this filter.

[1]: http://www.stack.nl/~dimitri/doxygen/index.html
[2]: https://bitbucket.org/raashid_ansari/asn1-doxygen-filter/src/master/commenting-style.md
[3]: https://www.stack.nl/~dimitri/doxygen/manual/doxywizard_usage.html
[4]: https://bitbucket.org/raashid_ansari/asn1-doxygen-filter/src/master/doxy.cfg
