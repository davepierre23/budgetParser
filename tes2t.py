usd_amount = 81.70
exchange_rate = 1.37
foreign_exchange_fee = 0.025

cad_amount = usd_amount * exchange_rate
total_cad_amount = cad_amount + (cad_amount * foreign_exchange_fee)

print("USD amount: $", usd_amount)
print("Exchange rate: 1 USD = ", exchange_rate, "CAD")
print("CAD amount before foreign exchange fee: $", cad_amount)
print("Foreign exchange fee: ", foreign_exchange_fee * 100, "%")
print("Total CAD amount including foreign exchange fee: $", total_cad_amount)
