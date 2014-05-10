from MapsRequestAPI import  *
from DBStuffAPI import *
from XlsxReader import *



class XlxsToMapsWrapper:
    LAT_LOG_FILE_NAME = '../akshaya-patra-data/lon and log details-xls.xlsx'
    def __init__(self):
        self.lat_lng_db = LngLatDB()
        pass

    def getLatLngData(self, file_name=LAT_LOG_FILE_NAME):
        self.rows = readXlsx(file_name, sheet=1, header=True)
        self.lat_lng_db.add_to_db(self.rows)

def main():
    xlxs_to_maps = XlxsToMapsWrapper()
    xlxs_to_maps.getLatLngData()
    return

if __name__ == '__main__':
    main()
