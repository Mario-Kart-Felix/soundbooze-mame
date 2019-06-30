import random

def weightRnd(numOfResults):
    result       = []
    numbers      = [0, 1, 2]
    weightings   = [0.10, 0.020, 0.70]

    for i in range(numOfResults):
      choice = random.random()
      currentSum = 0.0

      for r in range(len(numbers)):
          currentSum += weightings[r]
          if (choice <= currentSum):
               break

      result.append(numbers[r])

    return result

r = weightRnd(8)
print r
