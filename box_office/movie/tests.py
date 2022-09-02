from django.test import TestCase
from .models import BoxOffice

movie_list = BoxOffice.objects.order_by('-worldwide_gross')
l = []

for m in movie_list:
    l.append(m)

t = tuple(l)

l_r = []
for i in range(1, 31):
    l_r.append(i)
# r = 1

# while r < 31:
#     for m in movie_list:
#         print(f"{r} - {m}")
#         r += 1

x = l_r
y = l

for i, j in zip(x, y):
   print(str(i) + " / " + str(j))