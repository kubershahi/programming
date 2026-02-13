import math

def degree_to_radian(degree):
  ratio = (float) (degree/360)
  radian = ratio * 2 * math.pi
  return radian

def area(alpha, radiusA, beta, radiusB):
  radian_A = degree_to_radian(radiusA)
  radian_B = degree_to_radian(radiusB)
  sectorArea = 1/2 * (radiusA**2) * radian_A + 1/2 * (radiusB**2) * radian_B
  traingleArea = 1/2 * (radiusA**2) * math.sin(radian_A) +  1/2 *(radiusB**2) * math.sin(radian_B) 

  commonArea = sectorArea - traingleArea
  print(commonArea)
  return math.ceil(commonArea)

print(area(45,15,60,15))