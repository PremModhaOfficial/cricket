import unittest

from cricket_lib.enums import Opted


class MyTestCase(unittest.TestCase):
	
	def test_opted_opposite(self):
		_not = Opted.NOT
		bat = Opted.BAT
		bowl = Opted.BOWL
		self.assertEqual(_not, _not.opposite())
		self.assertEqual(bat, bowl.opposite())
		self.assertEqual(bowl, bat.opposite())


if __name__ == '__main__':
	unittest.main()
