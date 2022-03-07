from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Employee
import math

@login_required(login_url='/login/')
def create(request):
    global situation
    global situation_rest
    try:
        situation_all =Employee.objects.filter(name=request.user)
        situation = situation_all[situation_all.count()-1]
        situation =situation.status
    except:
        situation ="退勤"
    if situation =="出勤":
        situation ="退勤"
        situation_rest ="休憩開始"

    elif situation =="休憩開始":
        situation =""
        situation_rest ="休憩終了"
    elif situation =="休憩終了":
        situation ="退勤"
        situation_rest ="休憩開始"

    else:
        situation ="出勤"
        situation_rest =""
        rest ="rest_start"
    
    
    if request.user.is_superuser:
        administrator="新規従業員追加"
        history ="従業員履歴"
        payment ="従業員支払額"
    else:
        administrator=""
        history =""
        payment =""
        
    
    params ={
        'time':timezone.now(),
        'situation':situation,
        'situation_rest':situation_rest,
        'administrator':administrator,
        'history':history,
        'payment':payment,
        
    }
    return render(request,"attendance/create.html",params)

@login_required(login_url='/login/')
def record(request):
    last =Employee.objects.filter(name=request.user)
    last = last[last.count()-1]
    time_register =last.regist_date
    
    register =status
    params ={
        "login_user":request.user,
        "time":time_register,
        'register':register,
        
    }

    return render(request,"attendance/record.html",params)





@login_required(login_url='/login/')
def rest(request):
    global status
    time_register =timezone.now()
    params ={
        'time':time_register,
        'form':Employee(),
        'login_user':request.user,   
        'status':situation_rest,
    }
    if (request.method =="POST"):
        name =request.user
        status =situation_rest
        situation_all =Employee.objects.filter(name=request.user)
        #休憩時間
        if status=="休憩終了":
            rest_start_time = situation_all[situation_all.count()-1].regist_date
            time_rest_day =time_register-rest_start_time
        #休憩開始時
        else:
            time_rest_day =0
           

        #拘束時間
        time_restraint_day ="damy"

        
        employee =Employee(name=name,status=status,time_restraint_day=time_restraint_day,time_rest_day=time_rest_day)
        employee.save()
        return redirect(to="/attendance/record")
    return render(request,"attendance/rest.html",params)






from .models import basic_inf

@login_required(login_url='/login/')
def start_end(request):
    global status 
    global start_time
    status =situation
    time_register =timezone.now()
    params ={
        'time':timezone.now(),
        'form':Employee(),
        'login_user':request.user,  
        'situation':situation,
    }
    if (request.method =="POST"):
        name =request.user
        status =situation
        if status=="退勤":
            #拘束時間の計算
            situation_all =Employee.objects.filter(name=request.user)
            i =1
            data = situation_all[situation_all.count()-i].status
            rest_count =0
            while data!="出勤":
                i +=1
                data = situation_all[situation_all.count()-i].status
                if data=="休憩終了":
                    rest_count +=1
                    
            time_restraint_day =str(time_register-situation_all[situation_all.count()-i].regist_date)
            
            restraint = time_restraint_day.split(":")
            restraint_minute =int(restraint[0])*60+int(restraint[1])
            #休憩時間の合計
            rest = Employee.objects.filter(status="休憩終了")  
            rest_minute_sum =0
            for i in range(rest_count):
                rest_minute  = rest[i].time_rest_day.split(":")
                rest_minute  =int(rest_minute[0])*60+int(rest_minute[1])
                rest_minute_sum +=rest_minute
            #実働時間
            actual_working_hour =restraint_minute-rest_minute_sum

            data =basic_inf.objects.filter(name=request.user)
            #交通費
            transportation_expenses =data[data.count()-1].transportation_expenses
            #時給
            hourly_wage =data[data.count()-1].hourly_wage
            #1日の給料
            sum_pay =math.floor(actual_working_hour/60*int(hourly_wage))+int(transportation_expenses)

            basic =basic_inf(name=name,actual_working_hour=actual_working_hour,sum_pay=sum_pay)
            basic.save()
            


        #出勤時の処理
        else:
            rest_count =0
            start_time =timezone.now()
            restraint_minute =0
            rest_minute_sum=0
            actual_working_hour =0
            
        employee =Employee(name=name,status=status,time_restraint_day=restraint_minute,
        time_rest_day=rest_minute_sum)
        employee.save()
        return redirect(to="/attendance/record")
    return render(request,"attendance/start_end.html",params)


@login_required(login_url='/login/')
def new_staff(request):
    if (request.method =="POST"):
        name =request.POST["name"]
        transportation_expenses=request.POST["transportation_expenses"]
        hourly_wage =request.POST["hourly_wage"]
        basic =basic_inf(name=name,transportation_expenses=transportation_expenses,hourly_wage=hourly_wage)
        basic.save()
        return redirect(to="/admin/auth/user/add/")
        
                
    else:
        return render(request,"attendance/new_staff.html")
    
from .forms import EmployeeForm, FindForm
@login_required(login_url='/login/')
def history(request):
    if (request.method == 'POST'):
        msg = request.POST['find']
        form = FindForm(request.POST)
        history = Employee.objects.filter(name=msg)  
    else:
        form = FindForm()
        history =Employee.objects.all()
    history =history.order_by("regist_date").reverse()
   
    params ={
        'form':form,
        "login_user":request.user,
        "history":history,
        
    }
    return render(request,"attendance/history.html",params)

@login_required(login_url='/login/')
def edit(request,num):
    obj=Employee.objects.get(id=num)
    if (request.method =="POST"):
        status =EmployeeForm(request.POST,instance=obj)
        status.save()
        data =Employee.objects.filter(id=num)
        status =data[0].status
        name =data[0].name
        time =data[0].regist_date
        #退勤と押すところを休憩開始を押してしまった場合→退勤処理    
        if status =="退勤":
            #拘束時間の計算
            situation_all =Employee.objects.filter(name=name)
            i =1
            data = situation_all[situation_all.count()-i].status
            rest_count =0
            while data!="出勤":
                i +=1
                data = situation_all[situation_all.count()-i].status
                if data=="休憩終了":
                    rest_count +=1
                    
            time_restraint_day =str(time-situation_all[situation_all.count()-i].regist_date)
            
            restraint = time_restraint_day.split(":")
            restraint_minute =int(restraint[0])*60+int(restraint[1])
            #休憩時間の合計
            rest = Employee.objects.filter(status="休憩終了")  
            rest_minute_sum =0
            for i in range(rest_count):
                rest_minute  = rest[i].time_rest_day.split(":")
                rest_minute  =int(rest_minute[0])*60+int(rest_minute[1])
                rest_minute_sum +=rest_minute
            #実働時間
            actual_working_hour =restraint_minute-rest_minute_sum

            data =basic_inf.objects.filter(name=name)
            #交通費
            transportation_expenses =data[data.count()-1].transportation_expenses
            #時給
            hourly_wage =data[data.count()-1].hourly_wage
            #1日の給料
            sum_pay =math.floor(actual_working_hour/60*int(hourly_wage))+int(transportation_expenses)

            basic =basic_inf(name=name,actual_working_hour=actual_working_hour,sum_pay=sum_pay,regist_date=time)
            basic.save()
        #休憩開始と押すところを退勤を押してしまった場合→退勤取り消し、休憩開始処理
        else:
            time_rest_day =0
            time_restraint_day ="damy"
            emp =Employee(time_rest_day=time_rest_day,time_restraint_day=time_restraint_day)
            emp.save()
            basic =basic_inf(name="入力ミス",id =num,regist_date=time)
            basic.save()
        

        return redirect(to="/attendance/history")
    params ={
        'form':EmployeeForm(instance=obj),
        "id":num,
    }
    
    return render(request,"attendance/edit.html",params)




@login_required(login_url='/login/')
def payment(request):
    if (request.method == 'POST'):
        msg = request.POST['find']
        form = FindForm(request.POST)
        payment = basic_inf.objects.filter(name=msg)  
    else:
        form = FindForm()
        payment =basic_inf.objects.filter()
    payment =payment.order_by("regist_date").reverse()
    params ={
        'form':form,
        "payment":payment,
    }
    
    
    return render(request,"attendance/payment.html",params)

from .forms import InfForm
def pay_edit(request,num):
    obj=basic_inf.objects.get(id=num)
    if (request.method =="POST"):
        status =InfForm(request.POST,instance=obj)
        status.save()
       
        data =basic_inf.objects.filter(id=num)
        name =data[0].name
        regist_date =data[0].regist_date
        #交通費
        transportation_expenses =data[0].transportation_expenses
        #時給
        hourly_wage =data[0].hourly_wage
        #実働時間
        actual_working_hour =data[0].actual_working_hour
        #1日の給料
        sum_pay =math.floor(float(actual_working_hour)/60*int(hourly_wage))+int(transportation_expenses)
        basic =basic_inf(name=name,regist_date=regist_date,id=num,actual_working_hour=actual_working_hour,sum_pay=sum_pay,transportation_expenses=transportation_expenses,hourly_wage=hourly_wage)
        basic.save()





        return redirect(to="/attendance/payment")

    params ={
        'form':InfForm(instance=obj),
        "id":num,
    }
    
    return render(request,"attendance/pay_edit.html",params)
   

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse('create'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'regisration/login.html')





