## What is **e621dl**?
**e621dl** is an automated script which downloads content from e621.net. It can be used to create a local mirror of your favorite searches, and keep these searches up to date as new files are uploaded.

## How does **e621dl** work?
Put very simply, when **e621dl** starts, it determines:

1. Which searches you would like to perform by reading `tag.txt`.
2. Which tags you would like to avoid seeing by reading `blacklist.txt`).
3. The last time it was run by reading `config.txt`.

Once it knows these things, it goes through the searches one by one, and downloads *only* content uploaded since the last time it was run.

## Installing **e621dl**
- *You must install Python 2 [which you can find here](https://www.python.org/downloads/).*
- [Download the latest release of **e621dl**](https://github.com/wulfre/e621dl/releases/latest)
- Decompress the archive in any directory you would like.

## Running **e621dl**
- Open the terminal/command line in the directory you installed e621dl, and run `e621dl.py`
  - You may need to type `python e621dl.py` if python is not in your path.  
  - **Do not** double-click on `e621dl.py`.  You __must__ run it from the command line.

### First-Time Run
The first time you run **e621dl**, you should see something like:
```
e621dl      INFO     running e621dl version 2.5.2 -- Forked from 2.4.6
configfile  ERROR    new default file created: config.txt
configfile  ERROR       verify this file and re-run the program
config_file INFO     empty download directory created
tagfile     ERROR    new default file created: tags.txt
tagfile     ERROR       add to this file and re-run the program
blacklistfile ERROR    new default file created: blacklist.txt
blacklistfile ERROR     add to this file and re-run the program
e621dl      ERROR    error(s) encountered during initialization, see above
```
It's not as bad as it looks.  **e621dl** is telling you that it couldn't the *config*, *tags*, or *blacklist* files, so it created them.  This is totally normal behavior.

### Add searches to the tags file.
You must add at least one search you would like to perform to the tags file. Open it to find the most up-to-date instructions on how to configure it.

### [Optional] Add tags to the blacklist file.
If there are any tags you would like to avoid, you must add them to the blacklist file. Open it to find the most up-to-date instructions on how to configure it.

### [Optional] Modify the config file.
Most users will not need to modify the config file, `config.txt`, but feel free to edit it to your liking after reading the description, and values for each key. Please respect which values need quotation marks, as the script will fail to run if any are missing. The quotation marks indicate a *string value* as opposed to a *boolean* or *integer* value, which python can interpret only without quotation marks.

#### Config Keys, Values, and Descriptions

##### Common Values

| Key           | Quotation marks needed? | Acceptable Values            | Description                                                         |
| --------------------- | ------- | --------------------------- |-------------------------------------------------------------------- |
| download_directory    | Yes     | Valid system path                    | The path where **e621dl** puts downloaded files. It must must end with `/`.            |
| create_subdirectories | No      | `true` or `false`           | Create a directory for each group in the tag file.                |
| file_name     | Yes     | `md5` or `id`               | The name given to each downloaded file. Can either be the md5 sum or the post id. |
| last_run              | Yes     | Date `YYYY-MM-DD` | The last day **e621dl** was run. You may edit this freely to download older posts.                                |


##### Advanced Values
*(Most users will not need to change the advanced settings.)*

| Key           | Quotation marks needed? | Acceptable Values            | Description                                                  |
| --------------------- | ------- | --------------------------- |------------------------------------------------------------- |
| parallel_downloads    | No      | Integer 1 to 16                     | The maximum number of simultaneous downloads allowed to be performed.      |
| cache_name            | Yes     | Valid system path                    | The path of the file that **e621dl** will use to track previous downloads. |
| cache_size            | No      | Any positive integer        | The maximum number of items **e621dl**  will keep in the cache.                        |

## Normal Operation
Once you have added to the tags file, you should see something like this when you run **e621dl**:
```
e621dl      INFO     Running e621dl version 2.5.2b -- Forked from 2.4.6
e621dl      INFO     e621dl was last run on 2016-11-26
e621dl      INFO     Checking for new uploads tagged: cat
e621dl      INFO     3 new (7 found, 0 missing tags, 0 blacklisted, 4 downloaded, 0 cached)

e621dl      INFO     starting download of 3 files

Downloading:        [###################################] 100.00% Done...

e621dl      INFO     successfully downloaded 3 files
e621dl      INFO     last run updated to 2016-11-27
```
There's actually quite a bit of information here.  Since last time **e621dl** was run (2014-06-26) there have been 7 uploads that match the search "cat".  4 of these have been downloaded previously, so they will be skipped.  But 3 are new, and they are downloaded.  Once they have been downloaded, **e621dl** updates its last run date to the current date (2014-06-27).  

### Automation of **e621dl**
Savvy users should realize at this point that they could simply schedule **e621dl** to run nightly in the wee hours of the morning, and their local collection will always be up-to-date...  However, how you do this is completely dependent on your platform and outside the scope of this guide.

## Feedback and Feature Requests
If you have any ideas for how things might work better, or about features you'd like to see in the future, open an issue and I will try to read it as soon as possible.

## Donations
Since this script was initially written by @wwyaiykycnf I will leave their donation section exactly the way they left it before I forked the repository.

If you've benefitted from this *free* project, why not [buy me something on Amazon?](http://amzn.com/w/20RZIUHXLO6R4) There's tons of cheap bullshit on there I would totally get a kick out of owning.   

Alternatively, drop me an email at wwyaiykycnf+features@gmail.com and say thanks. Your support (monetary or not) provides me the motivation to keep fixing bugs and adding new features, so thanks for thinking of me!
