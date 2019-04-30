import re


def generate_colours(colour_name: str=None, rgb_code: tuple=(), alpha: int=1.0):

    defined_color_dict = {
        "black": (0,0,0,alpha), "white": (255,255,255,alpha),
        "red": 	(255,0,0,alpha), "lime": (0,255,0,alpha),
        "blue": (0,0,255,alpha), "yellow": (255,255,0,alpha),
        "cyan": (0,255,255,alpha), "aqua": (0,255,255,alpha),
        "magenta": (255,0,255,alpha), "fuchsia": (255,0,255,alpha),
        "silver": (192,192,192,alpha),
        "maroon": (128,0,0,alpha), "olive": (128,128,0,alpha),
        "green": (0,128,0,alpha), "purple": (128,0,128,alpha),
        "teal": (0,128,128,alpha), "navy": (0,0,128,alpha),
        "dark red": (139,0,0,alpha), "brown": (165,42,42,alpha),
        "firebrick": (178,34,34,alpha), "crimson": (220,20,60,alpha), 
        "tomato": (255,99,71,alpha), "coral": (255,127,80,alpha),
        "indian_red": (205,92,92,alpha), "light_coral": (240,128,128,alpha),
        "dark_salmon": (233,150,122,alpha), "salmon": (250,128,114,alpha),
        "light_salmon": (255,160,122,alpha), "orange_red": (255,69,0,alpha),
        "dark_orange": (255,140,0,alpha), "orange": (255,165,0,alpha),
        "gold": (255,215,0,alpha), "dark_golden_rod": (184,134,11,alpha),
        "golden_rod": (218,165,32,alpha), "pale_golden_rod": (238,232,170,alpha),
        "dark_khaki": (189,183,107,alpha), "khaki": (240,230,140,alpha), 
        "yellow_green": (154,205,50,alpha), "dark_olive_green": (85,107,47,alpha),
        "olive_drab": (107,142,35,alpha), "lawn_green": (124,252,0,alpha),
        "chart_reuse": (127,255,0,alpha), "green_yellow": (173,255,47,alpha),
        "dark_green": (0,100,0,alpha), "forest_green": (34,139,34,alpha),
        "lime_green": (50,205,50,alpha),
        "light_green": (144,238,144,alpha), "pale_green": (152,251,152,alpha),
        "dark_sea_green": (143,188,143,alpha), "medium_spring_green": (0,250,154,alpha),
        "spring_green": (0,255,127,alpha), "sea_green": (46,139,87,alpha), 
        "medium_aqua_marine": (102,205,170,alpha),"medium_sea_green": (60,179,113,alpha),
        "light_sea_green": (32,178,170,alpha), "dark_slate_gray": (47,79,79,alpha),
        "dark_cyan": (0,139,139,alpha), "light_cyan": (224,255,255,alpha),
        "dark_turquoise": (0,206,209,alpha), "turquoise": (64,224,208,alpha),
        "medium_turquoise": (72,209,204,alpha), "pale_turquoise": (175,238,238,alpha),
        "aqua_marine": (127,255,212,alpha),"powder_blue": (176,224,230,alpha),
        "cadet_blue": (95,158,160,alpha),"steel_blue": (70,130,180,alpha),
        "corn_flower_blue": (100,149,237,alpha),
        "deep_sky_blue": (0,191,255,alpha), "dodger_blue": (30,144,255,alpha),
        "light_blue": (173,216,230,alpha), "sky_blue": (135,206,235,alpha),
        "light_sky_blue": (135,206,250,alpha), "midnight_blue": (25,25,112,alpha),
        "dark_blue": (0,0,139,alpha), "medium_blue": (0,0,205,alpha),
        "dim_gray": (105,105,105,alpha), "dim_grey": (105,105,105, alpha),
        "gray": (128,128,128,alpha), "grey": (128,128,128,alpha),
        "dark_gray": (169,169,169,alpha),  "dark_grey": (169,169,169,alpha),
    }


    colour_raw_data = """
        royal blue 	#4169E1 	(65,105,225)
        blue violet 	#8A2BE2 	(138,43,226)
        indigo 	#4B0082 	(75,0,130)
        dark slate blue 	#483D8B 	(72,61,139)
        slate blue 	#6A5ACD 	(106,90,205)
        medium slate blue 	#7B68EE 	(123,104,238)
        medium purple 	#9370DB 	(147,112,219)
        dark magenta 	#8B008B 	(139,0,139)
        dark violet 	#9400D3 	(148,0,211)
        dark orchid 	#9932CC 	(153,50,204)
        medium orchid 	#BA55D3 	(186,85,211)
        purple 	#800080 	(128,0,128)
        thistle 	#D8BFD8 	(216,191,216)
        plum 	#DDA0DD 	(221,160,221)
        violet 	#EE82EE 	(238,130,238)
        magenta / fuchsia 	#FF00FF 	(255,0,255)
        orchid 	#DA70D6 	(218,112,214)
        medium violet red 	#C71585 	(199,21,133)
        pale violet red 	#DB7093 	(219,112,147)
        deep pink 	#FF1493 	(255,20,147)
        hot pink 	#FF69B4 	(255,105,180)
        light pink 	#FFB6C1 	(255,182,193)
        pink 	#FFC0CB 	(255,192,203)
        antique white 	#FAEBD7 	(250,235,215)
        beige 	#F5F5DC 	(245,245,220)
        bisque 	#FFE4C4 	(255,228,196)
        blanched almond 	#FFEBCD 	(255,235,205)
        wheat 	#F5DEB3 	(245,222,179)
        corn silk 	#FFF8DC 	(255,248,220)
        lemon chiffon 	#FFFACD 	(255,250,205)
        light golden rod yellow 	#FAFAD2 	(250,250,210)
        light yellow 	#FFFFE0 	(255,255,224)
        saddle brown 	#8B4513 	(139,69,19)
        sienna 	#A0522D 	(160,82,45)
        chocolate 	#D2691E 	(210,105,30)
        peru 	#CD853F 	(205,133,63)
        sandy brown 	#F4A460 	(244,164,96)
        burly wood 	#DEB887 	(222,184,135)
        tan 	#D2B48C 	(210,180,140)
        rosy brown 	#BC8F8F 	(188,143,143)
        moccasin 	#FFE4B5 	(255,228,181)
        navajo white 	#FFDEAD 	(255,222,173)
        peach puff 	#FFDAB9 	(255,218,185)
        misty rose 	#FFE4E1 	(255,228,225)
        lavender blush 	#FFF0F5 	(255,240,245)
        linen 	#FAF0E6 	(250,240,230)
        old lace 	#FDF5E6 	(253,245,230)
        papaya whip 	#FFEFD5 	(255,239,213)
        sea shell 	#FFF5EE 	(255,245,238)
        mint cream 	#F5FFFA 	(245,255,250)
        slate gray 	#708090 	(112,128,144)
        light slate gray 	#778899 	(119,136,153)
        light steel blue 	#B0C4DE 	(176,196,222)
        lavender 	#E6E6FA 	(230,230,250)
        floral white 	#FFFAF0 	(255,250,240)
        alice blue 	#F0F8FF 	(240,248,255)
        ghost white 	#F8F8FF 	(248,248,255)
        honeydew 	#F0FFF0 	(240,255,240)
        ivory 	#FFFFF0 	(255,255,240)
        azure 	#F0FFFF 	(240,255,255)
        snow 	#FFFAFA 	(255,250,250)
        dim gray / dim grey 	#696969 	(105,105,105)
        silver 	#C0C0C0 	(192,192,192)
        gainsboro 	#DCDCDC 	(220,220,220)
        white smoke 	#F5F5F5 	(245,245,245)
    """

    colour_data = colour_raw_data.split("\n")[1:-1]

    for colour in colour_data:

        if len(colour) > 0:

            colour_raw_name, _, rgb_tuple = re.sub(r"^\s+", "", colour).split("\t")
            colour_raw_name = '_'.join(colour_raw_name.split(" "))
            defined_color_dict[colour_raw_name] = tuple([int(x) for x in rgb_tuple[2:-2].split(",")] + [alpha])

    if colour_name:
    
        return  "rgba({})".format(
            ','.join(
                [str(x) for x in defined_color_dict[colour_name]]
            )
        )

    if len(rgb_code) == 3:

        return 'rgba({0},{1})'.format(
            ','.join([str(x) for x in rgb_code]), alpha
        )

    return defined_color_dict