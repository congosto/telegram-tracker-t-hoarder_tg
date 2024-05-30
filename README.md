::: {align="center"}
# **telegram-tracker-t-hoarder_tg**: `a Python-based open-source tool for Telegram`(fork de Telegram-tracker)

------------------------------------------------------------------------

[![GitHub forks](https://img.shields.io/github/forks/estebanpdl/telegram-tracker.svg?style=social&label=Fork&maxAge=2592000)](https://GitHub.com/estebanpdl/telegram-tracker/network/) [![GitHub stars](https://img.shields.io/github/stars/estebanpdl/telegram-tracker?style=social)](https://github.com/estebanpdl/telegram-tracker/stargazers) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/estebanpdl/telegram-tracker/blob/main/LICENCE) [![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://twitter.com/estebanpdl) [![Made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Twitter estebanpdl](https://badgen.net/badge/icon/twitter?icon=twitter&label)](https://twitter.com/estebanpdl)

------------------------------------------------------------------------
:::

## Overview

### About this version of Telegram-tracker

**telegram-tracker** is an excellent implementation for extracting information from Telegram channels. However, it does not retain context of what has been downloaded, which makes it challenging to automatically update channels with the latest messages. The lack of context can lead to message repetitions if a channel is downloaded more than once.

This version of telegram-tracker aims to download messages from Telegram channels and keep them updated with new messages, **avoiding duplicates**. To achieve this, it **maintains context** for each download by recording the date and time, the most recent message, and the total number of downloaded messages. It also stores context for all downloaded channels and their related channels.

The safest procedure for downloading channels is to do it one by one:

1.  Download the channel using the main.py command.

2.  Convert the JSON messages from the channel to CSV using the build-dataset.py command.

Usually, a download can take many hours or even days. If the scripts are interrupted, following this procedure ensures a safer restart, preventing the storage of repeated messages."

### Changes introduced in this Telegram-tracker fork

-   **Corrections/changes**:
    -   Fix a warning about using a deprecated parameter
    -   Fixed some download errors with exceptions
    -   Added a **download progress bar**. Some channels can have millions of messages and it was not known how much was left to download. This progress bar takes as the number of messages the number of the last published message (the message ids are consecutive numbers starting from 1). The channel may have deleted messages, the download percentage will rarely reach 100%, but it gives an idea of ​​the percentage of deleted messages
    -   The script **build-datasets.py**, which converted all JSON files to CSV, has been replaced by **build-dataset.py**, which only converts the JSON from a single channel to CSV. Added exception handling in the script
    -   The **--min-id parameter** has been removed as it is no longer necessary, given that updates with new messages are now automatic.
    -   The **--batch-file** parameter has been removed to ensure that channels are downloaded one by one using **main.py**, and then the JSON files are converted to CSV using the **build-datasets.py** command. When you want to download a list of channels, you can do so using:
        -   A shell script **menu.py**
        -   The **telegram-tracker.ipynb** notebook included in this repository, prepared to be used in **Google's Colab environment**
-   **Added context**:
    -   The file **related_channels.csv** with the names of the related channels has been added to the download directory
    -   The **log_download.csv** file has been added to the JSON directory of each channel. For each download, the date of the download, the most recent message number, and the number of downloaded messages are stored in this file. This allows channels to be updated with the latest messages automatically without using the **--min-id** parameter, which has been removed.
    -   For **snowball downloading**, context is saved in a file **{channel}\_n2_log.csv** with the operations carried out by the channels in order to resume the download at the point it left off after an interruption
    -   To **download a group** of channels, context is saved in a file **{group}\_log.csv** with the operations carried out by the channels in order to resume the download at the point it left off after an interruption
    -   In the root directory of the data, two files have been added:
        -   **collected_channels_all.csv**: contains all the downloaded channels.
        -   **related_channel_all.csv**: includes all channels related to the downloaded channels. These channels may appear in multiple datasets, which is why we also store the number of times they appear in other downloads and the directories where they can be found.

### Colab environemt

This fork includes a notebook to run these scripts in the colab environment.

Requirements:

-   Have a Google account
-   Have a Telegram account
-   Create an App in Telegram <https://my.telegram.org/auth?to=apps> and follow the steps to obtain the Id and API KEY
-   Fill the telegram-tracker configuration file (config/config.ini) with the App data
-   Upload the repository to drive
-   Open **telegram-tracker.ipynb** in the colab environment (clicking on the notebook will open it in the environment)

The **telegram-tracker.ipynb** notebook will mount drive so that the scripts can be executed from there

### Local enviroment

This tool connects to Telegram's API. It generates JSON files containing channel's data, including channel's information and posts. You can search for a specific channel, or a set of channels provided in a text file (one channel per line.)

You can access it in command mode, but with the **menu.py** script you can download in a controlled way

-   A channel

-   Snowball from a channel

-   A group of channels

**Software required**

-   [Python 3.x](https://www.python.org/)
-   [Telegram API credentials](https://my.telegram.org/auth?to=apps)
    -   Telegram account
    -   App `api_id`
    -   App `api_hash`

**Python required libraries**

-   [Telethon](https://docs.telethon.dev/en/stable/)
-   [Pandas](https://pandas.pydata.org/)
-   [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)
-   [tqdm](https://tqdm.github.io/)
-   [Networkx](https://networkx.org/)
-   [Matplotlib](https://matplotlib.org/)
-   [Louvain Community Detection](https://github.com/taynaud/python-louvain)

## Installing

-   **Via git clone**

```         
https://github.com/congosto/telegram-tracker-t-hoarder_tg.git
```

This will create a directory called `telegram-tracker` which contains the Python scripts. Cloning allows you to easily upgrade and switch between available releases.

-   **From the github download button**

Download the ZIP file from github and use your favorite zip utility to unpack the file `telegram-tracker-t-hoarder_tg.zip` on your preferred location.

**After cloning or downloding the repository, install the libraries from `requirements.txt`.**

```         
pip install -r requirements.txt
```

or

```         
pip3 install -r requirements.txt
```

**Once you obtain an API ID and API hash on my.telegram.org, populate the `config/config.ini` file with the described values.**

``` ini

[Telegram API credentials]
api_id = api_id
api_hash = api_hash
phone = phone
```

*Note: Your phone must be included to authenticate for the first time. Use the format +\<code\>\<number\> (e.g., +19876543210). Telegram API will send you a code via Telegram app that you will need to include.*

<br />

------------------------------------------------------------------------

# Example usage by commands

## `main.py`

This Python script will connect to Telegram's API and handle your API request.

### Options

-   `--telegram-channel` Specifies Telegram Channel to download data from.
-   `--limit-download-to-channel-metadata` Will collect channels metadata only, not channel's messages. (default = False)
-   `--output, -o` Specifies a folder to save collected data. If not given, script will generate a default folder called `./output/data`

<br />

### Structure of output data

```         
├──🗂 output
|   └──🗂 data
|       └──🗂 <channel_name>
|           └──<channel_name>.json
|           └──<channel_name>_messages.json
|       └──chats.txt // TM channels, groups, or users' IDs found in data.
|       └──collected_chats.csv // TM channels or groups found in data (e.g., forwards)
|       └──collected_chats.xlsx // TM channels or groups found in data (e.g., forwards)
|       └──counter.csv // TM channels, groups or users found in data (e.g., forwards)
|       └──user_exceptions.txt // From collected_chats, these are mostly TM users' which 
|                                   metadata was not possible to retrieve via the API
|       └──msgs_dataset.csv // Posts and messages from the requested channels
```

<br />

## **Examples**

<br />

### **Basic request**

```         
python main.py --telegram-channel channelname`
```

**Expected output**

-   Files of collected channels:
    -   chats.txt
    -   collected_chats.csv
    -   user_exceptions.txt
    -   counter.csv
    -   collected_chanels
-   A new folder: <channel_name> containing
    -   A JSON file containing channel's profile metadata
    -   A JSON file containing posts from the requested channel
    -   log_downloads.csv

<br />

### **Request using a text file containing a set of channels**

Download the channels one by one with the same output directory

```         
for chanel in channels:
   python main.py  --telegram-channel channel --output './path/to/channels'
   build-datasets.py --telegram-channel channel --data-path './path/to/channels'
```

**Expected output**

-   Files of collected channels:
    -   chats.txt
    -   collected_chats.csv
    -   user_exceptions.txt
    -   counter.csv
    -   collected_chanels
-   New folders - based on the number of requested channels: <channel_name> containing
    -   A JSON file containing channel's profile metadata
    -   A JSON file containing posts from the requested channel
    -   log_downloads.csv

These examples will retrieve all posts available through the API from the requested channel. If you want to collect channel's information only, without posts, you can run:

<br />

### **Limit download to channel's metadata only**

```         
python main.py --telegram-channel channelname --limit-download-to-channel-metadata
```

<br />

### **Updating channel's data**

It is automatic because it has context

```         
python main.py --telegram-channel channelname --output './path/to/channels'
```

**Expected output**

-   Files of collected channels:
    -   chats.txt
    -   collected_chats.csv
    -   user_exceptions.txt
    -   counter.csv
    -   collected_chanels
-   A new folder: <channel_name> containing
    -   A JSON file containing channel's profile metadata
    -   A JSON file containing posts from the requested channel
    -   log_downloads.csv

<br />

### **Specify output folder**

The script allows you to specify a specific output directory to save collected data. The sxcript will create those folders in case do not exist.

```         
python main.py --telegram-channel channelname --output ./path/to/chosen/directory`
```

The expected output is the same a described above but data will be save using the chosen directory.

<br />

------------------------------------------------------------------------

## `build-dataset.py`

This Python script reads a channel the collected files and creates a new dataset containing messages from the requested channels. By default, the created dataset will be located in the `output` folder.

If you provided a specific directory to save collected data, you need to provide the same path to use this script.

### Options

-   `-telegram-channel channel --data-path` Path were data is located. Will use `./output/data` if not given.

If a specific directory was not provided in `main.py`, run:

```         
python build-dataset.py
```

If you provided a specific directory using the option `--output` in `main.py`, run:

```         
python build-dataset.py --data-path ./path/to/chosen/directory
```

These option will create the above-mentioned dataset: `msgs_dataset.csv`, a file containing posts and messages from the requested channels.

<br />

------------------------------------------------------------------------

## `channels-to-network.py`

This Python script builds a network graph. By default, the file will be located in the `output` folder. The script also saves a preliminary graph: `network.png` using the modules matplotlib, networkx, and python-louvain, which implements community detection. You can import the GEFX Graph File using different softwares, including Gephi.

### Options

-   `--data-path` Path were data is located. Will use `./output/data` if not given.

If a specific directory was not provided in `main.py`, run:

```         
python channels-to-network.py
```

If you provided a specific directory using the option `--output` in `main.py`, run:

```         
python channels-to-network.py --data-path ./path/to/chosen/directory
```
