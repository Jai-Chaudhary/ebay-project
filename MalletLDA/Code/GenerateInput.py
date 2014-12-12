from lxml import etree
import os

#Define root path of extracted xml file here
AccessorySourceRoot="/Users/Yanjing/ebay-data/SourceData/womens accessories/"
ShoesSourceRoot="/Users/Yanjing/ebay-data/SourceData/womens shoes/"
ClothingSourceRoot="/Users/Yanjing/ebay-data/SourceData/womens clothing/" 
CollectiblesSourceRoot="/Users/Yanjing/ebay-data/SourceData/collectibles/" 
 
sourcefile_root=[AccessorySourceRoot,ShoesSourceRoot,ClothingSourceRoot,CollectiblesSourceRoot]

#Declare new files to store generated input file for mallet
AccessoryInput='/Users/Yanjing/ebay-data/inputForMallet/AccessoriesInput.txt'
ShoesInput='/Users/Yanjing/ebay-data/inputForMallet/ShoesInput.txt'
ClothingInput='/Users/Yanjing/ebay-data/inputForMallet/ClothingInput.txt'
CombinedInput='/Users/Yanjing/ebay-data/inputForMallet/CrossCSAInput.txt'
CrossCollInput='/Users/Yanjing/ebay-data/inputForMallet/CrossCollInput.txt'

#Filter Item Specifics
accessory_specifics=["Material","Pattern","Style"]
shoes_specifics=["Brand","Style","Size"]
clothing_specifics=["Brand","Style","Size"]

Itemspecifics=[accessory_specifics,shoes_specifics,clothing_specifics,[]]

file_list_write=[open(AccessoryInput, 'w'),open(ShoesInput, 'w'),open(ClothingInput, 'w'),open(CrossCollInput, 'w')]
file_list_read=[open(AccessoryInput, 'r'),open(ShoesInput, 'r'),open(ClothingInput, 'r')]

item_dict={} 
item={}

for n in range(0,len(sourcefile_root)) :   
    for root, dirs, files in os.walk(sourcefile_root[n], topdown=False):
        #walk through extracted xml file
        for name in files:
            title=[]
            itemID=[]
            itemSpecific=[]           
            inputfile=open(os.path.join(root,name),'r')
            tree = etree.parse(inputfile)       
            items= tree.xpath('/GetMultipleItemsResponse/Item')
            #Parse items in each extracted xml file        
            for item in items:
                temp=""
                if item.find('ItemID').text in item_dict.keys():
                    continue            
                item_dict[item.find('ItemID').text]=1 
                     
                title.append(item.find('Title').text.encode('ascii', 'ignore').replace(","," "))
                itemID.append(item.find('ItemID').text) 
                itemSpec=item.find('ItemSpecifics')
                if(itemSpec==None):
                    itemSpecific.append("")
                else:
                    if Itemspecifics[n]:
                        for k in range(1,len(itemSpec)+1):
                            valuename=itemSpec.find('NameValueList['+str(k)+']').find('Name').text.encode('ascii', 'ignore')
                            if valuename in Itemspecifics[n]:
                                temp+=" "+(itemSpec.find('NameValueList['+str(k)+']').find('Value')).text.encode('ascii', 'ignore')
                    else:
                        for k in range(1,len(itemSpec)+1):
                            temp+=" "+(itemSpec.find('NameValueList['+str(k)+']').find('Value')).text.encode('ascii', 'ignore')
                itemSpecific.append(temp.replace("\n",""))            
            leng=len(title)   
             
            #generate input file for mallet                               
            for j in range(0,leng):
                file_list_write[n].write(itemID[j]+":"+",en,"+title[j]+itemSpecific[j]+"\n")

    
            inputfile.close()
    file_list_write[n].close() 

writer = open(CombinedInput, "w")


for n in range(0,len(sourcefile_root)-1):
    writer.write(file_list_read[n].read())
    file_list_read[n].close()

writer.close()
