import sys

def chooseItems(member, items, item_count):
    """Adapted application of 0-1 Knapsack. Finds the cost each member
    can carry, then finds the items each member is holding"""
    # citation https://en.wikipedia.org/wiki/Knapsack_problem#Dynamic_programming_in-advance_algorithm
    # used the pseudocode provided
    # https://www.geeksforgeeks.org/python-program-for-dynamic-programming-set-10-0-1-knapsack-problem/
    # for how to set up opt
    opt = [[0 for x in range(member[0]+1)] for x in range(item_count+1)]
    for i in range(len(items)+1):
        # for each item...
        for w in range(member[0]+1):
            # find best value at buttom-up approach to carrying capacity of the family member
            if i == 0 or w == 0:
                # initialize at 0
                opt[i][w] = 0
            elif items[i-1][1] <= w:
                # compare current value and weight to that of it added with current item info
                if items[i-1][0] + opt[i-1][w-items[i-1][1]] > opt[i-1][w]:
                    opt[i][w] = items[i-1][0] + opt[i-1][w-items[i-1][1]]
                else:
                    opt[i][w] = opt[i-1][w]
            else:
                opt[i][w] = opt[i-1][w]

    carrying_val = max(opt[-1])
    track_items = carrying_val
    carried_items = []
    track_weight = member[0]
    # citation https://www.geeksforgeeks.org/printing-items-01-knapsack/  only for finding items carried
    for i in range(len(items), 0, -1):
        if track_items <= 0:
            break
        if track_items == opt[i-1][track_weight]:
            continue
        else:
            carried_items.append(items[i - 1][2])
            track_items -= items[i - 1][0]
            track_weight -= items[i - 1][1]
    data_for_member = [carrying_val, carried_items]
    return data_for_member

def efficientShopping(family, items, NoOfItems):
    """collect items carried by each member of the family,
    as well as the total cost accrued by the family"""
    cost = 0
    result = {}
    # items are sorted by price
    # items closer to list start are items that family wants
    for f in range(len(family)):
        member_data = chooseItems(family[f], items, NoOfItems)
        cost += member_data[0]
        result[family[f][1] + 1] = member_data[1]
    # get data in sorted order by family member id
    final_data = {}
    for i in range(len(family)):
        final_data[i+1] = result[i+1]
    final_data["total"] = cost
    return final_data

sys.stdin = open('shopping.txt', 'r')
testcases = int(input())
all_data = []
for case in range(1, testcases+1):
    # let x be number of items
    x = int(input())
    item_info = []
    family = []
    for i in range(x):
        # get item info
        item = input()
        item = item.split()
        price = int(item[0])
        weight = int(item[1])
        # recombine, with item id number
        priceWeight = [price, weight, i+1]
        item_info.append(priceWeight)
    # citation https://stackoverflow.com/questions/36955553/sorting-list-of-lists-by-the-first-element-of-each-sub-list
    # used to sort an array by first entry in subarrays
    item_info = sorted(item_info, key=lambda k: k[0], reverse=True)
    numInFam = int(input())
    for j in range(numInFam):
        # add each family member's capacity, as well as their order of appearance (id)
        weightLimit = int(input())
        family.append([weightLimit, j])
    family_sorted = sorted(family, key=lambda k: k[0])
    case_number = efficientShopping(family_sorted, item_info, x)
    all_data.append(case_number)

# write to file
dataOut = open('results.txt', 'w')
for case_number in range(len(all_data)):
    dataOut.write("Test Case ")
    dataOut.write(str(case_number+1))
    dataOut.write("\n")
    dataOut.write("Total Price: ")
    dataOut.write(str(all_data[case_number]['total']))
    dataOut.write("\n")
    dataOut.write("Member Items:")
    dataOut.write("\n")
    for family_member in range(1, len(all_data[case_number])):
        dataOut.write(str(family_member))
        dataOut.write(": ")
        for item in all_data[case_number][family_member]:
            dataOut.write(str(item))
            dataOut.write(" ")
        dataOut.write("\n")
dataOut.close()