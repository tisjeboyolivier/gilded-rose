# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if "Sulfuras" in item.name:     # Does not decrease in quality nor date
                item.sell_in += 1
                item.quality = 80
            elif item.name == "Aged Brie":  # Gains quality
                item.quality = min(50, item.quality+1)
                if item.sell_in <= 0:
                    item.quality = min(50, item.quality+1)
            elif "Backstage passes" in item.name:   # 0 quality after date passed, increases in certain ranges
                if item.sell_in <= 0:
                    item.quality = 0
                elif 0 <= item.sell_in <= 5:
                    item.quality = min(50, item.quality+3)
                elif 6 <= item.sell_in <= 10:
                    item.quality = min(50, item.quality+2)
                else:
                    item.quality = min(50, item.quality+1)
            elif "Conjured" in item.name:   # Drops in quality twice as fast as standard items
                item.quality = max(0, item.quality-2)
                if item.sell_in <= 0:
                    item.quality = max(0, item.quality-2)
            else:  # Standard items
                item.quality = max(0, item.quality-1)
                if item.sell_in <= 0:
                    item.quality = max(0, item.quality-1)
            item.sell_in -= 1

    def old_update_quality(self):
        for item in self.items:
            if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
