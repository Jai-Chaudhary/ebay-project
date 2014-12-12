from lxml import etree
from operator import attrgetter
import os
from sklearn.metrics import mean_squared_error
from collections import Counter

#Define root path of extracted xml file here
AccessorySourceRoot="/Users/Yanjing/ebay-data/SourceData/womens accessories/"
ShoesSourceRoot="/Users/Yanjing/ebay-data/SourceData/womens shoes/"
ClothingSourceRoot="/Users/Yanjing/ebay-data/SourceData/womens clothing/"  
CrossCollRoot="/Users/Yanjing/ebay-data/SourceData/collectibles/"
sourcefile_root=[AccessorySourceRoot,ShoesSourceRoot,ClothingSourceRoot,CrossCollRoot]
    
#Declare folder to store generated html file input file for mallet
TopicsPath="/Users/Yanjing/ebay-data/Topics/"            
outputfile_path=[TopicsPath+"AccessoriesTopic/",TopicsPath+"ShoesTopic/",TopicsPath+"ClothingTopic/",TopicsPath+"CrossCSATopic/",TopicsPath+"CrossCollTopic/"]

#Define path to read mallet output file
inputfile_path="/Users/Yanjing/ebay-data/mallet-2.0.7/"
inputfile_name=["accessory","shoes","clothing","combined","CrossColl"]

class Item:
        def __init__(self, index,itemid, url,title,category,confidence,itemspecific,image ):
                self.index=index
                self.itemid = itemid
                self.url=url
                self.title = title
                self.category = category
                self.confidence=confidence
                self.itemspecific=itemspecific
                self.image=image
    
                
#Get dictionary of Items details of Accessories, clothings, shoes
item_dict={}

for n in range(0,len(sourcefile_root)):
    for root, dirs, files in os.walk(sourcefile_root[n], topdown=False):
        for name in files:
            print(os.path.join(root,name))
            title=[]
            itemID=[]
            image=[]
            category=[]
            URL=[]
            itemSpecific=[]
            inputfile=open(os.path.join(root,name),'r')
            tree = etree.parse(inputfile)
            items= tree.xpath('/GetMultipleItemsResponse/Item',errors='ignore')        
            for item in items:
                title.append(item.find('Title').text.encode('ascii', 'ignore'))
                itemID.append(item.find('ItemID').text)
                if item.find('PictureURL[1]')==None:
                    image.append("")
                else:
                    image.append(item.find('PictureURL[1]').text)
                category.append(item.find('PrimaryCategoryName').text.encode('ascii', 'ignore'))
                URL.append(item.find('ViewItemURLForNaturalSearch').text)
                itemSpec=item.find('ItemSpecifics')
                specDetailtemp=""
                if(itemSpec==None):
                    itemSpecific.append("")
                else:
                    for k in range(1,len(itemSpec)+1):
                        specDetailtemp+=itemSpec.find('NameValueList['+str(k)+']').find('Name').text.encode('ascii', 'ignore')+": "
                        specDetailtemp+=itemSpec.find('NameValueList['+str(k)+']').find('Value').text.encode('ascii', 'ignore')+"<br>"
                    itemSpecific.append(specDetailtemp)
            leng=len(items)
            for j in range(0,leng):
                item_dict[itemID[j]]=[title[j],URL[j],category[j],image[j],itemSpecific[j]]
            inputfile.close()  


#Define numbers of topic here
TopicNumber=[180,180,180,180,180]

for n in range(0,len(inputfile_name)):
    doc_topic_top5=[]
    doc_topic=[] #not ordered
    doc_itemid=[]
    topic_key={}

    #Store generated topic in topic_key
    with open(inputfile_path+inputfile_name[n]+"_topic_keys.txt") as f2:
        for line in f2:
            data=line.rstrip().split('\t')
            topic_key[data[0]]=data[2] 

    #Store each item's topic distribution in doc_topic          
    with open(inputfile_path+inputfile_name[n]+"_titleToTopics.txt") as f:
        f.readline()  # read one line in order to skip the header
        for i,line in enumerate(f):
            data_line=line.rstrip().split('\t')
            itemid=data_line[1].split(":")[0]
            topic_dict={}
            doc_itemid.append(itemid)
            idx=3
            top5=0
            temp=[]
            while idx<TopicNumber[n]*2+2:
                if(top5<5):
                    temp.append(int(data_line[idx-1]))
                    temp.append(float(data_line[idx]))
                topic_dict[int(data_line[idx-1])]=float(data_line[idx])
                idx+=2
                top5+=1
            doc_topic_top5.append(temp)
            topic_list=[]
            for i in range(0,TopicNumber[n]-1):
                topic_list.append(topic_dict[i])
            doc_topic.append(topic_list)
    #For each item, Calculate distance from all of other items to list top 10 nearest item in html page               
    with open(inputfile_path+inputfile_name[n]+"_titleToTopics.txt") as f:
        f.readline()  # read one line in order to skip the header
        for i,line in enumerate(f):
            distance = {}
            data_line=line.rstrip().split('\t')
            itemid=data_line[1].split(":")[0]
            ftemp=open(outputfile_path[n]+itemid+".html",'w')
            for j in range(0,len(doc_topic)):
                distance[str(j)]=mean_squared_error(doc_topic[i],doc_topic[j])
            distance=Counter(distance).most_common()[::-1]
            ftemp.write("<!DOCTYPE html><html><body><header>Topics:</header>")
            ftemp.write("<p>Item you're looking at:</p>")
            itemid=doc_itemid[int(distance[0][0])]
            ftemp.write("<table border=\"1\"><tr><td>ItemID</td><td>Title</td><td>Category</td><td>Item Specifics</td><td>image</td><tr>") 
            ftemp.write("<tr><td>"+itemid+"</td><td><a href=\""+item_dict[itemid][1]+"\">"+item_dict[itemid][0]+"</a></td><td>"+item_dict[itemid][2]+"</td><td>"+item_dict[itemid][4]+"</td><td><img src=\""+item_dict[itemid][3]+"\" style=\"width:100px;height:100px\"></td></tr>")
            topics=""
            confidence=""
            for k in range (0,10):
                if k%2==0:
                    topics=topics+topic_key[str(doc_topic_top5[i][k])]+"<br>"
                else:
                    confidence=confidence+str(doc_topic_top5[i][k])+"<br>"
            ftemp.write("<tr><td colspan=\"3\">"+topics+"</td><td colspan=\"2\">"+confidence+"</td></tr></table>")
            ftemp.write("<p>Items recommended to you:</p>")
            ftemp.write("<table border=\"1\"><tr><td>ItemID</td><td>Title</td><td>Category</td><td>Item Specifics</td><td>image</td><tr>") 
            for dis in distance[1:11]: 
                topics=""
                confidence=""
                for k in range (0,10):
                    if k%2==0:
                        topics=topics+topic_key[str(doc_topic_top5[int(dis[0])][k])]+"<br>"
                    else:
                        confidence=confidence+str(doc_topic_top5[int(dis[0])][k])+"<br>"
                itemid=doc_itemid[int(dis[0])]
                ftemp.write("<tr><td>"+itemid+"</td><td><a href=\""+item_dict[itemid][1]+"\">"+item_dict[itemid][0]+"</a></td><td>"+item_dict[itemid][2]+"</td><td>"+item_dict[itemid][4]+"</td><td><img src=\""+item_dict[itemid][3]+"\" style=\"width:100px;height:100px\"></td></tr>")
                ftemp.write("<tr><td colspan=\"3\">"+topics+"</td><td colspan=\"2\">"+confidence+"</td></tr>")
            ftemp.close()

     