PATH = '/home/cristopher/Dropbox/Challenge/'

class Data_Mining():
    
    def import_data(self):
        
        import urllib2        
        url = "http://aima.cs.berkeley.edu/data/iris.csv"
        u = urllib2.urlopen(url)
        localFile = open('iris.csv', 'w')
        localFile.write(u.read())
        localFile.close()
    
    def plot_data(self):
        from numpy import genfromtxt, zeros
        
        data = genfromtxt(PATH + 'test_subdataset.csv',delimiter=',',usecols=(0,1,2,3,4,5,6,7)) 
        target = genfromtxt(PATH + 'test_subdataset.csv',delimiter=',',usecols=(8,9,10),dtype=str)
              
        t = zeros(len(target))
        
        print t.tolist()
        print len(data.tolist())
              
        from sklearn.naive_bayes import GaussianNB
        classifier = GaussianNB()
        classifier.fit(data,t) # training on the iris dataset
        
        print classifier.predict(data[0])

if __name__ == '__main__':
    Data_Mining().plot_data()