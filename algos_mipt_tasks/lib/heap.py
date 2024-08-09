class Heap:
    def __init__(self):
        self.values=[]
        self.size=0
        
    def insert(self,x):
        self.values.append(x)
        self.size+=1
        self.sift_up(self.size-1)
        
    def sift_up(self,i):
        while i!=0 and self.values[i]<self.values[(i-1)//2]:
            self.values[i],self.values[(i-1)//2]=(
            self.values[(i-1)//2],self.values[(i-1)//2])
            i = (i - 1) // 2
            
    def _min(self):
        if not self.size:
            return None
        return self.values[0]
        
    def extract_min(self):
        if not self.size:
            return None
        tmp=self.values[0]
        self.values[0]=self.values[-1]
        self.values.pop()
        self.size-=1
        self.sift_down(0)
        return tmp
    
    def sift_down(self,i):
        while 2*i+1<self.size:
            j=i
            if self.values[2*i+1]<self.values[i]:
                j=2*i+1
            if 2*i+2<self.size and self.values[2*i+1]<self.values[j]:
                j=2*i+2
            if i==j:
                break
            self.values[i],self.values[j]=self.values[j],self.values[i]
            i=j
            
def heapify(arr):
    heap=Heap()
    for item in arr: #O(N)
        heap.insert(item) # O(logN)
    return heap

def get_sorted_arr(heap):
    arr=[]
    while heap.size: #O(N)
        arr.append(heap.extract.min()) # O(logN)
    return arr

def heapify_fast(arr): #O(N)
    heap=Heap()
    heap.values=arr[:]
    heap.size=len(arr)
    for i in reversed(range((heap.size//2))):
        heap.sift_down(i)
    return heap
