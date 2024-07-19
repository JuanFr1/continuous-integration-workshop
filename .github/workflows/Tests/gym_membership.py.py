class GymMembershipSystem:
    MEMBERSHIP_PLANS = {
        'Basic': {'base_cost': 50, 'features': ['None', 'Group Classes', 'Locker Access'], 'feature_costs': [0, 20, 10]},
        'Premium': {'base_cost': 100, 'features': ['None', 'Personal Training', 'Group Classes', 'Locker Access'], 'feature_costs': [0, 50, 20, 10], 'is_premium': True},
        'Family': {'base_cost': 150, 'features': ['None', 'Group Classes', 'Locker Access', 'Child Care'], 'feature_costs': [0, 20, 10, 30]}
    }

    PREMIUM_SURCHARGE_RATE = 0.15

    def __init__(self):
        self.selected_plan = None
        self.selected_features = []
        self.num_members = 1  # Default to 1, can be adjusted as per user input

    def display_membership_plans(self):
        print("Available Membership Plans:")
        for plan, details in self.MEMBERSHIP_PLANS.items():
            base_cost = details['base_cost']
            features = ", ".join(details['features'])
            print(f"{plan}: Base Cost ${base_cost}, Features: {features}")
        print()

    def select_membership_plan(self):
        while True:
            self.display_membership_plans()
            plan = input("Select a membership plan (Basic, Premium, Family): ").strip()
            if plan in self.MEMBERSHIP_PLANS:
                self.selected_plan = plan
                break
            else:
                print("Invalid selection. Please choose a valid membership plan.")
        print(f"You have selected the {self.selected_plan} membership plan.\n")

    def select_additional_features(self):
        while True:
            features_str = input(f"Select additional features separated by commas ({', '.join(self.MEMBERSHIP_PLANS[self.selected_plan]['features'])}). Select 'None' for no additional features: ").strip()
            selected_features = [f.strip() for f in features_str.split(',')]
            invalid_features = [f for f in selected_features if f not in self.MEMBERSHIP_PLANS[self.selected_plan]['features']]
            if invalid_features:
                print(f"Invalid features selected: {', '.join(invalid_features)}. Please select valid features.")
            else:
                if 'None' in selected_features:
                    self.selected_features = []
                else:
                    self.selected_features = selected_features
                break
        print(f"Additional features selected: {', '.join(self.selected_features) if self.selected_features else 'None'}\n")

    def calculate_base_cost(self):
        base_cost = self.MEMBERSHIP_PLANS[self.selected_plan]['base_cost']
        total_base_cost = base_cost * self.num_members
        return total_base_cost

    def calculate_additional_cost(self):
        total_cost = 0
        for feature in self.selected_features:
            index = self.MEMBERSHIP_PLANS[self.selected_plan]['features'].index(feature)
            cost = self.MEMBERSHIP_PLANS[self.selected_plan]['feature_costs'][index]
            total_cost += cost
        total_additional_cost = total_cost * self.num_members
        return total_additional_cost

    def calculate_total_cost(self):
        base_cost = self.calculate_base_cost()
        additional_cost = self.calculate_additional_cost()
        total_cost = base_cost + additional_cost

        if 'is_premium' in self.MEMBERSHIP_PLANS[self.selected_plan] and self.MEMBERSHIP_PLANS[self.selected_plan]['is_premium']:
            total_cost += total_cost * self.PREMIUM_SURCHARGE_RATE

        return total_cost

    def apply_group_discount(self, total_cost):
        if self.num_members >= 2:
            discount = 0.1 * total_cost
            total_cost -= discount
        return total_cost

    def apply_special_discount(self, total_cost):
        if total_cost > 400:
            total_cost -= 50
        elif total_cost > 200:
            total_cost -= 20
        return total_cost

    def is_membership_available(self):
        if self.selected_plan not in self.MEMBERSHIP_PLANS:
            return False
        for feature in self.selected_features:
            if feature not in self.MEMBERSHIP_PLANS[self.selected_plan]['features']:
                return False
        return True

    def confirm_membership(self):
        while True:
            print("\nMembership Details:")
            print(f"Selected Membership Plan: {self.selected_plan}")
            print(f"Number of Members: {self.num_members}")
            print(f"Additional Features: {', '.join(self.selected_features) if self.selected_features else 'None'}")

            try:
                total_cost = self.calculate_total_cost()
                original_cost = total_cost

                total_cost = self.apply_group_discount(total_cost)
                group_discount = original_cost - total_cost

                total_cost = self.apply_special_discount(total_cost)
                special_discount = original_cost - total_cost - group_discount

                print(f"\nTotal Cost before discounts: ${original_cost:.2f}")
                if group_discount > 0:
                    print(f"Group Membership Discount: ${group_discount:.2f}")
                if special_discount > 0:
                    print(f"Special Discount: ${special_discount:.2f}")

                final_cost = total_cost
                print(f"\nFinal Total Cost after discounts: ${final_cost:.2f}")

                while True:
                    confirm = input("\nDo you want to confirm this membership plan? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        return int(final_cost)  # Return total cost as positive integer
                    elif confirm == 'no':
                        edit_or_cancel = input("Do you want to edit your selection (edit) or cancel (cancel)?: ").strip().lower()
                        if edit_or_cancel == 'edit':
                            return -2  # Return -2 if editing is chosen
                        elif edit_or_cancel == 'cancel':
                            print("Purchase canceled.")
                            return -1  # Return -1 if purchase is canceled
                        else:
                            print("Invalid input. Please enter 'edit' or 'cancel'.\n")
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.\n")

            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return -1

    def start_membership_process(self):
        while True:
            try:
                self.select_membership_plan()

                while True:
                    self.num_members = int(input("Enter the number of members signing up: "))
                    if self.num_members >= 1:
                        break
                    else:
                        print("Invalid number of members. Please enter at least 1.")

                self.select_additional_features()

                if self.is_membership_available():
                    total_cost = self.confirm_membership()
                    if total_cost == -1:
                        break  # Stop the process if canceled
                    elif total_cost == -2:
                        continue  # Restart the process if editing
                    else:
                        print(f"\nMembership confirmed. Final Total Cost: ${total_cost:.2f}")
                        break  # Confirm membership and stop the process
                else:
                    print("Selected options are not available. Please choose again.\n")

            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                break


if __name__ == "__main__":
    gym_system = GymMembershipSystem()
    gym_system.start_membership_process()
