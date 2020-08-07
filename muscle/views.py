from django.shortcuts import render, redirect
from django.utils import timezone
from .models import trainlog,BodyWeight
from .forms import  trainlogform,BodyWeightform

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pytz


today = str(timezone.now()).split('-')
def index(request,year=today[0],month=today[1],span=1):
    train= trainlog.objects.all().order_by('used_date')
    body=BodyWeight.objects.all()
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


        if "weghtbutton" in data.keys():

            weight=data['weight']
            BodyWeight.objects.create(
                used_date=used_date,
                weight=weight,
            )

            return redirect (to='/muscle/{}/{}/{}'.format(year,month,span))            


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
    train=trainlog.objects.filter(used_date__year=year,used_date__month=month)
    values=[0,0,0,0,0,0]
    for i in label:
        for t,n in zip(train,range(0,6)):
            if t.category==i:
                values[n]=values[n]+1


    angles = np.linspace(0, 2 * np.pi, len(label) + 1, endpoint=True)
    values = np.concatenate((values, [values[0]]))  # 閉じた多角形にする
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-')  # 外枠
    ax.fill(angles, values, alpha=0.25)  # 塗りつぶし
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, label)  # 軸ラベル
    ax.set_rlim(0 ,5)
    fig.savefig('muscle/static/images/rador_chart_{}_{}_{}.svg'.format(year,month,span),transparent=True)
    plt.close(fig)
    return None
##label value 保存名を渡せば作ってくれる
def plot_polar(labels, values):
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)
    values = np.concatenate((values, [values[0]]))  # 閉じた多角形にする
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-')  # 外枠
    ax.fill(angles, values, alpha=0.25)  # 塗りつぶし
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)  # 軸ラベル
    ax.set_rlim(0 ,250)
   



#同様にspanなしの状態まで復元
def draw_linear(year,month,span):

    weight=BodyWeight.objects.filter(used_date__year=year,used_date__month=month).order_by('used_date')
    daylist=[]
    weightlist=[]
    for w in weight:
        #daylist.append()<=後回し（span変更時の仕様確認必要）
        weightlist.append(w.weight)
    plt.plot(weightlist)
    plt.savefig('muscle/static/images/bar_{}_{}_{}.svg'.format(year,month,span),transparent=True)   

    return None