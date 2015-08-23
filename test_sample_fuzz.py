# Works with 1.2 and v1.3:
# $ . ~/trees/virtualenv-b2g/bin/activate
# (in a virtualenv) $ rlwrap gaiatest --address=localhost:2828 --testvars=testVars.json --restart test_sample_fuzz.py
# $ clear && grep -i "JavaScript Error" out.txt | sort | uniq -c | sort -n -r

# Idea for generational: https://marionette_client.readthedocs.org/en/latest/
# Find list of tappable IDs, then tap a random ID in each app

# Idea for mutation: https://github.com/mozilla-b2g/gaia/blob/master/tests/python/gaia-ui-tests/gaiatest/tests/endurance/test_endurance_settings.py
# overwrite settings function within the TestEnduranceSettings object to navigate to a random screen

import gaiatest
import marionette
import random
import sys
import time

APP_LAUNCH_TIMEOUT = 0.5
IGNORE_APPS_NAMES = []
IGNORE_APPS_NAMES.append('Dev')  # new app in v1.3
IGNORE_APPS_NAMES.append('Marketplace')
IGNORE_APPS_NAMES.append('Membuster')
IGNORE_APPS_NAMES.append('Mochitest')
IGNORE_APPS_NAMES.append('PackStubTest')
IGNORE_APPS_NAMES.append('Stage')  # new app in v1.3
IGNORE_APPS_NAMES.append('Test Agent')
IGNORE_APPS_NAMES.append('Test Container')
IGNORE_APPS_NAMES.append('Test OTASP')
IGNORE_APPS_NAMES.append('Test receiver#1')
IGNORE_APPS_NAMES.append('Test Receiver#2')
IGNORE_APPS_NAMES.append('Test receiver (inline)')
IGNORE_APPS_NAMES.append('Test Wap Push')  # new app in v1.3
IGNORE_APPS_NAMES.append('Usage')
cookie = 'REMOV'
cookie += 'EME    '


def demo_shuffling_opening_non_opened_apps(apps, installed_apps, running_apps):
    count = 1
    random.shuffle(installed_apps)
    print installed_apps
    for app_name in installed_apps:
        if app_name not in IGNORE_APPS_NAMES and app_name not in running_apps and count <= 3:  # launch 3 apps at a time
            print str(count) + ': ' + app_name
            apps.launch(app_name)
            time.sleep(APP_LAUNCH_TIMEOUT)
            running_apps.append(app_name)
            count += 1
    return running_apps


def demo_non_stop_launching_apps(apps, installed_apps):
    count = 1
    while True:
        app_name = random.choice(installed_apps)
        if app_name not in IGNORE_APPS_NAMES:
            count += 1
            print str(count) + ' Opening: ' + app_name
            print_frc_lines('apps.launch("' + app_name + '")')
            apps.launch(app_name)
            time.sleep(APP_LAUNCH_TIMEOUT)


def get_installed_app_names(apps):
    '''
    Returns a list of names of installed apps.
    '''
    names = []
    installedApps = apps.installed_apps
    for index in xrange(len(installedApps)):
        names.append(installedApps[index].name)
    return names


def get_running_app_names(apps):
    '''
    Returns a list of names of running apps.
    '''
    names = []
    runningApps = apps.running_apps
    for index in xrange(len(runningApps)):
        names.append(runningApps[index].name)
    return names


def print_frc_lines(line):
    print cookie + line


def main():
    fuzzSeed = time.time()
    random.seed(fuzzSeed)
    print 'fuzzSeed is: ' + str(fuzzSeed)

    mari = marionette.Marionette()
    mari.start_session()
    apps = gaiatest.GaiaApps(mari)
    # The following 2 lines used to work in 1.2 and 1.3 B2G Desktop/emulators, but not yet the Flame
    #lock = gaiatest.LockScreen(mari)
    #lock.unlock()

    installed_apps = get_installed_app_names(apps)
    print installed_apps
    running_apps = get_running_app_names(apps)
    print running_apps

    start(apps, installed_apps, running_apps)


def start(apps, installed_apps, running_apps):
    # DDBEGIN
    #demo_shuffling_opening_non_opened_apps(apps, installed_apps, running_apps)
    demo_non_stop_launching_apps(apps, installed_apps)
    # DDEND

main()
