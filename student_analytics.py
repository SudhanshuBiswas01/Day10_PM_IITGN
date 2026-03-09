# student_analytics.py
# Part A - Student Performance Analytics Module
# IIT Gandhinagar - PGD Assignment

from collections import defaultdict
from typing import Optional


def create_student(name: str, roll: str, **marks) -> dict:
    """Create a student record with name, roll number and subject marks.

    Args:
        name: Full name of the student.
        roll: Roll number (e.g., 'R001').
        **marks: Subject marks as keyword arguments (e.g., math=85, python=92).

    Returns:
        A dict with keys: 'name', 'roll', 'marks', 'attendance'.
        Attendance defaults to 100.0 if not provided.

    Raises:
        ValueError: If name or roll is empty, or if any mark is out of 0-100.

    Examples:
        >>> s = create_student('Amit', 'R001', math=85, python=92, ml=78)
        >>> s['name']
        'Amit'
    """
    if not name or not name.strip():
        raise ValueError("Student name cannot be empty.")
    if not roll or not roll.strip():
        raise ValueError("Roll number cannot be empty.")

    # pull attendance out of marks if passed, default 100.0
    attendance = float(marks.pop('attendance', 100.0))

    # validate marks are in 0-100 range
    for subject, score in marks.items():
        if not (0 <= score <= 100):
            raise ValueError(f"Mark for {subject} must be between 0 and 100.")

    return {
        'name': name.strip(),
        'roll': roll.strip(),
        'marks': dict(marks),
        'attendance': attendance
    }


def calculate_gpa(*marks: float, scale: float = 10.0) -> float:
    """Calculate GPA from any number of marks on a given scale.

    Args:
        *marks: Variable number of marks (floats).
        scale: The GPA scale to convert to. Defaults to 10.0.

    Returns:
        GPA as a float rounded to 2 decimal places.
        Returns 0.0 if no marks are provided.

    Raises:
        ValueError: If scale is zero or negative.

    Examples:
        >>> calculate_gpa(85, 92, 78)
        8.5
    """
    if scale <= 0:
        raise ValueError("Scale must be a positive number.")
    if not marks:
        return 0.0

    avg = sum(marks) / len(marks)
    gpa = (avg / 100.0) * scale
    return round(gpa, 2)


def get_top_performers(students: list, n: int = 5, subject: Optional[str] = None) -> list:
    """Return top n students ranked by subject score or overall average.

    Args:
        students: List of student dicts.
        n: Number of top students to return. Defaults to 5.
        subject: Subject name to rank by. If None, ranks by overall average.

    Returns:
        List of top n student dicts sorted in descending order of score.
        Returns empty list if students list is empty.

    Examples:
        >>> get_top_performers(students, n=1, subject='python')
        [{'name': 'Amit', ...}]
    """
    if not students:
        return []

    n = max(1, n)  # n should be at least 1

    def score_key(student):
        marks = student.get('marks', {})
        if not marks:
            return 0.0
        if subject:
            return marks.get(subject, 0.0)
        return sum(marks.values()) / len(marks)

    sorted_students = sorted(students, key=score_key, reverse=True)
    return sorted_students[:n]


def generate_report(student: dict, **options) -> str:
    """Generate a formatted performance report string for a student.

    Args:
        student: A student dict with keys 'name', 'roll', 'marks', 'attendance'.
        **options: Optional keyword arguments:
            include_rank (bool): Include rank info in report. Defaults to True.
            include_grade (bool): Include letter grade. Defaults to True.
            verbose (bool): Include detailed marks breakdown. Defaults to False.

    Returns:
        A formatted report string.

    Raises:
        ValueError: If student dict is missing required keys.

    Examples:
        >>> generate_report(student, include_grade=True, verbose=True)
        'Student Report: Amit ...'
    """
    required_keys = ['name', 'roll', 'marks']
    for key in required_keys:
        if key not in student:
            raise ValueError(f"Student record is missing required key: '{key}'")

    include_rank = options.get('include_rank', True)
    include_grade = options.get('include_grade', True)
    verbose = options.get('verbose', False)

    marks = student.get('marks', {})
    avg = sum(marks.values()) / len(marks) if marks else 0.0
    attendance = student.get('attendance', 'N/A')

    # determine grade
    def get_grade(average):
        if average >= 90: return 'A'
        elif average >= 75: return 'B'
        elif average >= 60: return 'C'
        else: return 'D'

    lines = []
    lines.append(f"=== Student Report ===")
    lines.append(f"Name     : {student['name']}")
    lines.append(f"Roll No  : {student['roll']}")
    lines.append(f"Attendance: {attendance}%")
    lines.append(f"Average  : {avg:.2f}")

    if include_grade:
        lines.append(f"Grade    : {get_grade(avg)}")

    if include_rank:
        lines.append(f"(Rank info requires full student list)")

    if verbose:
        lines.append("--- Subject Marks ---")
        for subject, score in marks.items():
            lines.append(f"  {subject.capitalize():<10}: {score}")

    return "\n".join(lines)


def classify_students(students: list) -> dict:
    """Classify students into grade buckets A, B, C, D based on average marks.

    Args:
        students: List of student dicts.

    Returns:
        A defaultdict with keys 'A', 'B', 'C', 'D', each containing
        a list of student dicts in that grade range.
        Returns empty defaultdict if input is empty.

    Examples:
        >>> result = classify_students(students)
        >>> result['A']
        [{'name': 'Priya', ...}]
    """
    result = defaultdict(list)

    if not students:
        return result

    for student in students:
        marks = student.get('marks', {})
        if not marks:
            result['D'].append(student)
            continue

        avg = sum(marks.values()) / len(marks)

        if avg >= 90:
            result['A'].append(student)
        elif avg >= 75:
            result['B'].append(student)
        elif avg >= 60:
            result['C'].append(student)
        else:
            result['D'].append(student)

    return result


# quick manual check when running this file directly
if __name__ == "__main__":
    s1 = create_student('Amit', 'R001', math=85, python=92, ml=78)
    s2 = create_student('Priya', 'R002', math=95, python=88, ml=91)
    s3 = create_student('Rahul', 'R003', math=60, python=55, ml=62)
    s4 = create_student('Sneha', 'R004', math=72, python=78, ml=70)

    students = [s1, s2, s3, s4]

    print("--- calculate_gpa ---")
    print(calculate_gpa(85, 92, 78))           # 8.5

    print("\n--- get_top_performers (by python) ---")
    top = get_top_performers(students, n=1, subject='python')
    print(top[0]['name'])                       # Amit

    print("\n--- generate_report (verbose) ---")
    print(generate_report(s2, include_grade=True, verbose=True))

    print("\n--- classify_students ---")
    classified = classify_students(students)
    for grade, group in classified.items():
        print(f"Grade {grade}: {[s['name'] for s in group]}")
