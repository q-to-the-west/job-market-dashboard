#import requests;
import ollama;

mod = 'llama3.1';

#query = requests.get('https://bulbapedia.bulbagarden.net/wiki/Hattrem_(Pok%C3%A9mon)');
#promb = 'please parse the text content of this html page and summarize it for me';
#print(query.text);

try:
    ollama.show(mod);
    print(f'{mod} found');
except:
    print(f'pulling model {mod}');
    ollama.pull(mod);

prom = 'What is love?';
#message1 = {'role':'user','content':query};
message2 = {'role':'user','content':prom};

print('Sending response');
response = ollama.chat(model=mod, messages=[message2]);

print(response['message']['content']);
