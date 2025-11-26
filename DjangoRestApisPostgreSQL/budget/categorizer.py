import json
import pandas as pd
import re

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
    def apply(self, df, description_col, category_col="Category"):
        results = df[description_col].apply(self.categorize_with_source)
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
        Adds new description patterns to categories and saves file.
        """

        unknowns = df[df["Category"] == "Unknown"]

        if unknowns.empty:
            print("🎉 No unknown transactions.")
            return df

        print(f"\nFound {len(unknowns)} unknown transactions.\n")

        category_names = list(self.categories.keys())
        for idx, row in unknowns.iterrows():
            description = row["Description"]
            clear_desc, city, province = self.parse_description(description)
            print("-" * 70)
            print(f"Date:         {row['Date']}")
            print(f"Description:  {clear_desc}")
            print(f"Amount:       {row['Amount']}")
            print(f"Origin:       {row['Origin']}")
            print(f"Source File:  {row['source_file']}")
            print()

            for i, cat in enumerate(category_names, 1):
                print(f"{i}. {cat}")

            choice = input("\nSelect category number (ENTER to skip): ")

            if not choice.strip():
                print("⏩ Skipped.\n")
                continue

            try:
                category = category_names[int(choice) - 1]
            except:
                print("❌ Invalid choice. Skipped.\n")
                continue

            # Update DataFrame
            df.at[idx, "Category"] = category
            df.at[idx, "CategorySource"] = "Manual"

            # Prepare description for saving
   

            # Add new keyword to category
            if clear_desc not in self.categories[category]:
                self.categories[category].append(clear_desc)

                # Remove duplicates
                self.categories[category] = sorted(list(set(self.categories[category])))

                print(f"✔ Assigned '{description}' → {category}\n")

            # Save updated categories back to Python file
        self.save_categories()

        print("✅ Finished processing all unknown transactions.\n")
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