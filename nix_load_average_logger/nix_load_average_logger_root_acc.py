#!/bin/env python3

# Copyright (c) 2018. All rights reserved. OculusD.com, Inc. Please refer to the LICENSE.txt file for full license information. Licensed in terms of the GPLv3 License.

from odc_pycommons import HOME
from odc_pycommons.models import SensorAxisReading, RootAccount, Thing
from odc_pyadminlibs.persistence.root_account_persistence import read_root_account_by_email_address
from odc_pyadminlibs.persistence.thing_persistence import read_all_things_for_linked_root_account_id
from odc_pyadminlibs.actions.authentication import authenticate_root_account, get_thing_token_using_root_account
from odc_pyadminlibs.actions.data import log_data_with_root_account
import os, sys, getopt
from datetime import datetime

ROOT_ACC_EMAIL = None
THING_ID = None


def print_help():
    print('{} -e <root_account_email> -t <thing_id>'.format(os.path.basename(__file__)))
    sys.exit(2)


def parse_input_args(argv):
    global ROOT_ACC_EMAIL
    global THING_ID
    try:
      opts, args = getopt.getopt(argv,"he:t:",["email=","thing="])
    except getopt.GetoptError:
      print_help()
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-e", "--email"):
            ROOT_ACC_EMAIL = arg
        elif opt in ("-t", "--thing"):
            THING_ID = arg
    if ROOT_ACC_EMAIL is None or THING_ID is None:
        print_help()


def get_utc_timestamp(with_decimal: bool=False):
    epoch = datetime(1970,1,1,0,0,0)
    now = datetime.utcnow()
    timestamp = (now - epoch).total_seconds()
    if with_decimal:
        return timestamp
    return int(timestamp)


def load_root_account()->RootAccount:
    try:
        return read_root_account_by_email_address(email_address=ROOT_ACC_EMAIL, persistence_path=HOME, persistence_file='root_account')
    except:
        print_help()


def auth_root_account(root_account: RootAccount)->RootAccount:
    now = get_utc_timestamp()
    if root_account.root_account_session_create_timestamp is not None:
        if isinstance(root_account.root_account_session_create_timestamp, int):
            print('\tCached token timestamp: {}'.format(root_account.root_account_session_create_timestamp))
            print('\t                   now: {}'.format(now))
            if root_account.root_account_session_create_timestamp > (now-60):
                root_account.root_account_session_token = None
                root_account.root_account_session_create_timestamp = 0
                auth_result = authenticate_root_account(root_account=root_account, persist_token=True)
                if auth_result['IsError'] is False:
                    root_account = auth_result['RootAccountObj']
            else:
                print('\tUsing cached token...')
        else:
            root_account.root_account_session_token = None
            root_account.root_account_session_create_timestamp = 0
            auth_result = authenticate_root_account(root_account=root_account, persist_token=True)
            if auth_result['IsError'] is False:
                root_account = auth_result['RootAccountObj']
    else:
        auth_result = authenticate_root_account(root_account=root_account, persist_token=True)
        if auth_result['IsError'] is False:
            root_account = auth_result['RootAccountObj']
    if root_account.root_account_session_token is None:
        print('error: Failed to authenticate')
        print_help()
    return root_account


def load_thing(root_account: RootAccount)->Thing:
    thing = None
    things = read_all_things_for_linked_root_account_id(linked_root_account_id=root_account.root_account_ref, persistence_path=HOME, persistence_file='things')
    try:
        thing = things[THING_ID]
    except:
        print('Thing "{}" not found'.format(THING_ID))
        print_help()
    return thing


def get_thing_token(root_account: RootAccount, thing: Thing)->Thing:
    if thing.thing_token is not None:
        print('\tUsing cached thing token')
        return thing
    thing_token_result = get_thing_token_using_root_account(root_account=root_account, thing=thing)
    if thing_token_result['IsError'] is False:
        thing = thing_token_result['Thing']
    return thing


def record_load_average(root_account: RootAccount, thing: Thing):
    system_load = os.getloadavg()
    print('Load Data: {}'.format(system_load))
    thing.thing_sensors['Load Sensor'].sensor_axes['1 Minute Load Average'].add_reading(SensorAxisReading(reading_value=system_load[0]))
    thing.thing_sensors['Load Sensor'].sensor_axes['5 Minute Load Average'].add_reading(SensorAxisReading(reading_value=system_load[1]))
    thing.thing_sensors['Load Sensor'].sensor_axes['15 Minute Load Average'].add_reading(SensorAxisReading(reading_value=system_load[2]))
    result = log_data_with_root_account(root_account=root_account, thing=thing)
    if result['IsError'] is False:
        print('\tNumber of records captured: {}'.format(result['RecordsCaptured']))
    else:
        print('\tError Message: {}'.format(result['ErrorMessage']))
        

def main():
    parse_input_args(sys.argv[1:])
    print('Loading root_account "{}"'.format(ROOT_ACC_EMAIL))
    root_account = load_root_account()
    print('Authenticating root_account')
    root_account = auth_root_account(root_account=root_account)
    print('Loading thing')
    thing = load_thing(root_account=root_account)
    print('Confirming thing token')
    thing = get_thing_token(root_account=root_account, thing=thing)
    print('Capturing load average')
    record_load_average(root_account=root_account, thing=thing)
    print('DONE')


if __name__ == '__main__':
    main()


# EOF
