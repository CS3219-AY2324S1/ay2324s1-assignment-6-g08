import utility


# Input tests
class TestInputs:
    def test_single_string(self):
        str = "s = abcde"
        assert utility.parse_input(str) == {"s": "abcde"}

    def test_single_integer(self):
        str = "n = 15"
        assert utility.parse_input(str) == {"n": 15}

    def test_single_float(self):
        str = "n = 15.0"
        assert utility.parse_input(str) == {"n": 15.0}

    def test_single_array(self):
        str = "nums = [1, 2, 3, 4]"
        assert utility.parse_input(str) == {"nums": [1, 2, 3, 4]}

    def test_nested_arrays(self):
        str = "nums = [[1, 2, 3], [4, 5, 6]]"
        assert utility.parse_input(str) == {"nums": [[1, 2, 3], [4, 5, 6]]}

    def test_nested_arrays_null(self):
        str = "nums = [[1, 2, 3], [4, 5, null]]"
        assert utility.parse_input(str) == {"nums": [[1, 2, 3], [4, 5, None]]}

    def test_multiple_variables_single_type(self):
        str = "n = 5, m = 6"
        assert utility.parse_input(str) == {"n": 5, "m": 6}

    def test_multiple_variables_multiple_types(self):
        str = "n = 5, nums = [1, 2, 3, 4]"
        assert utility.parse_input(str) == {"n": 5, "nums": [1, 2, 3, 4]}

    def test_multiple_variables_arrays(self):
        str = "n = [1, 2, 3], m = [4, 5, 6]"
        assert utility.parse_input(str) == {"n": [1, 2, 3], "m": [4, 5, 6]}


# Output Tests
class TestOutputs:
    def test_single_string(self):
        str = "abcde"
        assert utility.parse_output(str) == "abcde"

    def test_single_float(self):
        str = "15.0"
        assert utility.parse_output(str) == 15.0

    def test_single_integer(self):
        str = "15"
        assert utility.parse_output(str) == 15

    def test_array(self):
        str = "[1, 2, 3]"
        assert utility.parse_output(str) == [1, 2, 3]

    def test_nested_array(self):
        str = "[[1, 2], [2, 3]]"
        assert utility.parse_output(str) == [[1, 2], [2, 3]]

    def test_nested_array_null(self):
        str = "[[1, null], [2, 3]]"
        assert utility.parse_output(str) == [[1, None], [2, 3]]
