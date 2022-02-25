from osgeo import ogr
from abc import ABCMeta, abstractmethod
from typing import List

class IGISDAL:

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_query_as_list(query_str) -> List[List]:
        raise NotImplementedError

    @abstractmethod
    def query_geometry(self, layer_name) -> dict[int, ogr.Geometry]:
        raise NotImplementedError

    @abstractmethod
    def execute_query_as_dictionary(self, query_str: str) -> List[dict]:
        raise NotImplementedError
    
class GISDAL(IGISDAL):

    OPENFILEGDB = "OpenFileGDB"
    FILEGDB = "FileGDB"
    SHAPEFILE = "ESRI Shapefile"
    GEOJSON = "GeoJSON"
    SQLITE = "SQLite"
    READONLY = 0
    READWRITE = 1
    
    def __init__(self, gdb_path: str, driver: str = OPENFILEGDB, mode: int = READONLY) -> None:
        self.gdb_path = gdb_path
        self.driver = ogr.GetDriverByName(driver)
        if self.driver is None:
            raise ValueError("Specified driver is not compiled into GDAL")
        if mode != GISDAL.READONLY and mode != GISDAL.READWRITE:
            raise ValueError("Mode must be 0 or 1")
        self.ds: ogr.DataSource = self.driver.Open(self.gdb_path, mode)

    def _execute_query(self, query_str, result_func):
        layer = self.ds.ExecuteSQL(query_str)
        result_func(layer)
        self.ds.ReleaseResultSet(layer)


    def execute_query_as_list(self, query_str: str) -> List[List]:
        results = []
        def query_to_array(layer):
            i = True
            while i:
                feature = layer.GetNextFeature()
                if feature is not None:
                    result = []
                    cnt = 0
                    j = True
                    while j:
                        value = feature.GetField(cnt)
                        if value is not None:
                            result.append(value)
                            cnt = cnt + 1
                        else:
                            j = False
                    results.append(result)
                else:
                    i = False
        self._execute_query(query_str, query_to_array)
        return results

    def execute_query_as_dictionary(self, query_str: str) -> List[List]:
        results = []
        def query_to_dictionary(layer: ogr.Layer):
            layer_def: ogr.FeatureDefn = layer.GetLayerDefn()
            schema: List[str] = []
            for i in range(layer_def.GetFieldCount()):
                field_def: ogr.FieldDefn = layer_def.GetFieldDefn(i)
                schema.append(field_def.GetName())
            i = True
            while i:
                feature: ogr.Feature = layer.GetNextFeature()
                if feature is not None:
                    result = {}
                    for j in schema:
                        value = feature.GetField(feature.GetFieldIndex(j))
                        result[j] = value
                    results.append(result)
                else:
                    i = False
        self._execute_query(query_str, query_to_dictionary)
        return results

    def query_geometry(self, layer_name) -> dict[int, ogr.Geometry]:
        results: dict[int, ogr.Geometry] = {}
        layer: ogr.Layer = self.ds.GetLayerByName(layer_name)
        sentinel = True
        while sentinel:
            feature: ogr.Feature = layer.GetNextFeature()
            if feature is not None:
                geometry: ogr.Geometry = feature.GetGeometryRef()
                cloned_geometry: ogr.Geometry = geometry.Clone()
                obj_id = feature.GetFID()
                results[obj_id] = cloned_geometry
            else:
                sentinel = False
        return results


