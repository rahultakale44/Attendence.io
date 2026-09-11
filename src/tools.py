"""
Attendance eligibility tools for LangChain agent.
"""

import math
from langchain_core.tools import tool


@tool
def check_attendance_eligibility(attended: int, total: int) -> str:
    """
    Check if a student meets the minimum attendance requirement of 75%.
    
    Args:
        attended: Number of classes attended
        total: Total number of classes held
        
    Returns:
        String indicating eligibility status with percentage
    """
    # Validate inputs
    if total <= 0:
        return "ERROR: Total classes must be greater than 0."
    
    if attended < 0:
        return "ERROR: Attended classes cannot be negative."
    
    if attended > total:
        return "ERROR: Attended classes cannot exceed total classes."
    
    # Calculate attendance percentage
    attendance_percentage = (attended / total) * 100
    
    # Check eligibility (75% minimum)
    if attendance_percentage >= 75.0:
        return f"ELIGIBLE: {attendance_percentage:.1f}% attendance (meets 75% requirement)."
    else:
        return f"NOT ELIGIBLE: {attendance_percentage:.1f}% attendance (below 75%)."


@tool
def classes_needed_for_eligibility(
    attended: int,
    total_so_far: int,
    remaining_classes: int
) -> str:
    """
    Calculate how many additional classes must be attended to reach 75% eligibility.
    
    Args:
        attended: Number of classes attended so far
        total_so_far: Total number of classes held so far
        remaining_classes: Number of classes remaining in the semester
        
    Returns:
        String explaining how many classes need to be attended
    """
    # Validate inputs
    if total_so_far <= 0:
        return "ERROR: Total classes so far must be greater than 0."
    
    if attended < 0:
        return "ERROR: Attended classes cannot be negative."
    
    if attended > total_so_far:
        return "ERROR: Attended classes cannot exceed total classes so far."
    
    if remaining_classes < 0:
        return "ERROR: Remaining classes cannot be negative."
    
    # Calculate final total
    final_total = total_so_far + remaining_classes
    
    # Calculate minimum classes needed for 75%
    min_classes_needed = math.ceil(final_total * 0.75)
    
    # Calculate additional classes required
    additional_needed = min_classes_needed - attended
    
    # Check current status
    current_percentage = (attended / total_so_far) * 100
    
    # Calculate what final percentage would be if attended all remaining
    final_if_all_attended = attended + remaining_classes
    final_percentage_if_all = (final_if_all_attended / final_total) * 100
    
    # Handle different cases
    if attended >= min_classes_needed:
        return (f"ALREADY ELIGIBLE: You have attended {attended} classes. "
                f"Current attendance: {current_percentage:.1f}%. "
                f"You already meet the 75% requirement.")
    
    if additional_needed > remaining_classes:
        final_possible = attended + remaining_classes
        final_percentage = (final_possible / final_total) * 100
        return (f"IMPOSSIBLE: Even if you attend all {remaining_classes} remaining classes, "
                f"you will only have {final_possible}/{final_total} = {final_percentage:.1f}% attendance. "
                f"You need {min_classes_needed} total classes but can only reach {final_possible}.")
    
    # Normal case - eligibility is achievable
    classes_can_miss = remaining_classes - additional_needed
    final_attendance = min_classes_needed
    final_percentage = (final_attendance / final_total) * 100
    
    return (f"CLASSES NEEDED: You must attend at least {additional_needed} more classes out of "
            f"{remaining_classes} remaining. "
            f"This means you can miss at most {classes_can_miss} classes. "
            f"Final attendance would be {final_attendance}/{final_total} = {final_percentage:.1f}%.")
