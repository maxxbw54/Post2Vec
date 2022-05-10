import subprocess
from ProgrammingToolkit.python.lib.utils.diff_util import diff_parser_from_str
from unidiff import PatchSet
import logging


# def git_clone(project_url, folder_path):
#     args = ['clone', project_url, folder_path]
#     try:
#         subprocess.check_call(['git'] + list(args))
#     except Exception as e:
#         print("git clone failed! url=%s" % project_url)
#         print(e)
#         return False
#     return True


def git_clone(usr_name, repo_name, folder_path):
    from ProgrammingToolkit.python.lib.utils.html_util import get_html
    project__url = 'https://github.com/{}/{}'.format(usr_name, repo_name)
    if 'This is not the web page you are looking for' in get_html(project__url):
        logging.warning("Repo {} not exists!".format(project__url))
        return False
    project_git_url = 'https://github.com/{}/{}.git'.format(usr_name, repo_name)
    args = ['clone', project_git_url, folder_path]
    try:
        subprocess.check_call(['git'] + list(args))
    except Exception as e:
        logging.error("git clone failed! args={}\nerror:{}".format(args, e))
        return False
    return True


def git_log(work_dir):
    import os
    cmd = "git log --pretty=short > git.log"
    try:
        subprocess.call(cmd, shell=True, cwd=work_dir)
    except Exception as e:
        logging.error("git log failed! cmd={}\nerror:{}".format(cmd, e))
        return False
    log_fpath = os.path.join(work_dir, 'git.log')
    return log_fpath


def get_com_msg(com, git_repo_dir):
    """
    get commit message for a specific repo and commit
    :param com:
    :param git_repo_dir:
    :return:
    """
    cmd = "git log --format=%%B -n 1 %s" % com
    try:
        com_msg = subprocess.check_output(cmd, shell=True, cwd=git_repo_dir).decode("utf-8").strip()
    except Exception as e:
        logging.error("get_com_msg failed! cmd={}\nerror:{}".format(cmd, e))
        return None
    return com_msg


def get_all_commits(work_dir):
    """
    Untested
    :param commit:
    :param work_dir:
    :return:
    """
    cmd = "git log --pretty=format:\"%H\""
    try:
        commits = subprocess.check_output(cmd, shell=True, cwd=work_dir).decode("utf-8").strip().split('\n')
    except Exception as e:
        logging.error("get_all_commits failed! cmd={}\nerror:{}".format(cmd, e))
        return None
    return commits


def get_coms_by_substring_in_msg(work_dir, substr):
    """
    Untested
    :param commit:
    :param work_dir:
    :return:
    """
    cmd = "git log --pretty=format:\"%H\" --grep='{}'".format(substr)
    try:
        commits = subprocess.check_output(cmd, shell=True, cwd=work_dir).decode("utf-8").strip().split('\n')
    except Exception as e:
        logging.error("get_coms_by_substring_in_msg failed! cmd={}\nerror:{}".format(cmd, e))
        return None
    if commits == ['']:
        return []
    return commits


def get_commit_time(work_dir, com=None):
    """
    Untested
    :param commit:
    :param work_dir:
    :return:
    """
    if com is None:
        cmd = "git log -1 --format=%ci"
    else:
        cmd = "git show -s --format=%ci {}".format(com)
    try:
        com_time = subprocess.check_output(cmd, shell=True, cwd=work_dir).decode("utf-8").strip().split('\n')
    except Exception as e:
        logging.error("get_commit_time failed! cmd={}\nerror:{}".format(cmd, e))
        return None
    return com_time


def git_show(work_dir, com, rel_fpath):
    cmd = "git show {}:{}".format(com, rel_fpath)
    try:
        fstr = subprocess.check_output(cmd, shell=True, cwd=work_dir).decode("utf-8").strip()
    except Exception as e:
        logging.error("git_show failed! cmd={}\nerror:{}".format(cmd, e))
        return None
    return fstr


'/data/bowen/data/Transformation4J/FBMining/repo/'


def parse_time(time_str):
    """
    example 2017-12-14 21:58:44 +0800
    :param time_str:
    :return:
    """
    [year, month, day] = time_str.split(' ')[0].split('-')[0:3]
    [hh, mm, ss] = time_str.split(' ')[1].split(':')[0:3]
    time_zone = time_str.split(' ')[2]
    return {'year': int(year), 'month': int(month), 'day': int(day), 'hour': int(hh), 'minute': int(mm),
            'second': int(ss), 'time zone': int(time_zone)}


def get_changed_file_list_from_com(com, work_dir):
    """
    :param com:
    :param work_dir:
    :return:
    """
    cmd = "git diff-tree --no-commit-id --name-only -r %s" % com
    try:
        flist = subprocess.check_output(cmd, shell=True, cwd=work_dir).decode("utf-8").strip().split('\n')
    except Exception as e:
        logging.error("get_changed_file_list_from_com failed! cmd={}\nerror:{}".format(cmd, e))
        return None
    return flist


def get_changed_file_list_between_two_coms(com1, com2, work_dir):
    """

    :param com:
    :param work_dir:
    :return:
    """
    cmd = "git diff --name-only {} {}".format(com1, com2)
    try:
        flist = subprocess.check_output(cmd, shell=True, cwd=work_dir).decode("utf-8").strip().split('\n')
    except Exception as e:
        logging.error("get_changed_file_list_from_com failed! cmd={}\nerror:{}".format(cmd, e))
        return None
    return flist


def git_checkout(folder_path, commit_sha=None, force=False):
    if force:
        cmd = "git reset --hard"
        subprocess.call(cmd, shell=True, cwd=folder_path)
    if commit_sha is None:
        args = ['--git-dir', folder_path + '/.git', '--work-tree', folder_path, 'checkout', 'master']
    else:
        args = ['--git-dir', folder_path + '/.git', '--work-tree', folder_path, 'checkout', commit_sha]
    try:
        subprocess.check_call(['git'] + list(args))
    except Exception as e1:
        # To address: Please, commit your changes or stash them before you can merge.
        try:
            clean_args = ['--git-dir', folder_path + '/.git', '--work-tree', folder_path, 'clean', '-d', '-fx', '.']
            subprocess.check_call(['git'] + list(clean_args))
            reset_args = ['--git-dir', folder_path + '/.git', '--work-tree', folder_path, 'reset', '--hard']
            subprocess.check_call(['git'] + list(reset_args))
            # pull_args = ['--git-dir', folder_path + '/.git', '--work-tree', folder_path, 'pull']
            # subprocess.check_call(['git'] + list(pull_args))
            subprocess.check_call(['git'] + list(args))
        except Exception as e2:
            logging.error("git Checkout failed! cmd={}\nerror:{}".format(args, e2))
            return False
        return True
    return True


def git_diff(folder_path, parent_com, cur_com, diff_mode=None):
    '''
    :param folder_path:
    :param parent_com:
    :param cur_com:
    :return:
    '''
    if diff_mode is not None:
        args = ['--git-dir', folder_path + '/.git', '--work-tree', folder_path, 'diff', diff_mode, '--unified=0',
                parent_com, cur_com]
    else:
        args = ['--git-dir', folder_path + '/.git', '--work-tree', folder_path, 'diff', '--unified=0', parent_com,
                cur_com]

    try:
        diff = subprocess.check_output(['git'] + list(args)).decode('latin-1').encode("utf-8").decode('utf-8').strip()
    except Exception as e:
        logging.error("git_diff failed! cmd={}\nerror:{}".format(args, e))
        return None
    return diff


def git_diff_single_file(folder_path, parent_com, buggy_rel_path, cur_com, cur_rel_path):
    '''
    :param folder_path:
    :param parent_com:
    :param cur_com:
    :return:
    '''
    args = ['--git-dir', folder_path + '/.git', '--work-tree', folder_path, 'diff', '--unified=0',
            parent_com + ':' + buggy_rel_path, cur_com + ':' + cur_rel_path]
    try:
        diff = subprocess.check_output(['git'] + list(args)).decode('latin-1').encode("utf-8").decode('utf-8').strip()
    except Exception as e:
        logging.error("git_diff failed! cmd={}\nerror:{}".format(args, e))
        return None
    return diff


def get_modified_file_list_from_diff(diff_str):
    diffs = diff_parser_from_str(diff_str)
    modified_sol_list = []
    for d in diffs:
        source_file = str(d.source_file)
        modified_sol_list.append(source_file)
    return modified_sol_list


def get_parent_commit(com, git_repo_dir):
    """
    Untested
    :param commit:
    :param work_dir:
    :return: a parent commit list
    """
    cmd = "git log --pretty=%%P -n 1 \"%s\"" % com
    try:
        par_commit = subprocess.check_output(cmd, shell=True, cwd=git_repo_dir).decode("utf-8").strip()
    except Exception as e:
        logging.error("get_parent_commit failed! cmd={}\nerror:{}".format(cmd, e))
        return None
    if len(par_commit) == 0:
        return None
    return par_commit.split(' ')[0]


def parse_diff_str(diff_str):
    return PatchSet(diff_str)


if __name__ == '__main__':
    # git_clone('https://github.com/XBWer/WordSimilarity.git', '/home/bowenxu/Downloads/test')
    # git_checkout('/home/bowenxu/Downloads/test/', '2664b848dcadb6f29d802c06006d78269347434a')
    # write_str = git_diff(
    #     '/home/bowenxu/Desktop/Research/ProgramRepair/SmartContract/SmartContractProject/data/manualDataset/3-GoodCases-FaultLocalization/checked_succeed_ambrosus#Ambrosus/cases/4-goodcase-less5/0be01e2c68499f6b76e849d20c2c5c98cf1b7179_diff_cd491e113285d9b7ef6bddea562932744863e823/new',
    #     'cd491e113285d9b7ef6bddea562932744863e823', '0be01e2c68499f6b76e849d20c2c5c98cf1b7179')
    # write_str= git_diff('/home/bowenxu/Downloads/test','179586fef4a816b16b3541ac490b79777909b3c4','71cfe15ea81d4c6e677dc1d0d161237d7b910fb4')
    # print(write_str)
    # git_log("/data/bowen/SmartContract-FixPattern/Repos/7070#fabric/github_repo")

    parse_time('2017-12-14 21:58:44 +0800')
