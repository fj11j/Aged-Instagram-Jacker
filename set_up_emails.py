import string

with open('results.txt') as f:
    for name in f:
        name = name.replace('\n', '')
        with open('emails.txt', 'a+') as c:
            c.write(name + '@gmail.com\n')
        for letter in string.ascii_lowercase:
                with open('emails.txt', 'a+') as a:
                    a.write(name + letter + '@gmail.com\n')
