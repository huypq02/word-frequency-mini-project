import unittest
import os
import src.pipeline.text_stats as ts

class TestTextStats(unittest.TestCase):
    def setUp(self):
        self.filename = "filename.txt"
        self.rootpath = "data"
        with open(os.path.join(self.rootpath, self.filename), "w", encoding="utf-8") as f:
            f.write("Xin chào! Đây là ví dụ về dự án nhỏ. Xin chào mọi người.")
    
    def test_import_data(self):
        data = ts.import_data(self.filename, self.rootpath)
        self.assertIsInstance(data, str)
