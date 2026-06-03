import sys
import unittest
from unittest.mock import Mock
sys.modules['kmk.keys'] = Mock()
sys.modules['kmk.kmk_keyboard'] = Mock()
sys.modules['kmk.utils'] = Mock()


class Key:
    pass

class ModifierKey:
    pass
class ModifiedKey:
    pass
sys.modules['kmk.keys'].Key = Key
sys.modules['kmk.keys'].ModifiedKey= ModifiedKey
sys.modules['kmk.keys'].ModifierKey= ModifierKey

class DVP():
    def __init__(self):
        self.GRV = '`'
        self.QUOT = '\''
        self.BSPC = '⇐'
        self.SPC = ' '
        self.ENTER = '↓'
        self.LEFT_PAREN = '('
        self.RIGHT_PAREN = ')'

    def __getitem__(self, name):
        if name == 'SPC':
            return ' '
        if name == 'LSFT':
            return lambda x: x
        if name == '_':
            return '\''
        return name

    # Doubling up for KC
    def LSFT(self, c):
        return c.upper()

sys.modules['dvp'] = Mock()
sys.modules['dvp'].DVP = DVP
sys.modules['kmk.keys'].KC = DVP()

class Key:
    pass
sys.modules['kmk.keys'].Key = Key


from midi4key import Chord, MTKey

#from dvp import DVP
DVP = DVP()

required = [
        ('S', 's', False),
        ('F', 'f', False),
        ('SCP', 'd', False),
        ('SCPXIn', 'done', True), # 2nd group vowel -> $e
        #('FCPUuie', 'buo'), # not buie
        # [FCP][U][uie][]
        #('FCPUIua', 'biu', False), # # not baia
        # [FCP][U][uia][]
        # actually biu is weird too
        # buie is better! (the e snuck in)
        ('FCPUiu', 'bui', False), # ACTUALLY this is better
        ('FCPIiu', 'bai', False), # The more sane option
        ('FCNXIUuiencs', 'xcol', False), # Not xhuiel - not cross-group
        # [FCN][XIU][uie][ncs]
        ('FCPRIzcs', 'Boue', True),
        # [FCP][RI][][zcs] - RI doesn't generate a vowel so it shouldn't add the trailing E (or generate the vowel side at all)

        ('Nieas', 'neas', False),
        # ('Nieas', 'neas'), # test 2nd-only too?
        ('ieas', '\'s', True),
        ('PXuinz', 'spy', True), # uinz = $y
        ('PRuinzf', 'print', False), # uinz should not generate $y if it's not the entire group 3 + 4

        ('Iias', 'ious', True), # it's an Ii but that's not the entire pattern so it shouldn't generate ai

        ('CRuiazc', 'truck', False), # this broke before
        ('ieas', '\'s', True),
        ('ZPeaz', 'gr', True),
        ]

class TestGeneration(unittest.TestCase):
    def assertGenerated(self, generated, expected):
        self.assertEqual("".join(generated), expected)

    def test_required(self):
        for keys, output, ending in required:
            with self.subTest(i=keys,o=output):
                sut = Chord()
                for key in keys:
                    sut.add(key)
                self.assertGenerated(sut.result(), output)
                # Make sure the word was terminated
                sut.reset()
                for key in 'ua':
                    sut.add(key)
                if ending:
                    self.assertEqual("".join(sut.result()), " a")
                else:
                    self.assertEqual("".join(sut.result()), "a")


if __name__ == '__main__':
    unittest.main()

