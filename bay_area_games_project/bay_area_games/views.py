"""
前端展示视图
"""
from django.shortcuts import render


def index(request):
    """首页"""
    return render(request, "index.html")


def dashboard(request):
    """仪表盘"""
    return render(request, "dashboard.html")


def teams(request):
    """代表队管理"""
    return render(request, "teams.html")


def athletes(request):
    """运动员管理"""
    return render(request, "athletes.html")


def events(request):
    """赛事管理"""
    return render(request, "events.html")


def results(request):
    """成绩管理"""
    return render(request, "results.html")


def statistics(request):
    """数据统计"""
    return render(request, "statistics.html")


def referees(request):
    """裁判管理"""
    return render(request, "referees.html")


def sponsors(request):
    """商务合作管理"""
    return render(request, "sponsors.html")


def logistics(request):
    """后勤保障管理"""
    return render(request, "logistics.html")