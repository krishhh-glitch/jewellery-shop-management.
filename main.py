import os
from dotenv import load_dotenv
from supabase import create_client

# =====================================
# SUPABASE CONNECTION
# =====================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# =====================================
# VIEW INVENTORY
# =====================================

def view_inventory():
    try:
        response = supabase.table("inventory").select("*").execute()
        products = response.data

        print("\n========== JEWELLERY INVENTORY ==========")

        if not products:
            print("No products found.")
            return

        for product in products:
            print("\nItem Code:", product.get("item_code"))
            print("Name:", product.get("name"))
            print("Category:", product.get("category"))
            print("Metal:", product.get("metal_type"))
            print("Gross Weight:", product.get("gross_weight_g"), "grams")
            print("Net Weight:", product.get("net_weight_g"), "grams")
            print("Making Charge:", product.get("making_charge_value"))
            print("----------------------------------------")

    except Exception as error:
        print("Unable to fetch inventory:", error)


# =====================================
# ADD JEWELLERY
# =====================================

def add_jewellery():
    print("\n========== ADD NEW JEWELLERY ==========")

    item_code = input("Enter Item Code: ").strip()
    name = input("Enter Jewellery Name: ").strip()
    category = input("Enter Category: ").strip()
    metal_type = input("Enter Primary Metal Type: ").strip()

    try:
        gross_weight = float(input("Enter Gross Weight: "))
        net_weight = float(input("Enter Net Weight: "))
        stone_weight = float(input("Enter Stone Weight: "))

        making_charge_type = input(
            "Making Charge Type (PER_GRAM/FIXED): "
        ).upper().strip()

        making_charge_value = float(
            input("Enter Making Charge Value: ")
        )

        if not all([item_code, name, category, metal_type]):
            print("All text fields are required.")
            return

        if gross_weight <= 0 or net_weight <= 0:
            print("Weights must be greater than zero.")
            return

        if net_weight > gross_weight:
            print("Net weight cannot exceed gross weight.")
            return

        if stone_weight < 0 or making_charge_value < 0:
            print("Values cannot be negative.")
            return

        if making_charge_type not in ["PER_GRAM", "FIXED"]:
            print("Invalid making charge type.")
            return

        product_data = {
            "item_code": item_code,
            "name": name,
            "category": category,
            "metal_type": metal_type,
            "gross_weight_g": gross_weight,
            "net_weight_g": net_weight,
            "stone_weight_ct": stone_weight,
            "making_charge_type": making_charge_type,
            "making_charge_value": making_charge_value
        }

        supabase.table("inventory").insert(product_data).execute()

        print("\nJewellery added successfully!")

    except ValueError:
        print("Please enter valid numeric values.")

    except Exception as error:
        print("Unable to add jewellery:", error)


# =====================================
# SEARCH JEWELLERY
# =====================================

def search_jewellery():
    print("\n========== SEARCH JEWELLERY ==========")

    item_code = input("Enter Item Code: ").strip()

    try:
        response = (
            supabase.table("inventory")
            .select("*")
            .eq("item_code", item_code)
            .execute()
        )

        products = response.data

        if not products:
            print("No jewellery found.")
            return

        product = products[0]

        print("\n========== PRODUCT DETAILS ==========")
        print("Item Code:", product.get("item_code"))
        print("Name:", product.get("name"))
        print("Category:", product.get("category"))
        print("Metal:", product.get("metal_type"))
        print("Gross Weight:", product.get("gross_weight_g"))
        print("Net Weight:", product.get("net_weight_g"))
        print("Stone Weight:", product.get("stone_weight_ct"))
        print("Making Charge:", product.get("making_charge_value"))
        print("Availability:", product.get("is_available"))

    except Exception as error:
        print("Search failed:", error)


# =====================================
# ADD JEWELLERY COMPONENTS
# =====================================

def add_components():

    print("\n========== ADD JEWELLERY COMPONENTS ==========")

    item_code = input("Enter Jewellery Item Code: ").strip()

    try:
        # Find jewellery item
        response = (
            supabase.table("inventory")
            .select("*")
            .eq("item_code", item_code)
            .execute()
        )

        products = response.data

        if not products:
            print("Jewellery item not found.")
            return

        product = products[0]
        item_id = product["id"]

        print("\nSelected Jewellery:", product["name"])
        print("Item Code:", item_code)

        print("\nComponent Types:")
        print("1. METAL")
        print("2. GEMSTONE")
        print("3. OTHER")

        component_choice = input("Choose Component Type: ").strip()

        component_types = {
            "1": "METAL",
            "2": "GEMSTONE",
            "3": "OTHER"
        }

        if component_choice not in component_types:
            print("Invalid component type.")
            return

        component_type = component_types[component_choice]

        material_name = input(
            "Enter Material Name (Gold, Silver, Diamond, Ruby): "
        ).strip()

        purity = input(
            "Enter Purity (22K, 18K, 925, etc.) or leave blank: "
        ).strip()

        weight = float(input("Enter Weight: "))

        print("\nWeight Units:")
        print("1. Grams (g)")
        print("2. Carats (ct)")

        unit_choice = input("Choose Weight Unit: ").strip()

        if unit_choice == "1":
            weight_unit = "g"
        elif unit_choice == "2":
            weight_unit = "ct"
        else:
            print("Invalid weight unit.")
            return

        if not material_name:
            print("Material name is required.")
            return

        if weight <= 0:
            print("Weight must be greater than zero.")
            return

        rate_input = input(
            "Enter Rate Per Unit (leave blank if unknown): "
        ).strip()

        if rate_input:
            rate_per_unit = float(rate_input)

            if rate_per_unit < 0:
                print("Rate cannot be negative.")
                return
        else:
            rate_per_unit = None

        component_data = {
            "item_id": item_id,
            "component_type": component_type,
            "material_name": material_name,
            "purity": purity if purity else None,
            "weight": weight,
            "weight_unit": weight_unit,
            "rate_per_unit": rate_per_unit
        }

        supabase.table("item_components").insert(
            component_data
        ).execute()

        print("\nComponent added successfully!")

    except ValueError:
        print("Please enter valid numeric values.")

    except Exception as error:
        print("Unable to add component:", error)


# =====================================
# VIEW JEWELLERY COMPONENTS
# =====================================

def view_components():

    print("\n========== VIEW JEWELLERY COMPONENTS ==========")

    item_code = input("Enter Jewellery Item Code: ").strip()

    try:
        # Find jewellery
        response = (
            supabase.table("inventory")
            .select("*")
            .eq("item_code", item_code)
            .execute()
        )

        products = response.data

        if not products:
            print("Jewellery item not found.")
            return

        product = products[0]
        item_id = product["id"]

        # Fetch components
        component_response = (
            supabase.table("item_components")
            .select("*")
            .eq("item_id", item_id)
            .execute()
        )

        components = component_response.data

        print("\nJewellery:", product["name"])
        print("Item Code:", item_code)

        print("\n========== COMPONENT DETAILS ==========")

        if not components:
            print("No components added yet.")
            return

        for component in components:

            print("\nMaterial:", component["material_name"])
            print("Type:", component["component_type"])
            print("Purity:", component.get("purity"))
            print("Weight:", component["weight"], component["weight_unit"])
            print("Rate Per Unit:", component.get("rate_per_unit"))

            print("----------------------------------------")

    except Exception as error:
        print("Unable to fetch components:", error)

# =====================================
# UPDATE COMPONENT PRICE
# =====================================

def update_component_price():

    print("\n========== UPDATE COMPONENT PRICE ==========")

    item_code = input("Enter Jewellery Item Code: ").strip()

    try:
        # Find jewellery
        response = (
            supabase.table("inventory")
            .select("*")
            .eq("item_code", item_code)
            .execute()
        )

        products = response.data

        if not products:
            print("Jewellery item not found.")
            return

        item_id = products[0]["id"]

        # Fetch components
        response = (
            supabase.table("item_components")
            .select("*")
            .eq("item_id", item_id)
            .execute()
        )

        components = response.data

        if not components:
            print("No components found.")
            return

        print("\n========== AVAILABLE COMPONENTS ==========")

        for i, component in enumerate(components, start=1):
            print(
                i,
                component["material_name"],
                "-",
                component["weight"],
                component["weight_unit"],
                "- Current Price:",
                component.get("component_price")
            )

        choice = int(input("\nSelect component number: "))

        if choice < 1 or choice > len(components):
            print("Invalid selection.")
            return

        selected = components[choice - 1]

        if selected["component_type"] == "METAL":
            print("This is a metal component.")
            print("Metal prices are calculated using daily metal rates.")
            return

        price = float(input("Enter total component price in Rs.: "))

        if price < 0:
            print("Price cannot be negative.")
            return

        supabase.table("item_components").update({
            "component_price": price
        }).eq("id", selected["id"]).execute()

        print("\nComponent price updated successfully!")

    except ValueError:
        print("Please enter valid numeric values.")

    except Exception as error:
        print("Unable to update component price:", error)

# =====================================
# MIXED-MATERIAL PRICE CALCULATOR
# =====================================

def calculate_price():

    print("\n========== JEWELLERY PRICE CALCULATOR ==========")

    item_code = input("Enter Jewellery Item Code: ").strip()

    try:

        # Find jewellery
        response = (
            supabase.table("inventory")
            .select("*")
            .eq("item_code", item_code)
            .execute()
        )

        products = response.data

        if not products:
            print("Jewellery item not found.")
            return

        product = products[0]

        if not product.get("is_available", True):
            print("This jewellery item is unavailable.")
            return

        item_id = product["id"]

        # Fetch components
        response = (
            supabase.table("item_components")
            .select("*")
            .eq("item_id", item_id)
            .execute()
        )

        components = response.data

        if not components:
            print("No components added to this jewellery.")
            return

        # Fetch latest metal rates
        rate_response = (
            supabase.table("metal_rates")
            .select("*")
            .order("updated_date", desc=True)
            .limit(1)
            .execute()
        )

        rates = rate_response.data

        if not rates:
            print("No metal rates found.")
            return

        rate = rates[0]

        total_material_value = 0

        print("\n========== COMPONENT PRICE BREAKDOWN ==========")
        print("Jewellery:", product["name"])
        print("Item Code:", item_code)

        for component in components:

            material = component["material_name"].upper()
            component_type = component["component_type"].upper()
            purity = (component.get("purity") or "").upper()

            weight = float(component["weight"])
            unit = component["weight_unit"]

            component_value = 0

            # METAL CALCULATION
            if component_type == "METAL":

                if unit != "g":
                    print("Metal weight must be in grams.")
                    return

                if "GOLD" in material:

                    if "24K" in purity or "24 K" in purity:
                        metal_rate = float(rate["gold_24k"])

                    elif "22K" in purity or "22 K" in purity:
                        metal_rate = float(rate["gold_22k"])

                    elif "18K" in purity or "18 K" in purity:
                        metal_rate = float(rate["gold_18k"])

                    else:
                        print("Unsupported gold purity:", purity)
                        return

                elif "SILVER" in material:

                    metal_rate = float(rate["silver"])

                elif "PLATINUM" in material:

                    metal_rate = float(rate["platinum"])

                else:
                    print("Unsupported metal:", material)
                    return

                # Rates are per 10 grams
                rate_per_gram = metal_rate / 10

                component_value = weight * rate_per_gram

            # GEMSTONE / OTHER CALCULATION
            else:

                manual_price = component.get("component_price")

                if manual_price is None:
                    print("\nPrice missing for:", material)
                    print("Please update its component price first.")
                    return

                component_value = float(manual_price)

            total_material_value += component_value

            print("\nMaterial:", material)
            print("Weight:", weight, unit)
            print("Component Value: Rs.", round(component_value, 2))

        # MAKING CHARGES
        making_type = product["making_charge_type"]
        making_value = float(product["making_charge_value"])

        if making_type == "PER_GRAM":
            making_charge = (
                float(product["net_weight_g"]) * making_value
            )
        else:
            making_charge = making_value

        # FINAL CALCULATION
        subtotal = total_material_value + making_charge

        print("\n========================================")
        print("Total Material Value: Rs.", round(total_material_value, 2))
        print("Making Charges: Rs.", round(making_charge, 2))

        print("----------------------------------------")
        print("ESTIMATED SUBTOTAL: Rs.", round(subtotal, 2))
        print("========================================")

        print("\nGST, discounts and other charges are not included.")

    except Exception as error:
        print("Price calculation failed:", error)


# =====================================
# MAIN MENU
# =====================================

def main():

    while True:

        print("\n========================================")
        print("     JEWELLERY SHOP MANAGEMENT SYSTEM")
        print("========================================")

        print("1. View Inventory")
        print("2. Add Jewellery")
        print("3. Search Jewellery")
        print("4. Calculate Jewellery Price")
        print("5. Add Jewellery Components")
        print("6. View Jewellery Components")
        print("7. Update Component Price")
        print("8. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            view_inventory()

        elif choice == "2":
            add_jewellery()

        elif choice == "3":
            search_jewellery()

        elif choice == "4":
            calculate_price()

        elif choice == "5":
            add_components()

        elif choice == "6":
            view_components()

        elif choice == "7":
            update_component_price()

        elif choice == "8":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice! Try again.")


# =====================================
# START APPLICATION
# =====================================

if __name__ == "__main__":
    main()