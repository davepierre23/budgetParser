class GiftCardDealChecker:
    def __init__(self):
        # 🎁 Your gift card deals
        self.deals = {
            "APPLEBEES": "Buy a $50 gift card → Get a $10 bonus card",
            "BOOSTER JUICE": "Buy a $30 gift card → Get a free smoothie or acai bowl",
            "BOSTON PIZZA": "Buy a $50 gift card → Get a $10 bonus card",
            "CINEPLEX": "Buy a $50 gift card → Get a coupon book",
            "COBS BREAD": "Buy a $30 gift card → Get a free scone",
            "DENNY": "Buy a $25 gift card → Get a $5 off coupon",
            "EAST SIDE MARIO": "Buy a $50 gift card → Get a free Jr. Chicken Parm",
            "HARVEY": "Buy a $25 gift card → Get a free Original Burger",
            "MCDONALD S": "Buy a $25 gift card → Get a free Big Mac or McChicken",
            "MONTANA": "Buy a $50 gift card → Get a free rib taster plate",
            "MOXIE": "Buy a $100 gift card → Get a $20 gift card",
            "NEW YORK FRIES": "Buy a $25 gift card → Get a free snack-size poutine",
            "PITA PIT": "Buy a $25 gift card → Get a $5 off coupon",
            "ST LOUIS": "Buy a $50 gift card → Get a $10 off coupon",
            "SUBWAY": "Buy a $50 gift card → Get a free footlong",
            "SWISS CHALET": "Buy a $50 gift card → Get a free Quarter Chicken Dinner",
            "ULTIMATE DINING CARD": "Buy a $50 gift card → Get a $50 bonus card",
        }

    def scan(self, df, description_col="CleanDescription", amount_col="Amount"):
        results = {}

        # Convert store names to list for iteration
        store_list = list(self.deals.keys())

        for _, row in df.iterrows():
            desc = str(row[description_col]).upper()
            amount = row[amount_col]

            for store in store_list:
                if store in desc:
                    if store not in results:
                        results[store] = {
                            "total": 0,
                            "deal": self.deals[store]
                        }
                    results[store]["total"] += amount

        # Round totals
        for store in results:
            results[store]["total"] = round(results[store]["total"], 2)

        return results

    def print_results(self, results):
        if not results:
            print("📭 No gift-card eligible purchases found this year.")
            return

        print("\n🎁 Gift Card Opportunities Found")
        print("=================================\n")

        for store, data in results.items():
            print(f"🏪 {store}")
            print(f"   → Total Spent: ${data['total']:,.2f}")
            print(f"   → Deal: {data['deal']}")
            print("")
