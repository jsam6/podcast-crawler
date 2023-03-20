## <u>This is a podcast crawler</u>

### Objective
Crawl and save podcast .mp3 and details.
Currently only supports Darknet Diaries podcast.

### Podcast
 - Darknet Diaries

#### Requirements
- Python3
- MySQL

#### Setup and run

```
$ python3 -m venv venv
$ venv\Scripts\activate

$ ./venv/Scripts/activate (cmd)
$ . venv/Scripts/activate (bash)

```

#### Run crawler
```
python index.py
```

#### Output

```
podcast-tracker
│   README.md
│   index.py    
│
└───output
│   └───Darknet.Diaries
│       └── 128-15.11.2022
|       |    │   128.mp3
|       |    │   data.json
│       └── 129-29.11.2022
│            | 129.mp3
│            | data.json
│   
└───crawlers
    └── DarknetDiaries.py
```