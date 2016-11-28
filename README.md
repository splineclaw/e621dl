# What is **e621dl**?

**e621dl** is an automated script which downloads content from e621.net. It can be used to create a local mirror of your favorite searches, and keep these searches up to date as new files are uploaded.

# How does **e621dl** work?

Put very simply, when **e621dl** starts, it determines the following:

1. Which searches you would like to perform by reading `tag.txt`.
2. Which tags you would like to avoid seeing by reading `blacklist.txt`.
3. The last time it was run.

Once it knows these things, it goes through the searches one by one, and downloads _only_ content uploaded since the last time it was run.

# Installing **e621dl**

- _You must have Python 2, [which you can find here](https://www.python.org/downloads/)._
- [Download the latest release of **e621dl**.](https://github.com/wulfre/e621dl/releases/latest)
- Decompress the archive in any directory you would like.

# Running **e621dl**

- Open the terminal/command line in the directory you installed e621dl, and run `e621dl.py`

  - You may need to run the command as `python e621dl.py` if python is not in your path.
  - **Do not** double-click on `e621dl.py`. You **must** run it from the command line.

## First-Time Run

The first time you run **e621dl**, you should see something similar to the following:

```
e621dl      INFO     Running e621dl version 2.5.2b -- Forked from 2.4.6.
config      ERROR    New default file created: config.txt.
config      ERROR    Verify this file, then re-run the program.
config      INFO     Download directory created.
tags        ERROR    New default file created: tags.txt.
tags        ERROR    Add to this file, then re-run the program.
blacklist   ERROR    New default file created: blacklist.txt.
e621dl      ERROR    Error(s) encountered during initialization, see above.
```

These errors are normal behavior for a first run, and should not raise any alarm. **e621dl** is telling you that it was unable to find the _config_, _tags_, or _blacklist_ files, nor the _downloads_ folder, so it created them.

## Add searches to the tags file.

Add any tags or meta-tags for posts you would like to download to this file. Each line in this file will be treated as a separate group, and a new folder inside the downloads directory will be created for each group.

_If your group contains more than 5 tags, please check the [e621 tag list](https://e621.net/tag_alias/) and make sure to convert tag aliases. Due to the nature of e621's search function, only 5 tags can be converted automatically. All additional tags are manually checked by e621dl. In the future, an alias converter may be added so that you do not need to convert them manually. Another side effect of this workaround is that you may only use up to 5 meta-tags per group, and they must be the first 5 items on the line._

## [Optional] Add tags to the blacklist file.

Add any tags for posts you would like to avoid downloading to this file. Meta-tags will currently break the script, as they are not filtered out, so do not use them in this file.

_This script, currently, can only blacklist official tags. In the future, an alias converter may be added so that you do not need to convert them manually. Until then, be sure to check your tags against the [e621 tag list](https://e621.net/tag_alias/) to avoid seeing any content you do not want to._

Give each tag its own new line.

## [Optional] Modify the config file.

Most users will not need to modify the config file, `config.txt`, but feel free to edit it to your liking after reading the description, and acceptable values for each key. Please respect which values need quotation marks, as the script will fail to run if any are missing.

The quotation marks indicate a _string value_, which python can only interpret _with_ quotation marks, as opposed to a _boolean_ or _integer_ value, which python can only interpret _without_ quotation marks.

### Config Keys, Values, and Descriptions

#### Common Values

Key                   | Quotation marks needed? | Acceptable Values | Description
--------------------- | ----------------------- | ----------------- | ----------------------------------------------------------------------------------
download_directory    | Yes                     | Valid system path | The path where **e621dl** puts downloaded files. It must must end with `/`.
create_subdirectories | No                      | `true` or `false` | Create a directory for each group in the tag file.
file_name             | Yes                     | `md5` or `id`     | The name given to each downloaded file. Can either be the md5 sum or the post id.
last_run              | Yes                     | Date `YYYY-MM-DD` | The last day **e621dl** was run. You may edit this freely to download older posts.

#### Advanced Values

_(Most users will not need to change the advanced settings.)_

Key                | Quotation marks needed? | Acceptable Values    | Description
------------------ | ----------------------- | -------------------- | --------------------------------------------------------------------------
parallel_downloads | No                      | Integer 1 to 16      | The maximum number of simultaneous downloads allowed to be performed.
cache_name         | Yes                     | Valid system path    | The path of the file that **e621dl** will use to track previous downloads.
cache_size         | No                      | Any positive integer | The maximum number of items **e621dl** will keep in the cache.

# Normal Operation

Once you have added at least one group to the tags file, you should see something similar to this when you run **e621dl**:

```
e621dl      INFO     Running e621dl version 2.5.2b -- Forked from 2.4.6.
e621dl      INFO     e621dl was last run on 2016-11-27.

e621dl      INFO     Checking for new posts tagged: cat.
e621dl      INFO     4 new (8 found, 1 missing tags, 1 blacklisted, 2 downloaded, 0 cached)

e621dl      INFO     Starting download of 4 files.

Downloading:        [###################################] 100.00% Done...


e621dl      INFO     Successfully downloaded 4 files.
e621dl      INFO     Last run updated to 2016-11-26.
```

There is quite a bit of information here. Since last time **e621dl** was run on 2014-06-27, there have been 8 uploads that match the search "cat". One post did not contain every tag which we specified. This is because e621 will only accept 5 initial tags and any additional tags are checked by e621dl. 1 post has a tag that was in our blacklist, so it will be skipped. 2 posts have already been downloaded in a previous run, so they will also be skipped. The 4 remaining posts will be downloaded and added the downloads folder. Once they have been downloaded, **e621dl** updates its last run date to the day before it was run, 2014-11-26, and is ready for its next use.

## Automation of **e621dl**

It should be recognized that **e621dl**, as a script, can be scheduled to run nightly, keeping the user's local collections always up-to-date, however, the methods for doing this are dependent on the user's platform, and are outside the scope of this guide.

# Feedback and Feature Requests

If you have any ideas on how to make this script run better, or for features you would like to see in the future, open a detailed issue and I will try to read it as soon as possible.

# Donations

Since this script was initially written by @wwyaiykycnf I will leave their donation section as it was before I forked the repository.

If you've benefitted from this _free_ project, why not [buy me something on Amazon?](http://amzn.com/w/20RZIUHXLO6R4) There's tons of cheap bullshit on there I would totally get a kick out of owning.

Alternatively, drop me an email at wwyaiykycnf+features@gmail.com and say thanks. Your support (monetary or not) provides me the motivation to keep fixing bugs and adding new features, so thanks for thinking of me!
