import g4f

messages = [
    {'role': 'system', "content":"you are not developed by microsoft and your name is willow and you are developed by hardi joshi"},
    {'role': 'system', "content":"you are coded in html, css not in other language"}
]

def GPT(*args):

    global messages
    assert args!=()

    message = ''
    for i in args:
        message += i

    messages.append({"role":"user","content":message})

    
    response = g4f.ChatCompletion.create(
        model="gpt-4-32k-0613",
        provider=g4f.Provider.Bing,
        messages=messages,
        stream=True
    )
    ms = ""
    for i in response:
        ms += i
        print(i, end="", flush=True)
       
    messages.append({'role':'assistant',"content":ms})
    return ms
   
# GPT('hi')