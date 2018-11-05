def tuplev(list):
    ''' Turns a list of tuples into an html table'''
    s = ""
    for row in list:#range(1, len(list)):
        s +='<tr>\n'
        for col in row:
            s += '<td>'
            s += str(col)
            s += '</td>\n'
        s += '</tr>\n'
    return s