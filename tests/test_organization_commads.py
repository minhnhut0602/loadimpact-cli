"""
Copyright 2015 Load Impact

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest
from collections import namedtuple

from click.testing import CliRunner
from unittest.mock import MagicMock
from loadimpactcli import organization_commands


class TestOrganizations(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        Organization = namedtuple('Organization', ['id', 'name'])
        self.org1 = Organization('1', 'org1')
        self.org2 = Organization('2', 'org2')
        Project = namedtuple('Project', ['id', 'name'])
        self.proj1 = Project('1', 'proj1')
        self.proj2 = Project('2', 'proj2')

    def test_list_organizations(self):
        client = organization_commands.client
        client.list_organizations = MagicMock(return_value=[self.org1, self.org2])
        result = self.runner.invoke(organization_commands.list_organizations, [])

        assert result.exit_code == 0
        assert result.output == '1\torg1\n2\torg2\n'

    def test_list_projects(self):
        client = organization_commands.client
        client.list_organization_projects = MagicMock(return_value=[self.proj1, self.proj2])
        result = self.runner.invoke(organization_commands.list_organization_projects, ['1'])

        assert result.exit_code == 0
        assert result.output == '1\tproj1\n2\tproj2\n'

    def test_list_projects_without_org_id(self):
        runner = CliRunner()
        result = runner.invoke(organization_commands.list_organization_projects, [])

        assert result.exit_code == 2
