import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

class Membership {
    private String name;
    private String benefits;
    private double cost;
    private boolean isPremium;

    public Membership(String name, String benefits, double cost, boolean isPremium) {
        this.name = name;
        this.benefits = benefits;
        this.cost = cost;
        this.isPremium = isPremium;
    }

    public String getName() {
        return name;
    }

    public String getBenefits() {
        return benefits;
    }

    public double getCost() {
        return cost;
    }

    public boolean isPremium() {
        return isPremium;
    }

    public void display() {
        System.out.println(name + " Membership:");
        System.out.println("Benefits: " + benefits);
        System.out.println("Cost: $" + cost);
    }
}

public class GymMembershipSelection {
    public static void main(String[] args) {
        ArrayList<Membership> memberships = new ArrayList<>();
        memberships.add(new Membership("Basic", "Access to gym equipment", 20.0, false));
        memberships.add(new Membership("Premium", "Access to gym equipment, group classes, and pool", 50.0, true));
        memberships.add(new Membership("Family", "Access to gym equipment, group classes, pool, and family discounts",
                80.0, false));

        Map<String, Double> additionalFeatures = new HashMap<>();
        additionalFeatures.put("Personal Trainer", 30.0);
        additionalFeatures.put("Nutrition Plan", 20.0);
        additionalFeatures.put("Spa Access", 25.0);

        Scanner scanner = new Scanner(System.in);

        System.out.println("Available Membership Plans:");
        for (int i = 0; i < memberships.size(); i++) {
            System.out.println((i + 1) + ". " + memberships.get(i).getName());
        }

        System.out.print("Select a membership plan (1-3): ");
        int choice = scanner.nextInt();
        Membership selectedMembership = memberships.get(choice - 1);

        System.out.println("You selected the " + selectedMembership.getName() + " plan.");
        selectedMembership.display();

        System.out.println("Would you like to add additional features? (yes/no)");
        String addFeatures = scanner.next();

        double additionalCost = 0;
        if (addFeatures.equalsIgnoreCase("yes")) {
            System.out.println("Available additional features:");
            int featureIndex = 1;
            for (String feature : additionalFeatures.keySet()) {
                System.out.println(featureIndex + ". " + feature + " ($" + additionalFeatures.get(feature) + ")");
                featureIndex++;
            }

            System.out.print("Select additional features (comma-separated, e.g., 1,2): ");
            String features = scanner.next();
            String[] selectedFeatures = features.split(",");

            for (String feature : selectedFeatures) {
                int featureNumber = Integer.parseInt(feature.trim());
                String featureName = (String) additionalFeatures.keySet().toArray()[featureNumber - 1];
                additionalCost += additionalFeatures.get(featureName);
            }
        }

        double totalCost = selectedMembership.getCost() + additionalCost;

        // Apply special offer discounts
        if (totalCost > 400) {
            totalCost -= 50;
        } else if (totalCost > 200) {
            totalCost -= 20;
        }

        // Apply premium membership surcharge
        if (selectedMembership.isPremium()) {
            totalCost *= 1.15;
        }

        // Group membership discount
        System.out.print("How many members are signing up together? ");
        int groupSize = scanner.nextInt();
        if (groupSize >= 2) {
            totalCost *= 0.90;
            System.out.println("A 10% group discount has been applied.");
        }

        System.out.println("Total cost with additional features and discounts: $" + totalCost);

        // User confirmation
        System.out.println("Please confirm your membership selection:");
        selectedMembership.display();
        System.out.println("Additional features cost: $" + additionalCost);
        System.out.println("Total cost: $" + totalCost);
        System.out.print("Confirm membership (yes/no): ");
        String confirm = scanner.next();

        if (confirm.equalsIgnoreCase("yes")) {
            System.out.println("Membership confirmed. Thank you for joining!");
        } else {
            System.out.println("Membership selection canceled. Please start over.");
        }

        scanner.close();
    }
}