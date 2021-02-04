#ans = 0
#neg_flag = False
#x = int(input("Enter an integer: "))
#if x < 0:
#    neg_flag = True
#while ans**2 < x:
#    ans = ans + 1
#if ans**2 == x:
#    print("Square root of", x, "is", ans)
#else:
#    print(x, "is not a perfect square")
#    if neg_flag:
#        print("Just checking... did you mean", -x, "?")


#n = 0
#while n < 5:
#    print(n)
#    n = n+1




x = 0
n = input("You are in the Lost Forest\n****************\n****************\n :)\n****************\n****************\nGo left or right? ")
while n == "right" and x < 3 or n == "Right" and x < 3:
    x = x+1
    n = input("You are in the Lost Forest\n****************\n****************\n :|\n****************\n****************\nGo left or right? ")
while n == "right" and x < 5 or n == "Right" and x < 5:
    x = x+1
    n = input(
        "You are in the Lost Forest\n****************\n****************\n :(\n****************\n****************\nGo left or right? ")
if n == "right" or n == "Right":
    n = print("You are in the Lost Forest forever!\n****************\n******       ***\n  (╯°□°）╯︵ ┻━┻\n****************\n**************** ")
elif n == "left" or n == "Left":
    print("\nYou got out of the Lost Forest!\n\o/")
else:
    print("You are stuck in a Tree!")