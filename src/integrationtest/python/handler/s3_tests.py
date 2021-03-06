from __future__ import print_function, absolute_import, division

import unittest2

from s3_tests_base import S3TestsBase


class S3Tests(S3TestsBase):
    def test_search_unwanted_resources_dry_run(self):
        self._create_bucket('test-bucket1', 'eu-west-1')
        self.s3_handler.dry_run = True

        resources = self.s3_handler.fetch_unwanted_resources()
        uniq_resources = self._uniq(resources)
        self.assertEqual(len(uniq_resources), 1)

        self.s3_handler.delete(uniq_resources[0])

        resources = self.s3_handler.fetch_unwanted_resources()
        uniq_resources = self._uniq(resources)
        self.assertEqual(len(uniq_resources), 1)

    def test_search_unwanted_resources_dry_run_with_key(self):
        self._create_bucket('test-bucket2', 'eu-west-1', create_key=True)
        self.s3_handler.dry_run = True

        resources = self.s3_handler.fetch_unwanted_resources()
        uniq_resources = self._uniq(resources)
        self.assertEqual(len(uniq_resources), 1)
        conn = self.s3_handler.connect_to_region(uniq_resources[0].region,
                                                 uniq_resources[0].wrapped.name)
        bucket = conn.get_bucket(uniq_resources[0].wrapped.name)
        all_keys = bucket.get_all_keys()
        self.assertEqual(len(all_keys), 1)

        self.s3_handler.delete(uniq_resources[0])

        resources = self.s3_handler.fetch_unwanted_resources()
        uniq_resources = self._uniq(resources)
        self.assertEqual(len(uniq_resources), 1)

    def test_search_unwanted_resources_dry_run_sigv4(self):
        self._create_bucket('test-bucket4', 'eu-central-1')
        self.s3_handler.dry_run = True

        resources = self.s3_handler.fetch_unwanted_resources()
        uniq_resources = self._uniq(resources)
        self.assertEqual(len(uniq_resources), 1)

        self.s3_handler.delete(uniq_resources[0])

        resources = self.s3_handler.fetch_unwanted_resources()
        uniq_resources = self._uniq(resources)
        self.assertEqual(len(uniq_resources), 1)

    def test_search_unwanted_resources_dry_run_sigv4_with_key(self):
        self._create_bucket('test-bucket4', 'eu-central-1', create_key=True)
        self.s3_handler.dry_run = True

        resources = self.s3_handler.fetch_unwanted_resources()
        uniq_resources = self._uniq(resources)
        self.assertEqual(len(uniq_resources), 1)
        conn = self.s3_handler.connect_to_region(uniq_resources[0].region,
                                                 uniq_resources[0].wrapped.name)
        bucket = conn.get_bucket(uniq_resources[0].wrapped.name)
        all_keys = bucket.get_all_keys()
        self.assertEqual(len(all_keys), 1)

        self.s3_handler.delete(uniq_resources[0])

        resources = self.s3_handler.fetch_unwanted_resources()
        uniq_resources = self._uniq(resources)
        self.assertEqual(len(uniq_resources), 1)

    def test_search_unwanted_resources_no_dry_run(self):
        self.s3_handler.dry_run = False
        self._create_bucket('test-bucket8', 'eu-west-1', create_key=False)

        resources = self.s3_handler.fetch_unwanted_resources()
        uniq_resources = self._uniq(resources)
        self.assertEqual(len(uniq_resources), 1)

        self.s3_handler.delete(uniq_resources[0])

        resources = self.s3_handler.fetch_unwanted_resources()
        uniq_resources = self._uniq(resources)
        self.assertEqual(len(uniq_resources), 0)

        # Prevent self.tearDown() from failing with "404 Not Found".
        self.our_buckets = []

    def test_search_unwanted_resources_no_dry_run_with_key(self):
        self.s3_handler.dry_run = False
        self._create_bucket('test-bucket9', 'eu-west-1', create_key=True)

        resources = self.s3_handler.fetch_unwanted_resources()
        uniq_resources = self._uniq(resources)
        self.assertEqual(len(uniq_resources), 1)
        conn = self.s3_handler.connect_to_region(uniq_resources[0].region,
                                                 uniq_resources[0].wrapped.name)
        bucket = conn.get_bucket(uniq_resources[0].wrapped.name)
        all_keys = bucket.get_all_keys()
        self.assertEqual(len(all_keys), 1)

        self.s3_handler.delete(uniq_resources[0])

        resources = self.s3_handler.fetch_unwanted_resources()
        uniq_resources = self._uniq(resources)
        self.assertEqual(len(uniq_resources), 0)

        # Prevent self.tearDown() from failing with "404 Not Found".
        self.our_buckets = []


if __name__ == "__main__":
    unittest2.main()
