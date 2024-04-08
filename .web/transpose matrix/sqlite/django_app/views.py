import datetime
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_app import models

"""
        # http://localhost:8000/?param_date_from=03-01-2024&param_date_to=04-01-2024
        {'2024-03-01': {
            "юбилейны":27000,
            "Умка":2000"}
        ,
            '2024-04-01': {
                "умка":2000
            }}



    {'2024-03-01': {'
        Юбилейный':
        {
            Сладости: 1000,
            Другое:2000},
    'Умка':
    {
        Другое: 2000}
    },
    '2024-04-01': {'Юбилейный': 21000}}


    data_2 = [
        ["дата", "название", "Сладости", "другое"],
        ["2024-03-01", "Юбилейный", "20000", "2500"],
        ["2024-03-01", "Умка", "0", "27000"],
    ]



    [(1, datetime.date(2024, 3, 1), 'Юбилейный', 10, 2000, 'Сладости'),
    (2, datetime.date(2024, 4, 1), 'Юбилейный', 7, 3000, 'Сладости'),
    (3, datetime.date(2024, 3, 1), 'Умка', 18, 1500, 'Другое'),
    (4, datetime.date(2024, 5, 1), 'Умка', 5, 10000, 'Сладости'),
    (5, datetime.date(2024, 3, 1), 'Юбилейный', 5, 500, 'Другое')]
    """


@api_view(["GET"])
def home(request):

    param_date_from = datetime.datetime.strptime(
        request.GET.get("param_date_from"), "%m-%d-%Y"
    )
    param_date_to = datetime.datetime.strptime(
        request.GET.get("param_date_to"), "%m-%d-%Y"
    )
    cursor = connection.cursor()

    query_old = f"""
     WITH dat as (
                   SELECT month, shop, category, SUM(count*price) as total
                   FROM django_app_products 
                   WHERE month BETWEEN '{param_date_from.strftime("%Y-%m-%d")}' and  '{param_date_to.strftime("%Y-%m-%d")}' 
                   GROUP BY month, shop, category
                   )
                   
                   
                   SELECT  
                   month, shop, sladosti, other 
                   FROM  dat PIVOT 
                   (SUM(total) FOR category IN ( 'Сладости' sladosti, 'Другое' other ) as pivot_table)
    
    """
    query = f""" SELECT
                        month,
                        shop,
                        SUM(CASE WHEN category = 'Сладости' THEN total ELSE 0 END) as sladosti,
                        SUM(CASE WHEN category = 'Другое' THEN total ELSE 0 END) as other
                        FROM (
                            SELECT
                                strftime('%Y-%m', month) as month,
                                shop,
                                category,
                                SUM(count * price) as total
                            FROM django_app_products
                            WHERE month BETWEEN '{param_date_from.strftime("%Y-%m-%d")}' AND '{param_date_to.strftime("%Y-%m-%d")}'
                            GROUP BY strftime('%Y-%m', month), shop, category
                        ) as dat
                        GROUP BY month, shop;
                   """
    # print(query)
    cursor.execute(query)
    data = cursor.fetchall()

    filter_date = models.Products.objects.filter(month__gte=param_date_from).filter(
        month__lte=param_date_to
    )
    data_1 = {}
    for i in filter_date:
        month_key = str(i.month.strftime("%Y-%m"))
        shop_key = str(i.shop)
        category_key = str(i.category)

        if month_key not in data_1:
            data_1[month_key] = {}

        if shop_key not in data_1[month_key]:
            data_1[month_key][shop_key] = {}

        if category_key not in data_1[month_key][shop_key]:
            data_1[month_key][shop_key][category_key] = 0

        old_totalPrice = (
            data_1.get(month_key, {}).get(shop_key, {}).get(category_key, 0)
        )
        data_1[month_key][shop_key][category_key] = old_totalPrice + i.count * i.price

    data_2 = []

    for k1, v1 in data_1.items():
        for k2, v2 in v1.items():
            sladosti = v2.get("Сладости", 0)
            other = v2.get("Другое", 0)
            data_2.append([k1, k2, sladosti, other])
    data_2 = sorted(data_2, key=lambda x: (x[0], x[1]))
    return Response(data={"messgae": data_2, "message_2": data})
