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
* if you have downloaded files till page 4. you can use the slice property to get other part of the comic eg
```
python3 getcomic-downloader.py -o 5-10 "spider-man"
```

### What can de done after this
* Probably solve some of the bugs in it
* It can be made as a module to be used with other programs

### Bugs
* Sometimes the "zip" file can be downloaded as "cbr". It can be solved easily by renameing it as ".zip". but still will be good to just download it as a "zip" file
