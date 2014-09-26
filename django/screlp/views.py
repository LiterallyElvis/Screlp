from django.http import HttpResponse
import time
from django.shortcuts import render
# Create your views here.
from screlp.backend import geog, parse

def home(request):
    """

    :param request:
    :return:
    """
    return render(request, 'home.html')


def result(request):
    """

    :param request:
    :return:
    """
    args = dict()
    args['address'] = request.GET['a']
    args['term'] = request.GET['t']
    args['radius'] = request.GET['r']
    args['density'] = request.GET['d']
    args['category'] = request.GET['c']

    start = time.time()
    origin = geog.get_geocode(args)
    results = geog.generate_coords(origin, int(args['density']), int(args['radius']))
    # yelp_results = parse.scrape_yelp(args, results)
    # screlp.src.files.create_search_map(origin, results, True, int(args.radius))
    # screlp.src.files.write_csv_file(yelp_results)
    time_taken = "Execution time: {:.2f}{}".format((time.time() - start), " seconds")

    if 'q' in request.GET:
        message = 'Search took: {}'.format(time_taken)
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)