import hashlib

def file2md5(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), ''):
            md5.update(chunk)
    return md5.hexdigest()

if __name__ == "__main__":
    file = "E:\dd.txt"
    default_hashcode = "50F84DAF3A6DFD6A9F20C9F8EF428942"
    default_hashcode = default_hashcode.lower() 
    hashcode =file2md5(file)
    
    if default_hashcode != hashcode:    
        print "It is not same!!!"
        print default_hashcode
        print hashcode
    else:
        print "it is same!!!"