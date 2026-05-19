from ai_engine import get_ai_matches

results = get_ai_matches(
    origin="Dallas",
    destination="Atlanta",
    truck="Van",
    max_deadhead=150,
    min_price=1000,
    top_n=10
)

print(results)