# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import os
from django.shortcuts import render_to_response 
from wordcloud import WordCloud, STOPWORDS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from summarizer import summarize
import glob 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import requests
from langCodes import langcode

import sys
reload(sys)
sys.setdefaultencoding('utf8')
file_path="/home/neo/speech_recg/mainapp/static/audio"

# Create your views here.
def getlist(request):
    files = (file for file in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, file)))
    return render_to_response('index.html',{'files':files})

def navaction(request):
    act=request.GET.get('act')
   
    if act == 'listen':
        files = (file for file in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, file)))
        return render_to_response('listen.html',{'result':files})
   
    if act == 'trans':
        return render(request,'trans.html')

def gettrans(request):
    search_text=request.GET.get('search_text')
    search_text =  search_text.encode(encoding='UTF-8')
    blob = TextBlob(str(search_text))
    lan = blob.detect_language()
    result = blob.translate(from_lang=lan,to="en")
    lan = langcode.get(lan)
    return render_to_response('iframe.html',{'result':result,'lan':lan})


def getfilename(request):
    fname = request.GET.get('select')
    search_text=request.GET.get('search_text')
    search_text =  search_text.encode(encoding='UTF-8')
   
    result_dict = search(fname,search_text)
    return render_to_response('display.html',{'result':result_dict.items()})

def goaction(request):
    fname = request.GET.get('yo')
    if(fname):
      action =  fname.split()[0]
      file_name = fname.split()[1]

      if(action == "Word_Cloud"):
          get_wordcloud(file_name)
          return render(request,'Word_Cloud.html')

      if(action == "Summarize"):
          summaryList = summ(file_name)
          return render_to_response('Summarize.html',{'summaryList':summaryList})

      if(action == "Sentiment_Analysis"):
          pos,neg,neu=get_sentiment(file_name)
          return render_to_response('Sentiment_Analysis.html',{'pos':pos,'neg':neg,'neu':neu})
 
      if(action == "Translate"):
          trans,lan = translate(file_name)
          return render_to_response('Translate.html',{'trans':trans,'lan':lan})
  
def get_wordcloud(filename):
    with open("/home/neo/speech_recg/mainapp/static/audio/"+filename.split('.')[0]+"/"+filename.split('.')[0]+".txt",'r') as myFile:
      data = myFile.read().replace('\n',' ')
    wordcloud = WordCloud(stopwords=STOPWORDS,background_color='white',width=800,height=600).generate(str(data))

    fig = plt.figure(1)
    plt.imshow(wordcloud)
    plt.axis('off')
#   plt.show()
    fig.savefig("/home/neo/speech_recg/mainapp/static/images/wordCloud.png")
    return

def summ(filename):
    title = "Test"	
    with open("/home/neo/speech_recg/mainapp/static/audio/"+filename.split('.')[0]+"/"+filename.split('.')[0]+".txt",'r') as myFile:
      data = myFile.read().replace('\n',' ')
    answer = summarize(title,data)
    return answer

def translate(filename):
    title = "Test" 
    with open("/home/neo/speech_recg/mainapp/static/audio/"+filename.split('.')[0]+"/"+filename.split('.')[0]+".txt",'r') as myFile:
      data = myFile.read().replace('\n',' ')
    #dt = summarize(title,data) 
    blob = TextBlob(str(data))
    lan = blob.detect_language().split('-')[0]
    if lan=='en':
        lan="English"
        return data,lan
    data = blob.translate(from_lang=lan,to="en")
    lan=langcode.get(lan)
    return data,lan

def get_dictlist(dir_name,filename,find):
    result = []
    os.chdir("/home/neo/speech_recg/mainapp/static/audio/"+dir_name)
    directory = "/home/neo/speech_recg/mainapp/static/audio/" + dir_name
    for searchfile in glob.glob(directory+ "/*.chunk*.txt"):
      with open(searchfile,'r') as f:
        for line in f:
          if find in line:
            result.append(line.replace(find,"<b><mark>"+find+"</mark></b>"))
    return result

def search(filename,find):
  result = []
  response = {}
  directory = "/home/neo/speech_recg/mainapp/static/audio/"
  if filename=="ALL":
    for dir_name in os.listdir(directory): 
      if os.path.isdir("/home/neo/speech_recg/mainapp/static/audio/"+dir_name):
        temp = get_dictlist(dir_name,filename,find)
        if temp:
          response[dir_name] = temp
  else:
    dir_name = filename.split('.')[0]
    response[filename] = get_dictlist(dir_name,filename,find) 
  return response


def get_sentiment(filename):
    text = ""
    analyzer = SentimentIntensityAnalyzer()
    with open("/home/neo/speech_recg/mainapp/static/audio/"+filename.split('.')[0]+"/"+filename.split('.')[0]+".txt",'r') as myfile:
        text = myfile.read().replace('\n',' ')
    vs = analyzer.polarity_scores(text)
    vs['pos'] = vs['pos'] * 100
    vs['neg'] = vs['neg'] * 100
    vs['neu'] = vs['neu'] * 100

    return vs['pos'],vs['neg'],vs['neu']
