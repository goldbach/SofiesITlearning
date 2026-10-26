def gennemsnit(maalinger):
    return sum(maalinger) / len(maalinger)


print("Starter beregning ...")
print(gennemsnit([20.1, 21.3, 22.0]))
print(gennemsnit("21.3"))
print("Færdig")
