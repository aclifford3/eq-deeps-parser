'''Tests for eq_deeps_parser.py'''

import unittest
import eq_deeps_parser


class TestEqDeepsParser(unittest.TestCase):
    '''Tests for eq_deeps_parser.py'''
    def test_get_contribution_from_melee_dmg_log(self):
        '''Get a contribution when combat log is a damage dealt event'''
        log = '[Tue Jul 21 05:12:05 2020] You kick Sssszzz the Stone for 1 point of damage.'

        actual = eq_deeps_parser.get_contribution(log)
        expected = eq_deeps_parser.Contribution('You', 'Sssszzz the Stone', 1, 0)

        self.assertEqual(expected.participant, actual.participant)
        self.assertEqual(expected.target, actual.target)
        self.assertEqual(expected.damage_dealt, actual.damage_dealt)
        self.assertEqual(expected.healing_dealt, actual.healing_dealt)

    def test_get_contribution_from_healing_log(self):
        '''Get contribution when combat log is healing event'''
        log = '[Tue Jul 21 05:12:05 2020] Wocas has healed you for 15 points of damage.'

        actual = eq_deeps_parser.get_contribution(log)
        expected = eq_deeps_parser.Contribution('Wocas', 'you', 0, 15)

        self.assertEqual(expected.participant, actual.participant)
        self.assertEqual(expected.target, actual.target)
        self.assertEqual(expected.damage_dealt, actual.damage_dealt)
        self.assertEqual(expected.healing_dealt, actual.healing_dealt)

    def test_get_contribution_damage_shield_log(self):
        '''In different logs participant capitalization is different'''
        log = '[Fri Jul 24 19:32:04 2020] a belligerent beach bum was hit by non-melee for 7 points of damage.'

        actual = eq_deeps_parser.get_contribution(log)
        expected = eq_deeps_parser.Contribution('Damage Shield', 'a belligerent beach bum', 7, 0)

        self.assertEqual(expected.participant, actual.participant)
        self.assertEqual(expected.target, actual.target)
        self.assertEqual(expected.damage_dealt, actual.damage_dealt)
        self.assertEqual(expected.healing_dealt, actual.healing_dealt)

if __name__ == '__main__':
    unittest.main()
