# Ubuntu Package Log Analyzer
This a python2 script that generates a *.csv report conatining information about manually-installed or removed packages by analyzing apt-get logs at (/Var/log/apt). Information consists of package name, status, package management app used, date / time and the name of the history file containing that particular info.
* Tested  on Ubuntu 16.04 Xenial.
# Notes:
* Currently, the script only process apt-get and synaptic logs, it does not process aptitude logs (yet).
* The report will be created in the first folder under (/home/).
