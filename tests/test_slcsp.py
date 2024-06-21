import pytest

from collections import defaultdict
from slcsp.slcsp import Slcsp

@pytest.fixture
def mocker_zip_csv_data(mocker):
    # Read a mocked /etc/release file
    sample_zip_csv_data = """
        zipcode,state,county_code,name,rate_area\n
        36749,AL,01001,Autauga,11\n
        36703,AL,01001,Autauga,11\n
        36003,AL,01001,Autauga,11\n
    """
    mocked_etc_release_data = mocker.mock_open(read_data=sample_zip_csv_data)
    mocker.patch("builtins.open", mocked_etc_release_data)

class TestSlcsp:
    def test_parse_zips_csv_file(mocker_zip_csv_data):
        test_data_dict = {
            "36749": set([('AL', '11')]),
            "36003": set([('AL', '11')]),
            "86507": set([('AZ', '1')]),
            "85671": set([('AZ', '7')]),
            "86336": set([('AZ', '1')]),
        }

        test_rate_areas_by_zip_code = defaultdict(set, test_data_dict)
        slcsp = Slcsp('./tests/data/plans.csv', './tests/data/zips.csv')

        rate_areas_by_zip_code = slcsp._parse_zips_csv_file()
        print(test_rate_areas_by_zip_code)
        print(rate_areas_by_zip_code)

        assert test_rate_areas_by_zip_code == rate_areas_by_zip_code