from Parameters import *

Test_img=[]
for i,u in enumerate(os_sorted(os.listdir(f"{save_path}/Test_image/"))):
    iimg=Image.open(f"{save_path}/Test_image/{u}")
    iimg=iimg.resize((300,300))
    iimg=iimg.convert('L')
    iimg=np.array(iimg)
    Test_img.append(iimg)

Img=[]
for i,u in enumerate(os_sorted(os.listdir(f"{save_path}Data/"))):
    Img.append(np.load(f"{save_path}Data/{u}"))
def cost_calculation(choice,b,Test_img,k):
    cost=np.empty((1,np.shape(b)[1]))
    if choice==0:
        for i in range(np.shape(b)[1]):
            pcc=np.corrcoef(Img[b[0,i]][:,:,b[1,i]].flat,Test_img[k].flat)
            pcc=pcc[0,1]
            if pcc<=0: pcc=0.1
            cost[0,i]=pcc
    else:
        pass
    return cost

def final_offspring(b,offspring,probid,k):
    cost=cost_calculation(choice,offspring,Test_img,k)
    costid=cost.argsort()
    costid=np.resize(costid,(1,np.shape(offspring)[1]))
    fioffspring=offspring[:,costid[0][(np.shape(offspring)[1])//2:]]
    b[:,0:np.shape(b)[1]//2]=b[:,probid[0][((np.shape(b)[1])//2):]]
    b[:,(np.shape(b)[1]//2):]=fioffspring
    return b

def Roulette(b,k):
    cst=cost_calculation(choice,b,Test_img,k)
    prob=cst/np.sum(cst)
    probid=np.resize(prob.argsort(),(1,np.shape(b)[1]))
    b=b[:,probid[0]]
    idd=b[:,np.random.choice(b.shape[1], size=Population_size,replace=True, p=prob[0])]
    offspring=np.empty((2,Population_size))
    for i in range(np.shape(b)[1]//2):
        crosprob=np.random.choice([0,1], size=1, p=[1-Cross_over_prob,Cross_over_prob])
        if crosprob[0]==1:
            crosprobgene=np.random.choice([0,1], size=2,replace=False, p=[0.5,0.5])
            crosprobgene=np.resize(crosprobgene,(2,1))
            offspring[crosprobgene[1][0],2*i:2*(i+1)]=np.dot(np.fliplr(np.identity(2,dtype=int)),np.dot(idd[:,2*i:2*(i+1)].T,crosprobgene)).T[0]
            offspring[crosprobgene[0][0],2*i:2*(i+1)]=idd[crosprobgene[0][0],2*i:2*(i+1)]
            offspring[1,2*i]=int(offspring[1,2*i]%np.shape(Img[int(offspring[0,2*i])])[2])
            offspring[1,2*i+1]=int(offspring[1,2*i+1]%np.shape(Img[int(offspring[0,2*i+1])])[2])
                
        else:
            offspring[:,2*i:2*(i+1)]=idd[:,2*i:2*(i+1)]
        offspring=offspring.astype('int64')
    b=final_offspring(b,offspring,probid,k)
    return b

def Mutation(b,Mp):
    mutprob=np.random.choice([0,1], size=np.shape(b)[1], p=[1-Mp,Mp])
    mutid=np.where(mutprob>0)
    if len(mutid[0])==0:
        pass
    else:
        for i in mutid[0]:
            b[0,i]=np.random.randint(len(animaln))
            b[1,i]=np.random.choice(animalno[b[0,i]])
    return b

        


