marifuzz
========

A user interaction fuzzer for Firefox OS, based on the Marionette framework.

Known to work since FxOS 1.2, tested only up to 2.0.

(tested on 20150716160204 v2.0.)

Assumptions:
============
1. Gone through First-Time Use wizard.
2. Disabled display turn-off timer.
3. Disabled lockscreen manually.
4. Debugging via USB is switched to "ADB only" mode.
5. Create a virtualenv called gaiatest20 in ~/trees using `virtualenv ~/trees/gaiatest20`.
6. Install gaiatest-v2.0 from pip using `~/trees/gaiatest20/bin/pip install gaiatest-v2.0`.
7. Run `adb forward tcp:2828 tcp:2828`.
8. Change into marifuzz directory using `cd ~/trees/marifuzz`.
9. Have a testvars file, e.g. ~/trees/marifuzz/testVars.json
```
{
    "acknowledged_risks": true,
    "skip_warning": true
}
```
10. Allow python-2.7 to accept incoming network connections.
11. Run `~/trees/gaiatest20/bin/gaiatest --address=localhost:2828 --testvars=testVars.json --restart test_sample_fuzz.py`.

If using gaiatest from pip:
===========================

Warning: may not work, use gaiatest-v2.0 for FxOS 2.0 for now.

After creating a virtualenv and installing gaiatest via pip, changed TreeherderRequest to TreeherderClient in the following file:
```
~/trees/b2g-venv/lib/python2.7/site-packages/thclient/client.py
```
  * Notes:
```
  File "/Users/skywalker/trees/b2g-venv/lib/python2.7/site-packages/gaiatest/mixins/treeherder.py", line 20, in <module>
    from thclient import TreeherderRequest, TreeherderJobCollection

$ ~/trees/b2g-venv/bin/pip freeze
blessings==1.6
boto==2.38.0
gaiatest==0.32
httplib2==0.9.1
manifestparser==1.1
marionette-client==0.8.5
marionette-transport==0.4
mozcrash==0.14
mozdevice==0.45
mozfile==1.1
mozhttpd==0.7
mozinfo==0.8
mozlog==2.11
moznetwork==0.26
mozprocess==0.22
mozprofile==0.24
mozrunner==6.7
moztest==0.7
mozversion==1.2
oauth2==1.5.211
requests==2.7.0
treeherder-client==1.5
wheel==0.24.0
```
