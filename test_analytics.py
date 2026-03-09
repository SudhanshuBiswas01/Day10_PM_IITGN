# test_analytics.py
# Unit tests for student_analytics.py
# Testing all functions with at least 3 assertions each

from student_analytics import (
    create_student,
    calculate_gpa,
    get_top_performers,
    generate_report,
    classify_students
)

# -----------------------------------------------
# Tests for create_student
# -----------------------------------------------

def test_create_student():
    s = create_student('Amit', 'R001', math=85, python=92, ml=78)
    assert s['name'] == 'Amit', "Name should be Amit"
    assert s['roll'] == 'R001', "Roll should be R001"
    assert s['marks']['math'] == 85, "Math should be 85"
    assert s['marks']['python'] == 92, "Python should be 92"
    assert s['attendance'] == 100.0, "Default attendance should be 100.0"

    # test custom attendance
    s2 = create_student('Priya', 'R002', math=90, attendance=85.5)
    assert s2['attendance'] == 85.5, "Attendance should be 85.5"

    # test empty name raises ValueError
    try:
        create_student('', 'R003', math=70)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    # test invalid mark out of range
    try:
        create_student('Test', 'R004', math=110)
        assert False, "Should have raised ValueError for mark > 100"
    except ValueError:
        pass

    print("create_student: all tests passed")


# -----------------------------------------------
# Tests for calculate_gpa
# -----------------------------------------------

def test_calculate_gpa():
    # basic check
    result = calculate_gpa(85, 92, 78)
    assert result == 8.5, f"Expected 8.5 but got {result}"

    # perfect score
    assert calculate_gpa(100, 100, 100) == 10.0, "Perfect score should give 10.0"

    # no marks
    assert calculate_gpa() == 0.0, "Empty marks should return 0.0"

    # custom scale
    result = calculate_gpa(80, 90, scale=4.0)
    assert result == 3.4, f"Expected 3.4 but got {result}"

    # invalid scale
    try:
        calculate_gpa(80, 90, scale=0)
        assert False, "Should raise ValueError for scale=0"
    except ValueError:
        pass

    print("calculate_gpa: all tests passed")


# -----------------------------------------------
# Tests for get_top_performers
# -----------------------------------------------

def test_get_top_performers():
    students = [
        create_student('Amit', 'R001', math=85, python=92, ml=78),
        create_student('Priya', 'R002', math=95, python=88, ml=91),
        create_student('Rahul', 'R003', math=60, python=55, ml=62),
    ]

    # top 1 by python - Amit has 92
    top = get_top_performers(students, n=1, subject='python')
    assert len(top) == 1, "Should return 1 student"
    assert top[0]['name'] == 'Amit', "Amit should be top in python"

    # top 1 overall - Priya avg = (95+88+91)/3 = 91.33
    top_overall = get_top_performers(students, n=1)
    assert top_overall[0]['name'] == 'Priya', "Priya should top overall"

    # empty list
    assert get_top_performers([]) == [], "Empty list should return []"

    # n greater than list length - should return all
    all_students = get_top_performers(students, n=10)
    assert len(all_students) == 3, "Should return all 3 students"

    print("get_top_performers: all tests passed")


# -----------------------------------------------
# Tests for generate_report
# -----------------------------------------------

def test_generate_report():
    s = create_student('Priya', 'R002', math=95, python=88, ml=91)

    report = generate_report(s)
    assert 'Priya' in report, "Report should contain student name"
    assert 'R002' in report, "Report should contain roll number"

    # with grade
    report_grade = generate_report(s, include_grade=True)
    assert 'Grade' in report_grade, "Report should show grade"

    # verbose mode
    report_verbose = generate_report(s, verbose=True)
    assert 'math' in report_verbose.lower() or 'Math' in report_verbose, \
        "Verbose report should include subject marks"

    # missing required key should raise ValueError
    try:
        generate_report({'name': 'X'})
        assert False, "Should raise ValueError for missing keys"
    except ValueError:
        pass

    print("generate_report: all tests passed")


# -----------------------------------------------
# Tests for classify_students
# -----------------------------------------------

def test_classify_students():
    students = [
        create_student('Amit', 'R001', math=85, python=92, ml=78),   # avg ~85 -> B
        create_student('Priya', 'R002', math=95, python=88, ml=91),  # avg ~91.3 -> A
        create_student('Rahul', 'R003', math=60, python=55, ml=62),  # avg ~59 -> D
        create_student('Sneha', 'R004', math=72, python=78, ml=70),  # avg ~73.3 -> B
    ]

    result = classify_students(students)

    assert 'Priya' in [s['name'] for s in result['A']], "Priya should be in A"
    assert 'Rahul' in [s['name'] for s in result['D']], "Rahul should be in D"
    # Amit avg=85 -> B, Sneha avg=73.3 -> C
    assert len(result['B']) == 1, "Only Amit should be in B"
    assert 'Sneha' in [s['name'] for s in result['C']], "Sneha avg 73.3 should be in C"

    # empty list
    empty_result = classify_students([])
    assert len(empty_result) == 0, "Empty list should give empty dict"

    # student with no marks goes to D
    no_marks = {'name': 'Ghost', 'roll': 'R999', 'marks': {}, 'attendance': 100.0}
    r = classify_students([no_marks])
    assert 'Ghost' in [s['name'] for s in r['D']], "Student with no marks should be in D"

    print("classify_students: all tests passed")


# -----------------------------------------------
# Run all tests
# -----------------------------------------------

if __name__ == "__main__":
    test_create_student()
    test_calculate_gpa()
    test_get_top_performers()
    test_generate_report()
    test_classify_students()
    print("\nAll tests passed successfully!")
