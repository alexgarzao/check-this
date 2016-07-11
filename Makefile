# Email reminders
# Author: Alex S. Garzão <alexgarzao@gmail.com>
# Makefile

setup:
	virtualenv .env && . .env/bin/activate && pip install -r requirements.txt

run:	clean
	python check-this/check_this.py

checkcode:	lint pep8

lint:
	pylint *.py check-this/*.py

pep8:
	pep8 *.py check-this/*.py

clean:
	rm -f check-this/*.pyc
