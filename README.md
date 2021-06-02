# Getcomic-downloader
This is for downloading comics from getscomics website [link](https://getcomics.info/)

### Needed Packages
* BeautifulSoup

### How to Use it
* First make a directory here names "downloads"
* Run the script with python3 and the required arguments
```
python3 getcomic-downloader.py -o <pages> <search>
```
all the files will be downloaded to the downloads folder

### What can de done after this
* Probably solve some of the bugs in it
* Use threading to speedup the download (Though im not sure the server can handle all the bandwidth so we need to be careful)
* It can be made as a module to be used with other programs

### Bugs
* Sometimes the "zip" file can be downloaded as "cbr". It can be solved easily by renameing it as ".zip". but still will be good to just download it as a "zip" file
