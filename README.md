# What is **e621dl**?

**e621dl** is an automated script, originally by [**@wwyaiykycnf**](https://github.com/wwyaiykycnf), which downloads images from e621.net. It can be used to create a local mirror of your favorite searches, and keep these searches up to date as new files are uploaded.

# How does **e621dl** work?

Put very simply, when **e621dl** starts, it determines the following based on the `config.ini` file:

- Which tags you would like to avoid seeing by reading the blacklist section.
- Which searches you would like to perform by reading your tag group sections.
- How far back to look for posts by reading your settings section.

Once it knows these things, it goes through the searches one by one, and downloads _only_ content that matches your search request, and has passed through all specified filters.

# Installing and Setting Up **e621dl**

- Download and install [the latest release of Python 3](https://www.python.org/downloads/).
- Download [the latest release of **e621dl**](https://github.com/wulfre/e621dl/releases).
  - Decompress the archive into any directory you would like.
- Download and install the required packages from the Python Package Index by opening your terminal/command line in the directory you decompressed e621dl into and running the command `pip install -r requirements.txt`.

# Running **e621dl**

- Open your terminal/command line in the directory you decompressed e621dl into, and run the command `python e621dl.py`.

## First-Time Run

The first time you run **e621dl**, you should see something similar to the following:

```
e621dl      INFO     Running e621dl version X.X.X -- Forked from 2.4.6.
config      ERROR    No config file found.
config      INFO     New default file created: "config.ini".
tags        ERROR    Please add at least one tag group to "config.ini".
e621dl      INFO     Error(s) occurred during initialization, see above for more information.
```

These errors are normal behavior for a first run, and should not raise any alarm. **e621dl** is telling you that it was unable to find the _config_, _tags_, or _blacklist_ files, nor the _downloads_ folder, so it created them.

## Add search groups to the config file.

Create sections in the `config.ini` to specify which posts you would like to download. In the default config file, an example is provided for you. Each section will have its own directory inside the downloads folder.

The following characters are not allowed in section names: `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`, and ` ` as they can cause issues in windows file directories. If any of these characters are used, they will be replaced with the `_` character. The `/` character _is_ allowed to be used in section names, but it will be understood as a sub-directory. This may be useful to some users for organization. For example: separating `[Canine/Fox]` and `[Canine/Wolf]`, and separating `[Feline/Tiger]` and `[Feline/Lion]`

Commas should be used to separate tags and ratings.

One side effect of the workaround used to search an unlimited number tags is that you may only use up to 5 meta tags `:`, negative tags `-`, operational tags `~`, or wildcard tags `*` per group, and they must be the first 5 items in the group. See [the e621 cheatsheet](https://e621.net/help/show/cheatsheet) for more information on these special types of tags.

## [Optional] Add blacklisted tags to the config file.

Add any tags for posts you would like to avoid downloading to the blacklist section of the `config.ini` file. Meta tags `:`, negative tags `-`, operational tags `~`, and wildcard tags `*` will potentially break the script, as they are currently not filtered out of the blacklist, so do not use them in this section.

Commas should be used to separate tags.

_Please check your blacklist tags against the [e621 tag list](https://e621.net/tag_alias/) for content you absolutely do not want to see. At this time, I do not have a reliable automatic check._

## [Optional] Modify the settings in the config file.

The settings section of the `config.ini` is designed to be easily modified and difficult to break by any user, as much of the information needed by **e621dl** is dynamically taken from the computer it is being run on. Feel free to edit it to your liking after reading the description, and acceptable values for each key.

### Config Keys, Values, and Descriptions

Key                   | Acceptable Values | Description
--------------------- |  -----------------| ----------------------------------------------------------------------------------
days_to_check         |Integer            | How many days from the past to check for new posts. You may edit this freely to download posts from as early as you would like.

## Normal Operation

Once you have added at least one group to the tags file, you should see something similar to this when you run **e621dl**:

```
e621dl      INFO     Running e621dl version X.X.X -- Forked from 2.4.6.
e621dl      INFO     Parsing config.

e621dl      INFO     Looking for new posts since YYYY-MM-DD.

e621dl      INFO     Group "Canine/Fox" detected, checking for new posts tagged: "fox, feral".
e621dl      INFO     19 new files.
                     37 total files found.
                     10 have an unwanted rating.
                     3 have a low score.
                     0 are missing tags.
                     1 are blacklisted.
                     4 have been previously downloaded.

e621dl      INFO     Starting download of 19 files.
Downloading          |████████████████████████████████████| 100% (19 / 19)
```

# Automation of **e621dl**

It should be recognized that **e621dl**, as a script, can be scheduled to run as often as you like, keeping the your local collections always up-to-date, however, the methods for doing this are dependent on your platform, and are outside the scope of this quick-guide.

# Feedback and Requests

If you have any ideas on how to make this script run better, or for features you would like to see in the future, [open an issue](https://github.com/Wulfre/e621dl/issues) and I will try to read it as soon as possible.

# Donations

_Since this script was initially written by [**@wwyaiykycnf**](https://github.com/wwyaiykycnf) I will leave their donation section as it was before I forked the repository._

If you've benefitted from this _free_ project, why not [buy me something on Amazon?](http://amzn.com/w/20RZIUHXLO6R4) There's tons of cheap bullshit on there I would totally get a kick out of owning.

Alternatively, drop me an email at wwyaiykycnf+features@gmail.com and say thanks. Your support (monetary or not) provides me the motivation to keep fixing bugs and adding new features, so thanks for thinking of me!
