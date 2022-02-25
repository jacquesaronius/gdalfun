import unittest
import sys
sys.path.append("..")
from gis_dal import GISDAL
from zip import ZipFactory, Zip

class TestQueryExistingTrails(unittest.TestCase):
    
    def test_basic_query(self):

        zip: Zip = ZipFactory.create("../EXISTING_TRAILS.zip")
        ext_path = zip.extract()
        dal = GISDAL(f"{ext_path}/EXISTING_TRAILS.gdb", GISDAL.OPENFILEGDB)
        results = dal.execute_query_as_list("SELECT NAME FROM EXISTING_TRAILS")
        for i in results:
            print(f"{i[0]}")
        self.assertEqual(len(results), 4247)
    
    def test_basic_query_as_dictionary(self):

        zip: Zip = ZipFactory.create("../EXISTING_TRAILS.zip")
        ext_path = zip.extract()
        dal = GISDAL(f"{ext_path}/EXISTING_TRAILS.gdb", GISDAL.OPENFILEGDB)
        results = dal.execute_query_as_dictionary("SELECT NAME FROM EXISTING_TRAILS")
        for i in results:
            print(f"{i}")
        self.assertEqual(len(results), 4247)

    def test_basic_query_all_fields_as_dictionary(self):

        zip: Zip = ZipFactory.create("../EXISTING_TRAILS.zip")
        ext_path = zip.extract()
        dal = GISDAL(f"{ext_path}/EXISTING_TRAILS.gdb", GISDAL.OPENFILEGDB)
        results = dal.execute_query_as_dictionary("SELECT OBJECTID, * FROM EXISTING_TRAILS")
        for i in results:
            print(f"{i}")
        self.assertEqual(len(results), 4247)

    def test_test_geometry_count(self):
        zip: Zip = ZipFactory.create("../EXISTING_TRAILS.zip")
        ext_path = zip.extract()
        dal = GISDAL(f"{ext_path}/EXISTING_TRAILS.gdb", GISDAL.OPENFILEGDB)
        results = dal.query_geometry("EXISTING_TRAILS")
        for i in results.keys():
            print(f"{i} => {results[i]}")
        self.assertEqual(len(results), 4247)

if __name__ == "__main__":
    unittest.main()


        
