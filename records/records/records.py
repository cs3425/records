
# fill in the params dictionary, write functions to update it
# with the entered arguments to __init__, write functions
# to get_all_records and store results as a dataframe.
# have all functions run during init so that the initialized
# object calls the request and returns a full dataframe.

import requests
import pandas as pd


class Records:
    def __init__(self, q=None, interval=None):

        self.q = q
        self.interval = interval
        self.form_interval = ','.join(str(i) for i in self.interval)  # format interval input as "str,str"
        self.params = {
            "q": self.q,
            "year": self.form_interval,
            "basisOfRecord": "PRESERVED_SPECIMEN",
            "hasCoordinate": "true",
            "hasGeospatialIssue": "false",
            "country": "US",
            "offset": "0",
            "limit": "300"
        }
        self.df = self._get_all_records()  # stores the return var

    def _get_all_records(self):
        "iterate until end of records"
        start = 0
        data = []  # append all the data to this empty list (fill as we go)

        baseurl = "http://api.gbif.org/v1/occurrence/search?"

        while 1:
            # make request and store results
            res = requests.get(
                url=baseurl,
                params=self.params,  # params dict gets updated every iteration by code below
            )
            # increment counter
            self.params["offset"] = str(int(self.params["offset"]) + 300)

            # concatenate data
            idata = res.json()
            data += idata["results"]

            # stop when end of record is reached
            if idata["endOfRecords"]:  # attribute of data, when true we exit
                break

        return pd.DataFrame(data)
