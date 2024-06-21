
import csv

from collections import OrderedDict, defaultdict

class Slcsp:
    """
        Class that uses data found in the plans and zips CSV files to determine the second
        lowest cost silver plan (SLCSP) of a group of zip codes found in a slscp CSV file.
    """
    def __init__(self, plans_csv_file: str, zips_csv_file: str) -> None:
        self.zips_csv_file = zips_csv_file  
        self.plans_csv_file = plans_csv_file
        # self.silver_plans_rates_by_zip_code = defaultdict(dict)
        self.slscp_data = OrderedDict()
                    
    
    def set_slscp_data(self, slcsp_csv_file) -> None:
        """
            Finds the associated rate for the zip codes found in the slcsp_csv_file using the
            data found in plans_csv_file and zips_csv_file. When determining the rate for zip
            codes, keep the order of the entries.

            Logic:

        """
        rate_areas_by_zip_code = self._parse_zips_csv_file()
        silver_plan_rates_by_rate_area = self._parse_plans_csv_file()

        with open(slcsp_csv_file) as slcsp_csv:
            slcsp_csv_reader = csv.reader(slcsp_csv)
            self.slcsp_csv_file = slcsp_csv_file

            # Skip the header row
            # Make sure to check for the header instead
            next(slcsp_csv_reader, None)

            for row in slcsp_csv_reader:
                zip_code = row[0]
                slcsp_rate = None
                
                rate_areas = rate_areas_by_zip_code[zip_code]

                if rate_areas:
                    if len(rate_areas) == 1:
                        rate_area = next(iter(rate_areas))
                        rate_area_silver_plan_rates = silver_plan_rates_by_rate_area[rate_area]

                        if rate_area_silver_plan_rates:
                            # Can potentially sort in _parse_plans_csv_file instead
                            sorted_rate_area_silver_plan_rates = sorted(list(rate_area_silver_plan_rates))

                            # Can't find SLCSP if there is only one available rate
                            if len(sorted_rate_area_silver_plan_rates) > 1:
                                slcsp_rate = sorted_rate_area_silver_plan_rates[1]

                    # This part below could potentially be logging messages
                    #        else:
                    #            print("This only had one rate")
                        # else:
                        #    print("This rate area does not have any rates!!")
                    # else:
                    #     print("Can't determine SLSCP due to zip code containing two rate areas")

                self.slscp_data[zip_code] = slcsp_rate

    
    def print_slscp_data(self) -> None:
        """
            Prints the zip code with the corresponding SLSCP. If no SLSCP can be determined,
            the rates value will be empty.
        """
        print("zipcode,rate")
        
        for zip_code, slcsp_rate in self.slscp_data.items():
            if slcsp_rate is None:
                slcsp_rate = ""
            else:
                slcsp_rate = '{:.2f}'.format(slcsp_rate)

            print(f"{zip_code},{slcsp_rate}")


    def _parse_zips_csv_file(self) -> defaultdict:
        """
            Parses zips_csv_file to find the rate areas of zip codes.

            It is exepcted for zips_csv_file to have the following columns:
                zipcode, state, county_code, name, rate_area
        """
        rate_areas_by_zip_code = defaultdict(set)

        with open(self.zips_csv_file) as zips_csv:
            zips_csv_file_reader = csv.reader(zips_csv)

            # Skip the header row
            # Make sure to check for the header instead
            next(zips_csv_file_reader, None)

            for row in zips_csv_file_reader:
                zipcode = row[0]
                state = row[1]
                rate_area_number = row[4]
                rate_area = (state, rate_area_number)
                rate_areas_by_zip_code[zipcode].add(rate_area)

        return rate_areas_by_zip_code


    def _parse_plans_csv_file(self) -> defaultdict:
        """
            Parses plans_csv_file to find the rates of rate_areas.

            It is exepcted for plans_csv_file to have the following columns:
                plan_id, state, meta_level, rate, rate_area 
        """
        silver_plan_rates_by_rate_area = defaultdict(set)

        with open(self.plans_csv_file) as plans_csv:
            plans_csv_file_reader = csv.reader(plans_csv)

            # Skip the header row
            # Make sure to check for the header instead
            next(plans_csv_file_reader, None)

            for row in plans_csv_file_reader:
                state = row[1]
                metal_level = row[2]
                rate = row[3]
                rate_area_number = row[4]
                rate_area = (state, rate_area_number)

                # Ensuring we find the silver plan in case of a capitlization error 
                if metal_level.lower() == "silver":
                    silver_plan_rates_by_rate_area[rate_area].add(float(rate))

        return silver_plan_rates_by_rate_area
    

if __name__ == "__main__":
    slcsp = Slcsp('./data/plans.csv', './data/zips.csv')
    slcsp.set_slscp_data('./data/slcsp.csv')
    slcsp.print_slscp_data()
