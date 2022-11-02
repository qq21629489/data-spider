l = []

for i in l:
    print(type(i))

l = ', '.join([x['language'] + ':' + x['ability'] for x in l])
print(l)