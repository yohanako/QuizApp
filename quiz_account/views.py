from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from quiz_account.forms import SignUpForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from .forms import CreateQuestionForm
#from .models import Questions
from django.http import HttpResponseRedirect
from .import forms as QFORM
from .import models as QMODEL
from django.shortcuts import render
from django.http import HttpResponse
#from .models import Questions
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from . import forms,models
from django.contrib.auth.models import Group
from django.db import models
from .models import Course, Student
from datetime import date, timedelta
from django.db.models import Sum
from django.conf import settings

def home(request):
	return render(request, 'accounts/home.html', {})

def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			messages.success(request, ('Login Successfully!'))
			return redirect('home')
		else:
			messages.success(request,('Incorrect - Please try again!'))
			return redirect('login')

	else:
		return render(request, 'accounts/login.html', {})


def logout_user(request):

	logout(request)
	messages.success(request,('Logout Successfully!'))
	return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ('Register Successfully!'))
			return redirect('login')

	else:
		form = SignUpForm()
	context = {'form': form}
	return render(request, 'accounts/register.html', context)

def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance= request.user)
		if form.is_valid():
			form.save()
			messages.success(request,('You Have Edited Your Profile...'))
			return redirect('home')
	else:
		form = EditProfileForm(instance= request.user)

	context = {'form': form}
	return render(request, 'accounts/edit_profile.html', context)

def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			messages.success(request,('You Have Edited Your Password...'))
			return redirect('home')
	else:
		form = PasswordChangeForm(user= request.user)

	context = {'form': form}
	return render(request, 'accounts/change_password.html', context)
#lst = []
#answers = Questions.objects.all()
#anslist = []
#for i in answers:
#    anslist.append(i.answer)


#TEACHER

def teacher_base(request):
    return render(request, 'accounts/teacher_base.html')

def teacher_register(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ('Register Successfully!'))
			return redirect('accounts/teacher_login')

	else:
		form = SignUpForm()
	context = {'form': form}
	return render(request, 'accounts/teacher_register.html', context)

def teacher_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			messages.success(request, ('Login Successfully!'))
			return redirect('teacher_base')
		else:
			messages.success(request,('Incorrect - Please try again!'))
			return redirect('login')

	else:
		return render(request, 'accounts/teacher_login.html', {})


def teacher_logout(request):

	logout(request)
	messages.success(request,('Logout Successfully!'))
	return redirect('home')


def teacher_create_topic(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
    	courseForm=forms.CourseForm(request.POST)
    	if courseForm.is_valid():        
    		courseForm.save()
    	else:
    		print("form is invalid")
    	return HttpResponseRedirect('/teacher_see_topic')
    return render(request,'accounts/teacher_create_topic.html',{'courseForm':courseForm})

def teacher_see_topic(request):
	courses = Course.objects.all()
	return render(request,'accounts/teacher_see_topic.html',{'courses':courses})

def teacher_topic(request):
	return render(request,'accounts/teacher_topic.html')


def teacher_create(request):
	questionForm=QFORM.CreateQuestionForm()
	if request.method=='POST':
		questionForm=QFORM.CreateQuestionForm(request.POST)
		if questionForm.is_valid():
			question=questionForm.save(commit=False)
			course=QMODEL.Course.objects.get(id=request.POST.get('courseID'))
			question.course=course
			question.save()       
		else:
			print("form is invalid")
		return HttpResponseRedirect('/teacher_create_view')
	return render(request,'accounts/teacher_create.html',{'questionForm':questionForm})

def teacher_create_view(request):
    courses= QMODEL.Course.objects.all()
    return render(request,'accounts/teacher_create_view.html',{'courses':courses})

def teacher_create_question(request):
    return render(request,'accounts/teacher_create_question.html')


def teacher_see_question(request,pk):
    questions=QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request,'accounts/teacher_see_question.html',{'questions':questions})

def teacher_signup(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        return HttpResponseRedirect('/teacher_login')
    return render(request,'accounts/teacher_signup.html',context=mydict)


def teacher_click(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'accounts/teacher_click.html')


def student_signup(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('/login')
    return render(request,'accounts/student/student_signup.html',context=mydict)


#STUDENT


def student(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'accounts/student/student.html')


def student_quiz(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'accounts/student/student_quiz.html',{'courses':courses})


def take_quiz(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'accounts/student/take_quiz.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})


def start_quiz(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'accounts/student/start_quiz.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    return response

from .models import Student

def calculate_marks(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        student.save()
        #result = forms.save()

        return HttpResponseRedirect('see_score')



def see_score(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'accounts/student/see_score.html',{'courses':courses})
    


def check_score(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'accounts/student/check_score.html',{'results':results})

def student_score(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'accounts/student/student_score.html',{'courses':courses})
  