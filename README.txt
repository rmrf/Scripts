Scripts
=======

These scripts are used for general System Admin tasks

 * find_free_ip.py  Find Free (No dns name assign and Not Pingable) ip address
 * pingp.py     Ping with pictures which draw the response time line


#### Setup required python virtualenv
```bash
git clone git@github.com/balbalbas
cd Mycroft
virtualenv --distribute .venv
source env.sh
easy_install -U distribute
pip install -r pip-requires.txt


#### How to use
```bash
source env.sh

Then directly run these scripts, it's have self illustration
