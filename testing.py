import requests as re 

print(
    re.get('http://127.0.0.1:8000/status').content,
    re.get('http://127.0.0.1:8000/video?id=TYEqenKrbaM').content ,
    re.get('http://127.0.0.1:8000/query?q=title of the video').content,
    
    sep='\n\n\n'
)