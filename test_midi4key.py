import sys
import unittest
from unittest.mock import Mock
sys.modules['kmk.keys'] = Mock()
sys.modules['kmk.kmk_keyboard'] = Mock()
sys.modules['kmk.utils'] = Mock()


class Key:
    pass
sys.modules['kmk.keys'].Key = Key

class DVP():
    def __init__(self):
        self.GRV = '`'
        self.QUOT = '\''
        self.BSPC = '⇐'
        self.SPC = ' '

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
        ('S', 's'),
        ('F', 'f'),
        ('SCP', 'd'),
        ('SCPXIn', 'done'),
        ('FCPUuie', 'buo'), # not buie
        # [FCP][U][uie][]
        ('FCPUIua', 'biu'), # # not baia
        # [FCP][U][uia][]
        # actually biu is weird too
        ('FCNXIUuiencs', 'zcol'), # Not xhuiel - not cross-group
        # [FCN][XIU][uie][ncs]
        # 
        ('FCPRIzcs', 'Bl'), # not Baie. 2nd group doesn't generate so the flip-and-E doesn't apply
        # [FCP][RI][][zcs] - RI doesn't generate a vowel so it shouldn't add the trailing E (or generate the vowel side at all)
        ]

class TestGeneration(unittest.TestCase):
    def assertGenerated(self, generated, expected):
        self.assertEqual("".join(generated), expected)

    def test_required(self):
        for keys, output in required:
            with self.subTest(i=keys,o=output):
                sut = Chord()
                for key in keys:
                    sut.add(key)
                self.assertGenerated(sut.result(), output)



if __name__ == '__main__':
    unittest.main()

