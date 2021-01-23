import easy_multiple_select

class TestIsMultipleSelect:

    def test_hyphen_in_a_row(self):
        assert easy_multiple_select.is_multiple_select("2-5-7", 8) is False

    def test_operator_wrong_place_1(self):
        assert easy_multiple_select.is_multiple_select("-,5-7", 8) is False

    def test_operator_wrong_place_2(self):
        assert easy_multiple_select.is_multiple_select("3,-,7", 8) is False

    def test_operator_wrong_place_3(self):
        assert easy_multiple_select.is_multiple_select("3,5-,", 8) is False

    def test_operator_wrong_place_4(self):
        assert easy_multiple_select.is_multiple_select("-,5-7", 8) is False

    def test_operand_wrong(self):
        assert easy_multiple_select.is_multiple_select("a,5-7", 8) is False

    def test_wrong_type(self):
        assert easy_multiple_select.is_multiple_select(["1", ",", "3"], 8) is False

    def test_comma_only(self):
        assert easy_multiple_select.is_multiple_select("1,2,5,7", 8) is True

    def test_two_ranges(self):
        assert easy_multiple_select.is_multiple_select("1-4,6-8", 9) is True

    def test_zero_1(self):
        assert easy_multiple_select.is_multiple_select("0-3", 5) is False

    def test_zero_2(self):
        assert easy_multiple_select.is_multiple_select("0,3,6", 7) is False

    def test_over_max(self):
        assert easy_multiple_select.is_multiple_select("3,5-7", 6) is False


class TestRunMultipleTest:

    def test_comma_only(self):
        assert easy_multiple_select.run_multiple_select("1,2,5,7") == (1, 2, 5, 7)

    def test_two_ranges(self):
        assert easy_multiple_select.run_multiple_select("1-4,6-8") == (1, 2, 3, 4, 6, 7, 8)

    def test_single_comma(self):
        assert easy_multiple_select.run_multiple_select("1-4") == (1, 2, 3, 4)

    def test_single_hyphen(self):
        assert easy_multiple_select.run_multiple_select("1,4") == (1,4)