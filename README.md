# Control Room BLM API CLI Utility using Python
Description:
-----------
This utility uses python libraries to interact with Control Room BLM APIs. 

Version:
-----------
1.0 - 06/11/2020

Usage:
-----------
* importexportcli.py -s <\util> -u <\username> -k <\apikey> -url <\url> -id <\botid> -pkg <\packages> -l <\location>
* importexportcli.py -s <\util> -u <\username> -k <\apikey> -url <\url> -l <\location>
* importexportcli.py -h|--help
* importexportcli.py -v|--version

Examples:
-----------
* python importexportcli.py -s 'Export' -u 'apiuser' -k '"" ;e7ew(FSZM$<FQ]w4(n~ajnkX5&A22Pp\+|1OP' -url 'http://linuxa2019/' -id '996' -pkg 'false' -l 'C:/exportedfolder/exportbot.zip'
* For testing purpose, following can be used: python importexportcli.py -u "[Your testing parameter]"

Switches:
-----------
* <\util> Mandatory argument (-s) for either to do import or export. Export works right now as of 1.0. Example: 'export'
* <\username>  Mandatory argument (-u) for Control Room username. 
* <\apikey>  Mandatory argument (-k) for apikey for the username. If you have a quotation mark, put an extra quotation mark right after it to escape it. 
* <\url>  Mandatory argument (-url) for Control Room URL. Example: 'http://CRurl.com/'
* <\botid>  Mandatory argument (-botid) for fileID of the check-in bot. 
* <\packages>  Mandatory argument (-pkg) to include packages with the export. Example: 'true' or 'false'
* <\location>  Mandatory argument (-l) for where to export the bot. Needs to include the full path of the zip file. Example: C:/ExportDirectory/test1.zip
* -h --help  Show this screen.
* -v --version  Show version.

Contstaints:
-----------
* Only export is supported right now. 
* You will need to know the bot file ID which you can get from the control room. 
* You will need to specify exactly where you are trying to export. All the backslashes in the path needs to be changed to forward slashes (e.g: C:\ExportFolder\exportedbot.zip needs to be C:/ExportFolder/exportedbot.zip). 
* You will need to escape any special characters in your apikey if you keep seeing the help message.
* There is no as such error handling on this script right now for 1.0. 

Future:
-----------
* Add some sort of error handling and feedback. 
* Add prompt to ask for details.
* Add requirements.txt file. 
