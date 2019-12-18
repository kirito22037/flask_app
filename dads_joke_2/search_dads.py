import requests
from random import choice   #choses from a list , tuple

url="https://icanhazdadjoke.com/search"

def search_jokes(user_input):
    #json file are formate in a dictionary form
    obj1=requests.get(url,
                    headers={"Accept":"application/json"},
                    params={"term":user_input}
                    )

    return obj1

user_input=input("enter the term : ")
obj1=search_jokes(user_input)

print(obj1.json())

if obj1.json()['total_jokes']==0:
    print('NO JOKE RELATED TO THAT TOPIC FOUND!!')
    

elif obj1.json()['status']!=200:
    print("ERROR 404! CLIENT SIDE PROBLEM !")

else:
    jokes_collection=obj1.json()['results']  # a list of jokes with key id and joke
    total_jokes=obj1.json()['total_jokes']
    joke=choice(jokes_collection)['joke']
    print(f'joke : {joke}')

#if total_jokes==0:
#    print(f'sorry ! no jokes found for {user_input}')
#else:
#    print(joke)
