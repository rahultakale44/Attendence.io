"""
Tests for attendance eligibility tools.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools import check_attendance_eligibility, classes_needed_for_eligibility


def test_check_attendance_eligible():
    """Test attendance check for eligible student."""
    result = check_attendance_eligibility.invoke({"attended": 30, "total": 40})
    assert "ELIGIBLE" in result
    assert "75.0%" in result
    print("✅ Test passed: Eligible student (30/40 = 75%)")


def test_check_attendance_not_eligible():
    """Test attendance check for non-eligible student."""
    result = check_attendance_eligibility.invoke({"attended": 28, "total": 40})
    assert "NOT ELIGIBLE" in result
    assert "70.0%" in result
    print("✅ Test passed: Not eligible student (28/40 = 70%)")


def test_check_attendance_highly_eligible():
    """Test attendance check for highly eligible student."""
    result = check_attendance_eligibility.invoke({"attended": 36, "total": 40})
    assert "ELIGIBLE" in result
    assert "90.0%" in result
    print("✅ Test passed: Highly eligible student (36/40 = 90%)")


def test_check_attendance_invalid_total_zero():
    """Test attendance check with invalid total = 0."""
    result = check_attendance_eligibility.invoke({"attended": 10, "total": 0})
    assert "ERROR" in result
    assert "greater than 0" in result
    print("✅ Test passed: Invalid input (total = 0)")


def test_check_attendance_negative_attended():
    """Test attendance check with negative attended value."""
    result = check_attendance_eligibility.invoke({"attended": -5, "total": 40})
    assert "ERROR" in result
    assert "negative" in result
    print("✅ Test passed: Invalid input (negative attended)")


def test_check_attendance_attended_exceeds_total():
    """Test attendance check where attended > total."""
    result = check_attendance_eligibility.invoke({"attended": 50, "total": 40})
    assert "ERROR" in result
    assert "exceed" in result
    print("✅ Test passed: Invalid input (attended > total)")


def test_classes_needed_achievable():
    """Test calculation when eligibility is achievable."""
    result = classes_needed_for_eligibility.invoke({
        "attended": 28,
        "total_so_far": 40,
        "remaining_classes": 20
    })
    assert "CLASSES NEEDED" in result
    assert "17 more classes" in result
    print("✅ Test passed: Achievable eligibility (28/40, 20 remaining)")


def test_classes_needed_impossible():
    """Test calculation when eligibility is impossible."""
    result = classes_needed_for_eligibility.invoke({
        "attended": 20,
        "total_so_far": 40,
        "remaining_classes": 10
    })
    assert "IMPOSSIBLE" in result
    print("✅ Test passed: Impossible eligibility (20/40, 10 remaining)")


def test_classes_needed_already_eligible():
    """Test calculation when already eligible."""
    result = classes_needed_for_eligibility.invoke({
        "attended": 45,
        "total_so_far": 50,
        "remaining_classes": 10
    })
    assert "ALREADY ELIGIBLE" in result
    print("✅ Test passed: Already eligible (45/50 = 90%)")


def test_classes_needed_invalid_inputs():
    """Test calculation with invalid inputs."""
    result = classes_needed_for_eligibility.invoke({
        "attended": 50,
        "total_so_far": 40,
        "remaining_classes": 10
    })
    assert "ERROR" in result
    print("✅ Test passed: Invalid input (attended > total_so_far)")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("RUNNING ATTENDANCE TOOLS TESTS")
    print("=" * 60 + "\n")
    
    print("--- Testing check_attendance_eligibility ---")
    test_check_attendance_eligible()
    test_check_attendance_not_eligible()
    test_check_attendance_highly_eligible()
    test_check_attendance_invalid_total_zero()
    test_check_attendance_negative_attended()
    test_check_attendance_attended_exceeds_total()
    
    print("\n--- Testing classes_needed_for_eligibility ---")
    test_classes_needed_achievable()
    test_classes_needed_impossible()
    test_classes_needed_already_eligible()
    test_classes_needed_invalid_inputs()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✅")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_tests()
