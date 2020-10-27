# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):

    def print_items(self, day, items):
        print(f"\n-------- day {day} --------")
        print("name, sellIn, quality")
        for item in items:
            print(item, "")

    def test_no_negative_quality(self):
        items = [
            Item(name="Elixir of the Mongoose", sell_in=1, quality=-5),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=1, quality=50),
            Item(name="Conjured Mana Cake", sell_in=1, quality=3)
        ]
        for day in range(100):
            self.print_items(day, items)
            GildedRose(items).update_quality()
            self.print_items(day, items)

            for item in items:
                self.assertGreaterEqual(item.quality, 0, msg=item.name+"'s quality lower than 0")

    def test_max_quality(self):
        items = [
            Item(name="Aged Brie", sell_in=2, quality=777),
            Item(name="Aged Brie", sell_in=2, quality=46),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=100, quality=52),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=6, quality=45)
        ]
        for day in range(100):
            self.print_items(day, items)
            GildedRose(items).update_quality()
            self.print_items(day, items)

            for item in items:
                self.assertLessEqual(item.quality, 50, msg=item.name+"'s quality more than 50")

    def test_static_sulfuras(self):
        items = [
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=1, quality=800)
        ]
        pre_update_sell_dates = []
        for day in range(100):
            pre_update_sell_dates.clear()
            self.print_items(day, items)
            for item in items:
                pre_update_sell_dates.append(item.sell_in)
            GildedRose(items).update_quality()
            self.print_items(day, items)

            for pre_update_sell_date, post_update_item in zip(pre_update_sell_dates, items):
                self.assertEqual(post_update_item.quality, 80, msg=post_update_item.name+"'s quality is not 80")
                self.assertEqual(post_update_item.sell_in, pre_update_sell_date, msg=post_update_item.name+"'s sell_in date changed")

    def test_standard_item_decrease(self):
        items = [
            Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
            Item(name="Elixir of the Mongoose", sell_in=1, quality=20)
        ]
        pre_update_qualities = []
        for day in range(100):
            pre_update_qualities.clear()
            self.print_items(day, items)
            for item in items:
                pre_update_qualities.append(item.quality)
            GildedRose(items).update_quality()
            self.print_items(day, items)

            for pre_update_quality, post_update_item in zip(pre_update_qualities, items):
                if post_update_item.quality > 0:
                    if post_update_item.sell_in < 0 and pre_update_quality >= 2:
                        self.assertEqual(post_update_item.quality, pre_update_quality - 2,
                                         msg=post_update_item.name + "'s quality did not decrease by 2")
                    elif pre_update_quality >= 1:
                        self.assertEqual(post_update_item.quality, pre_update_quality - 1,
                                         msg=post_update_item.name + "'s quality did not decrease by 1")

    def test_conjured_decrease(self):
        items = [
            Item(name="Conjured Elixer of Coolness", sell_in=10, quality=19),
            Item(name="Conjured Mana Cake", sell_in=1, quality=20)
        ]
        pre_update_qualities = []
        for day in range(100):
            pre_update_qualities.clear()
            self.print_items(day, items)
            for item in items:
                pre_update_qualities.append(item.quality)
            GildedRose(items).update_quality()
            self.print_items(day, items)

            for pre_update_quality, post_update_item in zip(pre_update_qualities, items):
                if pre_update_quality > 0:
                    if post_update_item.sell_in < 0 and pre_update_quality >= 4:
                        self.assertEqual(post_update_item.quality, pre_update_quality - 4,
                                         msg=post_update_item.name + "'s quality did not decrease by 4")
                    elif pre_update_quality >= 2:
                        self.assertEqual(post_update_item.quality, pre_update_quality - 2,
                                         msg=post_update_item.name + "'s quality did not decrease by 2")

    def test_brie_increase(self):
        items = [
            Item(name="Aged Brie", sell_in=2, quality=0),
            Item(name="Aged Brie", sell_in=-10, quality=3)
        ]
        pre_update_qualities = []
        for day in range(100):
            pre_update_qualities.clear()
            self.print_items(day, items)
            for item in items:
                pre_update_qualities.append(item.quality)
            GildedRose(items).update_quality()
            self.print_items(day, items)

            for pre_update_quality, post_update_item in zip(pre_update_qualities, items):
                if post_update_item.sell_in < 0 and pre_update_quality <= 48:
                    self.assertEqual(post_update_item.quality, pre_update_quality+2,
                                     msg=post_update_item.name+"'s quality did not increase by 2")
                elif pre_update_quality <= 49:
                    self.assertEqual(post_update_item.quality, pre_update_quality+1,
                                     msg=post_update_item.name+"'s quality did not increase by 1")

    def test_backstage_passes_increase(self):
        items = [
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=20, quality=10),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=9, quality=10),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=6, quality=10),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=3, quality=10)
        ]
        pre_update_qualities = []
        for day in range(100):
            pre_update_qualities.clear()
            self.print_items(day, items)
            for item in items:
                pre_update_qualities.append(item.quality)
            GildedRose(items).update_quality()
            self.print_items(day, items)

            for pre_update_quality, post_update_item in zip(pre_update_qualities, items):
                if post_update_item.sell_in < 0:
                    self.assertEqual(post_update_item.quality, 0,
                                     msg=post_update_item.name+"'s quality did not become 0")
                elif 0 <= post_update_item.sell_in < 5:
                    self.assertEqual(post_update_item.quality, pre_update_quality+3,
                                     msg=post_update_item.name+"'s quality did not increase by 3")
                elif 5 <= post_update_item.sell_in < 10:
                    self.assertEqual(post_update_item.quality, pre_update_quality+2,
                                     msg=post_update_item.name+"'s quality did not increase by 2")
                else:
                    self.assertEqual(post_update_item.quality, pre_update_quality+1,
                                     msg=post_update_item.name+"'s quality did not increase by 1")


if __name__ == '__main__':
    unittest.main()
