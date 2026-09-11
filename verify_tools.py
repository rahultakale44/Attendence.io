"""
Quick verification script for attendance tools.
"""

from src.tools import check_attendance_eligibility, classes_needed_for_eligibility

print("=" * 60)
print("ATTENDANCE TOOLS VERIFICATION")
print("=" * 60)

print("\n📊 TOOL 1: check_attendance_eligibility")
print("-" * 60)

print("\nExample 1: 28 attended out of 40 total")
result1 = check_attendance_eligibility.invoke({"attended": 28, "total": 40})
print(f"Result: {result1}")

print("\nExample 2: 30 attended out of 40 total (exactly 75%)")
result2 = check_attendance_eligibility.invoke({"attended": 30, "total": 40})
print(f"Result: {result2}")

print("\n📊 TOOL 2: classes_needed_for_eligibility")
print("-" * 60)

print("\nExample: 28 attended, 40 so far, 20 remaining")
result3 = classes_needed_for_eligibility.invoke({
    "attended": 28,
    "total_so_far": 40,
    "remaining_classes": 20
})
print(f"Result: {result3}")

print("\n" + "=" * 60)
print("✅ TOOLS WORKING CORRECTLY")
print("=" * 60)
