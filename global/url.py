import requests




params = [{'natural':'woman', 'target':'Woman 20 year old','strength':'2','disentanglment':'2', 'save':'1'},{'natural':'Makeup', 'target':'no makeup','strength':'3','disentanglment':'0.0001','save':'2'},
          {'natural':'hair', 'target':'long black hair ','strength':'3','disentanglment':'2','save':'2'},
          {'natural':'colored background', 'target':'white background','strength':'4','disentanglment':'2','save':'2'},{'natural':'woman', 'target':'woman  smiling','strength':'-3','disentanglment':'2','save':'2'},
          {'natural':'woman', 'target':'woman average weight','strength':'2','disentanglment':'2','save':'2'}]


params2 = [{'natural':'man', 'target':'man 20 year old','strength':'2','disentanglment':'2', 'save':'1'},
          {'natural':'hair', 'target':'short black hair ','strength':'3','disentanglment':'2','save':'2'},
          {'natural':'colored background', 'target':'white background','strength':'4','disentanglment':'2','save':'2'},{'natural':'man', 'target':'man  smiling','strength':'-3','disentanglment':'2','save':'2'},
        {'natural':'man with beard', 'target':'no beard','strength':'2','disentanglment':'2','save':'2'},
          {'natural':'man', 'target':'man average weight','strength':'1','disentanglment':'2','save':'2'}]
params3 = [{'natural':'man', 'target':'woman','strength':'6','disentanglment':'13', 'save':'1'},]
url = "http://localhost:5000/result"
for i in range(len(params2)):
    params2[i]['save'] = str(i+1)
    r = requests.get(url, params=params2[i])
    print(r.url)

# for i2 in range(len(params2)):
#
#     r = requests.get(url, params=params2[i2])
#     print(r.url)