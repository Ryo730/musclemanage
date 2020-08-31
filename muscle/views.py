from django.shortcuts import render, redirect
from django.utils import timezone
from .models import trainlog,BodyWeight
from .forms import  trainlogform,BodyWeightform
from  django.db.models import Q
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pytz
import pylint

today = str(timezone.now()).split('-')
def index(request,year=today[0],month=today[1],span=1):

    if span==1:
        train=trainlog.objects.filter(used_date__year=year,used_date__month=month).order_by('-used_date')[:10]
    elif span==2:
        train=trainlog.objects.filter(Q(used_date__year=year),(Q(used_date__month=month)|Q(used_date__month=month-1))).order_by('-used_date')[:10]


    #body=BodyWeight.objects.all()
    trainform=trainlogform()
    weightform=BodyWeightform()
    for m in train:
        date = str(m.used_date).split(' ')[0]
        m.used_date = '/'.join(date.split('-')[1:3])
    context = {'year' : year,
            'month' : month,
            'train' : train,
            'trainform':trainform,
            'weightform':weightform,
            'span':span,
        }
    draw_graph(year,month,span)
    draw_linear(year,month,span)
    if request.method=='POST':
        data=request.POST
        used_date=data['used_date']
        #used_date = timezone.datetime.strptime(used_date, "%Y/%m/%d")
        #tokyo_timezone = pytz.timezone('Asia/Tokyo')
        #used_date = tokyo_timezone.localize(used_date)
        #used_date += datetime.timedelta(hours=9)

        
        #train側の送信ボタンが押された時
        if "train" in data.keys():
        
            used_date=data['used_date']
            comment=data['comment']
            category=data['category']
        
            trainlog.objects.create(
                used_date=used_date,
                comment=comment,
                category=category,)
            
            return redirect(to='/muscle/{}/{}/{}'.format(year,month,span))


        if "weightbutton" in data.keys():

            weight=data['weight']
            BodyWeight.objects.create(
                used_date=used_date,
                weight=weight,
            )

            return redirect (to='/muscle/{}/{}/{}'.format(year,month,span))            

#'muscle/base.html'
    return render(request, 'muscle/base.html', context)

#まず，spanなしの状態まで復元
def draw_graph(year,month,span):
#labelとvaluesを作る
    label=[
            'chest',
            'shoulder',
            'spine',
            'arm',
            'abs',
            'leg',
    ]
    if span==1:
        trains=trainlog.objects.filter(used_date__year=year,used_date__month=month).order_by('used_date')
    elif span==2:
        trains=trainlog.objects.filter(Q(used_date__year=year),(Q(used_date__month=month)|Q(used_date__month=month-1))).order_by('used_date')
    values=[0,0,0,0,0,0]
    #ここのアルゴリズムチェック必要
    for t in trains:
        for i,n in zip(label,range(0,6)):
            if t.category==i :
                values[n]+=1

    angles = np.linspace(0, 2 * np.pi, len(label) + 1, endpoint=True)
    values = np.concatenate((values, [values[0]]))  # 閉じた多角形にする
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-')  # 外枠
    ax.fill(angles, values, alpha=0.25)  # 塗りつぶし
    ax.set_thetagrids(angles[:-1] * 180 / np.pi,label)  # 軸ラベル 初期第一引数angles[:-1] * 180 / np.pi
    if max(values)>4:
        ax.set_rlim(0,7)
    else:
        ax.set_rlim(0,5)
    fig.savefig('muscle/static/images/rador_chart_{}_{}_{}.svg'.format(year,month,span),transparent=True)
    plt.close(fig)
    return None




#同様にspanなしの状態まで復元
def draw_linear(year,month,span):
    weight=0
    if span==1:
        weight=BodyWeight.objects.filter(used_date__year=year,used_date__month=month).order_by('used_date')
    if span==2:
        weight=BodyWeight.objects.filter(Q(used_date__year=year),(Q(used_date__month=month)|Q(used_date__month=month-1))).order_by('used_date')
    daylist=[]
    weightlist=[]
    for w in weight:
        #date = str(w.used_date).split(' ')[0]
        date=w.used_date.strftime('%m%d')
        daylist.append(date)
        #<=後回し（span変更時の仕様確認必要）
        weightlist.append(w.weight)
    plt.plot(daylist,weightlist)
    plt.xticks(rotation=90)
    plt.savefig('muscle/static/images/bar_{}_{}_{}.svg'.format(year,month,span),transparent=True)
    plt.close()
    return None