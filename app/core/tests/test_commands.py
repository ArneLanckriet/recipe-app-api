"""
Test custom Django manage commands
"""
from unittest import mock

from django.core.management import call_command
from django.db import OperationalError
from django.test import SimpleTestCase
from psycopg2 import OperationalError as Psycopg2OpError


@mock.patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """ Test commands."""

    def test_wait_for_db_ready(self, p_check):
        """Test waiting for database if database ready."""
        p_check.return_value = True

        call_command("wait_for_db")

        p_check.assert_called_once_with(databases=["default"])

    @mock.patch("time.sleep")
    def test_wait_for_db_delay(self, p_sleep, p_check):
        """Test waiting for db when getting OperationalError"""
        p_check.side_effect = [Psycopg2OpError] * 2 + \
                              [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        self.assertEqual(p_check.call_count, 6)
        p_check.assert_called_with(databases=["default"])
