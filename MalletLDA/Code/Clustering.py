import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfTransformer
from lxml import etree
import os
import random

#Define root path of extracted xml file here
AccessorySourceRoot="/Users/Yanjing/ebay-data/SourceData/womens accessories/"
ShoesSourceRoot="/Users/Yanjing/ebay-data/SourceData/womens shoes/"
ClothingSourceRoot="/Users/Yanjing/ebay-data/SourceData/womens clothing/" 
CollSourceRoot="/Users/Yanjing/ebay-data/SourceData/collectibles/"  

#Define location and file name which store mallet file
mallet_path="/Users/Yanjing/ebay-data/mallet-2.0.7/"
inputfile_name=["accessory","shoes","clothing","combined","CrossColl"]
 
sourcefile_root=[AccessorySourceRoot,ShoesSourceRoot,ClothingSourceRoot,CollSourceRoot]

class Item:
        def __init__(self, index,itemid, url,title,category,itemspecific,image ):
                self.index=index
                self.itemid = itemid
                self.url=url
                self.title = title
                self.category = category
                self.itemspecific=itemspecific
                self.image=image
                
#Get dictionary of Items specifics of Accessories, clothings, shoes
item_dict={}
                
for n in range(0,1):
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


for n in range(0,1):                                
    ##############################################################################
    # Generate sample data
    
    X=[]
    data=[] 
    
    with open(mallet_path+inputfile_path[n]+"_titleToTopics.txt") as f:
            f.readline()  # read one line in order to skip the header
            for line in f:
                data_line=line.rstrip().split('\t')
                itemid=data_line[1].split(":")[0]            
                index=int(data_line[2])
                temp=[]
                for i in range (3,362,2):
                    temp.append(float(data_line[i]))
                X.append(temp)
                data.append(Item(index,itemid,item_dict[itemid][1],item_dict[itemid][0],item_dict[itemid][2],item_dict[itemid][4],item_dict[itemid][3]))
    #X=random.sample(X, 6000)    
    X = StandardScaler().fit_transform(X)
 #  X = TfidfTransformer().fit_transform(X).toarray()
 #   print len(X)

 ##############################################################################
    # Compute DBSCAN
    db = DBSCAN(eps=0.1, min_samples=6).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    #print labels
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    
    print('Estimated number of clusters: %d' % n_clusters_)
    #print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))
    
    #confidence=metrics.silhouette_samples(X, labels)
    
    #print(confidence[0])
    
    ##############################################################################
    #Define path to store generated clusters 
    TopicsPath="/Users/Yanjing/ebay-data/Clusters/"            
    outputfile_path=[TopicsPath+"Accessories/cluster",TopicsPath+"Shoes/cluster",TopicsPath+"Clothing/cluster",TopicsPath+"CrossCSA/cluster",TopicsPath+"CrossColl/cluster"]    
    file_list_xml = []        
    #open files to store output
    for i in range(0,n_clusters_):
        ftemp=open(outputfile_path[n]+str(i)+".html",'w')
        ftemp.write("<table border=\"1\"><tr><td>ItemID</td><td>Title</td><td>Category</td><td>Item Specifics</td><td>image</td><tr>") 
        file_list_xml.append(ftemp)
        ftemp.close()
        print len(labels)
        print len(data)
    for idx,da in enumerate(data):
        if labels[idx]==-1:
            #print "skip"
            continue
        else:
            ftemp=open(outputfile_path[n]+str(labels[idx])+".html",'a+')
            ftemp.write("<tr><td>"+da.itemid+"</td><td><a href=\""+da.url+"\">"+da.title+"</a></td><td>"+da.category+"</td><td>"+da.itemspecific+"</td><td><img src=\""+da.image+"\" style=\"width:100px;height:100px\"></td></tr>")
            ftemp.close()
   