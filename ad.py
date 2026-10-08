from itertools import combinations

# ---------- Step 1: Dataset (transactions) ----------
transactions = [
    {"Milk", "Bread"},                    # C1
    {"Milk", "Bread", "Butter"},          # C2
    {"Bread", "Butter"},                  # C3
    {"Milk", "Bread", "Butter"},          # C4
    {"Milk", "Butter"},                   # C5
]

min_support = 0.40       # 40%
min_confidence = 0.70    # 70%
N = len(transactions)


# ---------- Helper: Support count ----------
def support_count(itemset):
    count = 0

    for t in transactions:
        if set(itemset).issubset(t):
            count += 1

    return count


# ---------- Step 2: Apriori Algorithm ----------
def apriori():

    all_frequent = {}

    items = sorted({i for t in transactions for i in t})

    # Level 1: Candidate 1-itemsets
    candidates = [frozenset([i]) for i in items]

    k = 1

    while candidates:

        print(f"\n--- Candidate {k}-itemsets (C{k}) ---")

        frequent = {}

        for c in candidates:

            cnt = support_count(c)
            sup = cnt / N

            status = "KEEP" if sup >= min_support else "REMOVE"

            print(
                f"{sorted(c)} count={cnt} "
                f"support={sup:.2f} -> {status}"
            )

            if sup >= min_support:
                frequent[c] = cnt

        print(
            f"Frequent {k}-itemsets (L{k}):",
            [sorted(f) for f in frequent]
        )

        all_frequent.update(frequent)

        # Generate candidates of size k+1
        keys = list(frequent.keys())

        new_candidates = set()

        for i in range(len(keys)):

            for j in range(i + 1, len(keys)):

                union = keys[i] | keys[j]

                if len(union) == k + 1:

                    # Prune step
                    all_subsets_ok = all(
                        frozenset(s) in frequent
                        for s in combinations(union, k)
                    )

                    if all_subsets_ok:
                        new_candidates.add(union)

        candidates = sorted(new_candidates, key=sorted)

        k += 1

    return all_frequent


# ---------- Step 3: Generate Association Rules ----------
def generate_rules(frequent):

    rules = []

    for itemset, cnt in frequent.items():

        if len(itemset) < 2:
            continue

        for r in range(1, len(itemset)):

            for left in combinations(itemset, r):

                left = frozenset(left)
                right = itemset - left

                confidence = cnt / frequent[left]

                lift = confidence / (frequent[right] / N)

                if confidence >= min_confidence:

                    rules.append(
                        (
                            left,
                            right,
                            cnt / N,
                            confidence,
                            lift
                        )
                    )

    return rules


# ---------- Main Program ----------
print("Total transactions :", N)
print("Minimum support :", min_support)
print("Minimum confidence :", min_confidence)

frequent_itemsets = apriori()


print("\n========== ALL FREQUENT ITEMSETS ==========")

ordered = sorted(
    frequent_itemsets.items(),
    key=lambda x: (len(x[0]), sorted(x[0]))
)

for itemset, cnt in ordered:

    print(
        f"{sorted(itemset)} "
        f"support = {cnt}/{N} = {cnt/N:.2f}"
    )


rules = generate_rules(frequent_itemsets)


print("\n========== ASSOCIATION RULES ==========")

if not rules:

    print("No rules satisfy the minimum confidence.")

else:

    rules.sort(
        key=lambda x: (-x[3], sorted(x[0]), sorted(x[1]))
    )

    for left, right, sup, conf, lift in rules:

        rule_text = f"{sorted(left)} -> {sorted(right)}"

        print(
            rule_text,
            f"support={sup:.2f}",
            f"confidence={conf:.2f}",
            f"lift={lift:.2f}"
        )
        