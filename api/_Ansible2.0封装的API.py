#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: StrongIt
# Ansible API And Version >=2.0

from __future__ import (absolute_import, division, print_function)

from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from collections import namedtuple
from ansible.playbook.play import Play
from ansible import constants as C
from ansible.parsing.splitter import parse_kv
from ansible.executor.playbook_executor import PlaybookExecutor
import os


class DoGoMinix(object):
    def __init__(self, inventory_file=None, passwords=None, verbosity=0, cb='defaults'):

        if passwords is None:
            passwords = {'conn_pass': '', 'become_pass': ''}

        if inventory_file is None:
            inventory_file = C.DEFAULT_HOST_LIST

        self.verbosity = verbosity
        self.inventory_file = inventory_file

        self.passwords = passwords

        self.cb = cb

        self._set_option = False

        # initialize needed objects
        self.variable_manager = VariableManager()

        self.loader = DataLoader()


    def _base_option(self):
        """ base option"""
        return dict(
            connection=C.DEFAULT_TRANSPORT,
            forks=C.DEFAULT_FORKS,
            become=False,
            become_method=C.DEFAULT_BECOME_METHOD,
            become_user=None,
            check=False,
            module_path=None,
            remote_user=C.DEFAULT_REMOTE_USER,
            private_key_file=C.DEFAULT_PRIVATE_KEY_FILE,
            ssh_common_args='',
            sftp_extra_args='',
            scp_extra_args='',
            ssh_extra_args='',
            verbosity=0,
            listhosts=False,
            listtags=False,
            listtasks=False,
            syntax=False,
            inventory=None
        )

    def set_option(self, **kwargs):
        """ set Options
        usage:
            base_option = self._base_option()
            _option = base_option.copy()
            _option.upadte({'verbosity': 1, 'forks': 20})
            self.set_option(**_option)
        """

        self._set_option = True

        self.options = self._options(**kwargs)


    def _options(self, **kwargs):
        """ set options
        """
        keys = kwargs.keys()
        Options = namedtuple('Options', keys)
        v = Options(**kwargs)

        if v.inventory is not None:
            self.inventory_file = v.inventory

        return v


    def _prepare_run(self):
        # initialize needed objects

        # when not set_option
        if self._set_option is False:
            _base_option = self._base_option().copy()
            self.options = self._options(**_base_option)

        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager,
                                   host_list=self.inventory_file)

        self.variable_manager.set_inventory(self.inventory)


    def run(self, play_data):
        pass


class DoGoAdHocCLI(DoGoMinix):
    def __init__(self, *args, **kwargs):
        """ example:
        adh = DoGoAdHocCLI(inventory_file='/etc/ansible/hosts', verbosity=3, cb='cmdb')
        _base_options = adh._base_option()
        options = _base_options.copy()
        options.update({
            'inventory': '/etc/ansible/hosts',
            'forks': 10
        })
        adh.set_option(**options)

        play_data = dict(
            name="DoGo CMDB gather facts",
            hosts=['localhost'],
            gather_facts=True,
            tasks=[dict(action=dict(module='setup'))]
        )
        return adh.run(play_data)

        """

        super(DoGoAdHocCLI, self).__init__(*args, **kwargs)


    def run(self, play_data):
        """
        paly_data = dict(
            name="Ansible Ad-Hoc",
            hosts=pattern,
            gather_facts=True,
            tasks=[dict(action=dict(module='service', args={'name': 'vsftpd', 'state': 'restarted'}), async=async, poll=poll)]
        )
        """
        self._prepare_run()

        play = Play().load(play_data, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=self.cb,
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
            )

            result = tqm.run(play)
            return result
        finally:
            if tqm:
                tqm.cleanup()


class DoGoPlaybookCLI(DoGoMinix):
    def __init__(self, *args, **kwargs):
        """ example:
        pb = DoGoPlaybookCLI(inventory_file='/etc/ansible/hosts', verbosity=3)
        ~~~~~~~
        _base_options = pb._base_option()
        options = _base_options.copy()
        options.update({
            'inventory': '/etc/ansible/hosts',
            'forks': 10
        })
        pb.set_option(**options)
        ~~~~~~~

        kw = {'playbooks': ['/etc/ansible/test.yml', '/etc/ansible/test2.yml'], limit='localhost'}
        return pb.run(**kw)

        """

        super(DoGoPlaybookCLI, self).__init__(*args, **kwargs)


    def run(self, playbooks, limit=''):
        """
        param: `playbooks`: type string or list, example: ['/etc/ansible/test.yml'], '/etc/ansible/test1.yml, /etc/ansible/test2.yml'
        param: `limit`:  eq --limit ''
        """
        self._prepare_run()

        results = 0

        if isinstance(playbooks, basestring):
            if ',' in playbooks:
                playbooks = [pl.strip() for pl in playbooks.split(',') if os.path.exists(pl)]
            else:
                playbooks = [playbooks.strip()]

        # --limit
        if limit:
            self.inventory.subset(limit)

        try:
            # create the playbook executor, which manages running the plays via a task queue manager
            pbex = PlaybookExecutor(playbooks=playbooks, inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, options=self.options, passwords=self.passwords)

            results = pbex.run()
        except Exception, ex:
            results = str(ex)
        finally:
            return results

