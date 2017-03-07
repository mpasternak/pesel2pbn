clean:
	find . -name \*~ -print0 | xargs -0 rm -fv 
	find . -name \*bak -print0 | xargs -0 rm -fv 
	find . -name \*pyc -print0 | xargs -0 rm -fv 
	find . -name \*\\.log -print0 | xargs -0 rm -fv 

uic: 
	cd pesel2pbn && pyuic5 pesel2pbn.ui > pesel2pbn_auto.py
