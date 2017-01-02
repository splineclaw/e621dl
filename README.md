# What is **e621dl**?

**e621dl** is an automated script, originally by [**@wwyaiykycnf**](https://github.com/wwyaiykycnf), which downloads content from e621.net. It can be used to create a local mirror of your favorite searches, and keep these searches up to date as new files are uploaded.

# How does **e621dl** work?

Put very simply, when **e621dl** starts, it determines the following:

- Which searches you would like to perform by reading `tag.txt`.
- Which tags you would like to avoid seeing by reading `blacklist.txt`.
- The last time it was run by reading `config.txt`.

Once it knows these things, it goes through the searches one by one, and downloads _only_ content uploaded since the last time it was run.

# Installing **e621dl**

- Download and install [the latest release of Python 2](https://www.python.org/downloads/).
- Download [the latest release of **e621dl**](https://github.com/wulfre/e621dl/releases/latest).

  - Decompress the archive in any directory you would like.

# Running **e621dl**

- Open the terminal/command line in the directory you installed e621dl, and run `e621dl.py`

  - You may need to run the command as `python e621dl.py` if python is not in your path.

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

## Add searches to the config file.

Add any tags or meta-tags for posts you would like to download their own sections in the `config.ini` file an example is provided for you. Each search will have its own directory inside the downloads folder.

Commas should be used to separate tags.

_If your group contains more than 5 tags, **e621dl** will try to automatically convert all additional tags to their proper alias and filter posts found from the first 5 tags. Until this feature is more thoroughly developed, you may need to consult the [e621 tag list](https://e621.net/tag_alias/) and manually convert aliases that do not get converted automatically. Otherwise, it would be greatly appreciated that you test the automatic tag conversion and report any issues._

One side effect of the workaround used to search an unlimited number tags is that you may only use up to 5 meta tags `:`, negative tags `-`, operational tags `~`, or wildcard tags `*` per group, and they must be the first 5 items in the group. See [the e621 cheatsheet](https://e621.net/help/show/cheatsheet) for more information on these special types of tags.

## [Optional] Add blacklisted tags to the config file.

Add any tags for posts you would like to avoid downloading to the blacklist section of the `config.ini` file. Meta tags `:`, negative tags `:`, operational tags `~`, and wildcard tags `*` will currently break the script, as they are not filtered out of the blacklist, so do not use them in this section.

Commas should be used to separate tags.

_**e621dl** will try to automatically convert all tags to their proper aliases. Until this feature is more thoroughly developed, you may want to check your tags against the [e621 tag list](https://e621.net/tag_alias/) and manually convert any tags for content you absolutely do not want to see. Otherwise, it would be greatly appreciated that you test the automatic tag conversion and report any issues._

## [Optional] Modify the settings in the config file.

Most users will not need to modify the settings section of the `config.ini` file, but feel free to edit it to your liking after reading the description, and acceptable values for each key.

### Config Keys, Values, and Descriptions

#### Common Values

Key                   | Acceptable Values | Description
--------------------- |  -----------------| ----------------------------------------------------------------------------------
last_run              |Date `YYYY-MM-DD` | The last day **e621dl** was run. You may edit this freely to download older posts.
parallel_downloads | Integer 1 to 16      | The maximum number of simultaneous downloads allowed to be performed.

## Normal Operation

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

# Automation of **e621dl**

It should be recognized that **e621dl**, as a script, can be scheduled to run nightly, keeping the user's local collections always up-to-date, however, the methods for doing this are dependent on the user's platform, and are outside the scope of this guide.

# Feedback and Requests

If you have any ideas on how to make this script run better, or for features you would like to see in the future, [open an issue](https://github.com/Wulfre/e621dl/issues) and I will try to read it as soon as possible.

# Donations

Since this script was initially written by [**@wwyaiykycnf**](https://github.com/wwyaiykycnf) I will leave their donation section as it was before I forked the repository.

If you've benefitted from this _free_ project, why not [buy me something on Amazon?](http://amzn.com/w/20RZIUHXLO6R4) There's tons of cheap bullshit on there I would totally get a kick out of owning.

Alternatively, drop me an email at wwyaiykycnf+features@gmail.com and say thanks. Your support (monetary or not) provides me the motivation to keep fixing bugs and adding new features, so thanks for thinking of me! ng of me! ng of me! ng of me! ng of me!
