from pythonpancakes import PancakeSwapAPI
import pprint as pp 
ps = PancakeSwapAPI()

summary = ps.tokens('0x4206931337dc273a630d328dA6441786BfaD668f')

print(summary)