from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Grade
from .forms import StudentForm, GradeForm
from django.db.models import Avg

def home(request):
    students = Student.objects.all()
    return render(request, 'grades/home.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    grades = Grade.objects.filter(student=student)
    total_marks = sum(grade.grade for grade in grades)
    average_grade = grades.aggregate(Avg('grade'))['grade__avg']
    letter_grade = get_letter_grade(average_grade)
    return render(request, 'grades/student_detail.html', {
        'student': student,
        'grades': grades,
        'total_marks': total_marks,
        'average_grade': average_grade,
        'letter_grade': letter_grade,
    })

def add_grade(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.student = student
            grade.save()
            return redirect('student_detail', student_id=student.id)
    else:
        form = GradeForm()
    return render(request, 'grades/add_grade.html', {'form': form, 'student': student})

def get_letter_grade(average_grade):
    if average_grade is None:
        return 'N/A'
    if average_grade >= 90:
        return 'A'
    elif average_grade >= 80:
        return 'B'
    elif average_grade >= 70:
        return 'C'
    elif average_grade >= 60:
        return 'D'
    else:
        return 'F'
