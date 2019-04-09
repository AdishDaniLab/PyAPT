def tohex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits))

print (tohex(-2147479549, 64))
print (tohex(2147479549, 64))