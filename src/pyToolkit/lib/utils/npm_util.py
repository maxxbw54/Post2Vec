# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     command_util
   Description :
   Author :       bowenxu
   date：          10/4/18
-------------------------------------------------
   Change Activity:
                   10/4/18:
-------------------------------------------------
"""

import os
import subprocess

from src.utils.file_util import write_file

import os

# school server
print('[PATH] If it is not executed on school server, please modify the value of PATH.')
os.environ[
    'PATH'] = '/home/bowen/Desktop/ProgramRepairforSmartContract/.env/bin:/home/bowen/.nvm/versions/node/v8.11.1/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin:/opt/dell/srvadmin/bin:'


def exec_npm_install_solcover(working_directory):
    '''
    execute "npm i solidity-coverage"
    :param working_directory:
    :return:
    '''
    if_success = True
    try:
        # subprocess.call("pkill node", stderr=subprocess.STDOUT, cwd=working_directory, shell=True)
        status = subprocess.check_output("npm install --save-dev solidity-coverage ; exit 0", stderr=subprocess.STDOUT,
                                         cwd=working_directory,
                                         shell=True)
        write_file(working_directory + '/exec_npm_solcov.log', status)
        if '+ solidity-coverage' not in status:
            if_success = False
    except Exception as e:
        if_success = False
        print('npm i solidity-coverage\n' + e.message)
    finally:
        return if_success


def exec_npm_install_specific_package(working_directory, package):
    '''
    execute "npm i package"
    :param working_directory:
    :return:
    '''
    if_success = True
    try:
        # subprocess.call("pkill node", stderr=subprocess.STDOUT, cwd=working_directory, shell=True)
        status = subprocess.check_output("npm install " + package + " ; exit 0", stderr=subprocess.STDOUT,
                                         cwd=working_directory,
                                         shell=True)
        write_file(working_directory + '/exec_npm_' + package + '.log', status)
    except Exception as e:
        if_success = False
        print('npm i ' + package + '\n' + e.message)
    finally:
        return if_success


def exec_npm_rebuild(working_directory):
    '''
    execute "npm rebuild"
    :param working_directory:
    :return:
    '''
    if_success = True
    try:
        # subprocess.call("pkill node", stderr=subprocess.STDOUT, cwd=working_directory, shell=True)
        status = subprocess.check_output("npm rebuild ; exit 0", stderr=subprocess.STDOUT, cwd=working_directory,
                                         shell=True)
        write_file(working_directory + '/exec_npm_rebuild.log', status)
    except Exception as e:
        if_success = False
        print('npm rebuild\n' + e.output)
        # raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    finally:
        return if_success


def exec_npm_install_all(working_directory):
    '''
    execute "npm i"
    :param working_directory:
    :return:
    '''
    if 'package.json' in os.listdir(working_directory) and 'package-lock.json' in os.listdir(working_directory):
        os.remove(working_directory + os.sep + 'package-lock.json')
    if_success = True
    status = ''
    try:
        # subprocess.call("pkill node", stderr=subprocess.STDOUT, cwd=working_directory, shell=True)
        status = subprocess.check_output("npm install ; exit 0", stderr=subprocess.STDOUT, cwd=working_directory,
                                         shell=True)
        write_file(working_directory + '/exec_npm_install.log', status)
    except Exception as e:
        if_success = False
        # print('npm install\n' + e.output)
        # raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    finally:
        return if_success


def exec_npm_init(working_directory):
    '''
    execute "npm i"
    :param working_directory:
    :return:
    '''
    if_success = True
    try:
        # subprocess.call("pkill node", stderr=subprocess.STDOUT, cwd=working_directory, shell=True)
        status = subprocess.check_output("npm init ; exit 0", stderr=subprocess.STDOUT, cwd=working_directory,
                                         shell=True)
        write_file(working_directory + '/exec_npm_init.log', status)
    except Exception as e:
        if_success = False
        print('npm init\n' + e.output)
        # raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    finally:
        return if_success


def exec_solcover(working_directory):
    '''
    execute "./node_modules/.bin/solidity-coverage"
    :param working_directory:
    :return:
    '''
    try:
        status = subprocess.call("pkill node", stderr=subprocess.STDOUT, cwd=working_directory, shell=True)
        status = subprocess.check_output("./node_modules/.bin/solidity-coverage ; exit 0",
                                         stderr=subprocess.STDOUT,
                                         cwd=working_directory, shell=True)
    except Exception as e:
        # print('./node_modules/.bin/solidity-coverage\n' + e.output)
        status = e.output
    finally:
        if 'coverage reports generated' in status:
            log_path = working_directory + '/exec-solcover-valid.log'
        else:
            log_path = working_directory + '/exec-solcover-invalid.log'
        write_file(log_path, status)
        from src.utils.truffle_util import analysis_truffle_test_result
        exec_result = analysis_truffle_test_result(log_path)
        # init
        exec_msg = None
        if 'Error: ENOENT: no such file or directory, open \'./allFiredEvents\'' in status:
            exec_msg = 'allFiredEventIssue'
        if_generated = True if 'coverage reports generated' in status else False
        return if_generated, exec_msg
