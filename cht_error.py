# Two sample lists
list_a = [
'980',
'1019',
'1074',
'Received by Mail',
'1036',
'362',
'994',
'834',
'915',
'891',
'340',
'1036',
'983',
'991',
'1020',
'306',
'742',
'426',
'767',
'1005',
'988',
'887',
'564',
'956',
'1055',
'1110',
'564',
'929',
'791',
'796',
'940',
'426',
'931',
'998',
'713',
'308',
'976',
'Received by Mail',
'782',
'456',
'795',
'1208',
'397',
'1068',
'953',
'949',
'934',
'1025',
'1070',
'1067',
'1196',
'1188',
'944',
'1111',
'Received by Mail',
'813',
'1218',

]
list_b = [
    
]

# Find missing entries in either list
missing_in_a = [item for item in list_b if item not in list_a]
missing_in_b = [item for item in list_a if item not in list_b]

print("Items missing in list A:", missing_in_a)
print("Items missing in list B:", missing_in_b)
