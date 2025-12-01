import json
import pandas as pd
import re
import string
from config import MODEL_DESCRIPTION, MODEL_CLEAN_DESCRIPT, MODEL_CATEGORY

class Categorizer:
    def __init__(self, categories, categories_path="categories.py"):
        """
        categories: dictionary imported from categories.py
        categories_path: file where categories are stored and saved
        """
        self.categories = categories
        self.categories_path = categories_path

    # --------------------------
    # RULE-BASED CATEGORIZATION
    # --------------------------
    def categorize_with_source(self, description: str):
        if (description is None) or (not isinstance(description, str)) or (description.strip() == ""):
            return "Unknown", "Rule: None"

        desc = description.upper()

        # Loop through category rules
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.upper() in desc:
                    return category, f"Rule: '{keyword}'"

        return "Unknown", "Rule: None"

    # --------------------------
    # APPLY TO DATAFRAME
    # --------------------------
    def apply(self, df, description_col, category_col=MODEL_CATEGORY):
        print(df)
        results = df[description_col].apply(self.categorize_with_source)
        print(f"Categorized {results.size} transactions using rule-based categorization.")
        print(results)
        print(type(results.iloc[0]), results.iloc[0])
        df[[category_col, "CategorySource"]] = pd.DataFrame(results.tolist(), index=df.index)
        return df

    # --------------------------
    # SAVE BACK TO categories.py
    # --------------------------
    def save_categories(self):
        """Write categories back into the Python file as valid Python code."""
        try:
            with open(self.categories_path, "w") as f:
                f.write("categories = ")
                f.write(json.dumps(self.categories, indent=4))  # Valid Python literal
            print(f"💾 Categories saved to {self.categories_path}\n")
        except Exception as e:
            print(f"⚠️ Error saving categories: {e}")

    # --------------------------
    # INTERACTIVE CATEGORIZER
    # --------------------------
    def interactive_categorizer(self, df):
        """
        Walk the user through unknown transactions.
        Adds new patterns immediately so next rows auto-categorize.
        Allows creation of new categories.
        """

        while True:

            # Refresh unknowns
            unknowns = df[df[MODEL_CATEGORY] == "Unknown"]

            if unknowns.empty:
                print("🎉 No unknown transactions remaining.")
                break

            print(f"\nFound {len(unknowns)} unknown transactions.\n")

            category_names = list(self.categories.keys())

            for idx, row in unknowns.iterrows():
                clear_desc = row[MODEL_CLEAN_DESCRIPT]
                description =row[MODEL_DESCRIPTION]

                print("-" * 70)
                print(f"Date:         {row['Date']}")
                print(f"Original Description:  {description}")
                print(f"Description:  {clear_desc}")
                print(f"Amount:       {row['Amount']}")
                print(f"Origin:       {row['Origin']}")
                print(f"Source File:  {row['source_file']}")
                print()

                # Show list of existing categories
                for i, cat in enumerate(category_names, 1):
                    print(f"{i}. {cat}")

                # Add "Create New Category" option
                create_index = len(category_names) + 1
                print(f"{create_index}. ➕ Create New Category")

                choice = input("\nSelect a category number (ENTER to skip): ")

                if not choice.strip():
                    print("⏩ Skipped.\n")
                    continue

                try:
                    choice_num = int(choice)
                except:
                    print("❌ Invalid input. Skipped.\n")
                    continue

                # ---- Option: Create New Category ----

                if choice_num == create_index:
                    new_category = input("\nEnter the name for your new category: ").strip()

                    if not new_category:
                        print("❌ Invalid category name. Skipped.\n")
                        continue

                    print(f"➕ Creating new category: {new_category}")

                    # Add new category to categories dictionary
                    self.categories[new_category] = []
                    category = new_category

                    # Add menu entry
                    category_names.append(new_category)

                # ---- Use existing category ----
                else:
                    if choice_num < 1 or choice_num > len(category_names):
                        print("❌ Invalid category number. Skipped.\n")
                        continue

                    category = category_names[choice_num - 1]

                # ---- Update DataFrame ----
                df.at[idx, MODEL_CATEGORY] = category
                df.at[idx, "CategorySource"] = "Manual"

                # ----------------------------------------------------
                # 🔥 NEW KEYWORD AUTOMATION PROCESS
                # ----------------------------------------------------
                print(f"\nSuggested keyword for automation: '{clear_desc}'")

                keyword_action = input(
                    "Choose: (A)ccept keyword, (R)eplace with custom keyword, (M)anual only: "
                ).strip().upper()

                keyword_to_save = None

                if keyword_action == "A":
                    keyword_to_save = clear_desc
                    print(f"✔ Accepted keyword: '{keyword_to_save}'")

                elif keyword_action == "R":
                    custom_kw = input("Enter your custom keyword: ").strip()
                    if custom_kw:
                        keyword_to_save = custom_kw
                        print(f"✔ Custom keyword saved: '{keyword_to_save}'")
                    else:
                        print("❌ Invalid custom keyword. Skipping automation.")

                else:
                    print("ℹ Manual only: No keyword automation.\n")

                # ---- Save keyword to dictionary (if any) ----
                if keyword_to_save:
                    if keyword_to_save not in self.categories[category]:
                        self.categories[category].append(keyword_to_save)
                        self.categories[category] = sorted(set(self.categories[category]))

                        print(f"✔ Added rule: '{keyword_to_save}' → {category}")

                        # Save categories instantly
                        self.save_categories()

                        # Re-apply auto-categorization
                        df = self.apply(df, MODEL_CLEAN_DESCRIPT, MODEL_CATEGORY)
                        print("🔄 Re-applied automatic rules.\n")

                break  # Restart loop with updated unknown list

        print("✅ Finished all unknowns.")
        return df



    def parse_description(self, description: str):
        """
        Parse description to remove location details (city, province).
        Returns cleaned description, city, province.
        """
        pattern = r"(.*?)(?:\s+([A-Z]{2,}(?:\s+[A-Z]{2,})?)(?:,\s*([A-Z]{2}))?)?$"
        match = re.match(pattern, description.strip())
        if match:
            clear_desc = match.group(1).strip()
            city = match.group(2).strip() if match.group(2) else ""
            province = match.group(3).strip() if match.group(3) else ""
            return clear_desc, city, province
        else:
            return description.strip(), "", ""
        

