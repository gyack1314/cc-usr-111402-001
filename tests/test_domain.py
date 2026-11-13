"""资料与现有领域接口的核对。"""
import unittest,tempfile,json
from pathlib import Path
from lake.storage import Storage
from lake.federation import inspect

class DomainTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.store=Storage(self.root/'objects')
        self.data=json.loads(Path('data/source.json').read_text(encoding='utf-8'))
    def test_existing_reader(self):
        self.assertTrue(inspect(self.data,self.store,self.root))

    def test_source_version_and_null(self):
        from lake.sources import Source
        d=self.data['sources']['air'];s=Source('air',d['release'],d['rows'],d['capabilities']);h=s.open('a7')
        self.assertFalse(s.page(h['token'],0,1)['complete']);self.assertTrue(s.page(h['token'],1,1)['complete'])
        with self.assertRaises(ValueError):s.open('a8')
        s.invalid=True
        with self.assertRaises(ValueError):s.page(h['token'],0,1)
