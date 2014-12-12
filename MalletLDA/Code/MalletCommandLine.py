import subprocess

mallet_path="ebay-data/mallet-2.0.7/"
mallet_input_file_path="ebay-data/inputForMallet/"

#Collectibles

subprocess.Popen('./'+mallet_path+'bin/mallet import-file --input '+mallet_input_file_path+'CrossCollInput.txt --output '+mallet_path+'CrossColl.mallet --keep-sequence --remove-stopwords',shell=True)
subprocess.Popen('./'+mallet_path+'bin/mallet train-topics --input '+mallet_path+'CrossColl.mallet --num-topics 180 --num-top-words 10 --num-iterations 200 --show-topics-interval 1000 --alpha 50.0 --beta .01 --output-doc-topics /Users/Yanjing/ebay-data/mallet-2.0.7/CrossColl_titleToTopics.txt --output-topic-keys /Users/Yanjing/ebay-data/mallet-2.0.7/CrossColl_topic_keys.txt',shell=True)

# #CSA

subprocess.Popen('./'+mallet_path+'bin/mallet import-file --input '+mallet_input_file_path+'AccessoriesInput.txt --output '+mallet_path+'accessory.mallet --keep-sequence --remove-stopwords',shell=True)
subprocess.Popen('./'+mallet_path+'bin/mallet import-file --input '+mallet_input_file_path+'ClothingInput.txt --output '+mallet_path+'clothing.mallet --keep-sequence --remove-stopwords',shell=True)
subprocess.Popen('./'+mallet_path+'bin/mallet import-file --input '+mallet_input_file_path+'ShoesInput.txt --output '+mallet_path+'shoes.mallet --keep-sequence --remove-stopwords',shell=True)
subprocess.Popen('./'+mallet_path+'bin/mallet import-file --input '+mallet_input_file_path+'CrossCSAInput.txt --output '+mallet_path+'CrossCSA.mallet --keep-sequence --remove-stopwords',shell=True)

subprocess.Popen('./'+mallet_path+'bin/mallet train-topics --input '+mallet_path+'clothing.mallet --num-topics 180 --num-top-words 10 --num-iterations 200 --show-topics-interval 1000 --alpha 0.3 --beta .01 --output-doc-topics '+mallet_path+'clothing_titleToTopics.txt --output-topic-keys '+mallet_path+'clothing_topic_keys.txt',shell=True)
subprocess.Popen('./'+mallet_path+'bin/mallet train-topics --input '+mallet_path+'accessory.mallet --num-topics 180 --num-top-words 10 --num-iterations 200 --show-topics-interval 1000 --alpha 0.3 --beta .01 --output-doc-topics '+mallet_path+'accessory_titleToTopics.txt --output-topic-keys '+mallet_path+'accessory_topic_keys.txt',shell=True)
subprocess.Popen('./'+mallet_path+'bin/mallet train-topics --input '+mallet_path+'shoes.mallet --num-topics 180 --num-top-words 10 --num-iterations 200 --show-topics-interval 1000 --alpha 0.3 --beta .01 --output-doc-topics '+mallet_path+'shoes_titleToTopics.txt --output-topic-keys '+mallet_path+'shoes_topic_keys.txt',shell=True)
subprocess.Popen('./'+mallet_path+'bin/mallet train-topics --input '+mallet_path+'CrossCSA.mallet --num-topics 180 --num-top-words 10 --num-iterations 200 --show-topics-interval 1000 --alpha 0.3 --beta .01 --output-doc-topics /'+mallet_path+'combined_titleToTopics.txt --output-topic-keys '+mallet_path+'combined_topic_keys.txt',shell=True)

