Backs up target directory extremely fast.

Mode 1 (Default): Copy Missing - Only copies file names not found in backup directory.
Mode 1 button has white and green arrows to show it is in Mode 1.

Mode 2: Comprehensive - Is Mode One plus compares file timestamps and copy is source timestamp is newer than backup timestamp.
Mode 2 button has white arrows to show it is in Mode 2.
Mode 2 comapres file modification timestamps and copies source file to destination if your destination timestamp < source timestamp.

Mode one is useful if you dont edit the files. (like a music library, picture directory etc...)
Mode two is useful if you edit files. (documents, or you edit your music and pictures too you can still use it...)

Configure in config.txt before use!

Initial backup will of course take time but after that it can be insanely fast.

I wrote this because I have a lot of files and when i back up id like it to be faster and
so instead of procrastinating i saved my future self time.

This will not delete 'depricated' files and folders from your chosen backup destination.

I use it to backup from my secondary internal drive to my external backup ssd, its been backing itself up at lightening speed as i write the code!
WARNING! Still in development! Please be careful and check paths and make sure everything is right before writing/backing up.

Best Case Example:
Secondary Internal Drive Tree:
  Archives
  Documents
  Music
  Pictures
  Programs (Steam+Steam Library, other things i keep portably away from drive C:\\)
  Video
Backup drive reflects Secondary Internal Drive Tree.

Backing up steam (for me 700GB+) with this should be much faster than pasting a new copy as this will only copy
what has changed and or what is missing. I will wait to test and compare. I Can't test yet but will soon.
  