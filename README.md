ebay-data
=========

Scripts to get ebay data

Sample Shell Command to extract title from xml response
sed -e "s/xmlns/ignore/" WomensAccessoriesResponse/WomensAccessoriesResponse1.xml | xmllint --xpath "/findItemsByCategoryResponse/searchResult/item/title" -
