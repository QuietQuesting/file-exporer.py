# Python Comandline Fileexporer by QuietQuesting

![banner](https://user-images.githubusercontent.com/73032440/97810544-eba25300-1c74-11eb-87ed-7de2b34c0a55.png)

This is a simple comandline file exporer script for windows :desktop_computer::notebook_with_decorative_cover: written in Python 3.9

### Features:
- Traverse through you computers files as you wish with classical comandline interface and intuitve text control
- High level file operations such as: Copy, move, delete files and folders
- Function which prompts user to select x amount of files/dirs (which I will use for other projects) 
- Default start directory with config.ini and custom start directory as start parameter

	
### Warnings:
##### Using this as a replacement for the Windows explorer or cmd is not recommended.
High level functions such as copying and moving doesn't copy all the metadata: On POSIX platforms, this means that file owner and group are lost as well as ACLs. On Mac OS, the resource fork and other metadata are not used. This means that resources will be lost and file type and creator codes will not be correct. On Windows, file owners, ACLs and alternate data streams are not copied.

The delete function moves, if possible files to the paper bin. In case that is not possible (most likely on Freedesktop platforms Linux, BSD, etc.) the script asks your permission to delete files directly, you can give this permission for all files or just for individual files.

**I am not responsible for any damage caused, you can read the source code before using this script for a reason!** 

Thanks for reading.


ToDo:
- [ ] Write Copy and move function 
- [ ] Quick Access Points
- [ ] Fix inconsistency with '/' and '\\' in paths. Leads easily to errors. 
- [ ] Write Unittest
- [ ] Create Folders
- [ ] Error testing

<div>The Icons made from <a href="http://www.onlinewebfonts.com/icon">Icon Fonts</a> are licensed by CC BY 3.0</div>
The Icons along with the text are combined and colored by me!
[Used this python color scheme](https://www.schemecolor.com/python-logo-colors.php)
