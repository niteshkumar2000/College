import re
import json

#Constants
stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

#helper to write contents to json file
def write_to_json_file(filename, content):
    with open(filename, 'w') as file:
        json_data = json.dumps(content, sort_keys=True, indent=2)
        file.write(json_data)
    print(f"Inverted Index written to json file") 

#helper to construct inverted index
def construct_inverted_index(filename):
    data = open(filename).readlines()
    del data[0]
    inverted_index = {}
    document_count = 0
    for document in data:
        document_count += 1
        for word in document.split(" "):
            word = (re.sub(r'[^\w\s]', '', word)).strip()
            if word not in stop_words and word != "":
                try:
                    inverted_index[word.lower()].add(document_count)
                except:
                    inverted_index[word.lower()] = set()
                    inverted_index[word.lower()].add(document_count)
            else:
                continue
    return inverted_index

if __name__ == '__main__':
    
    inverted_index = construct_inverted_index("movies_data.rtf")

    # write_to_json_file("inverted_index.json", inverted_index)

    print(f"Total number of words: {len(inverted_index.keys())}")
    """
    Total number of words: 3527
    """

    print(f"Query 1: To find the documents which contains man and day")
    print(inverted_index["man"] & inverted_index["day"])
    """
    Query 1: To find the documents which contains man and day
    {609, 10, 11, 16, 144, 146, 304, 305, 212, 373, 312, 62}
    """

    print(f"Query 2: To find the documents which contains love and not you")
    print(inverted_index["love"] - inverted_index["you"])
    """
    Query 2: To find the documents which contains love and not you
    {769, 12, 654, 16, 146, 147, 307, 312, 953, 578, 69, 845, 591, 602, 605, 609, 997, 488, 494}
    """

    print(f"Query 3: To find the documents which contains super or cool")
    print(inverted_index["super"] | inverted_index["cool"])
    """
    Query 3: To find the documents which contains super or cool
    {7, 10, 266, 396, 141, 16, 144, 145, 19, 150, 151, 281, 282, 155, 412, 285, 414, 39, 301, 430, 304, 312, 443, 316, 447, 66, 67, 81, 343, 217, 219, 94, 95, 249, 234, 109, 121, 378, 251, 380, 125}
    """



    