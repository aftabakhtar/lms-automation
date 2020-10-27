# lms-automation



## Installation

Cloning repository and installing requirements

```bash
# clone the repo
git clone https://github.com/aftabakhtar/lms-automation.git

# change the working directory to lms-automation
cd lms-automation

# install the requirements
python3 -m pip install -r requirements.txt
```



## Running

To run simply do:

```bash
python3 deadlines.py
```

however if you want to save user name and password so that you don't have to enter it everytime. 

**To remember username and password for later use**

```
python3 deadlines.py --user=USERNAME --pwd=PASSWORD
```

replace your username and password with `USERNAME` and `PASSWORD` respectively.

After entering your username and password with flags you will not be prompted again.



### Security Note:

Once a person saves password it is encrypted with a key and stored locally on the computer. Please do not share `.key` and `.pass` files with anyone.