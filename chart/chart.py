import random
from .colours import generate_colours


def chart_color(data_element_length) -> list:

    colors = generate_colours(None)
    color_key = list(colors.keys())

    return [
        color_key[random.randint(0, len(color_key))] for i in range(1, data_element_length)
    ]


def order_data(data: list) -> list:

    temp_storage = [list() for i in range(len(data[0]))]

    for d in data:

        for i in range(len(d)):

            temp_storage[i].append(d[i])

    return temp_storage


def generate_option(title: str, chart_type: str) -> dict:

    option_dict = {
        "responsive": True,
        "maintainAspectRatio": False,
        "title": {
            "display": True,
            "text": title,
            "fontSize": 20,
            "fontFamily": "Helvetica"
        },
        "legend": {
            "display": True,
            "position": "bottom"
        },
        "tooltips": {}
    }

    if title in ["bar", "line"]:

       option_dict.update(
           {
               "scales": {
                    "yAxes": [
                        {
                            "ticks": {
                                "beginAtZero": True
                            }
                        }
                    ]
                }
           }
       ) 

    return option_dict


def generate_bar(title: str, labelname: str, data: list):

    data_element_length = len(data[0])
    color_name_list = chart_color(data_element_length)
    
    temp_storage = order_data(data)              

    return {
        "type": "bar",
        "data": {
            "labels": temp_storage[0],
            "datasets": [
                {
                    "label": labelname,
                    "data": temp_storage[i + 1],
                    "backgroundColor": generate_colours(color_name_list[i], alpha=0.1),
                    "borderColor": generate_colours(color_name_list[i]),
                    "borderWidth": 2,
                } for i in range(len(temp_storage[1:]))
            ]
        },
        "options": generate_option(title, "bar")
    }


def generate_line(title: str, labelname: str, data: list, fill: bool=False):

    data_element_length = len(data[0])
    color_name_list = chart_color(data_element_length)
    
    temp_storage = order_data(data)            


    return {
        "type": "line",
        "data": {
            "labels": temp_storage[0],
            "datasets": [
                {
                    "label": labelname,
                    "data": temp_storage[i + 1],
                    "backgroundColor": generate_colours(color_name_list[i], alpha=0.2),
                    "borderColor": generate_colours(color_name_list[i]),
                    "borderWidth": 2,
                    "fill": fill,
                    "lineTension": 0.1
                } for i in range(len(temp_storage[1:]))
            ]
        },
        "options": generate_option(title, "line")
    }


def generate_pie(title: str, labelname: str, data: list) -> dict:

    data_element_length = len(data)
    color_name_list = chart_color(data_element_length)
    print(color_name_list)
    temp_storage = order_data(data)

    background_color = [
        generate_colours(color_name, alpha=0.5) for color_name in color_name_list
    ]

    print(background_color)
    return {
        "type": "pie",
        "data": {
            "labels": temp_storage[0],
            "datasets": [
                {
                    "label": labelname,
                    "data": temp_storage[i + 1],
                    "backgroundColor": background_color
                } for i in range(len(temp_storage[1:]))
            ]
        },
        "options": generate_option(title, "pie")
    }


def generate_scatter_plot(title: str, labelname: list, data: list) -> dict:

    color_name_list = chart_color(len(data[0]))
    
    temp_storage = order_data(data)

    return {
        "type": "scatter",
        "data": {
            "datasets": [
                {
                    "label": str(index),
                    "data": [
                        {
                            "x": d_0,
                            "y": d[index]
                        } for index, d_0 in enumerate(temp_storage[0])
                    ],
                    "backgroundColor": generate_colours(color_name_list[index], alpha=0.5),
                    "borderColor": generate_colours(color_name_list[index]),
                    "borderWidth": 2,
                    "lineTension": 0.1
                } for index, d in enumerate(temp_storage[1:])
            ]
        },
        "options": generate_option(title, "pie")
    }
