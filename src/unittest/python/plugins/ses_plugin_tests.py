from __future__ import print_function, absolute_import, division
import os
from unittest import TestCase
from moto import mock_ses
import boto

from monocyte.plugins.ses_plugin import AwsSesPlugin

os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['no_proxy'] = ''


class AwsSesPluginTest(TestCase):
    def setUp(self):
        self.unwanted_resources = "42"
        self.problematic_resources = "23"
        self.dry_run = True
        self.region = "eu-west-1"
        self.sender = "test@test.invalid"
        self.subject = "AWS Monocyte"
        self.recipients = ["test@test.invalid"]
        self.body = "myEmailBody"
        self.aws_ses_plugin = AwsSesPlugin(self.unwanted_resources,
                                           self.problematic_resources,
                                           self.dry_run, self.region,
                                           self.sender,
                                           self.subject, self.recipients,
                                           self.body)

    def test_ses_plugin_properties(self):
        self.assertEqual(self.aws_ses_plugin.sender, self.sender)
        self.assertEqual(self.aws_ses_plugin.recipients, self.recipients)
        self.assertEqual(self.aws_ses_plugin.body, self.body)

    @mock_ses
    def test_send_mail_ok(self):
        conn = boto.connect_ses('the_key', 'the_secret')
        conn.verify_email_identity(self.sender)

        self.aws_ses_plugin.send_email()

        send_quota = conn.get_send_quota()
        sent_count = int(
            send_quota['GetSendQuotaResponse']['GetSendQuotaResult'][
                'SentLast24Hours'])
        self.assertEqual(sent_count, 1)

    @mock_ses
    def test_send_mail_failure_non_verfied_email(self):
        non_verified_sender = 'non_verified_sender@test.invalid'
        aws_ses_plugin = AwsSesPlugin(self.unwanted_resources,
                                      self.problematic_resources,
                                      self.dry_run, self.region,
                                      non_verified_sender, self.subject,
                                      self.recipients, self.body)
        self.assertRaises(boto.exception.BotoServerError,
                          aws_ses_plugin.send_email)

    @mock_ses
    def test_send_mail_failure_no_sender(self):
        aws_ses_plugin = AwsSesPlugin(self.unwanted_resources,
                                      self.problematic_resources,
                                      self.dry_run, self.region,
                                      "sender@test.invalid", self.subject,
                                      self.recipients, self.body)
        self.assertRaises(boto.exception.BotoServerError,
                          aws_ses_plugin.send_email)
