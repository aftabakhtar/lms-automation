# lms-automation



## Installation

#### Step #1

Cloning repository and installing requirements

```bash
# clone the repo
git clone https://github.com/aftabakhtar/lms-automation.git

# change the working directory to lms-automation
cd lms-automation

# install the requirements
python3 -m pip install -r requirements.txt
```



#### Step #2

Download the web driver for the browser you use (links below) and extract it in the project directory.

**Google Chrome / Chromium:** https://chromedriver.chromium.org/downloads

**Firefox:** https://github.com/mozilla/geckodriver/releases



#### Step #3

For the **first and only time**, you would have to specify your `browser` and the name your `OS` (run the same commands if you need to respecify).

You can specify browser and driver name as following:

```bash
python3 deadlines.py --driver=chrome --os=linux
```

