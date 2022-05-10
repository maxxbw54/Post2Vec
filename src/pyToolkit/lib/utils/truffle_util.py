# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     truffle_util
   Description :
   Author :       bowenxu
   date：          18/4/18
-------------------------------------------------
   Change Activity:
                   18/4/18:
-------------------------------------------------
"""

from src.utils.file_util import write_file

import os

# school server
print('[PATH] If it is not executed on school server, please modify the value of PATH.')
os.environ[
    'PATH'] = '/home/bowen/Desktop/ProgramRepairforSmartContract/.env/bin:/home/bowen/.nvm/versions/node/v8.11.1/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin:/opt/dell/srvadmin/bin:'
#
DEVNULL = open(os.devnull, 'wb')

import subprocess

print('truffle version : %s' % subprocess.check_output("truffle version ; exit 0", shell=True))


def exec_truffle_test_large_limitation(working_directory):
    '''
    execute "pkill node ; testrpc ; truffle test;"
    :param working_directory:
    :return:
    '''
    import subprocess
    status = None
    try:
        subprocess.call("pkill node", stderr=subprocess.STDOUT,
                        cwd=working_directory, shell=True)
        process = subprocess.Popen('testrpc -l 100000000000000', shell=True, stdout=DEVNULL, stderr=subprocess.STDOUT)
        status = subprocess.check_output("truffle test ; exit 0", stderr=subprocess.STDOUT,
                                         cwd=working_directory,
                                         shell=True)
        process.kill()
    except subprocess.CalledProcessError as e:
        status = e.output
    finally:
        return status


def exec_truffle_test(working_directory):
    '''
    execute "pkill node ; testrpc ; truffle test;"
    :param working_directory:
    :return:
    '''
    import subprocess
    status = None
    log_path = working_directory + os.sep + 'exec_truffleTest.log'
    try:
        subprocess.call("pkill node", stderr=subprocess.STDOUT,
                        cwd=working_directory, shell=True)
        process = subprocess.Popen('testrpc', shell=True, stdout=DEVNULL, stderr=subprocess.STDOUT)
        # if process.poll() is None:
        status = subprocess.check_output("truffle test ; exit 0", stderr=subprocess.STDOUT,
                                         cwd=working_directory,
                                         shell=True)
        process.kill()
        # else:
        # do_nothing = None
        # raise Exception('testrpc failed!')
    except subprocess.CalledProcessError as e:
        status = e.output
    except Exception, e:
        status = e.output
        print('truffle test exception, please check:\n %s' % working_directory)
        write_file(log_path, status)
        return None
    finally:
        if 'Error: Exceeds block gas limit' in status:
            status = exec_truffle_test_large_limitation(working_directory)
        # do not swith the order
        if 'Could not connect to your Ethereum client.' in status:
            print('Configure error! Please modify truffle.js:\n %s' % working_directory)
            write_file(log_path, status)
            return None
        if 'Error: Cannot find module' in status:
            print('Cannot find module error! Please add module manually:\n %s' % working_directory)
            write_file(log_path, status)
            return None
        write_file(log_path, status)
        return analysis_truffle_test_result(log_path)


def clean_symbols(str_tmp):
    str_tmp = str_tmp.replace('[32m', '').replace('[33m', '').replace('[31m', '').replace('[92m', '').replace(
        '[90m', '').replace('✓', '').replace('[0m', '').strip()
    return str_tmp


def extract_msg(str_tmp, flag):
    '''
    remove symbols like [90m(grey), [32m(green), [33m(time cost), [31m(red),✓(passing), [0m
    Contract: Etherep
      [31m  7) should set debug to off
        > No events were emitted
      [31m  8) should set debug to on
        > No events were emitted
      [32m  ✓[90m should add an unweighted rating of 5 by mary for joe[33m (55ms)
      [32m  ✓[90m should add an unweighted rating of 5 by pat for mary[33m (48ms)
      [32m  ✓[90m joe, sam, and mary should add weighted ratings of 3 to pat[31m (104ms)

      Contract: RatingStore
      [32m  ✓[90m should show manager as account given in constructor
      [32m  ✓[90m should set the manager's score to 5[33m (38ms)
      [32m  ✓[90m should add a new unweighted rating of 5[31m (97ms)
      [32m  ✓[90m should reset the manager's score to 0[33m (63ms)
      [32m  ✓[90m should change controller to third account
      [32m  ✓[90m should change manager to second account
      [32m  ✓[90m should set debug to true
      [32m  ✓[90m should set debug to false[31m (160ms)
      [32m  ✓[0m[90m should add an unweighted rating of 5 by mary for joe[0m[33m (55ms)[0m
'
'

    [92m [32m 11 passing[90m (2s)
    [31m  8 failing
    :return: remove those symbols
    '''
    # remove time (*ms) or （*s)
    import re
    str_tmp = re.sub(r'\([0-9]+ms\)', '', str_tmp)
    str_tmp = re.sub(r'\([0-9]+s\)', '', str_tmp)
    if flag == 'passing':
        st_idx = str_tmp.index('✓') + len('✓')
        et_idx = len(str_tmp)
    else:
        st_idx = str_tmp.index(')') + 1
        et_idx = len(str_tmp)
    return clean_symbols(str_tmp[st_idx:et_idx])


def analysis_truffle_test_result(result_path):
    '''
    analysis report not only for truffle but also for solidity-coverage
    :param result_path:
    :return:
    '''
    import re
    exec_result = {}
    with open(result_path, "r") as f:
        for line in f:
            if '✓' in line:
                line = extract_msg(line, 'passing')
                exec_result[line] = 'passing'
            elif re.search(r'[31m\s[0-9]+\)', line) and 'Contract:' not in line:
                line = extract_msg(line, 'failing')
                exec_result[line] = 'failing'
    if exec_result == {}:
        return None
    return exec_result


if __name__ == '__main__':
    test_dir = '/home/bowenxu/Downloads/tmp/checked-succeed-gointollc#etherep-contracts/cases/3-goodcase-more5/4f9b7ef59a9cf5d8796e142d1d3a30ab3b114b0b_diff_cae8f281a47b5c06aa638cb590edfb502c8033d5/old'
    # exec_truffle_test(test_dir)
    dicttmp = analysis_truffle_test_result(test_dir + '/exec-truffleTest.log')
    for key in dicttmp.keys():
        for t in dicttmp[key]:
            print key, t
