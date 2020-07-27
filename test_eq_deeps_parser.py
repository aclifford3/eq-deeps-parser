import unittest

import eq_deeps_parser


class TestLogParser(unittest.TestCase):
    def test_get_combat_event_DamageDealtEvent(self):
        log = '[Tue Jul 21 05:12:05 2020] You kick Sssszzz the Stone for 1 point of damage.'

        actual = eq_deeps_parser.get_combat_event(log)
        expected = eq_deeps_parser.CombatEvent('You', 'Sssszzz the Stone', 1, 0)

        self.assertEqual(expected.actor, actual.actor)
        self.assertEqual(expected.target, actual.target)
        self.assertEqual(expected.damage_dealt, actual.damage_dealt)
        self.assertEqual(expected.healing_dealt, actual.healing_dealt)

    def test_get_combat_event_HealingEvent(self):
        log = '[Tue Jul 21 05:12:05 2020] Wocas has healed you for 15 points of damage.'

        actual = eq_deeps_parser.get_combat_event(log)
        expected = eq_deeps_parser.CombatEvent('Wocas', 'you', 0, 15)

        self.assertEqual(expected.actor, actual.actor)
        self.assertEqual(expected.target, actual.target)
        self.assertEqual(expected.damage_dealt, actual.damage_dealt)
        self.assertEqual(expected.healing_dealt, actual.healing_dealt)


if __name__ == '__main__':
    unittest.main()
