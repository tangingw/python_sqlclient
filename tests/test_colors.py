import unittest
from chart.colours import generate_colours


class TestColour(unittest.TestCase):

    def setUp(self):

        self.alpha = 0.5
        self.colours = {
            "maroon": (128,0,0,self.alpha), "olive": (128,128,0,self.alpha),
            "green": (0,128,0,self.alpha), "purple": (128,0,128,self.alpha),
            "teal": (0,128,128,self.alpha), "navy": (0,0,128,self.alpha),
            "dark red": (139,0,0,self.alpha), "brown": (165,42,42,self.alpha),
            "firebrick": (178,34,34,self.alpha), "crimson": (220,20,60,self.alpha), 
            "tomato": (255,99,71,self.alpha), "coral": (255,127,80,self.alpha),
            "indian_red": (205,92,92,self.alpha), "light_coral": (240,128,128,self.alpha),
            "dark_salmon": (233,150,122,self.alpha), "salmon": (250,128,114,self.alpha),
            "light_salmon": (255,160,122,self.alpha), "orange_red": (255,69,0,self.alpha),
            "dark_orange": (255,140,0,self.alpha), "orange": (255,165,0,self.alpha),
            "gold": (255,215,0,self.alpha), "dark_golden_rod": (184,134,11,self.alpha),
            "golden_rod": (218,165,32,self.alpha), "pale_golden_rod": (238,232,170,self.alpha),
            "dark_khaki": (189,183,107,self.alpha), "khaki": (240,230,140,self.alpha), 
            "yellow_green": (154,205,50,self.alpha), "dark_olive_green": (85,107,47,self.alpha),
            "olive_drab": (107,142,35,self.alpha), "lawn_green": (124,252,0,self.alpha),
            "chart_reuse": (127,255,0,self.alpha), "green_yellow": (173,255,47,self.alpha),
            "dark_green": (0,100,0,self.alpha), "forest_green": (34,139,34,self.alpha),
            "lime_green": (50,205,50,self.alpha)        
        }
    
    def test_color(self):

        for colour, colour_tuple in self.colours.items():

            colour_tuple_str = "rgba({})".format(
                ",".join([str(x) for x in colour_tuple])
            )

            self.assertEqual(
                generate_colours(colour, alpha=self.alpha),
                colour_tuple_str
            )

    def test_rgb_code(self):

        for _, colour_tuple in self.colours.items():

            colour_tuple_str = "rgba({})".format(
                ",".join([str(x) for x in colour_tuple])
            )

            self.assertEqual(
                generate_colours(rgb_code=colour_tuple[:3], alpha=self.alpha),
                colour_tuple_str
            )
