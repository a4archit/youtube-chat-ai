import requests as re 

# testing 
print(
    re.get('https://y-chat-ai.onrender.com/status').content,
    re.get('https://y-chat-ai.onrender.com/video?id=TYEqenKrbaM').content ,
    re.get('https://y-chat-ai.onrender.com/query?q=title of the video').content,
    
    sep='\n\n\n'
)
