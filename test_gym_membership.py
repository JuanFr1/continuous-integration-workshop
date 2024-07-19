import unittest
from unittest import mock
from gym_membership import GymMembershipSystem

class TestGymMembershipSystem(unittest.TestCase):
    def setUp(self):
        self.gym_system = GymMembershipSystem()

    def test_calculate_base_cost(self):
        self.gym_system.selected_plan = 'Basic'
        self.gym_system.num_members = 1
        self.assertEqual(self.gym_system.calculate_base_cost(), 50)

        self.gym_system.num_members = 3
        self.assertEqual(self.gym_system.calculate_base_cost(), 150)

    def test_calculate_additional_cost(self):
        self.gym_system.selected_plan = 'Basic'
        self.gym_system.selected_features = ['Group Classes', 'Locker Access']
        self.gym_system.num_members = 1
        self.assertEqual(self.gym_system.calculate_additional_cost(), 30)

        self.gym_system.num_members = 2
        self.assertEqual(self.gym_system.calculate_additional_cost(), 60)

        self.gym_system.selected_features = ['None']
        self.assertEqual(self.gym_system.calculate_additional_cost(), 0)

    def test_calculate_total_cost(self):
        self.gym_system.selected_plan = 'Basic'
        self.gym_system.selected_features = ['Group Classes']
        self.gym_system.num_members = 1
        self.assertEqual(self.gym_system.calculate_total_cost(), 70)

        self.gym_system.selected_plan = 'Premium'
        self.gym_system.selected_features = ['Personal Training']
        self.gym_system.num_members = 1
        expected_cost = 100 + 50 + (150 * 0.15)  # Base cost + feature cost + surcharge
        self.assertEqual(self.gym_system.calculate_total_cost(), expected_cost)

    def test_apply_group_discount(self):
        total_cost = 200
        self.gym_system.num_members = 1
        self.assertEqual(self.gym_system.apply_group_discount(total_cost), 200)

        self.gym_system.num_members = 2
        self.assertEqual(self.gym_system.apply_group_discount(total_cost), 180)

    def test_apply_special_discount(self):
        self.assertEqual(self.gym_system.apply_special_discount(500), 450)
        self.assertEqual(self.gym_system.apply_special_discount(300), 280)
        self.assertEqual(self.gym_system.apply_special_discount(150), 150)

    def test_is_membership_available(self):
        self.gym_system.selected_plan = 'Basic'
        self.gym_system.selected_features = ['Group Classes']
        self.assertTrue(self.gym_system.is_membership_available())

        self.gym_system.selected_features = ['Invalid Feature']
        self.assertFalse(self.gym_system.is_membership_available())

    def test_confirm_membership_cancel(self):
        self.gym_system.selected_plan = 'Basic'
        self.gym_system.selected_features = ['Group Classes']
        self.gym_system.num_members = 1

        with mock.patch('builtins.input', side_effect=['no', 'cancel']):
            self.assertEqual(self.gym_system.confirm_membership(), -1)

    def test_confirm_membership_edit(self):
        self.gym_system.selected_plan = 'Basic'
        self.gym_system.selected_features = ['Group Classes']
        self.gym_system.num_members = 1

        with mock.patch('builtins.input', side_effect=['no', 'edit']):
            self.assertEqual(self.gym_system.confirm_membership(), -2)

    def test_confirm_membership_yes(self):
        self.gym_system.selected_plan = 'Basic'
        self.gym_system.selected_features = ['Group Classes']
        self.gym_system.num_members = 1

        with mock.patch('builtins.input', side_effect=['yes']):
            total_cost = self.gym_system.calculate_total_cost()
            self.assertEqual(self.gym_system.confirm_membership(), int(total_cost))

if __name__ == '__main__':
    unittest.main()
