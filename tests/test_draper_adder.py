# -*- coding: utf-8 -*-
# All rights reserved-2022©.
import pytest

from src.draper_adder.draper_adder import draper_adder
from src.draper_adder.main import subset_finder


class TestDraper:
    def test_draper_adder_negative_error(self):
        """Test that draper_adder raises an error when given a negative number"""
        with pytest.raises(ValueError):
            draper_adder(-3, 5)

    def test_draper_adder_single_element(self):
        """Test that draper_adder returns the correct binary string for a single element"""
        assert draper_adder(1, 0) == "1"

    def test_draper_adder_two_elements(self):
        """Test that draper_adder returns the correct binary string for two elements"""
        assert draper_adder(5, 5) == "1010"

    def test_draper_adder_large_elements(self):
        """Test that draper_adder returns the correct binary string for large elements"""
        assert draper_adder(50, 5) == "110111"

    def test_draper_adder_zeros(self):
        """Test that draper_adder returns the correct binary string for zeros"""
        assert draper_adder(0, 0) == "0"


class TestSum:
    def test_qosf_problem(self):
        """Test that the QOSF problem is solved correctly"""
        assert subset_finder()[0][1] == ("1001", "111")

    def test_generalized_draoer(self):
        """Test that the generalized draper adder is solved correctly"""
        assert subset_finder(int_list=[1, 2, 4, 6], output=6)[0][1] == ('100', '10')
