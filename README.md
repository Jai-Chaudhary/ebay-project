eBay-Project
=========
###api-scripts

Scripts to get ebay data

Sample Shell Command to extract title from xml response
sed -e "s/xmlns/ignore/" WomensAccessoriesResponse/WomensAccessoriesResponse1.xml | xmllint --xpath "/findItemsByCategoryResponse/searchResult/item/title" -

###ExtractedXMLData

XML file extracted through eBay API

###MalletLDA
#####-Code
  * GenerateInput.py 
  
    Parse XML file and generate input file for Mallet
  * MalletCommandLine.py
  
    Run Mallet to generate topic model
  * ParseOutputSimilarity.py
  
    Parse topic model
    Calculate distance based similarity to generate recommender
    Write recommender to html file
  * Clustering.py
  
    Apply DBScan to generated topic model

#####-mallet-2.0.7/Scripts
Include scripts to calculate perplexity.

#####-inputForMallet
Include input file for Mallet (Clothing, Shoes, Accessory, CrossCSA, CrossColl)



