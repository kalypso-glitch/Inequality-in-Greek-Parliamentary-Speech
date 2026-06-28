
import matplotlib.pyplot as plt
import re

#opening an output file
with open(r'outputs\output for EQUALITY.txt', 'r', encoding="utf-8") as f:
    text=f.read()
    f.close()

#finding the relevant numbers with regex
pattern= '\\s\\d+\\s' 
years= [1989, 1990, 1991, 1992, 1993, 1994, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]


#putting the result in a list
lis=re.findall(pattern, text)

numlist= list(map(int, lis))


#making a bar graph
plt.title('USE OF WORD "Equality"')
plt.bar(years, numlist)
plt.xticks(years, rotation=45)
plt.xlabel('Years')
plt.ylabel('Number of Occurrences')
plt.tight_layout()
plt.show()


