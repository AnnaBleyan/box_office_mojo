from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import matplotlib.pyplot as plt
from datetime import date

from django.views import generic
from django.urls import reverse

from users.models import Profile
from .models import Movie, BoxOffice

def welcome(request):
    return render(request, 'movie/base.html')


@login_required(login_url='user_login')
def home(request):

    movie_list = BoxOffice.objects.order_by('-worldwide_gross')
    user = request.user

    context = {
        "movie_list": movie_list,
        "user": user,
    }

    return render(request, "users/user_profile.html", context)

def movie_list(request):
    movie_list = BoxOffice.objects.order_by('-worldwide_gross')
    m = []
    for movie in movie_list:
        if movie.movie_name not in m:
            m.append(movie)

    context = {'movie_list': m}
    return render(request, 'movie/movies.html', context)


@login_required(login_url='user_login')
def scrap(request):
    profile = Profile.objects.get(user_id=request.user.id)

    if profile.is_admin is True:

        URL = 'https://www.boxofficemojo.com/year/world/'

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find(id="table")

        movie_list = results.find_all("tr")

        for movie in movie_list[1:31]:
            tds = movie.find_all('td')
            dg = ""
            dgp = ""
            if len(tds[3].text) > 1:
                dg = ((tds[3].text)[1:]).replace(",", "")
            elif len(tds[3].text) == 1 and (tds[3].text)[0] == "-":
                dg = 0

            if len(tds[4].text) > 1:
                if (tds[4].text)[0] == "<":
                    dgp = (tds[4].text)[1:-1]
                else:
                    dgp = (tds[4].text)[:-1]
            elif len(tds[4].text) == 1 and (tds[4].text)[0] == "-":
                dgp = 0

            b = BoxOffice(movie_name=tds[1].text,
                          worldwide_gross=int(((tds[2].text)[1:]).replace(",", "")),
                          domestic_gross=int(dg),
                          domestic_gross_per=dgp,
                          foreign_gross=(((tds[5].text)[1:]).replace(",", "")),
                          foreign_gross_per=(tds[6].text)[:-1])
            b.save()
            m_list = BoxOffice.objects.all()
            context = {"movie_list": m_list}

        return render(request, "movie/movies.html", context=context)

    else:
        return render(request, "movie/scrap.html")



@login_required(login_url='user_login')
def graphic(request):
    profile = Profile.objects.get(user_id=request.user.id)


    movies = BoxOffice.objects.filter(scrap_time=date.today())[:6]

    x = []
    y = []
    for m in movies:
        x.append(m.movie_name)
        y.append(m.worldwide_gross)

    plt.scatter(x, y)
    plt.xlabel("Movie Name")
    plt.ylabel("gross expressed in billion dollars")
    plt.title("Movies' gross at theaters")
    plt.xticks(rotation=45, ha='right')
    spacing = 0.300
    plt.subplots_adjust(bottom=spacing)
    plt.savefig('static/wwg.svg')
    plt.close()

    return render(request, 'movie/graphic.html')


@login_required(login_url='user_login')
def domestic_graphic(request):
    profile = Profile.objects.get(user_id=request.user.id)

    movies = BoxOffice.objects.filter(scrap_time=date.today())[:6]

    x = []
    z = []
    for m in movies:
        x.append(m.movie_name)
        z.append(m.domestic_gross)

    plt.scatter(x, z)
    plt.xlabel("Movie Name")
    plt.ylabel("domestic gross expressed in billion dollars")
    plt.title("Movies' domestic gross at theaters")
    plt.xticks(rotation=45, ha='right')
    spacing = 0.300
    plt.subplots_adjust(bottom=spacing)
    plt.savefig('static/dg.svg')
    plt.close()

    return render(request, 'movie/domestic.html')


def movie_table(request):
    movie_list = BoxOffice.objects.filter(scrap_time=date.today())[:16]

    context = {'movie_list': movie_list}
    return render(request, 'movie/table.html', context)

@login_required(login_url='user_login')
def foreign_graphic(request):
    profile = Profile.objects.get(user_id=request.user.id)

    movies = BoxOffice.objects.filter(scrap_time=date.today())[:6]

    x = []
    z = []
    for m in movies:
        x.append(m.movie_name)
        z.append(m.foreign_gross)

    plt.scatter(x, z)
    plt.xlabel("Movie Name")
    plt.ylabel("foreign gross expressed in billion dollars")
    plt.title("Movies' foreign gross at theaters")
    plt.xticks(rotation=45, ha='right')
    spacing = 0.300
    plt.subplots_adjust(bottom=spacing)
    plt.savefig('static/fg.svg')
    plt.close()

    return render(request, 'movie/foreign.html')


@login_required(login_url='user_login')
def foreign_percent(request):
    profile = Profile.objects.get(user_id=request.user.id)

    movies = BoxOffice.objects.filter(scrap_time=date.today())[:6]

    x = []
    z = []
    for m in movies:
        x.append(m.movie_name)
        z.append(m.foreign_gross_per)

    plt.scatter(x, z)
    plt.xlabel("Movie Name")
    plt.ylabel("foreign gross share in worldwide gross")
    plt.title("Movies' foreign gross share")
    plt.xticks(rotation=45, ha='right')
    spacing = 0.300
    plt.subplots_adjust(bottom=spacing)
    plt.savefig('static/fgp.svg')
    plt.close()

    return render(request, 'movie/foreign_per.html')



@login_required(login_url='user_login')
def domestic_percent(request):
    profile = Profile.objects.get(user_id=request.user.id)

    movies = BoxOffice.objects.filter(scrap_time=date.today())[:6]

    x = []
    z = []
    for m in movies:
        x.append(m.movie_name)
        z.append(m.domestic_gross_per)

    plt.scatter(x, z)
    plt.xlabel("Movie Name")
    plt.ylabel("domestic gross share in worldwide gross")
    plt.title("Movies' domestic gross share")
    plt.xticks(rotation=45, ha='right')
    spacing = 0.300
    plt.subplots_adjust(bottom=spacing)
    plt.savefig('static/dgp.svg')
    plt.close()

    return render(request, 'movie/domestic_per.html')


def movie_table(request):
    movie_list = BoxOffice.objects.filter(scrap_time=date.today())[:8]

    context = {'movie_list': movie_list}
    return render(request, 'movie/table.html', context)

@login_required(login_url='user_login')
def movie_stat(request, movie_name):
    profile = Profile.objects.get(user_id=request.user.id)

    if profile.is_admin is True:
        movies = BoxOffice.objects.filter(movie_name=movie_name)[:5]

        x = []
        z = []
        for m in movies:
            x.append(m.scrap_time)
            z.append(m.worldwide_gross)

        plt.scatter(x, z)
        plt.title(f"{m.movie_name} Movie's worldwide gross data for the last 5 days")
        plt.xticks(rotation=45, ha='right')
        spacing = 0.300
        plt.subplots_adjust(bottom=spacing)
        plt.savefig('static/mstat.svg')
        plt.close()

        return render(request, 'movie/mstat.html', {"movies": movies})
    else:
        return render(request, "movie/scrap.html")



@login_required(login_url='user_login')
def mixed_graphic(request):
    profile = Profile.objects.get(user_id=request.user.id)

    movies = BoxOffice.objects.filter(scrap_time=date.today())[:6]

    x = []
    z = []
    for m in movies:
        x.append(m.movie_name)
        z.append(m.worldwide_gross)

    plt.scatter(x, z)
    plt.xlabel("Movie Name")
    plt.ylabel("worldwide, US and foreign gross expressed in billion dollars")
    plt.title("Movies'  gross at theaters")
    plt.xticks(rotation=45, ha='right')
    spacing = 0.300
    plt.subplots_adjust(bottom=spacing)
    plt.savefig('static/mg.svg')

    x = []
    z = []
    for m in movies:
        x.append(m.movie_name)
        z.append(m.domestic_gross)

    plt.scatter(x, z)
    plt.savefig('static/mg.svg')

    x = []
    z = []
    for m in movies:
        x.append(m.movie_name)
        z.append(m.foreign_gross)

    plt.scatter(x, z)
    plt.savefig('static/mg.svg')
    plt.close()

    return render(request, 'movie/mixed.html')
